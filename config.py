import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN', '8349358796:AAGh9cZHo31Ao1XTsh4TSgWlZRrPAAbgmS0')
ADMIN_IDS = [1920079641]  # O'z telegram ID laringizni kiriting

# Channel settings
DIGEST_CHANNEL_ID = os.getenv('DIGEST_CHANNEL_ID', '-1002319736714')  # Hafta dayjesti kanali ID

# Database settings
DATABASE_NAME = 'tiu_bot.db'

# Contact info
PHONE_NUMBER = '+998 71 200 09 09'
EMAIL = 'info@tiu.uz'
ADMISSION_EMAIL = 'admission@tiu.uz'

# Faculties
FACULTIES = {
    'uz': {
        'Yurisprudensiya': {
            'Yurisprudensiya': {
                '1-kurs': ['xq-1-1', 'xq-1-2'],
                '2-kurs': ['xq-2-1', 'xq-2-2']
            }
        },
        'Biznes va innovatsion ta\'lim': {
            'Bank ishi': {
                '1-kurs': ['b-1-1'],
                '2-kurs': []
            },
            'Buxgalteriya hisobi': {
                '1-kurs': ['bh-1-5'],
                '2-kurs': []
            },
            'Iqtisodiyot': {
                '1-kurs': ['i-1-9'],
                '2-kurs': []
            },
            'Marketing': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Menejment': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Moliya va moliyaviy texnologiyalar': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Axborot tizimlari va texnologiyalari': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Kiberxavfsizlik injiniringi': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Kompyuter injiniringi': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Dasturiy injiniring': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Maktabgacha ta\'lim': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Boshlang\'ich ta\'lim': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Psixologiya': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Xorijiy tili va adabiyoti: ingliz tili': {
                '1-kurs': [],
                '2-kurs': []
            },
            'Filologiya va tillarni o\'qitish (koreys tili)': {
                '1-kurs': [],
                '2-kurs': []
            }
        }
    },

    'ru': {
        'Юриспруденция': {
            'Юриспруденция': {
                '1-курс': ['xq-1-1', 'xq-1-2'],
                '2-курс': ['xq-2-1', 'xq-2-2']
            }
        },
        'Бизнес и инновационное образование': {
            'Банковское дело': {
                '1-курс': ['b-1-1'],
                '2-курс': []
            },
            'Бухгалтерский учет': {
                '1-курс': ['bh-1-5'],
                '2-курс': []
            },
            'Экономика': {
                '1-курс': ['i-1-9'],
                '2-курс': []
            },
            'Маркетинг': {
                '1-курс': [],
                '2-курс': []
            },
            'Менеджмент': {
                '1-курс': [],
                '2-курс': []
            },
            'Финансы и финансовые технологии': {
                '1-курс': [],
                '2-курс': []
            },
            'Мировая экономика и международные экономические отношения': {
                '1-курс': [],
                '2-курс': []
            },
            'Информационные системы и технологии': {
                '1-курс': [],
                '2-курс': []
            },
            'Инжиниринг кибербезопасности': {
                '1-курс': [],
                '2-курс': []
            },
            'Компьютерный инжиниринг': {
                '1-курс': [],
                '2-курс': []
            },
            'Программный инжиниринг': {
                '1-курс': [],
                '2-курс': []
            },
            'Дошкольное образование': {
                '1-курс': [],
                '2-курс': []
            },
            'Начальное образование': {
                '1-курс': [],
                '2-курс': []
            },
            'Психология': {
                '1-курс': [],
                '2-курс': []
            },
            'Иностранный язык и литература: английский язык': {
                '1-курс': [],
                '2-курс': []
            },
            'Филология и обучение языкам (корейский язык)': {
                '1-курс': [],
                '2-курс': []
            }
        }
    },

    'en': {
        'Law': {
            'Law': {
                '1st year': ['xq-1-1', 'xq-1-2'],
                '2nd year': ['xq-2-1', 'xq-2-2']
            }
        },
        'Business and Innovative Education': {
            'Banking': {
                '1st year': ['b-1-1'],
                '2nd year': []
            },
            'Accounting': {
                '1st year': ['bh-1-5'],
                '2nd year': []
            },
            'Economics': {
                '1st year': ['i-1-9'],
                '2nd year': []
            },
            'Marketing': {
                '1st year': [],
                '2nd year': []
            },
            'Management': {
                '1st year': [],
                '2nd year': []
            },
            'Finance and Financial Technologies': {
                '1st year': [],
                '2nd year': []
            },
            'World Economy and International Economic Relations': {
                '1st year': [],
                '2nd year': []
            },
            'Information Systems and Technologies': {
                '1st year': [],
                '2nd year': []
            },
            'Cybersecurity Engineering': {
                '1st year': [],
                '2nd year': []
            },
            'Computer Engineering': {
                '1st year': [],
                '2nd year': []
            },
            'Software Engineering': {
                '1st year': [],
                '2nd year': []
            },
            'Preschool Education': {
                '1st year': [],
                '2nd year': []
            },
            'Primary Education': {
                '1st year': [],
                '2nd year': []
            },
            'Psychology': {
                '1st year': [],
                '2nd year': []
            },
            'Foreign Language and Literature: English': {
                '1st year': [],
                '2nd year': []
            },
            'Philology and Language Teaching (Korean)': {
                '1st year': [],
                '2nd year': []
            }
        }
    }
}
