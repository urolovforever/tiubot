from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
from database.db import Database
from states.forms import ScheduleStates
from utils.helpers import t

db = Database()


def get_students_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '📅 Dars jadvali',
            '📚 Kutubxona / resurslar',
            '🎉 Talabalar hayoti / klublar'
        ],
        'ru': [
            '📅 Расписание занятий',
            '📚 Библиотека / ресурсы',
            '🎉 Студенческая жизнь / клубы'
        ],
        'en': [
            '📅 Class schedule',
            '📚 Library / resources',
            '🎉 Student life / clubs'
        ]
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.insert(KeyboardButton(t(user_id, 'back')))
    return keyboard


async def students_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '🎓 Talabalar uchun\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '🎓 Для студентов\n\nВыберите один из разделов:',
        'en': '🎓 For Students\n\nChoose one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_students_submenu_keyboard(user_id)
    )

async def schedule_start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        t(user_id, 'choose_faculty'),
        reply_markup=get_faculty_keyboard(user_id)
    )
    await ScheduleStates.waiting_for_faculty.set()


async def process_faculty(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await state.finish()
        await message.answer(
            t(user_id, 'main_menu'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    faculty = message.text
    await state.update_data(faculty=faculty)

    await message.answer(
        t(user_id, 'choose_course'),
        reply_markup=get_course_keyboard(user_id)
    )
    await ScheduleStates.waiting_for_course.set()


async def process_course(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_faculty'),
            reply_markup=get_faculty_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_faculty.set()
        return

    course = message.text
    data = await state.get_data()
    faculty = data.get('faculty')

    await state.update_data(course=course)

    groups = db.get_groups_by_faculty_course(faculty, course)

    if not groups:
        groups = [f'{course[0]}01-20', f'{course[0]}02-20', f'{course[0]}03-20', f'{course[0]}04-20']

    await message.answer(
        t(user_id, 'choose_group'),
        reply_markup=get_group_keyboard(user_id, groups)
    )
    await ScheduleStates.waiting_for_group.set()


async def process_group(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_course'),
            reply_markup=get_course_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_course.set()
        return

    group = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    course = data.get('course')

    schedule_image = db.get_schedule(faculty, course, group)

    if schedule_image:
        await message.answer_photo(
            schedule_image,
            caption=t(user_id, 'schedule_success')
        )
    else:
        await message.answer(t(user_id, 'schedule_not_found'))

    await state.finish()
    await message.answer(
        t(user_id, 'main_menu'),
        reply_markup=get_main_keyboard(user_id)
    )


async def library_resources_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''📚 Kutubxona

📖 50,000+ kitob
💻 100,000+ elektron kitob
🌐 Xalqaro bazalar

🌐 library.tiu.uz

Ish vaqti:
🕐 Dush-Juma: 8:00-20:00''',

        'ru': '''📚 Библиотека

📖 50,000+ книг
💻 100,000+ электронных книг
🌐 Международные базы

🌐 library.tiu.uz

Время работы:
🕐 Пн-Пт: 8:00-20:00''',

        'en': '''📚 Library

📖 50,000+ books
💻 100,000+ e-books
🌐 International databases

🌐 library.tiu.uz

Working hours:
🕐 Mon-Fri: 8:00-20:00'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_students_submenu_keyboard(user_id)
    )


async def student_life_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🎉 Talabalar hayoti

🎭 San'at klubi
⚽️ Sport
🎤 Debat
💼 Tadbirkorlik
🤝 Volontyorlik
🎮 E-sport

📱 @tiu_students''',

        'ru': '''🎉 Студенческая жизнь

🎭 Клуб искусства
⚽️ Спорт
🎤 Дебаты
💼 Предпринимательство
🤝 Волонтерство
🎮 E-sport

📱 @tiu_students''',

        'en': '''🎉 Student Life

🎭 Arts Club
⚽️ Sports
🎤 Debate
💼 Entrepreneurship
🤝 Volunteering
🎮 E-sport

📱 @tiu_students'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_students_submenu_keyboard(user_id)
    )


def register_students_handlers(dp: Dispatcher):
    dp.register_message_handler(
        students_handler,
        lambda message: message.text in ['🎓 Talabalar uchun', '🎓 Для студентов', '🎓 For Students']
    )

    dp.register_message_handler(
        schedule_start_handler,
        lambda message: message.text in ['📅 Dars jadvali', '📅 Расписание занятий', '📅 Class schedule'],
        state='*'
    )
    dp.register_message_handler(process_faculty, state=ScheduleStates.waiting_for_faculty)
    dp.register_message_handler(process_course, state=ScheduleStates.waiting_for_course)
    dp.register_message_handler(process_group, state=ScheduleStates.waiting_for_group)

    dp.register_message_handler(
        library_resources_info,
        lambda message: message.text in [
            '📚 Kutubxona / resurslar',
            '📚 Библиотека / ресурсы',
            '📚 Library / resources'
        ]
    )

    def register_student_life_handlers(dp: Dispatcher):
        dp.register_message_handler(
            student_life_info,
            lambda message: message.text in [
                '🎉 Talabalar hayoti / klublar',
                '🎉 Студенческая жизнь / клубы',
                '🎉 Student life / clubs'
            ]
        )