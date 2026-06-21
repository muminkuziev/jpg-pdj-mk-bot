# Scan2PDF Telegram Bot

Rasmni PDF qiladigan Telegram bot. CV_MK loyihasidan butunlay alohida.

## Funksiyalar

- Bitta rasmni PDF qilish
- Bir nechta rasmni bitta PDF qilish
- Oddiy PDF rejimi
- Skaner PDF rejimi: kamera bilan olingan rasmni kontrast/tiniqlik bilan yaxshilaydi
- A4 sahifaga joylash
- PDF yuborilgandan keyin vaqtinchalik fayllarni o'chirish
- Lokal polling rejimi
- Render'da webhook rejimi
- Docker/VPS uchun tayyor fayllar

## Papka Tuzilishi

```text
scan2pdf-bot/
  bot.py
  app/
    cleanup.py
    config.py
    image_processing.py
    keyboards.py
    pdf_builder.py
    sessions.py
  requirements.txt
  render.yaml
  Dockerfile
  docker-compose.yml
  .env.example
```

## Lokal Ishga Tushirish

1. BotFather orqali Telegram bot oching.
2. Tokenni oling.
3. `.env.example` faylidan `.env` yarating.
4. `.env` ichiga tokenni yozing:

```env
BOT_TOKEN=123456:YOUR_TOKEN
MAX_IMAGES=20
MAX_FILE_MB=10
TMP_DIR=tmp
```

5. Dependency o'rnating:

```bash
pip install -r requirements.txt
```

6. Botni ishga tushiring:

```bash
python bot.py
```

## Docker Bilan Ishga Tushirish

```bash
docker compose up -d --build
```

Loglarni ko'rish:

```bash
docker compose logs -f
```

To'xtatish:

```bash
docker compose down
```

## Render Deploy

1. GitHub'ga `scan2pdf-bot` loyihasini alohida repository qilib yuklang.
2. Render'da Blueprint yoki Web Service yarating.
3. `BOT_TOKEN` env variable qo'shing.
4. `render.yaml` avtomatik ishlaydi.

Render'da `RENDER_EXTERNAL_URL` bo'lsa bot webhook rejimida ishlaydi. Lokal kompyuterda esa polling rejimida ishlaydi.

Hozircha Render Free bilan boshlash mumkin. `Free` web service 15 daqiqa traffic bo'lmasa uxlab qoladi, shuning uchun Telegram bot birinchi xabarga kechroq javob berishi mumkin. Keyinchalik haqiqiy 24/7 kerak bo'lsa, `Starter` yoki undan yuqori planga o'ting.

## Limitlar

- `MAX_IMAGES`: bitta PDF uchun maksimal rasm soni, default 20
- `MAX_FILE_MB`: bitta rasm maksimal hajmi, default 10 MB

## Muhim

Bu loyiha CV_MK bilan aralashmaydi. Uni alohida repository sifatida ishlating.
