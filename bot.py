from __future__ import annotations

import asyncio
import logging
import uuid
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from app.cleanup import cleanup_old_tmp
from app.config import Settings, get_settings
from app.keyboards import CANCEL, MAKE_PDF, MODE_NORMAL, MODE_SCAN, NEW_PDF, main_menu, remove_keyboard, work_menu
from app.pdf_builder import build_pdf
from app.sessions import SessionStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("scan2pdf")

settings: Settings = get_settings()
bot = Bot(token=settings.bot_token)
dp = Dispatcher()
sessions = SessionStore(settings.tmp_dir)

WELCOME = (
    "Salom! Men rasmlarni PDF qilib beraman.\n\n"
    "Oddiy PDF - rasmni oq A4 sahifaga joylaydi.\n"
    "Skaner PDF - kamera rasmini tiniqlashtirib, hujjatga o'xshatadi."
)


def user_id(message: Message) -> int:
    if not message.from_user:
        raise RuntimeError("User is required")
    return message.from_user.id


def safe_file_name(name: str) -> str:
    clean = "".join(ch for ch in name if ch.isalnum() or ch in ("-", "_", "."))
    return clean[:80] or "scan"


async def start_mode(message: Message, mode: str) -> None:
    uid = user_id(message)
    sessions.start(uid, mode=mode)
    await message.answer(
        f"{mode} rejimi tanlandi.\n\n"
        "Endi bitta yoki bir nechta rasm yuboring. Tayyor bo'lgach, PDF yaratish tugmasini bosing.",
        reply_markup=work_menu(),
    )


async def save_photo(message: Message) -> Path:
    uid = user_id(message)
    session = sessions.get(uid)
    if not session:
        raise RuntimeError("Session is not started")

    photo = message.photo[-1]
    if photo.file_size and photo.file_size > settings.max_file_bytes:
        raise ValueError(f"Rasm hajmi {settings.max_file_mb} MB dan katta bo'lmasin")

    path = session.folder / f"img_{len(session.images) + 1:03d}_{uuid.uuid4().hex[:8]}.jpg"
    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, destination=path)
    return path


async def save_image_document(message: Message) -> Path:
    uid = user_id(message)
    session = sessions.get(uid)
    if not session:
        raise RuntimeError("Session is not started")

    document = message.document
    if not document:
        raise RuntimeError("Document is required")
    if not (document.mime_type or "").startswith("image/"):
        raise ValueError("Faqat rasm fayl yuboring")
    if document.file_size and document.file_size > settings.max_file_bytes:
        raise ValueError(f"Rasm hajmi {settings.max_file_mb} MB dan katta bo'lmasin")

    suffix = Path(document.file_name or "image.jpg").suffix.lower() or ".jpg"
    path = session.folder / f"img_{len(session.images) + 1:03d}_{uuid.uuid4().hex[:8]}{suffix}"
    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, destination=path)
    return path


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    cleanup_old_tmp(settings.tmp_dir)
    sessions.cancel(user_id(message))
    await message.answer(WELCOME, reply_markup=main_menu())


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message) -> None:
    sessions.cancel(user_id(message))
    await message.answer("Bekor qilindi. Yangi PDF boshlash uchun rejim tanlang.", reply_markup=main_menu())


@dp.message(F.text == NEW_PDF)
async def h_new_pdf(message: Message) -> None:
    sessions.cancel(user_id(message))
    await message.answer("Yangi PDF uchun rejim tanlang.", reply_markup=main_menu())


@dp.message(F.text == CANCEL)
async def h_cancel(message: Message) -> None:
    await cmd_cancel(message)


@dp.message(F.text.in_({MODE_NORMAL, MODE_SCAN}))
async def h_mode(message: Message) -> None:
    await start_mode(message, message.text or MODE_NORMAL)


@dp.message(F.photo)
async def h_photo(message: Message) -> None:
    uid = user_id(message)
    session = sessions.get(uid)
    if not session:
        await message.answer("Avval rejim tanlang.", reply_markup=main_menu())
        return
    if len(session.images) >= settings.max_images:
        await message.answer(f"Limit: bitta PDF uchun {settings.max_images} ta rasm.", reply_markup=work_menu())
        return

    try:
        path = await save_photo(message)
        count = sessions.add_image(uid, path)
        await message.answer(f"Rasm qo'shildi: {count}/{settings.max_images}", reply_markup=work_menu())
    except ValueError as exc:
        await message.answer(str(exc), reply_markup=work_menu())
    except Exception:
        log.exception("Photo save failed")
        await message.answer("Rasmni yuklashda xatolik bo'ldi. Qayta urinib ko'ring.", reply_markup=work_menu())


@dp.message(F.document)
async def h_document(message: Message) -> None:
    uid = user_id(message)
    session = sessions.get(uid)
    if not session:
        await message.answer("Avval rejim tanlang.", reply_markup=main_menu())
        return
    if len(session.images) >= settings.max_images:
        await message.answer(f"Limit: bitta PDF uchun {settings.max_images} ta rasm.", reply_markup=work_menu())
        return

    try:
        path = await save_image_document(message)
        count = sessions.add_image(uid, path)
        await message.answer(f"Rasm fayl qo'shildi: {count}/{settings.max_images}", reply_markup=work_menu())
    except ValueError as exc:
        await message.answer(str(exc), reply_markup=work_menu())
    except Exception:
        log.exception("Document save failed")
        await message.answer("Faylni yuklashda xatolik bo'ldi. Faqat rasm yuboring.", reply_markup=work_menu())


@dp.message(F.text == MAKE_PDF)
async def h_make_pdf(message: Message) -> None:
    uid = user_id(message)
    session = sessions.get(uid)
    if not session:
        await message.answer("Avval rejim tanlang.", reply_markup=main_menu())
        return
    if not session.images:
        await message.answer("PDF yaratish uchun kamida bitta rasm yuboring.", reply_markup=work_menu())
        return

    await message.answer("PDF tayyorlanmoqda...", reply_markup=remove_keyboard())
    output_name = safe_file_name(f"scan_{uuid.uuid4().hex[:8]}.pdf")
    output_path = session.folder / output_name
    scan_mode = session.mode == MODE_SCAN

    try:
        build_pdf(session.images, output_path=output_path, scan_mode=scan_mode)
        await message.answer_document(FSInputFile(output_path), caption="PDF tayyor")
        await message.answer("Yana PDF yaratish uchun rejim tanlang.", reply_markup=main_menu())
    except Exception:
        log.exception("PDF build failed")
        await message.answer("PDF yaratishda xatolik bo'ldi. Qayta urinib ko'ring.", reply_markup=main_menu())
    finally:
        sessions.cancel(uid)


@dp.message()
async def h_unknown(message: Message) -> None:
    session = sessions.get(user_id(message))
    if session:
        await message.answer("Rasm yuboring yoki PDF yaratish tugmasini bosing.", reply_markup=work_menu())
    else:
        await message.answer("Boshlash uchun rejim tanlang.", reply_markup=main_menu())


async def run_webhook() -> None:
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    webhook_path = f"/webhook/{settings.bot_token[-12:]}"
    webhook_url = f"{settings.render_external_url}{webhook_path}"
    await bot.set_webhook(webhook_url, drop_pending_updates=True)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)

    async def health(_: web.Request) -> web.Response:
        return web.Response(text="OK")

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", settings.port).start()
    log.info("Webhook server started on port %s", settings.port)
    await asyncio.Event().wait()


async def main() -> None:
    cleanup_old_tmp(settings.tmp_dir)
    if settings.render_external_url:
        await run_webhook()
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    asyncio.run(main())
