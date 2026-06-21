from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

MODE_NORMAL = "Oddiy PDF"
MODE_SCAN = "Skaner PDF"
MAKE_PDF = "PDF yaratish"
CANCEL = "Bekor qilish"
NEW_PDF = "Yangi PDF"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MODE_NORMAL), KeyboardButton(text=MODE_SCAN)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def work_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MAKE_PDF)],
            [KeyboardButton(text=CANCEL), KeyboardButton(text=NEW_PDF)],
        ],
        resize_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
