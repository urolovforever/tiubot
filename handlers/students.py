from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
from database.db import Database
from states.forms import ScheduleStates
from utils.helpers import t
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, InputMediaPhoto
import os
from pathlib import Path

db = Database()

# Loyiha ildiz papkasini aniqlash
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "photos"


def get_media_path(filename: str) -> str:
    """Media fayl yo'lini qaytaradi va mavjudligini tekshiradi"""
    path = MEDIA_DIR / filename
    return str(path) if path.exists() else None


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


# ===============================
# TALABALAR HAYOTI BO'LIMI
# ===============================

async def student_life_info(message: types.Message):
    """Talabalar hayoti asosiy menusi"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🎉 <b>Talabalar hayoti</b>

Quyidagi bo'limlardan birini tanlang ↓''',
        'ru': '''🎉 <b>Студенческая жизнь</b>

Выберите раздел ↓''',
        'en': '''🎉 <b>Student Life</b>

Choose a section ↓'''
    }

    keyboard = InlineKeyboardMarkup(row_width=1)

    if lang == 'uz':
        keyboard.add(
            InlineKeyboardButton("🎉 Talabalar klublari", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Kampus muhitidan fotolavhalar", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ Talaba hayotidagi 1 kun", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Amaliyot va Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_students_menu")
        )
    elif lang == 'ru':
        keyboard.add(
            InlineKeyboardButton("🎉 Студенческие клубы", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Фото кампуса", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ Один день из жизни студента", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Практика и Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Назад", callback_data="back_to_students_menu")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("🎉 Student Clubs", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Campus Photos", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ A Day in Student Life", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Internship & Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Back", callback_data="back_to_students_menu")
        )

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ---- 1. Talabalar klublari ----
clubs_data = {
    "uz": """🎉 <b>TALABALAR KLUBLARI</b>

🎯 <b>Yosh analitiklar klubi</b>
👤 Mentor: @imkamronbek

⚽️ <b>Futbol klubi</b>
👤 Mentor: @imkamronbek

♟ <b>Shaxmat-shashka klubi</b>
👤 Mentor: @imkamronbek

🎭 <b>San'at klubi</b>
👤 Mentor: @imkamronbek

📸 <b>Fotoklab</b>
👤 Mentor: @imkamronbek

💡 <b>Innovatsiya klubi</b>
👤 Mentor: @imkamronbek

🔗 Barcha klublar: @tiu_clubs""",

    "ru": """🎉 <b>СТУДЕНЧЕСКИЕ КЛУБЫ</b>

🎯 <b>Клуб молодых аналитиков</b>
👤 Ментор: @imkamronbek

⚽️ <b>Футбольный клуб</b>
👤 Ментор: @imkamronbek

♟ <b>Шахматно-шашечный клуб</b>
👤 Ментор: @imkamronbek

🎭 <b>Художественный клуб</b>
👤 Ментор: @imkamronbek

📸 <b>Фотоклуб</b>
👤 Ментор: @imkamronbek

💡 <b>Инновационный клуб</b>
👤 Ментор: @imkamronbek

🔗 Все клубы: @tiu_clubs""",

    "en": """🎉 <b>STUDENT CLUBS</b>

🎯 <b>Young Analysts Club</b>
👤 Mentor: @imkamronbek

⚽️ <b>Football Club</b>
👤 Mentor: @imkamronbek

♟ <b>Chess & Checkers Club</b>
👤 Mentor: @imkamronbek

🎭 <b>Art Club</b>
👤 Mentor: @imkamronbek

📸 <b>Photo Club</b>
👤 Mentor: @imkamronbek

💡 <b>Innovation Club</b>
👤 Mentor: @imkamronbek

