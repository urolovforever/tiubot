import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN', '8349358796:AAGh9cZHo31Ao1XTsh4TSgWlZRrPAAbgmS0')
ADMIN_IDS = [1920079641, 5384126744]  # O'z telegram ID laringizni kiriting

# Admin group for applications
# Murojaatlar adminlar guruhiga yuboriladi
ADMIN_GROUP_ID = os.getenv('ADMIN_GROUP_ID', -5012065617)  # Adminlar guruhi ID sini kiriting

# Channel settings
DIGEST_CHANNEL_ID = os.getenv('DIGEST_CHANNEL_ID', '-1003285608799')  # Hafta dayjesti kanali ID

# Library channel settings
LIBRARY_CHANNELS = {
    1: {'username': '@tiu_library_top', 'id': None},  # TOP-ADABIYOTLAR
    2: {'username': '@tiu_library_economics', 'id': None},  # IQTISODIY ADABIYOTLAR
    3: {'username': '@tiu_library_fiction', 'id': None},  # BADIY ADABIYOTLAR
    4: {'username': '@tiu_library_it', 'id': None},  # IT SOHA
    5: {'username': '@tiu_library_education', 'id': None},  # TA'LIM ADABIYOTLARI
    6: {'username': '@tiu_library_languages', 'id': None},  # XORIJIY TIL ADABIYOTLARI
    7: {'username': '@tiu_library_law', 'id': None},  # HUQUQIY SOHA
    8: {'username': '@tiu_library_science', 'id': None},  # ILMIY ADABIYOTLAR
    9: {'username': '@tiu_library_other', 'id': None},  # BOSHQA TURDAGI
}

# Database settings
DATABASE_NAME = 'tiu_bot.db'

# Faculties - NEW STRUCTURE: Faculty → Course → Direction → Groups
FACULTIES = {
    'uz': {
        'Biznes va innovatsion ta\'lim': {
            '1-kurs': {
                'Psixologiya': ['PS-1-25'],
                'Moliya va moliyaviy texnologiyalar': ['ML-1-25'],
                'Dasturiy injiniring': ['DI-1-25'],
                'Iqtisodiyot': ['EK-1-25', 'EK-2-25', 'EK-3-25', 'EK-4-25', 'EK-1-25r', 'EK-2-25r', 'EK-3-25r'],
                'Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar (mintaqalar va faoliyat turlari bo\'yicha)': ['XIM-1-25', 'XIM-2-25', 'XIM-3-25', 'XIM-4-25', 'XIM-1-25r', 'XIM-2-25r', 'XIM-3-25r'],
                'Bank ishi': ['BK-1-25'],
                'Menejment': ['MN-1-25', 'MN-2-25'],
                'Buxgalteriya hisobi': ['BH-1-25'],
                'Boshlang\'ich ta\'lim': ['BT-1-25'],
                'Xorijiy til va adabiyoti (ingliz tili)': ['XT-1-25', 'XT-2-25', 'XT-1-25r'],
                'Filologiya va tillarni o\'qitish (korayes tili)': ['KR-1-25'],
                'Kiberxavfsizlik injiniringi': ['CS-1-25', 'CS-2-25', 'CS-3-25', 'CS-1-25r', 'CS-2-25r']
            },
            '2-kurs': {
                'Xorijiy til va adabiyoti (ingliz tili)': ['XT-1-24', 'XT-2-24', 'XT-3-24', 'XT-1-24r'],
                'Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo\'yicha)': ['AT-1-24'],
                'Iqtisodiyot': ['EK-1-24', 'EK-2-24', 'MEK-1-24', 'EK-1-24r', 'EK-2-24r'],
                'Bank ishi': ['BK-1-24'],
                'Kiberxavfsizlik injiniringi': ['CS-1-24', 'CS-1-24r'],
                'Dasturiy injiniring': ['DI-1-24'],
                'Filologiya va tillarni o\'qitish (korayes tili)': ['KR-1-24'],
                'Boshlang\'ich ta\'lim': ['BT-1-24'],
                'Psixologiya': ['PS-1-24'],
                'Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar (mintaqalar va faoliyat turlari bo\'yicha)': ['XIM-1-24', 'XIM-2-24', 'XIM-1-24r', 'XIM-2-24r'],
                'Menejment': ['MN-1-24']
            },
            '3-kurs': {
                'Xorijiy til va adabiyoti (ingliz tili)': ['XT-1-23'],
                'Iqtisodiyot': ['EK-1-23'],
                'Kiberxavfsizlik injiniringi': ['CS-1-23']
            }
        },
        'Yurisprudensiya': {
            '1-kurs': [
                'HQ-1-25', 'HQ-2-25', 'HQ-3-25', 'HQ-4-25', 'HQ-5-25', 'HQ-6-25',
                'HQ-7-25', 'HQ-8-25', 'HQ-9-25', 'HQ-10-25', 'HQ-11-25', 'HQ-12-25',
                'HQ-13-25', 'HQ-14-25', 'HQ-15-25', 'HQ-16-25', 'HQ-17-25', 'HQ-18-25',
                'HQ-19-25', 'HQ-20-25', 'HQ-21-25', 'HQ-22-25', 'HQ-23-25', 'HQ-24-25',
                'HQ-25-25', 'HQ-26-25', 'HQ-27-25', 'HQ-28-25', 'HQ-29-25', 'HQ-30-25',
                'HQ-1-25r', 'HQ-2-25r', 'HQ-3-25r', 'HQ-4-25r', 'HQ-5-25r', 'HQ-6-25r',
                'HQ-7-25r', 'HQ-8-25r', 'HQ-9-25r'
            ],
            '2-kurs': [
                'HQ-1-24', 'HQ-2-24', 'HQ-3-24', 'HQ-4-24', 'HQ-5-24', 'HQ-6-24',
                'HQ-7-24', 'HQ-8-24', 'HQ-9-24', 'HQ-10-24', 'HQ-11-24', 'HQ-12-24',
                'HQ-13-24', 'HQ-14-24', 'HQ-15-24', 'HQ-16-24', 'HQ-17-24', 'HQ-18-24',
                'HQ-19-24', 'HQ-20-24', 'HQ-21-24', 'HQ-22-24',
                'HQ-1-24r', 'HQ-2-24r', 'HQ-3-24r', 'HQ-4-24r', 'HQ-5-24r', 'HQ-6-24r'
            ],
            '3-kurs': [
                'HQ-1-23', 'HQ-2-23', 'HQ-3-23', 'HQ-4-23', 'HQ-5-23', 'HQ-6-23'
            ]
        }
    },

    'ru': {
        'Бизнес и инновационное образование': {
            '1-курс': {
                'Психология': ['PS-1-25'],
                'Финансы и финансовые технологии': ['ML-1-25'],
                'Программный инжиниринг': ['DI-1-25'],
                'Экономика': ['EK-1-25', 'EK-2-25', 'EK-3-25', 'EK-4-25', 'EK-1-25r', 'EK-2-25r', 'EK-3-25r'],
                'Мировая экономика и международные экономические отношения (по регионам и видам деятельности)': ['XIM-1-25', 'XIM-2-25', 'XIM-3-25', 'XIM-4-25', 'XIM-1-25r', 'XIM-2-25r', 'XIM-3-25r'],
                'Банковское дело': ['BK-1-25'],
                'Менеджмент': ['MN-1-25', 'MN-2-25'],
                'Бухгалтерский учет': ['BH-1-25'],
                'Начальное образование': ['BT-1-25'],
                'Иностранный язык и литература (английский язык)': ['XT-1-25', 'XT-2-25', 'XT-1-25r'],
                'Филология и обучение языкам (корейский язык)': ['KR-1-25'],
                'Инжиниринг кибербезопасности': ['CS-1-25', 'CS-2-25', 'CS-3-25', 'CS-1-25r', 'CS-2-25r']
            },
            '2-курс': {
                'Иностранный язык и литература (английский язык)': ['XT-1-24', 'XT-2-24', 'XT-3-24', 'XT-1-24r'],
                'Информационные системы и технологии (по отраслям и областям)': ['AT-1-24'],
                'Экономика': ['EK-1-24', 'EK-2-24', 'MEK-1-24', 'EK-1-24r', 'EK-2-24r'],
                'Банковское дело': ['BK-1-24'],
                'Инжиниринг кибербезопасности': ['CS-1-24', 'CS-1-24r'],
                'Программный инжиниринг': ['DI-1-24'],
                'Филология и обучение языкам (корейский язык)': ['KR-1-24'],
                'Начальное образование': ['BT-1-24'],
                'Психология': ['PS-1-24'],
                'Мировая экономика и международные экономические отношения (по регионам и видам деятельности)': ['XIM-1-24', 'XIM-2-24', 'XIM-1-24r', 'XIM-2-24r'],
                'Менеджмент': ['MN-1-24']
            },
            '3-курс': {
                'Иностранный язык и литература (английский язык)': ['XT-1-23'],
                'Экономика': ['EK-1-23'],
                'Инжиниринг кибербезопасности': ['CS-1-23']
            }
        },
        'Юриспруденция': {
            '1-курс': [
                'HQ-1-25', 'HQ-2-25', 'HQ-3-25', 'HQ-4-25', 'HQ-5-25', 'HQ-6-25',
                'HQ-7-25', 'HQ-8-25', 'HQ-9-25', 'HQ-10-25', 'HQ-11-25', 'HQ-12-25',
                'HQ-13-25', 'HQ-14-25', 'HQ-15-25', 'HQ-16-25', 'HQ-17-25', 'HQ-18-25',
                'HQ-19-25', 'HQ-20-25', 'HQ-21-25', 'HQ-22-25', 'HQ-23-25', 'HQ-24-25',
                'HQ-25-25', 'HQ-26-25', 'HQ-27-25', 'HQ-28-25', 'HQ-29-25', 'HQ-30-25',
                'HQ-1-25r', 'HQ-2-25r', 'HQ-3-25r', 'HQ-4-25r', 'HQ-5-25r', 'HQ-6-25r',
                'HQ-7-25r', 'HQ-8-25r', 'HQ-9-25r'
            ],
            '2-курс': [
                'HQ-1-24', 'HQ-2-24', 'HQ-3-24', 'HQ-4-24', 'HQ-5-24', 'HQ-6-24',
                'HQ-7-24', 'HQ-8-24', 'HQ-9-24', 'HQ-10-24', 'HQ-11-24', 'HQ-12-24',
                'HQ-13-24', 'HQ-14-24', 'HQ-15-24', 'HQ-16-24', 'HQ-17-24', 'HQ-18-24',
                'HQ-19-24', 'HQ-20-24', 'HQ-21-24', 'HQ-22-24',
                'HQ-1-24r', 'HQ-2-24r', 'HQ-3-24r', 'HQ-4-24r', 'HQ-5-24r', 'HQ-6-24r'
            ],
            '3-курс': [
                'HQ-1-23', 'HQ-2-23', 'HQ-3-23', 'HQ-4-23', 'HQ-5-23', 'HQ-6-23'
            ]
        }
    },

    'en': {
        'Business and Innovative Education': {
            '1st year': {
                'Psychology': ['PS-1-25'],
                'Finance and Financial Technologies': ['ML-1-25'],
                'Software Engineering': ['DI-1-25'],
                'Economics': ['EK-1-25', 'EK-2-25', 'EK-3-25', 'EK-4-25', 'EK-1-25r', 'EK-2-25r', 'EK-3-25r'],
                'World Economy and International Economic Relations (by regions and types of activities)': ['XIM-1-25', 'XIM-2-25', 'XIM-3-25', 'XIM-4-25', 'XIM-1-25r', 'XIM-2-25r', 'XIM-3-25r'],
                'Banking': ['BK-1-25'],
                'Management': ['MN-1-25', 'MN-2-25'],
                'Accounting': ['BH-1-25'],
                'Primary Education': ['BT-1-25'],
                'Foreign Language and Literature (English)': ['XT-1-25', 'XT-2-25', 'XT-1-25r'],
                'Philology and Language Teaching (Korean)': ['KR-1-25'],
                'Cybersecurity Engineering': ['CS-1-25', 'CS-2-25', 'CS-3-25', 'CS-1-25r', 'CS-2-25r']
            },
            '2nd year': {
                'Foreign Language and Literature (English)': ['XT-1-24', 'XT-2-24', 'XT-3-24', 'XT-1-24r'],
                'Information Systems and Technologies (by networks and fields)': ['AT-1-24'],
                'Economics': ['EK-1-24', 'EK-2-24', 'MEK-1-24', 'EK-1-24r', 'EK-2-24r'],
                'Banking': ['BK-1-24'],
                'Cybersecurity Engineering': ['CS-1-24', 'CS-1-24r'],
                'Software Engineering': ['DI-1-24'],
                'Philology and Language Teaching (Korean)': ['KR-1-24'],
                'Primary Education': ['BT-1-24'],
                'Psychology': ['PS-1-24'],
                'World Economy and International Economic Relations (by regions and types of activities)': ['XIM-1-24', 'XIM-2-24', 'XIM-1-24r', 'XIM-2-24r'],
                'Management': ['MN-1-24']
            },
            '3rd year': {
                'Foreign Language and Literature (English)': ['XT-1-23'],
                'Economics': ['EK-1-23'],
                'Cybersecurity Engineering': ['CS-1-23']
            }
        },
        'Law': {
            '1st year': [
                'HQ-1-25', 'HQ-2-25', 'HQ-3-25', 'HQ-4-25', 'HQ-5-25', 'HQ-6-25',
                'HQ-7-25', 'HQ-8-25', 'HQ-9-25', 'HQ-10-25', 'HQ-11-25', 'HQ-12-25',
                'HQ-13-25', 'HQ-14-25', 'HQ-15-25', 'HQ-16-25', 'HQ-17-25', 'HQ-18-25',
                'HQ-19-25', 'HQ-20-25', 'HQ-21-25', 'HQ-22-25', 'HQ-23-25', 'HQ-24-25',
                'HQ-25-25', 'HQ-26-25', 'HQ-27-25', 'HQ-28-25', 'HQ-29-25', 'HQ-30-25',
                'HQ-1-25r', 'HQ-2-25r', 'HQ-3-25r', 'HQ-4-25r', 'HQ-5-25r', 'HQ-6-25r',
                'HQ-7-25r', 'HQ-8-25r', 'HQ-9-25r'
            ],
            '2nd year': [
                'HQ-1-24', 'HQ-2-24', 'HQ-3-24', 'HQ-4-24', 'HQ-5-24', 'HQ-6-24',
                'HQ-7-24', 'HQ-8-24', 'HQ-9-24', 'HQ-10-24', 'HQ-11-24', 'HQ-12-24',
                'HQ-13-24', 'HQ-14-24', 'HQ-15-24', 'HQ-16-24', 'HQ-17-24', 'HQ-18-24',
                'HQ-19-24', 'HQ-20-24', 'HQ-21-24', 'HQ-22-24',
                'HQ-1-24r', 'HQ-2-24r', 'HQ-3-24r', 'HQ-4-24r', 'HQ-5-24r', 'HQ-6-24r'
            ],
            '3rd year': [
                'HQ-1-23', 'HQ-2-23', 'HQ-3-23', 'HQ-4-23', 'HQ-5-23', 'HQ-6-23'
            ]
        }
    }
}
