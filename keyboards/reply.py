from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.db import Database
from utils.helpers import t, is_admin

db = Database()

def get_main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    keyboard.add(
        KeyboardButton(t(user_id, 'about_tiu')),
        KeyboardButton(t(user_id, 'admission'))
    )
    keyboard.add(
        KeyboardButton(t(user_id, 'students')),
        KeyboardButton(t(user_id, 'applications'))
    )
    keyboard.add(
        KeyboardButton(t(user_id, 'events')),  # Tadbirlar taqvimi
        KeyboardButton(t(user_id, 'news'))
    )
    keyboard.add(
        KeyboardButton(t(user_id, 'contact')),
        KeyboardButton(t(user_id, 'settings'))
    )

    # Admin panel button
    if is_admin(user_id):
        keyboard.insert(KeyboardButton(t(user_id, 'admin_panel')))

    return keyboard


def get_back_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_cancel_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_settings_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'change_language')))
    keyboard.insert(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_language_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(
        KeyboardButton('🇺🇿 O\'zbek'),
        KeyboardButton('🇷🇺 Русский'),
        KeyboardButton('🇬🇧 English')
    )
    return keyboard


def get_phone_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'phone_button'), request_contact=True))
    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_faculty_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    from config import FACULTIES
    from database.db import Database

    db = Database()
    lang = db.get_user_language(user_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for faculty in FACULTIES.get(lang, FACULTIES['uz']):
        keyboard.insert(KeyboardButton(faculty))
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_course_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    from config import COURSES
    from database.db import Database
    from utils.helpers import t

    lang = db.get_user_language(user_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for course in COURSES.get(lang, COURSES['uz']):
        keyboard.insert(KeyboardButton(course))
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_group_keyboard(user_id: int, groups: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for group in groups:
        keyboard.insert(KeyboardButton(group))
    keyboard.insert(KeyboardButton(t(user_id, 'back')))
    return keyboard

def get_events_keyboard(user_id: int, events: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for event in events:
        # event[0] = id, event[1] = title
        title = event[1][:30] + '...' if len(event[1]) > 30 else event[1]
        keyboard.add(KeyboardButton(f"{event[0]}. {title}"))
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_skip_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Skip va bekor qilish tugmalari"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    skip_texts = {
        'uz': '⏭ O\'tkazib yuborish',
        'ru': '⏭ Пропустить',
        'en': '⏭ Skip'
    }

    keyboard.add(
        KeyboardButton(skip_texts.get(lang, skip_texts['uz'])),
        KeyboardButton(t(user_id, 'cancel'))
    )
    return keyboard


def get_admin_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Admin klaviatura - yangilangan"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '📬 Yangi murojaatlar',
            '✅ Javob berilganlar',
            '📊 Statistika',
            '📢 Broadcast',
            '➕ Tadbir qo\'shish',
            '📝 Tadbirlarni boshqarish'
        ],
        'ru': [
            '📬 Новые обращения',
            '✅ Отвеченные',
            '📊 Статистика',
            '📢 Рассылка',
            '➕ Добавить мероприятие',
            '📝 Управление мероприятиями'
        ],
        'en': [
            '📬 New Applications',
            '✅ Answered',
            '📊 Statistics',
            '📢 Broadcast',
            '➕ Add Event',
            '📝 Manage Events'
        ]
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.add(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard

def get_broadcast_confirm_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Broadcast tasdiqlash klaviaturasi"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    confirm_texts = {
        'uz': '✅ Ha, yuborish',
        'ru': '✅ Да, отправить',
        'en': '✅ Yes, send'
    }

    keyboard.add(
        KeyboardButton(confirm_texts.get(lang, confirm_texts['uz'])),
        KeyboardButton(t(user_id, 'cancel'))
    )
    return keyboard


def get_statistics_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Statistika klaviaturasi"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['📅 Haftalik', '📆 Oylik'],
        'ru': ['📅 Недельная', '📆 Месячная'],
        'en': ['📅 Weekly', '📆 Monthly']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.add(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard
