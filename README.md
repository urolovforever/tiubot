# 🎓 TIU Official Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Aiogram](https://img.shields.io/badge/Aiogram-2.25.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Tashkent International University rasmiy Telegram boti**

[O'rnatish](#-ornatish) • [Xususiyatlar](#-xususiyatlar) • [Struktura](#-loyiha-strukturasi) • [Qo'llanma](#-qollanma)

</div>

---

## 📋 Mundarija

- [Umumiy ma'lumot](#-umumiy-malumot)
- [Xususiyatlar](#-xususiyatlar)
- [Talablar](#-talablar)
- [O'rnatish](#-ornatish)
- [Konfiguratsiya](#-konfiguratsiya)
- [Loyiha strukturasi](#-loyiha-strukturasi)
- [Foydalanish](#-foydalanish)
- [Admin panel](#-admin-panel)
- [Database](#-database)
- [Jadval qo'shish](#-jadval-qoshish)
- [Muammolarni hal qilish](#-muammolarni-hal-qilish)
- [Hissa qo'shish](#-hissa-qoshish)
- [Litsenziya](#-litsenziya)

---

## 🌟 Umumiy ma'lumot

TIU Official Bot - bu Tashkent International University uchun ishlab chiqilgan to'liq funksional Telegram bot. Bot talabalar, abituriyentlar va universitet xodimlari uchun qulay interfeys orqali barcha zarur ma'lumotlarni taqdim etadi.

### ✨ Asosiy imkoniyatlar

- 🌐 **3 tilda** - O'zbek, Rus, Ingliz
- 📱 **Reply Keyboard** - Faqat reply keyboard, inline yo'q
- 🗂 **Submenu tizimi** - Har bir bo'limda ichki menyular
- 📅 **Dars jadvali** - Fakultet → Yo'nalish → Kurs → Guruh
- 📬 **Murojaatlar** - To'liq feedback tizimi
- 👨‍💼 **Admin panel** - Murojaatlar va tadbirlar boshqaruvi
- 📢 **Tadbirlar** - Universitet tadbirlari e'lonlari

---

## 🎯 Xususiyatlar

### 👥 Foydalanuvchilar uchun:

#### 1️⃣ **TIU haqida** (4 ta submenu)
- 🎓 Universitet haqida qisqacha ma'lumot
- 🌍 Hamkor universitetlar
- 📚 Fakultetlar va dasturlar
- 🎥 Video turlar

#### 2️⃣ **Qabul** (5 ta submenu)
- 📋 Qabul shartlari
- 💰 To'lov va grant tizimi
- 🌐 Online ro'yxatdan o'tish
- 📞 Qabul bo'limi bilan bog'lanish
- ❓ Tez-tez so'raladigan savollar

#### 3️⃣ **Talabalar uchun** (4 ta submenu)
- 📅 Dars jadvali (4 bosqichli)
- 🧾 To'lov tizimi
- 📚 Kutubxona / resurslar
- 🎉 Talabalar hayoti / klublar

#### 4️⃣ **Dars jadvali** (Talabalar ichida)
- Fakultet tanlash (2 ta: IT va Biznes)
- Yo'nalish tanlash (har birida 9 ta)
- Kurs tanlash (1-4 kurs)
- Guruh tanlash
- Jadval rasmini olish

#### 5️⃣ **Tadbirlar**
- Tadbirlar ro'yxati
- Tadbir tafsilotlari
- Sana va manzil

#### 6️⃣ **Murojaatlar** (6 bosqichli)
- Kim sifatida (Talaba/Abituriyent/Ota-ona/Xodim)
- Murojaat turi (Savol/Taklif/Shikoyat/Tashakkur)
- Matn yozish
- Telefon raqam
- Fayl biriktirish (ixtiyoriy)
- Mening murojaatlarim

#### 7️⃣ **Yangiliklar** (3 ta submenu)
- 🆕 So'nggi yangiliklar
- 🎥 Video yangiliklar
- 🗓 Tadbirlar taqvimi

#### 8️⃣ **Aloqa**
- Manzil, telefon, email
- Ijtimoiy tarmoqlar havolalari

#### 9️⃣ **Sozlamalar**
- 🌐 Tilni o'zgartirish
- Til tanlovi saqlanadi

### 👨‍💼 Admin uchun:

- 📬 **Murojaatlarni ko'rish** - Barcha yangi murojaatlar
- 💬 **Javob berish** - `/reply_<id>` orqali
- ➕ **Tadbir qo'shish** - Yangi tadbirlar e'lon qilish
- 🗑 **Tadbirlarni o'chirish** - Eski tadbirlarni boshqarish
- 📊 **To'liq ma'lumot** - Foydalanuvchi ID, username, telefon

---

## 📦 Talablar

- Python 3.8 yoki yuqori
- pip (Python package manager)
- Telegram Bot Token ([@BotFather](https://t.me/BotFather) dan)
- SQLite3 (Python bilan birga keladi)

---

## 🚀 O'rnatish

### 1. Repository'ni clone qiling

```bash
git clone https://github.com/yourusername/tiu-bot.git
cd tiu-bot
```

### 2. Virtual environment yarating

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 4. `.env` faylini yarating

```bash
# .env.example faylidan nusxa oling
cp .env.example .env

# Yoki Windows da
copy .env.example .env
```

`.env` faylini oching va BOT_TOKEN ni kiriting:
```env
BOT_TOKEN=your_actual_bot_token_here
ADMIN_GROUP_ID=-5012065617
DIGEST_CHANNEL_ID=-1003285608799
```

> **Muhim:** BOT_TOKEN majburiy. `.env` faylida bo'lmasa bot ishlamaydi.

### 5. `config.py` ni sozlang

`config.py` faylida admin ID larini o'zgartiring:

```python
ADMIN_IDS = [123456789]  # O'z telegram ID ngizni kiriting
```

💡 **ID ni qanday bilish:**
- [@userinfobot](https://t.me/userinfobot) ga `/start` yozing
- Bot sizga ID ni beradi

### 6. Botni ishga tushiring

```bash
python bot.py
```

✅ Bot ishga tushdi! Telegram'da botingizni `/start` bilan ishga tushiring.

---

## ⚙️ Konfiguratsiya

### `config.py` fayli

```python
# Bot sozlamalari (.env faylidan o'qiladi)
BOT_TOKEN = os.getenv('BOT_TOKEN')  # MAJBURIY - .env faylida bo'lishi kerak
ADMIN_IDS = [123456789, 987654321]  # Admin ID lari

# Fakultetlar va yo'nalishlar
FACULTIES = {
    'uz': {
        'Biznes va innovatsion ta\'lim': {...},
        'Yurisprudensiya': {...}
    },
    'ru': {...},
    'en': {...}
}
```

### Muhim sozlamalar

| O'zgaruvchi | Tavsif | Joylashuv |
|-------------|--------|-----------|
| `BOT_TOKEN` | Telegram bot tokeni (MAJBURIY) | `.env` |
| `ADMIN_GROUP_ID` | Murojaatlar guruhi ID | `.env` |
| `DIGEST_CHANNEL_ID` | Haftalik yangiliklar kanali | `.env` |
| `ADMIN_IDS` | Admin foydalanuvchilar ID lari | `config.py` |
| `FACULTIES` | Fakultet va yo'nalishlar | `config.py` |

---

## 📁 Loyiha strukturasi

```
tiu_bot/
├── 📄 bot.py                      # Asosiy ishga tushiruvchi fayl
├── ⚙️ config.py                   # Konfiguratsiya va sozlamalar
├── 🔐 .env                        # Bot tokeni (git'ga qo'shilmaydi)
├── 📝 .env.example                # Namuna environment fayli
├── 📋 requirements.txt            # Production kutubxonalari
├── 📋 requirements-dev.txt        # Development kutubxonalari (testlar)
├── 📖 README.md                   # Bu fayl
├── 🚫 .gitignore                  # Git ignore fayli
│
├── 📂 database/
│   ├── __init__.py
│   └── db.py                      # Database operatsiyalari (SQLite)
│
├── 📂 keyboards/
│   ├── __init__.py
│   ├── reply.py                   # Reply klaviaturalar
│   └── inline.py                  # Inline klaviaturalar
│
├── 📂 handlers/
│   ├── __init__.py
│   ├── start.py                   # Start va orqaga komandalar
│   ├── settings.py                # Sozlamalar va til
│   ├── about.py                   # TIU haqida (4 submenu)
│   ├── contact.py                 # Aloqa ma'lumotlari
│   ├── admission.py               # Qabul (5 submenu)
│   ├── students.py                # Talabalar (4 submenu + jadval)
│   ├── news.py                    # Yangiliklar (3 submenu)
│   ├── events.py                  # Tadbirlar
│   ├── event_quick_create.py      # Tez tadbir qo'shish
│   ├── applications.py            # Murojaatlar (6 bosqich)
│   ├── library.py                 # Kutubxona tizimi
│   ├── universal_broadcast.py     # Broadcast tizimi
│   ├── channel_handler.py         # Kanal postlarini saqlash
│   └── admin.py                   # Admin panel
│
├── 📂 utils/
│   ├── __init__.py
│   ├── translations.py            # 3 tilda tarjimalar
│   ├── helpers.py                 # Yordamchi funksiyalar
│   └── event_reminders.py         # Tadbir eslatmalari
│
├── 📂 states/
│   ├── __init__.py
│   └── forms.py                   # FSM states
│
├── 📂 scripts/                    # Yordamchi skriptlar
│   ├── init_library_categories.py # Kutubxona kategoriyalarini yaratish
│   └── add_demo_books.py          # Demo kitoblarni qo'shish
│
├── 📂 tests/                      # Testlar
│   ├── conftest.py
│   ├── unit/                      # Unit testlar
│   └── integration/               # Integration testlar
│
└── 📂 photos/                     # Rasm fayllar
```

---

## 📱 Foydalanish

### Oddiy foydalanuvchi

1. Botni `/start` bilan ishga tushiring
2. Tilni tanlang (agar birinchi marta bo'lsa)
3. Asosiy menyudan kerakli bo'limni tanlang
4. Har bir bo'limda submenyular mavjud
5. "⬅️ Orqaga" tugmasi bilan qaytish mumkin

### Navigatsiya strukturasi

```
🏠 Asosiy menyu
│
├─ 🏫 TIU haqida
│  ├─ 🎓 Universitet haqida
│  ├─ 🌍 Hamkor universitetlar
│  ├─ 📚 Fakultetlar
│  ├─ 🎥 Video turlar
│  └─ ⬅️ Orqaga
│
├─ 🧑‍🎓 Qabul
│  ├─ 📋 Qabul shartlari
│  ├─ 💰 To'lov va grant
│  ├─ 🌐 Online ro'yxat
│  ├─ 📞 Bog'lanish
│  ├─ ❓ FAQ
│  └─ ⬅️ Orqaga
│
├─ 🎓 Talabalar uchun
│  ├─ 📅 Dars jadvali
│  │  ├─ Fakultet tanlash
│  │  ├─ Yo'nalish tanlash
│  │  ├─ Kurs tanlash
│  │  └─ Guruh tanlash
│  ├─ 🧾 To'lov tizimi
│  ├─ 📚 Kutubxona
│  ├─ 🎉 Klublar
│  └─ ⬅️ Orqaga
│
├─ 📢 Tadbirlar
│
├─ 📬 Murojaatlar
│  ├─ ✍️ Murojaat yuborish
│  │  ├─ Kim sifatida
│  │  ├─ Murojaat turi
│  │  ├─ Matn
│  │  ├─ Telefon
│  │  └─ Fayl (ixtiyoriy)
│  ├─ 🔎 Mening murojaatlarim
│  └─ ⬅️ Orqaga
│
├─ 📰 Yangiliklar
│  ├─ 🆕 So'nggi yangiliklar
│  ├─ 🎥 Video
│  ├─ 🗓 Tadbirlar taqvimi
│  └─ ⬅️ Orqaga
│
├─ 📞 Aloqa
│
├─ ⚙️ Sozlamalar
│  ├─ 🌐 Tilni o'zgartirish
│  └─ ⬅️ Orqaga
│
└─ 👨‍💼 Admin panel (faqat adminlar)
   ├─ 📬 Murojaatlar
   ├─ ➕ Tadbir qo'shish
   ├─ 📝 Tadbirlar boshqaruvi
   └─ ⬅️ Orqaga
```

---

## 👨‍💼 Admin panel

### Admin komandalar

#### 1. Murojaatlarga javob berish

Yangi murojaat kelganda admin shunday xabar oladi:

```
🆕 Yangi murojaat #5

👤 Foydalanuvchi:
  • Ism: John Doe
  • Username: @johndoe
  • ID: 123456789
  • Link: tg://user?id=123456789
  • Telefon: +998901234567

📋 Murojaat:
  • Kim: Talaba
  • Turi: Savol

💬 Matn:
Salom! Qabul bo'yicha savol...

📌 Javob: /reply_5
```

Javob berish:
```
/reply_5
```

Keyin matn yozasiz va javob yuboriladi.

#### 2. Tadbir qo'shish

1. Admin panel → ➕ Tadbir qo'shish
2. Nom kiriting
3. Tavsif kiriting
4. Sana kiriting (25.12.2024)
5. Manzil kiriting
6. Rasm yuboring (yoki `skip`)

#### 3. Tadbirlarni o'chirish

1. Admin panel → 📝 Tadbirlarni boshqarish
2. O'chiriladigan tadbirni tanlang
3. Tasdiqlang

---

## 💾 Database

### Jadvallar strukturasi

#### **users** jadvali
```sql
- user_id (PRIMARY KEY)    -- Telegram user ID
- username                 -- @username
- full_name                -- To'liq ism
- phone_number             -- Telefon raqam
- language                 -- uz/ru/en
- registration_date        -- Ro'yxatdan o'tgan sana
```

#### **applications** jadvali
```sql
- id (AUTOINCREMENT)       -- Murojaat ID
- user_id                  -- Foydalanuvchi ID
- username                 -- @username
- full_name                -- To'liq ism
- phone_number             -- Telefon raqam
- message                  -- Murojaat matni
- file_id                  -- Fayl ID (agar bor bo'lsa)
- status                   -- new/answered
- created_at               -- Yaratilgan vaqt
- admin_response           -- Admin javobi
```

#### **events** jadvali
```sql
- id (AUTOINCREMENT)       -- Tadbir ID
- title                    -- Nom
- description              -- Tavsif
- date                     -- Sana
- location                 -- Manzil
- image_id                 -- Rasm ID
- created_at               -- Yaratilgan vaqt
```

#### **schedules** jadvali
```sql
- id (AUTOINCREMENT)       -- Jadval ID
- faculty                  -- Fakultet
- direction                -- Yo'nalish
- course                   -- Kurs
- group_name               -- Guruh
- image_id                 -- Jadval rasmi ID
- created_at               -- Yaratilgan vaqt
```

---

## 📅 Jadval qo'shish

### Python orqali

```python
from database.db import Database

db = Database()

# Jadval qo'shish
db.save_schedule(
    faculty='IT fakulteti',
    direction='Dasturiy injiniring',
    course='2-kurs',
    group_name='201-21',
    image_id='AgACAgIAAxkBAAIC...'  # Telegram file_id
)
```

### File ID ni qanday olish?

#### Metod 1: Bot orqali
1. Jadval rasmini botga yuboring
2. `bot.log` faylida file_id ni toping

#### Metod 2: Maxsus handler
```python
@dp.message_handler(content_types=['photo'])
async def get_photo_id(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.answer(f"File ID: {file_id}")
```

### Ko'p jadval qo'shish

```python
from database.db import Database

db = Database()

jadvallar = [
    ('IT fakulteti', 'Dasturiy injiniring', '1-kurs', '101-23', 'AgACAgIA...'),
    ('IT fakulteti', 'Dasturiy injiniring', '1-kurs', '102-23', 'AgACAgIA...'),
    ('IT fakulteti', 'Dasturiy injiniring', '2-kurs', '201-22', 'AgACAgIA...'),
    ('Biznes fakulteti', 'Marketing', '1-kurs', '101-23', 'AgACAgIA...'),
]

for fakultet, yonalish, kurs, guruh, file_id in jadvallar:
    db.save_schedule(fakultet, yonalish, kurs, guruh, file_id)
    print(f"✅ Qo'shildi: {fakultet} - {yonalish} - {kurs} - {guruh}")
```

---

## 🐛 Muammolarni hal qilish

### Bot javob bermayapti

**Muammo:** Bot ishlamayapti

**Yechim:**
```bash
# 1. Bot tokenini tekshiring
cat .env

# 2. Loglarni ko'ring
tail -f bot.log

# 3. Botni qayta ishga tushiring
python bot.py
```

### Admin panel ko'rinmayapti

**Muammo:** Admin tugmasi ko'rinmayapti

**Yechim:**
```python
# config.py da ID ni tekshiring
ADMIN_IDS = [your_id]  # To'g'ri ID kiriting

# O'z ID ni bilish: @userinfobot
```

### Jadval topilmayapti

**Muammo:** "Jadval topilmadi" xabari

**Yechim:**
```python
# Database'ni tekshiring
import sqlite3
conn = sqlite3.connect('tiu_bot.db')
cursor = conn.cursor()

# Barcha jadvallarni ko'rish
cursor.execute("SELECT * FROM schedules")
print(cursor.fetchall())

# Fakultet va yo'nalish nomlari to'g'ri yozilganini tekshiring
```

### Import xatoligi

**Muammo:** `ModuleNotFoundError`

**Yechim:**
```bash
# Virtual environment aktivlashtirilganini tekshiring
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Kutubxonalarni qayta o'rnating
pip install -r requirements.txt
```

### Database xatoligi

**Muammo:** Database'ga yozib bo'lmayapti

**Yechim:**
```bash
# Database faylini o'chiring va qayta yarating
rm tiu_bot.db
python bot.py
```

---

## 📊 Loglar

### Log faylini ko'rish

```bash
# Hozirgi loglarni ko'rish
tail -f bot.log

# Oxirgi 100 qatorni ko'rish
tail -100 bot.log

# Xatolarni qidirish
grep ERROR bot.log

# Ma'lum bir foydalanuvchini qidirish
grep "user_id: 123456789" bot.log
```

### Log darajalari

- **INFO** - Oddiy ma'lumot
- **WARNING** - Ogohlantirish
- **ERROR** - Xatolik
- **CRITICAL** - Jiddiy xatolik

---

## 🔒 Xavfsizlik

### Muhim sozlamalar

1. **.env faylini git'ga qo'shmang**
   ```bash
   # .gitignore faylida
   .env
   *.db
   ```

2. **Admin ID larini maxfiy saqlang**
   ```python
   # config.py
   ADMIN_IDS = [123456789]  # Faqat ishonchli odamlar
   ```

3. **Database'ni backup qiling**
   ```bash
   # Har kuni backup
   cp tiu_bot.db backups/tiu_bot_$(date +%Y%m%d).db
   ```

4. **Loglarni tekshiring**
   ```bash
   # Har kuni loglarni ko'ring
   tail -100 bot.log
   ```

---

## 🚢 Production'ga deploy qilish

### 1. Server'ga o'rnatish

```bash
# Server'ga ulanish
ssh user@your-server.com

# Repository clone qilish
git clone https://github.com/yourusername/tiu-bot.git
cd tiu-bot

# Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env yaratish
nano .env
# BOT_TOKEN ni kiriting

# Botni ishga tushirish
nohup python bot.py &
```

### 2. Systemd service (tavsiya etiladi)

```bash
# Service fayl yaratish
sudo nano /etc/systemd/system/tiu-bot.service
```

```ini
[Unit]
Description=TIU Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/tiu-bot
Environment="PATH=/home/yourusername/tiu-bot/venv/bin"
ExecStart=/home/yourusername/tiu-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service'ni ishga tushirish
sudo systemctl daemon-reload
sudo systemctl enable tiu-bot
sudo systemctl start tiu-bot

# Status tekshirish
sudo systemctl status tiu-bot

# Loglarni ko'rish
sudo journalctl -u tiu-bot -f
```

### 3. Docker (ixtiyoriy)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

```bash
# Build va run
docker build -t tiu-bot .
docker run -d --name tiu-bot --restart always tiu-bot
```

---

## 🤝 Hissa qo'shish

Loyihaga hissa qo'shmoqchimisiz? Quyidagi qadamlarga amal qiling:

1. **Fork qiling** - Repository'ni fork qiling
2. **Branch yarating** - `git checkout -b feature/YangiXususiyat`
3. **Commit qiling** - `git commit -m 'Yangi xususiyat qo'shildi'`
4. **Push qiling** - `git push origin feature/YangiXususiyat`
5. **Pull Request oching** - GitHub'da PR oching

### Kod yozish qoidalari

- Python PEP 8 standartiga amal qiling
- Har bir funksiyaga docstring yozing
- Test yozing (agar mumkin bo'lsa)
- README'ni yangilang

---

## 📞 Yordam va qo'llab-quvvatlash

### Savollar

Savollar bo'lsa:
- 📧 Email: info@tiu.uz
- 💬 Telegram: @tiuofficial
- 🌐 Website: www.tiu.uz

### Bug report

Bug topsangiz:
- GitHub Issues: [github.com/yourusername/tiu-bot/issues](https://github.com/yourusername/tiu-bot/issues)
- Xatolikni batafsil tavsiflang
- Log faylini ilova qiling

---

## 📜 Litsenziya

MIT License

```
Copyright (c) 2024 Tashkent International University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎉 Minnatdorchilik

- [Aiogram](https://github.com/aiogram/aiogram) - Telegram Bot API wrapper
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variables
- Barcha kontributorlar va foydalanuvchilarga

---

## 📊 Statistika

![GitHub stars](https://img.shields.io/github/stars/yourusername/tiu-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/tiu-bot?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/tiu-bot?style=social)

---

<div align="center">

**Made with ❤️ by TIU IT Team**

[⬆ Yuqoriga qaytish](#-tiu-official-telegram-bot)

</div>