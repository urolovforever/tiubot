"""
Initialize library categories
Run this script once to create the 9 library categories in the database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.db import Database
from datetime import datetime

DATABASE_NAME = 'tiu_bot.db'

# Library categories data
CATEGORIES = [
    {
        'id': 1,
        'name_uz': 'TOP-ADABIYOTLAR',
        'name_ru': 'ТОП ЛИТЕРАТУРА',
        'name_en': 'TOP LITERATURE',
        'emoji': '📕',
        'channel_username': '@tiu_library_top',
        'channel_id': None  # Will be set when bot joins the channel
    },
    {
        'id': 2,
        'name_uz': 'IQTISODIY ADABIYOTLAR',
        'name_ru': 'ЭКОНОМИЧЕСКАЯ ЛИТЕРАТУРА',
        'name_en': 'ECONOMIC LITERATURE',
        'emoji': '📊',
        'channel_username': '@tiu_library_economics',
        'channel_id': None
    },
    {
        'id': 3,
        'name_uz': 'BADIY ADABIYOTLAR',
        'name_ru': 'ХУДОЖЕСТВЕННАЯ ЛИТЕРАТУРА',
        'name_en': 'FICTION',
        'emoji': '🎨',
        'channel_username': '@tiu_library_fiction',
        'channel_id': None
    },
    {
        'id': 4,
        'name_uz': 'IT SOHA',
        'name_ru': 'IT СФЕРА',
        'name_en': 'IT FIELD',
        'emoji': '💻',
        'channel_username': '@tiu_library_it',
        'channel_id': None
    },
    {
        'id': 5,
        'name_uz': 'TA\'LIM ADABIYOTLARI',
        'name_ru': 'ПЕДАГОГИЧЕСКАЯ ЛИТЕРАТУРА',
        'name_en': 'EDUCATIONAL LITERATURE',
        'emoji': '📚',
        'channel_username': '@tiu_library_education',
        'channel_id': None
    },
    {
        'id': 6,
        'name_uz': 'XORIJIY TIL ADABIYOTLARI',
        'name_ru': 'ИНОСТРАННЫЕ ЯЗЫКИ',
        'name_en': 'FOREIGN LANGUAGE LITERATURE',
        'emoji': '🌍',
        'channel_username': '@tiu_library_languages',
        'channel_id': None
    },
    {
        'id': 7,
        'name_uz': 'HUQUQIY SOHA',
        'name_ru': 'ЮРИДИЧЕСКАЯ СФЕРА',
        'name_en': 'LAW FIELD',
        'emoji': '⚖️',
        'channel_username': '@tiu_library_law',
        'channel_id': None
    },
    {
        'id': 8,
        'name_uz': 'ILMIY ADABIYOTLAR',
        'name_ru': 'НАУЧНАЯ ЛИТЕРАТУРА',
        'name_en': 'SCIENTIFIC LITERATURE',
        'emoji': '🔬',
        'channel_username': '@tiu_library_science',
        'channel_id': None
    },
    {
        'id': 9,
        'name_uz': 'BOSHQA TURDAGI',
        'name_ru': 'ДРУГОЕ',
        'name_en': 'OTHER',
        'emoji': '📖',
        'channel_username': '@tiu_library_other',
        'channel_id': None
    }
]


def init_categories():
    """Initialize library categories in database"""

    # First, ensure database and all tables exist
    print("📦 Initializing database tables...")
    db = Database(DATABASE_NAME)
    print("✅ Database tables created successfully!\n")

    # Now add categories
    conn = db.get_connection()
    c = conn.cursor()

    try:
        for category in CATEGORIES:
            # Check if category already exists
            c.execute("SELECT id FROM library_categories WHERE id=?", (category['id'],))
            existing = c.fetchone()

            if existing:
                print(f"⚠️  Category {category['id']}: {category['name_uz']} already exists, skipping...")
                continue

            # Insert category
            c.execute('''
                INSERT INTO library_categories
                (id, name_uz, name_ru, name_en, emoji, channel_id, channel_username, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                category['id'],
                category['name_uz'],
                category['name_ru'],
                category['name_en'],
                category['emoji'],
                category['channel_id'],
                category['channel_username'],
                1,  # is_active
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            print(f"✅ Added category {category['id']}: {category['name_uz']}")

        conn.commit()
        print("\n✅ All library categories initialized successfully!")
        print("\n📌 Next steps:")
        print("1. Create 9 private Telegram channels with the usernames listed above")
        print("2. Add the bot as admin to each channel")
        print("3. Give the bot these permissions: Post messages, Delete messages, Read message history")
        print("4. Upload books to the channels as PDF files with captions")
        print("5. Use the admin panel to add books to the database")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    print("🚀 Initializing library categories...")
    init_categories()
