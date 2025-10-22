from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.helpers import t, is_admin


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
        KeyboardButton(t(user_id, 'news')),
        KeyboardButton(t(user_id, 'contact'))
    )
    keyboard.insert(KeyboardButton(t(user_id, 'settings')))

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

    db = Database()
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


def get_admin_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'view_applications')))
    keyboard.add(KeyboardButton(t(user_id, 'add_event')))
    keyboard.add(KeyboardButton(t(user_id, 'manage_events')))
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_events_keyboard(user_id: int, events: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for event in events:
        # event[0] = id, event[1] = title
        title = event[1][:30] + '...' if len(event[1]) > 30 else event[1]
        keyboard.add(KeyboardButton(f"{event[0]}. {title}"))
    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard
