import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN', '7910568707:AAE4ARRRTumtc2XxqcH6JsY-tGsbxIvuLr4')
ADMIN_IDS = [1220079641]  # O'z telegram ID laringizni kiriting

# Database settings
DATABASE_NAME = 'tiu_bot.db'

# Contact info
PHONE_NUMBER = '+998 71 200 09 09'
EMAIL = 'info@tiu.uz'
ADMISSION_EMAIL = 'admission@tiu.uz'

# Faculties
FACULTIES = {
    'uz': {
        'Xalqaro munosabatlar': {
            'Yurisprudensiya': {
                '1-kurs': ['YU-101', 'YU-102'],
                '2-kurs': ['YU-201', 'YU-202'],
                '3-kurs': ['YU-301'],
                '4-kurs': ['YU-401']
            },
            'Iqtisodiyot': {
                '1-kurs': ['IQ-101', 'IQ-102'],
                '2-kurs': ['IQ-201', 'IQ-202'],
                '3-kurs': ['IQ-301'],
                '4-kurs': ['IQ-401']
            },
            'Siyosatshunoslik': {
                '1-kurs': ['SI-101'],
                '2-kurs': ['SI-201'],
                '3-kurs': ['SI-301'],
                '4-kurs': ['SI-401']
            },
            'Xalqaro huquq': {
                '1-kurs': ['XH-101'],
                '2-kurs': ['XH-201'],
                '3-kurs': ['XH-301'],
                '4-kurs': ['XH-401']
            },
            # Shu tarzda 18 ta yo‘nalishni shu fakultetga qo‘shish mumkin
        },
        'Axborot texnologiyalari': {
            'Kiberxavfsizlik': {
                '1-kurs': ['KB-101', 'KB-102'],
                '2-kurs': ['KB-201', 'KB-202'],
                '3-kurs': ['KB-301'],
                '4-kurs': ['KB-401']
            },
            'Dasturiy injiniring': {
                '1-kurs': ['DI-101', 'DI-102'],
                '2-kurs': ['DI-201', 'DI-202'],
                '3-kurs': ['DI-301'],
                '4-kurs': ['DI-401']
            },
            'Kompyuter injiniring': {
                '1-kurs': ['KI-101'],
                '2-kurs': ['KI-201'],
                '3-kurs': ['KI-301'],
                '4-kurs': ['KI-401']
            },
            'Sun’iy intellekt': {
                '1-kurs': ['AI-101'],
                '2-kurs': ['AI-201'],
                '3-kurs': ['AI-301'],
                '4-kurs': ['AI-401']
            },
            # Bu yerda ham 18 tagacha yo‘nalish qo‘shish mumkin
        }
    },

    'ru': {
        'Международные отношения': {
            'Юриспруденция': {
                '1-курс': ['Ю-101', 'Ю-102'],
                '2-курс': ['Ю-201', 'Ю-202'],
                '3-курс': ['Ю-301'],
                '4-курс': ['Ю-401']
            },
            'Экономика': {
                '1-курс': ['ЭК-101', 'ЭК-102'],
                '2-курс': ['ЭК-201', 'ЭК-202'],
                '3-курс': ['ЭК-301'],
                '4-курс': ['ЭК-401']
            },
            # ...
        },
        'Информационные технологии': {
            'Кибербезопасность': {
                '1-курс': ['КБ-101', 'КБ-102'],
                '2-курс': ['КБ-201', 'КБ-202'],
                '3-курс': ['КБ-301'],
                '4-курс': ['КБ-401']
            },
            # ...
        }
    },

    'en': {
        'International Relations': {
            'Law': {
                '1st year': ['LAW-101', 'LAW-102'],
                '2nd year': ['LAW-201', 'LAW-202'],
                '3rd year': ['LAW-301'],
                '4th year': ['LAW-401']
            },
            'Economics': {
                '1st year': ['ECO-101', 'ECO-102'],
                '2nd year': ['ECO-201', 'ECO-202'],
                '3rd year': ['ECO-301'],
                '4th year': ['ECO-401']
            },
            # ...
        },
        'Information Technology': {
            'Cybersecurity': {
                '1st year': ['CS-101', 'CS-102'],
                '2nd year': ['CS-201', 'CS-202'],
                '3rd year': ['CS-301'],
                '4th year': ['CS-401']
            },
            # ...
        }
    }
}