🔗 All clubs: @tiu_clubs"""
}


async def student_clubs_callback(callback: types.CallbackQuery):
    """Talabalar klublari callback handler"""
    lang = db.get_user_language(callback.from_user.id)

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_text = "🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back"
    keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_student_life"))

    await callback.message.edit_text(
        clubs_data.get(lang, clubs_data['uz']),
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback.answer()


# ---- 2. Kampus fotolavhalari ----
async def campus_photos_callback(callback: types.CallbackQuery):
    """Kampus fotolari callback handler"""
    lang = db.get_user_language(callback.from_user.id)

    captions = {
        'uz': '🎓 <b>Kampus muhitidan fotolavhalar</b>\n\n🏛 Zamonaviy o\'quv binolari\n🌳 Yashil maydonlar\n📚 Kutubxona\n☕️ Student zonalari',
        'ru': '🎓 <b>Фото кампуса</b>\n\n🏛 Современные учебные корпуса\n🌳 Зелёные зоны\n📚 Библиотека\n☕️ Студенческие зоны',
        'en': '🎓 <b>Campus Photos</b>\n\n🏛 Modern academic buildings\n🌳 Green areas\n📚 Library\n☕️ Student zones'
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_text = "🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back"
    keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_student_life"))

    # Fotosuratlar ro'yxati
    photo_filenames = ["campus1.png", "campus2.png", "campus3.png", "campus4.png"]
    photo_paths = []

    # Mavjud fayllarni tekshirish
    for filename in photo_filenames:
        path = get_media_path(filename)
        if path:
            photo_paths.append(path)

    try:
        if photo_paths:
            # Agar fotolar mavjud bo'lsa
            await callback.message.delete()

            media_group = []
            for i, photo_path in enumerate(photo_paths):
                if i == 0:
                    media_group.append(InputMediaPhoto(
                        media=InputFile(photo_path),
                        caption=captions.get(lang, captions['uz']),
                        parse_mode="HTML"
                    ))
                else:
                    media_group.append(InputMediaPhoto(media=InputFile(photo_path)))

            await callback.message.answer_media_group(media_group)
            await callback.message.answer("⬆️", reply_markup=keyboard)
        else:
            # Agar fotolar mavjud bo'lmasa
            await callback.message.edit_text(
                f"{captions.get(lang, captions['uz'])}\n\n📷 Fotosuratlar hozircha mavjud emas.",
                parse_mode="HTML",
                reply_markup=keyboard
            )

    except Exception as e:
        # Har qanday xatolik yuz bersa
        try:
            await callback.message.edit_text(
                f"{captions.get(lang, captions['uz'])}\n\n📷 Fotosuratlar yuklanmoqda...",
                parse_mode="HTML",
                reply_markup=keyboard
            )
        except:
            await callback.message.answer(
                f"{captions.get(lang, captions['uz'])}\n\n📷 Fotosuratlar yuklanmoqda...",
                parse_mode="HTML",
                reply_markup=keyboard
            )

    await callback.answer()


# ---- 3. Talaba hayotidagi 1 kun ----
async def student_day_vlog_callback(callback: types.CallbackQuery):
    """Talaba hayotidagi 1 kun callback handler"""
    lang = db.get_user_language(callback.from_user.id)

    texts = {
        'uz': '''☕️ <b>Talaba hayotidagi 1 kun</b>

🎬 Bizning talabalarimizning bir kunlik hayotini tomosha qiling:

🔗 https://youtube.com/watch?v=YOUR_VIDEO_ID

📱 Ko'proq videolar: @tiu_students''',

        'ru': '''☕️ <b>Один день из жизни студента</b>

🎬 Посмотрите один день из жизни наших студентов:

🔗 https://youtube.com/watch?v=YOUR_VIDEO_ID

📱 Больше видео: @tiu_students''',

        'en': '''☕️ <b>A Day in Student Life</b>

🎬 Watch a day in the life of our students:

🔗 https://youtube.com/watch?v=YOUR_VIDEO_ID

📱 More videos: @tiu_students'''
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_text = "🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back"
    keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_student_life"))

    await callback.message.edit_text(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    await callback.answer()


# ---- 4. Career Center ----
async def career_center_callback(callback: types.CallbackQuery):
    """Career Center callback handler"""
    lang = db.get_user_language(callback.from_user.id)

    texts = {
        'uz': '''💼 <b>AMALIYOT VA CAREER CENTER</b>

🎯 <b>Bizning imkoniyatlarimiz:</b>

✅ Kompaniyalarda amaliyot
✅ Karyera maslahat xizmatlari
✅ Rezyume tayyorlash
✅ Suhbatlarga tayyorgarlik
✅ Ish o'rinlari bilan tanishish
✅ Networking tadbirlari

📞 <b>Bog'lanish:</b>
👤 Career Center: @career_mentor
📱 Telegram: @tiu_career

🌐 Ko'proq ma'lumot: career.tiu.uz''',

        'ru': '''💼 <b>ПРАКТИКА И CAREER CENTER</b>

🎯 <b>Наши возможности:</b>

✅ Стажировки в компаниях
✅ Карьерные консультации
✅ Подготовка резюме
✅ Подготовка к собеседованиям
✅ Знакомство с вакансиями
✅ Networking мероприятия

📞 <b>Контакты:</b>
👤 Career Center: @career_mentor
📱 Telegram: @tiu_career

🌐 Подробнее: career.tiu.uz''',

        'en': '''💼 <b>INTERNSHIP & CAREER CENTER</b>

🎯 <b>Our opportunities:</b>

✅ Company internships
✅ Career counseling services
✅ Resume preparation
✅ Interview preparation
✅ Job vacancy introductions
✅ Networking events

📞 <b>Contact:</b>
👤 Career Center: @career_mentor
📱 Telegram: @tiu_career

🌐 More info: career.tiu.uz'''
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_text = "🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back"
    keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_student_life"))

    photo_path = get_media_path("career_center.jpg")

    try:
        if photo_path and os.path.exists(photo_path):
            # Agar foto mavjud bo'lsa
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=InputFile(photo_path),
                caption=texts.get(lang, texts['uz']),
                parse_mode="HTML",
                reply_markup=keyboard
            )
        else:
            # Agar foto mavjud bo'lmasa - faqat matn yuborish
            await callback.message.edit_text(
                texts.get(lang, texts['uz']),
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
    except Exception as e:
        # Har qanday xatolik - faqat matn
        try:
            await callback.message.edit_text(
                texts.get(lang, texts['uz']),
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        except:
            await callback.message.answer(
                texts.get(lang, texts['uz']),
                parse_mode="HTML",
                reply_markup=keyboard
            )

    await callback.answer()


# ---- Orqaga qaytish handlarlari ----
async def back_to_student_life_callback(callback: types.CallbackQuery):
    """Talabalar hayoti menyusiga qaytish"""
    lang = db.get_user_language(callback.from_user.id)

    texts = {
        'uz': '''🎉 <b>Talabalar hayoti</b>

Quyidagi bo'limlardan birini tanlang ↓''',
        'ru': '''🎉 <b>Студенческая жизнь</b>

Выберите раздел ↓''',
        'en': '''🎉 <b>Student Life</b>

Choose a section ↓'''
    }

    keyboard = InlineKeyboardMarkup(row_width=1)

    if lang == 'uz':
        keyboard.add(
            InlineKeyboardButton("🎉 Talabalar klublari", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Kampus muhitidan fotolavhalar", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ Talaba hayotidagi 1 kun", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Amaliyot va Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_students_menu")
        )
    elif lang == 'ru':
        keyboard.add(
            InlineKeyboardButton("🎉 Студенческие клубы", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Фото кампуса", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ Один день из жизни студента", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Практика и Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Назад", callback_data="back_to_students_menu")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("🎉 Student Clubs", callback_data="student_clubs"),
            InlineKeyboardButton("🎓 Campus Photos", callback_data="campus_photos"),
            InlineKeyboardButton("☕️ A Day in Student Life", callback_data="student_day_vlog"),
            InlineKeyboardButton("💼 Internship & Career Center", callback_data="career_center"),
            InlineKeyboardButton("🔙 Back", callback_data="back_to_students_menu")
        )

    try:
        await callback.message.edit_text(
            texts.get(lang, texts['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except:
        await callback.message.answer(
            texts.get(lang, texts['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )

    await callback.answer()


async def back_to_students_menu_callback(callback: types.CallbackQuery):
    """Talabalar uchun asosiy menyusiga qaytish"""
    user_id = callback.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '🎓 Talabalar uchun\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '🎓 Для студентов\n\nВыберите один из разделов:',
        'en': '🎓 For Students\n\nChoose one of the sections:'
    }

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_students_submenu_keyboard(user_id)
    )
    await callback.answer()


# ===============================
# HANDLERLARNI RO'YXATDAN O'TKAZISH
# ===============================

def register_students_handlers(dp: Dispatcher):
    """Asosiy talabalar handler"""
    # Talabalar uchun asosiy menyu
    dp.register_message_handler(
        students_handler,
        lambda message: message.text in ['🎓 Talabalar uchun', '🎓 Для студентов', '🎓 For Students']
    )

    # Dars jadvali
    dp.register_message_handler(
        schedule_start_handler,
        lambda message: message.text in ['📅 Dars jadvali', '📅 Расписание занятий', '📅 Class schedule'],
        state='*'
    )
    dp.register_message_handler(process_faculty, state=ScheduleStates.waiting_for_faculty)
    dp.register_message_handler(process_course, state=ScheduleStates.waiting_for_course)
    dp.register_message_handler(process_group, state=ScheduleStates.waiting_for_group)

    # Kutubxona
    dp.register_message_handler(
        library_resources_info,
        lambda message: message.text in [
            '📚 Kutubxona / resurslar',
            '📚 Библиотека / ресурсы',
            '📚 Library / resources'
        ]
    )

    # Talabalar hayoti - message handler
    dp.register_message_handler(
        student_life_info,
        lambda msg: msg.text in [
            '🎉 Talabalar hayoti / klublar',
            '🎉 Студенческая жизнь / клубы',
            '🎉 Student life / clubs'
        ]
    )

    # Talabalar hayoti - callback handlers
    dp.register_callback_query_handler(
        student_clubs_callback,
        lambda c: c.data == "student_clubs"
    )
    dp.register_callback_query_handler(
        campus_photos_callback,
        lambda c: c.data == "campus_photos"
    )
    dp.register_callback_query_handler(
        student_day_vlog_callback,
        lambda c: c.data == "student_day_vlog"
    )
    dp.register_callback_query_handler(
        career_center_callback,
        lambda c: c.data == "career_center"
    )
    dp.register_callback_query_handler(
        back_to_student_life_callback,
        lambda c: c.data == "back_to_student_life"
    )
    dp.register_callback_query_handler(
        back_to_students_menu_callback,
        lambda c: c.data == "back_to_students_menu"
    )