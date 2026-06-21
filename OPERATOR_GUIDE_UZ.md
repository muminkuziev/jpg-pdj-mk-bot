# Operator uchun qisqa yo'riqnoma

## Botni tayyorlash

1. Telegram'da @BotFather oching.
2. `/newbot` bosing.
3. Bot nomi va username bering.
4. Tokenni oling.
5. `C:\Users\ggani\scan2pdf-bot\.env` faylini yarating.
6. Ichiga yozing:

```env
BOT_TOKEN=TOKENNI_SHU_YERGA_QOYING
MAX_IMAGES=20
MAX_FILE_MB=10
TMP_DIR=tmp
```

## Lokal test

```powershell
cd C:\Users\ggani\scan2pdf-bot
pip install -r requirements.txt
python bot.py
```

Keyin Telegram'da botga `/start` yuboring.

## Bot qanday ishlaydi

1. Foydalanuvchi `/start` bosadi.
2. `Oddiy PDF` yoki `Skaner PDF` tanlaydi.
3. Bitta yoki bir nechta rasm yuboradi.
4. `PDF yaratish` bosadi.
5. Bot PDF fayl qaytaradi.

## Qaysi rejimni tanlash kerak

- `Oddiy PDF`: rasm sifati o'zgarmaydi, A4 PDF bo'ladi.
- `Skaner PDF`: kamera bilan olingan hujjat rasmini tiniqlashtiradi.

## Render deploy uchun tavsiya

Hozircha Render Free bilan boshlash mumkin.
Render Free 15 daqiqa traffic bo'lmasa uxlab qoladi, shuning uchun Telegram bot birinchi xabarga kechroq javob berishi mumkin.
Keyinchalik haqiqiy 24/7 kerak bo'lsa, Render'da `Starter` yoki undan yuqori planga o'ting.

Render sozlamalari:

```text
Service type: Web Service
Build command: pip install --upgrade pip && pip install --prefer-binary -r requirements.txt
Start command: python bot.py
Health check path: /health
Plan: Free
```

Environment Variables:

```env
BOT_TOKEN=BotFather bergan token
MAX_IMAGES=20
MAX_FILE_MB=10
TMP_DIR=tmp
```

GitHub'ga `.env` faylini yubormang. Token faqat Render Environment Variables ichida turadi.
