# 📚 Kutubxona Tizimi (Library System)

TIU Bot uchun yaratilgan kutubxona tizimi - foydalanuvchilar 9 ta kategoriya orqali PDF kitoblarni ko'rishi va yuklab olishi mumkin.

## 📋 Tizim tavsifi

- **9 ta kategoriya** - har bir kategoriya uchun alohida Telegram kanali
- **Sahifalash** - har sahifada 15 ta kitob
- **Qidirish** - kitob yoki muallif nomi bo'yicha
- **Sevimlilar** - foydalanuvchi o'z sevimli kitoblarini saqlashi mumkin
- **Statistika** - admin uchun yuklab olishlar statistikasi

## 🏗️ Kategoriyalar

| # | Kategoriya | Emoji | Kanal |
|---|-----------|-------|-------|
| 1 | TOP-ADABIYOTLAR | 📕 | @tiu_library_top |
| 2 | IQTISODIY ADABIYOTLAR | 📊 | @tiu_library_economics |
| 3 | BADIY ADABIYOTLAR | 🎨 | @tiu_library_fiction |
| 4 | IT SOHA | 💻 | @tiu_library_it |
| 5 | TA'LIM ADABIYOTLARI | 📚 | @tiu_library_education |
| 6 | XORIJIY TIL ADABIYOTLARI | 🌍 | @tiu_library_languages |
| 7 | HUQUQIY SOHA | ⚖️ | @tiu_library_law |
| 8 | ILMIY ADABIYOTLAR | 🔬 | @tiu_library_science |
| 9 | BOSHQA TURDAGI | 📖 | @tiu_library_other |

## 🚀 O'rnatish

### 1. Database'ni yaratish

Kategoriyalarni database'ga qo'shish:

```bash
python init_library_categories.py
```

Bu skript 9 ta kategoriyani database'ga qo'shadi.

### 2. Telegram kanallarni yaratish

Har bir kategoriya uchun **private** Telegram kanal yaratish kerak:

1. Telegram'da yangi kanal yarating
2. Kanal turini **Private** qilib belgilang
3. Kanal username'ini yuqoridagi jadvalga mos ravishda o'rnating
4. Bot'ni kanalga **admin** sifatida qo'shing
5. Bot'ga quyidagi ruxsatlarni bering:
   - ✅ Post messages
   - ✅ Delete messages
   - ✅ Read message history

### 3. Kitoblarni qo'shish

Kitoblarni qo'shish uchun 2 ta yo'l:

#### A. Qo'lda (database ga bevosita)

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('tiu_bot.db')
c = conn.cursor()

