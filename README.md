# TIU Official Telegram Bot

Tashkent International University rasmiy Telegram boti.

## Bot haqida

Bu bot TIU talabalar, abituriyentlar va universitet xodimlari uchun mo'ljallangan. Bot orqali quyidagi imkoniyatlardan foydalanish mumkin:

- **3 tilda ishlaydi**: O'zbek, Rus, Ingliz
- **TIU haqida**: Universitet, hamkor universitetlar, fakultetlar, video turlar
- **Qabul**: Qabul shartlari, to'lov va grant, online ro'yxat, FAQ
- **Talabalar uchun**: Dars jadvali, to'lov tizimi, kutubxona, klublar
- **Tadbirlar**: Universitet tadbirlari e'lonlari va eslatmalar
- **Murojaatlar**: Savol, taklif, shikoyat yuborish va javob olish
- **Yangiliklar**: So'nggi yangiliklar, video, tadbirlar taqvimi
- **Admin panel**: Murojaatlarni boshqarish, tadbir qo'shish, broadcast

---

## Tez boshlash (Quick Start)

### 1. Talablar

- Python 3.8+
- pip
- Telegram Bot Token ([@BotFather](https://t.me/BotFather) dan olish)

### 2. O'rnatish

```bash
# Repository'ni clone qiling
git clone <repository-url>
cd tiubot

# Virtual environment yarating
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki Windows da:
# venv\Scripts\activate

# Kutubxonalarni o'rnating
pip install -r requirements.txt
```
### 3. Botni ishga tushirish

```bash
python bot.py
```

Bot ishga tushdi! Telegram'da botga `/start` yuboring.

---

## Loyiha strukturasi

```
tiubot/
├── bot.py                 # Asosiy fayl - botni shu fayl bilan ishga tushirasiz
├── config.py              # Konfiguratsiya (fakultetlar, yo'nalishlar)
├── .env                   # Bot sozlamalari (token, ID lar)
├── requirements.txt       # Python kutubxonalari
├── database/
│   └── db.py              # SQLite database operatsiyalari
├── handlers/              # Barcha bot handlerlari
│   ├── start.py           # /start va asosiy menyu
│   ├── admin.py           # Admin panel
│   ├── applications.py    # Murojaatlar
│   ├── events.py          # Tadbirlar
│   └── ...                # Boshqa handlerlar
├── keyboards/             # Klaviaturalar
├── utils/                 # Yordamchi funksiyalar
├── states/                # FSM holatlar
└── photos/                # Rasm fayllar
```

---

## Server'da ishga tushirish (Production)

### Oddiy usul (nohup)

```bash
# Botni background'da ishga tushirish
nohup python bot.py > /dev/null 2>&1 &

# Jarayonni ko'rish
ps aux | grep bot.py

# To'xtatish
pkill -f bot.py
```

### Systemd service (tavsiya etiladi)

```bash
# Service fayl yaratish
sudo nano /etc/systemd/system/tiubot.service
```

Fayl tarkibi:
```ini
[Unit]
Description=TIU Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/tiubot
Environment="PATH=/home/ubuntu/tiubot/venv/bin"
ExecStart=/home/ubuntu/tiubot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service'ni ishga tushirish
sudo systemctl daemon-reload
sudo systemctl enable tiubot
sudo systemctl start tiubot

# Status tekshirish
sudo systemctl status tiubot

# Loglarni ko'rish
sudo journalctl -u tiubot -f
```

### Docker bilan (ixtiyoriy)

```bash
# Build
docker build -t tiubot .

# Run
docker run -d --name tiubot --restart always --env-file .env tiubot
```

---

## Muhim fayllar

| Fayl | Tavsif | Git'da |
|------|--------|--------|
| `.env` | Bot tokeni va ID lar | Ha |
| `requirements.txt` | Python kutubxonalar | Ha |
| `tiu_bot.db` | SQLite database | Yo'q |
| `bot.log` | Log fayli | Yo'q |

---

## Environment o'zgaruvchilari

| O'zgaruvchi | Tavsif | Majburiy |
|-------------|--------|----------|
| `BOT_TOKEN` | Telegram bot tokeni | Ha |
| `ADMIN_IDS` | Admin ID lari (vergul bilan) | Ha |
| `ADMIN_GROUP_ID` | Murojaatlar guruhi ID | Yo'q |
| `DIGEST_CHANNEL_ID` | Yangiliklar kanali ID | Yo'q |

---

## Muammolarni hal qilish

### Bot ishlamayapti

```bash
# Loglarni tekshiring
tail -f bot.log

# Token to'g'ri kiritilganini tekshiring
cat .env | grep BOT_TOKEN

# Virtual environment aktivmi?
which python  # venv/bin/python bo'lishi kerak
```

### ModuleNotFoundError

```bash
# venv ni aktivlashtiring
source venv/bin/activate

# Kutubxonalarni qayta o'rnating
pip install -r requirements.txt
```

### Database xatosi

```bash
# Database ni qayta yarating
rm tiu_bot.db
python bot.py
```

### Admin panel ko'rinmayapti

`.env` dagi `ADMIN_IDS` da o'z Telegram ID ingiz borligini tekshiring.

---

## Loglar

```bash
# Jonli log ko'rish
tail -f bot.log

# Xatolarni qidirish
grep ERROR bot.log

# Oxirgi 50 qator
tail -50 bot.log
```

---

## Texnologiyalar

- **Python 3.8+**
- **Aiogram 2.25.1** - Telegram Bot API wrapper
- **SQLite** - Database
- **python-dotenv** - Environment variables

---
