"""
Add demo books to library
This script adds sample books to test the library system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.db import Database
from datetime import datetime

def add_demo_books():
    """Add some demo books for testing"""

    db = Database('tiu_bot.db')
    conn = db.get_connection()
    c = conn.cursor()

    # Demo books data
    demo_books = [
        # IT SOHA (category_id = 4)
        {
            'category_id': 4,
            'title_uz': 'Python dasturlash',
            'title_ru': 'Программирование на Python',
            'title_en': 'Python Programming',
            'author': 'Mark Lutz',
            'year': 2023,
            'pages': 1648,
            'language': 'Ingliz',
            'description': 'Python dasturlash tili bo\'yicha to\'liq qo\'llanma. Boshlang\'ich va ilg\'or mavzular.',
            'file_id': None,  # Will be set when actual PDF is uploaded
            'is_featured': 1
        },
        {
            'category_id': 4,
            'title_uz': 'JavaScript: The Definitive Guide',
            'title_ru': 'JavaScript: Полное руководство',
            'title_en': 'JavaScript: The Definitive Guide',
            'author': 'David Flanagan',
            'year': 2020,
            'pages': 706,
            'language': 'Ingliz',
            'description': 'JavaScript dasturlash tili bo\'yicha mukammal qo\'llanma.',
            'file_id': None,
            'is_featured': 1
        },

        # IQTISODIY ADABIYOTLAR (category_id = 2)
        {
            'category_id': 2,
            'title_uz': 'Iqtisodiyot nazariyasi',
            'title_ru': 'Теория экономики',
            'title_en': 'Principles of Economics',
            'author': 'N. Gregory Mankiw',
            'year': 2022,
            'pages': 896,
            'language': 'O\'zbek',
            'description': 'Iqtisodiyot asoslari va nazariyasi bo\'yicha fundamental qo\'llanma.',
            'file_id': None,
            'is_featured': 1
        },
        {
            'category_id': 2,
            'title_uz': 'Mikroiqtisodiyot',
            'title_ru': 'Микроэкономика',
            'title_en': 'Microeconomics',
            'author': 'Robert Pindyck',
            'year': 2021,
            'pages': 784,
            'language': 'O\'zbek',
            'description': 'Mikroiqtisodiyot nazariyasi va amaliyoti.',
            'file_id': None,
            'is_featured': 0
        },

        # HUQUQIY SOHA (category_id = 7)
        {
            'category_id': 7,
            'title_uz': 'O\'zbekiston Respublikasining Fuqarolik kodeksi',
            'title_ru': 'Гражданский кодекс Республики Узбекистан',
            'title_en': 'Civil Code of Uzbekistan',
            'author': 'O\'zbekiston Respublikasi',
            'year': 2023,
            'pages': 520,
            'language': 'O\'zbek',
            'description': 'O\'zbekiston Respublikasining Fuqarolik kodeksi - eng so\'nggi tahrir.',
            'file_id': None,
            'is_featured': 1
        },

        # TOP-ADABIYOTLAR (category_id = 1)
        {
            'category_id': 1,
            'title_uz': 'O\'tkan kunlar',
            'title_ru': 'Минувшие дни',
            'title_en': 'Bygone Days',
            'author': 'Abdulla Qodiriy',
            'year': 2020,
            'pages': 520,
            'language': 'O\'zbek',
            'description': 'O\'zbek adabiyotining eng yaxshi asarlaridan biri.',
            'file_id': None,
            'is_featured': 1
        },
        {
            'category_id': 1,
            'title_uz': 'Mehrobdan chayon',
            'title_ru': 'Скорпион из алтаря',
            'title_en': 'Scorpion from the Altar',
            'author': 'Abdulla Qodiriy',
            'year': 2020,
            'pages': 448,
            'language': 'O\'zbek',
            'description': 'Klassik o\'zbek romanlaridan.',
            'file_id': None,
            'is_featured': 1
        },

        # BADIY ADABIYOTLAR (category_id = 3)
        {
            'category_id': 3,
            'title_uz': 'Ikki eshik orasi',
            'title_ru': 'Между двух дверей',
            'title_en': 'Between Two Doors',
            'author': 'O\'tkir Hoshimov',
            'year': 2019,
            'pages': 380,
            'language': 'O\'zbek',
            'description': 'Zamonaviy o\'zbek adabiyotining eng yaxshi namunalaridan.',
            'file_id': None,
            'is_featured': 0
        },

        # TA'LIM ADABIYOTLARI (category_id = 5)
        {
            'category_id': 5,
            'title_uz': 'Pedagogika asoslari',
            'title_ru': 'Основы педагогики',
            'title_en': 'Fundamentals of Pedagogy',
            'author': 'I.P. Podlasiy',
            'year': 2022,
            'pages': 640,
            'language': 'O\'zbek',
            'description': 'Pedagogika nazariyasi va amaliyoti bo\'yicha asosiy qo\'llanma.',
            'file_id': None,
            'is_featured': 1
        },

        # XORIJIY TIL ADABIYOTLARI (category_id = 6)
        {
            'category_id': 6,
            'title_uz': 'English Grammar in Use',
            'title_ru': 'Английская грамматика в использовании',
            'title_en': 'English Grammar in Use',
            'author': 'Raymond Murphy',
            'year': 2019,
            'pages': 380,
            'language': 'Ingliz',
            'description': 'Ingliz tili grammatikasi bo\'yicha eng mashhur qo\'llanma.',
            'file_id': None,
            'is_featured': 1
        },

        # ILMIY ADABIYOTLAR (category_id = 8)
        {
            'category_id': 8,
            'title_uz': 'Fizika asoslari',
            'title_ru': 'Основы физики',
            'title_en': 'Fundamentals of Physics',
            'author': 'David Halliday',
            'year': 2021,
            'pages': 1328,
            'language': 'Ingliz',
            'description': 'Fizika bo\'yicha fundamental qo\'llanma.',
            'file_id': None,
            'is_featured': 0
        }
    ]

    print("📚 Demo kitoblar qo'shilmoqda...\n")

    try:
        for book in demo_books:
            # Check if book already exists (by title)
            c.execute("SELECT id FROM library_books WHERE title_uz=?", (book['title_uz'],))
            existing = c.fetchone()

            if existing:
                print(f"⚠️  '{book['title_uz']}' allaqachon mavjud, o'tkazib yuborildi")
                continue

            # Insert book
            c.execute('''
                INSERT INTO library_books
                (category_id, title_uz, title_ru, title_en, author, year, pages,
                 language, description, file_id, channel_message_id, download_count, is_featured, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                book['category_id'],
                book['title_uz'],
                book['title_ru'],
                book['title_en'],
                book['author'],
                book['year'],
                book['pages'],
                book['language'],
                book['description'],
                book['file_id'],
                None,  # channel_message_id
                0,     # download_count
                book['is_featured'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            print(f"✅ Qo'shildi: {book['title_uz']} - {book['author']}")

        conn.commit()
        print("\n✅ Barcha demo kitoblar muvaffaqiyatli qo'shildi!")

        # Show statistics
        c.execute("SELECT COUNT(*) FROM library_books")
        total_books = c.fetchone()[0]

        c.execute("""
            SELECT c.name_uz, COUNT(b.id) as book_count
            FROM library_categories c
            LEFT JOIN library_books b ON c.id = b.category_id
            GROUP BY c.id
            ORDER BY c.id
        """)

        print("\n📊 Kategoriyalar bo'yicha kitoblar soni:")
        for row in c.fetchall():
            print(f"   {row[0]}: {row[1]} kitob")

        print(f"\n📚 Jami: {total_books} kitob")

        print("\n⚠️  MUHIM:")
        print("   Haqiqiy PDF fayllarni yuklash uchun:")
        print("   1. Telegram kanallariga PDF fayllarni yuklang")
        print("   2. Bot orqali file_id'ni oling")
        print("   3. Database'da file_id ustunini yangilang")

    except Exception as e:
        print(f"❌ Xatolik: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    print("🚀 Demo kitoblarni qo'shish...\n")
    add_demo_books()