c.execute('''
    INSERT INTO library_books
    (category_id, title_uz, title_ru, title_en, author, year, pages, language, description, file_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    1,  # category_id (1 = TOP-ADABIYOTLAR)
    "O'tkan kunlar",  # title_uz
    "Минувшие дни",  # title_ru
    "Bygone Days",  # title_en
    "Abdulla Qodiriy",  # author
    2020,  # year
    520,  # pages
    "O'zbek",  # language
    "O'zbek adabiyotining eng yaxshi asarlaridan biri",  # description
    "FILE_ID_HERE",  # file_id - PDF file_id from Telegram
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # created_at
))

conn.commit()
conn.close()
```

#### B. Telegram kanaldan forward qilish (tavsiya etiladi)

1. Telegram kanaliga PDF kitobni caption bilan yuklang:
   ```
   📘 O'tkan kunlar
   ✍️ Abdulla Qodiriy
   📅 2020
   📄 520 sahifa
   ```

2. Bot post'dan `file_id`'ni oladi
3. Kitobni database'ga qo'shish uchun quyidagi formatda SQL query yuboring

## 📱 Foydalanuvchi oqimi

### 1. Kutubxona menyusini ochish

```
User: [📚 Kutubxona tugmasini bosadi]

Bot: 📚 KUTUBXONA

Kategoriyani tanlang:

[3x3 grid inline keyboard ko'rsatiladi]
┌──────────────┬──────────────┬──────────────┐
│ 📕 TOP       │ 📊 IQTISODIY │ 🎨 BADIY     │
│ (234 kitob)  │ (189 kitob)  │ (156 kitob)  │
├──────────────┼──────────────┼──────────────┤
│ 💻 IT        │ 📚 TA'LIM    │ 🌍 TIL       │
│ (145 kitob)  │ (98 kitob)   │ (167 kitob)  │
├──────────────┼──────────────┼──────────────┤
│ ⚖️ HUQUQ     │ 🔬 ILMIY     │ 📖 BOSHQA    │
│ (123 kitob)  │ (178 kitob)  │ (89 kitob)   │
└──────────────┴──────────────┴──────────────┘
[🌟 Tavsiya etiladigan kitoblar]
[⭐ Sevimli kitoblar]
```

### 2. Kategoriya tanlash va kitoblar ro'yxati

```
User: [📊 IQTISODIY ADABIYOTLAR]

Bot: 📚 IQTISODIY ADABIYOTLAR (189 kitob)

Kerakli kitob raqamini yozing:

/1  📕 Iqtisodiyot nazariyasi - G. Mankiw (2022)
/2  📗 Mikro iqtisodiyot - R. Pindyck (2021)
/3  📘 Makro iqtisodiyot - O. Blanchard (2023)
...
/15 📘 Bozor iqtisodiyoti - F. Mishkin (2020)

📄 Sahifa 1 / 13
📄 Keyingi 15 ta: /next

🔍 Qidirish: Kitob yoki muallif nomini yozing
🔙 Orqaga: /back
```

### 3. Kitobni yuklab olish

```
User: /3

Bot: 📥 Yuklanmoqda...

Bot: [Kitob ma'lumoti]
📘 Makro iqtisodiyot
✍️ Muallif: Olivier Blanchard
📅 Yil: 2023
📄 Sahifalar: 672
🗂 Kategoriya: Iqtisodiy adabiyotlar
🌐 Til: O'zbek

[PDF fayl yuboriladi]

✅ Kitob muvaffaqiyatli yuborildi!

💡 Boshqa kitoblar:
- Keyingi kitob: /4
- Kategoriyaga qaytish: /back

[Inline tugmalar:]
[⭐ Sevimlilar] [🔙 Orqaga]
```

### 4. Sahifalash

```
User: /next

Bot: [Keyingi 15 ta kitob ko'rsatiladi]
📚 IQTISODIY ADABIYOTLAR (189 kitob)

/16 📕 ...
/17 📗 ...
...
/30 📘 ...

📄 Sahifa 2 / 13
📄 Oldingi 15 ta: /prev
📄 Keyingi 15 ta: /next
```

### 5. Qidirish

```
User: Mankiw

Bot: 🔍 Qidiruv natijalari "Mankiw":

/1  📕 Iqtisodiyot nazariyasi - G. Mankiw (2022)
/45 📗 Makroiqtisodiyot - N. Gregory Mankiw (2021)

🔙 Orqaga: /back
```

## 🛠️ Database strukturasi

### library_categories

| Ustun | Turi | Tavsif |
|-------|------|--------|
| id | INTEGER | Primary key |
| name_uz | TEXT | Kategoriya nomi (o'zbek) |
| name_ru | TEXT | Kategoriya nomi (rus) |
| name_en | TEXT | Kategoriya nomi (ingliz) |
| emoji | TEXT | Kategoriya emoji |
| channel_id | TEXT | Telegram kanal ID |
| channel_username | TEXT | Telegram kanal username |
| is_active | INTEGER | Faol/nofaol (0/1) |
| created_at | TEXT | Yaratilgan vaqt |

### library_books

| Ustun | Turi | Tavsif |
|-------|------|--------|
| id | INTEGER | Primary key |
| category_id | INTEGER | Kategoriya ID (FK) |
| title_uz | TEXT | Kitob nomi (o'zbek) |
| title_ru | TEXT | Kitob nomi (rus) |
| title_en | TEXT | Kitob nomi (ingliz) |
| author | TEXT | Muallif |
| year | INTEGER | Nashr yili |
| pages | INTEGER | Sahifalar soni |
| language | TEXT | Kitob tili |
| description | TEXT | Tavsif |
| file_id | TEXT | Telegram file_id |
| channel_message_id | INTEGER | Kanal message ID |
| download_count | INTEGER | Yuklab olishlar soni |
| is_featured | INTEGER | Tavsiya etilgan (0/1) |
| created_at | TEXT | Yaratilgan vaqt |

### library_downloads

| Ustun | Turi | Tavsif |
|-------|------|--------|
| id | INTEGER | Primary key |
| book_id | INTEGER | Kitob ID (FK) |
| user_id | INTEGER | Foydalanuvchi ID |
| downloaded_at | TEXT | Yuklab olingan vaqt |

### library_favorites

| Ustun | Turi | Tavsif |
|-------|------|--------|
| id | INTEGER | Primary key |
| book_id | INTEGER | Kitob ID (FK) |
| user_id | INTEGER | Foydalanuvchi ID |
| added_at | TEXT | Qo'shilgan vaqt |

## 📊 Statistika (Admin)

Admin `/library_stats` buyrug'i orqali statistikani ko'rishi mumkin:

```
📊 Kutubxona statistikasi:

📚 Jami kitoblar: 1,379
📥 Jami yuklab olishlar: 12,456
👥 Faol foydalanuvchilar: 2,345

🔝 Top kategoriyalar:
1. IT SOHA - 3,456 yuklab olish
2. IQTISODIY - 2,789 yuklab olish
3. HUQUQIY - 1,987 yuklab olish

📖 Top kitoblar:
1. "Python dasturlash" - 567 marta
2. "Marketing asoslari" - 456 marta
3. "Iqtisodiyot nazariyasi" - 389 marta
```

## 🔐 Xavfsizlik

- **Private kanallar**: Faqat bot admin sifatida kanalga kirishi mumkin
- **File ID cache**: Birinchi yuborilgandan keyin file_id database'da saqlanadi
- **Download tracking**: Har bir yuklab olish statistikaga yoziladi

## 🐛 Muammolarni hal qilish

### 1. Kategoriyalar ko'rinmayapti

```bash
# Database'ni tekshiring
sqlite3 tiu_bot.db "SELECT * FROM library_categories;"

# Agar bo'sh bo'lsa, kategoriyalarni qayta qo'shing
python init_library_categories.py
```

### 2. Kitoblar yuborilmayapti

- Bot kanal adminmi?
- Bot'da to'g'ri ruxsatlar bormi?
- `file_id` to'g'rimi?

### 3. Qidiruv ishlamayapti

- Kitob nomlari to'g'ri kiritilganmi?
- Database'da ma'lumotlar bormi?

## 📝 Keyingi qadamlar

1. ✅ Admin panel orqali kitob qo'shish funksiyasini qo'shish
2. ✅ Bulk import (CSV/Excel dan)
3. ✅ Kitob tahrirlash funksiyasi
4. ✅ Kanal sync (kanaldan avtomatik book import)
5. ✅ PDF preview (birinchi sahifa)

## 👨‍💻 Muallif

TIU Bot Development Team

## 📄 Litsenziya

Internal use only - Tashkent International University
