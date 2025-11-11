from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_direction_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
from database.db import Database
from states.forms import ScheduleStates, LibraryStates
from utils.helpers import t
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, InputMediaPhoto
import os
import asyncio
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
        t(user_id, 'choose_direction'),
        reply_markup=get_direction_keyboard(user_id, faculty)
    )
    await ScheduleStates.waiting_for_direction.set()


async def process_direction(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_faculty'),
            reply_markup=get_faculty_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_faculty.set()
        return

    direction = message.text
    data = await state.get_data()
    faculty = data.get('faculty')

    await state.update_data(direction=direction)

    await message.answer(
        t(user_id, 'choose_course'),
        reply_markup=get_course_keyboard(user_id, faculty, direction)
    )
    await ScheduleStates.waiting_for_course.set()


async def process_course(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        await message.answer(
            t(user_id, 'choose_direction'),
            reply_markup=get_direction_keyboard(user_id, faculty)
        )
        await ScheduleStates.waiting_for_direction.set()
        return

    course = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    direction = data.get('direction')

    await state.update_data(course=course)

    # Get groups from FACULTIES config
    from config import FACULTIES
    lang = db.get_user_language(user_id)
    faculties_lang = FACULTIES.get(lang, FACULTIES['uz'])

    groups = []
    if faculty in faculties_lang and direction in faculties_lang[faculty] and course in faculties_lang[faculty][direction]:
        groups = faculties_lang[faculty][direction][course]

    # If no groups found in config, try database
    if not groups:
        groups = db.get_groups_by_faculty_direction_course(faculty, direction, course)

    # If still no groups, use empty list (will show message)
    if not groups:
        groups = []

    await message.answer(
        t(user_id, 'choose_group'),
        reply_markup=get_group_keyboard(user_id, groups)
    )
    await ScheduleStates.waiting_for_group.set()


async def process_group(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        direction = data.get('direction')
        await message.answer(
            t(user_id, 'choose_course'),
            reply_markup=get_course_keyboard(user_id, faculty, direction)
        )
        await ScheduleStates.waiting_for_course.set()
        return

    group = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    direction = data.get('direction')
    course = data.get('course')

    schedule_image = db.get_schedule_with_direction(faculty, direction, course, group)

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


async def library_resources_info(message: types.Message, state: FSMContext):
    """Redirect to new library system with categories"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # Clear any previous state
    await state.finish()
    await LibraryStates.choosing_category.set()

    # Import here to avoid circular dependency
    from handlers.library import get_library_categories_keyboard

    keyboard = get_library_categories_keyboard(lang)

    await message.answer(
        t(user_id, 'library_title'),
        reply_markup=keyboard
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

    try:
        await callback.answer()
    except Exception:
        pass


# ---- 2. Kampus fotolavhalari ----
async def campus_photos_callback(callback: types.CallbackQuery):
    """Kampus fotolari callback handler"""
    # Darhol callback javobini yuborish - bu loading hourglass ni ko'rsatadi
    try:
        await callback.answer()
    except Exception:
        pass

    lang = db.get_user_language(callback.from_user.id)

    captions = {
        'uz': '🎓 <b>Kampus muhitidan fotolavhalar</b>\n\n🏛 Zamonaviy o\'quv binolari\n🌳 Yashil maydonlar\n📚 Kutubxona\n☕️ Student zonalari',
        'ru': '🎓 <b>Фото кампуса</b>\n\n🏛 Современные учебные корпуса\n🌳 Зелёные зоны\n📚 Библиотека\n☕️ Студенческие зоны',
        'en': '🎓 <b>Campus Photos</b>\n\n🏛 Modern academic buildings\n🌳 Green areas\n📚 Library\n☕️ Student zones'
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    back_text = "🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back"
    keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_student_life"))

    try:
        # Eski xabarni o'chirish (kutmasdan)
        asyncio.create_task(callback.message.delete())

        # Avval cache dan file_id larni tekshiramiz
        cached_file_ids = db.get_cached_media_group('campus')

        if cached_file_ids and len(cached_file_ids) > 0:
            # Cache dan yuborish - juda tez!
            media_group = []
            for i, file_id in enumerate(cached_file_ids):
                if i == 0:
                    media_group.append(
                        InputMediaPhoto(
                            media=file_id,
                            caption=captions.get(lang, captions['uz']),
                            parse_mode="HTML"
                        )
                    )
                else:
                    media_group.append(InputMediaPhoto(media=file_id))

            await callback.message.answer_media_group(media=media_group)
        else:
            # Cache yo'q - diskdan yuklash va cache ga saqlash
            available_photos = []
            for i in range(1, 7):
                for ext in ['.jpg', '.png']:
                    filename = f"campus{i}{ext}"
                    path = get_media_path(filename)
                    if path and os.path.exists(path):
                        available_photos.append((i, path))
                        break

            if available_photos:
                media_group = []
                for i, photo_path in enumerate(available_photos):
                    if i == 0:
                        media_group.append(
                            InputMediaPhoto(
                                media=InputFile(photo_path[1]),
                                caption=captions.get(lang, captions['uz']),
                                parse_mode="HTML"
                            )
                        )
                    else:
                        media_group.append(InputMediaPhoto(media=InputFile(photo_path[1])))

                # Media group yuborish va file_id larni saqlash
                sent_messages = await callback.message.answer_media_group(media=media_group)

                # File_id larni cache ga saqlash
                for idx, msg in enumerate(sent_messages):
                    if msg.photo:
                        file_id = msg.photo[-1].file_id
                        db.save_cached_file_id(f'campus_{idx+1}', file_id)
            else:
                await callback.message.answer(
                    f"{captions.get(lang, captions['uz'])}\n\n📷 Fotosuratlar hozircha mavjud emas.",
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
                return

        # Tugma bilan alohida xabar yuborish
        await callback.message.answer(
            "⬇️",
            reply_markup=keyboard
        )

    except Exception as e:
        # Har qanday xatolik yuz bersa
        await callback.message.answer(
            f"{captions.get(lang, captions['uz'])}\n\n📷 Fotosuratlar yuklanmoqda...",
            parse_mode="HTML",
            reply_markup=keyboard
        )


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

    try:
        await callback.answer()
    except Exception:
        pass


# ---- 4. Career Center ----
async def career_center_callback(callback: types.CallbackQuery):
    """Career Center callback handler"""
    # Darhol callback javobini yuborish
    try:
        await callback.answer()
    except Exception:
        pass

    lang = db.get_user_language(callback.from_user.id)

    texts = {
        'uz': '''💼 <b>AMALIYOT VA CAREER CENTER</b>

🇰🇷 <b>TIU talabalari Koreyada!</b>

40 kunlik amaliyot davomida TIU talabalari Seul shahrining mashhur diqqatga sazovor joylariga, jumladan tarixiy Gyeongbokgung saroyiga tashrif buyurishdi. 🏯✨

📍 Bugun esa ular Koreyaning nufuzli kompaniyalaridan biri — Hyundai Heavy Industries – Engine & Machinery Division ga tashrif buyurib, muhandislik jarayonlari haqida qiziqarli ma'lumotlarga ega bo'lishdi.

Shuningdek, talabalar Koreyaning dengiz bo'yidagi go'zal shahri Busan ga yo'l olishmoqda. 🌊🚆

Bu safar davomida ular nafaqat bilim va tajriba orttirmoqda, balki Koreya madaniyati va sanoati bilan yaqindan tanishishmoqda. 🇺🇿🤝🇰🇷

━━━━━━━━━━━━━━━━━━

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

🇰🇷 <b>Студенты TIU в Корее!</b>

В течение 40-дневной стажировки студенты TIU посетили знаменитые достопримечательности Сеула, включая исторический дворец Кёнбоккун. 🏯✨

📍 Сегодня они также посетили одну из престижных компаний Кореи — Hyundai Heavy Industries – Engine & Machinery Division и получили интересную информацию об инженерных процессах.

Кроме того, студенты направляются в прекрасный прибрежный город Корея - Пусан. 🌊🚆

Во время этой поездки они не только увеличивают знания и опыт, но и знакомятся с культурой и промышленностью Кореи. 🇺🇿🤝🇰🇷

━━━━━━━━━━━━━━━━━━

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

🇰🇷 <b>TIU Students in Korea!</b>

During a 40-day internship, TIU students visited Seoul's famous attractions, including the historic Gyeongbokgung Palace. 🏯✨

📍 Today they also visited one of Korea's prestigious companies — Hyundai Heavy Industries – Engine & Machinery Division and gained interesting insights into engineering processes.

Additionally, students are heading to Korea's beautiful coastal city - Busan. 🌊🚆

During this trip, they are not only increasing their knowledge and experience, but also getting closely acquainted with Korean culture and industry. 🇺🇿🤝🇰🇷

━━━━━━━━━━━━━━━━━━

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

    try:
        # Eski xabarni o'chirish (kutmasdan)
        asyncio.create_task(callback.message.delete())

        # Avval cache dan file_id larni tekshiramiz
        cached_file_ids = db.get_cached_media_group('career')

        if cached_file_ids and len(cached_file_ids) > 0:
            # Cache dan yuborish - juda tez!
            media_group = []
            for i, file_id in enumerate(cached_file_ids):
                if i == 0:
                    media_group.append(
                        InputMediaPhoto(
                            media=file_id,
                            caption=texts.get(lang, texts['uz']),
                            parse_mode="HTML"
                        )
                    )
                else:
                    media_group.append(InputMediaPhoto(media=file_id))

            await callback.message.answer_media_group(media=media_group)
        else:
            # Cache yo'q - diskdan yuklash va cache ga saqlash
            available_photos = []
            for i in range(1, 7):
                for ext in ['.jpg', '.png']:
                    filename = f"career{i}{ext}"
                    path = get_media_path(filename)
                    if path and os.path.exists(path):
                        available_photos.append((i, path))
                        break

            if available_photos:
                media_group = []
                for i, photo_path in enumerate(available_photos):
                    if i == 0:
                        media_group.append(
                            InputMediaPhoto(
                                media=InputFile(photo_path[1]),
                                caption=texts.get(lang, texts['uz']),
                                parse_mode="HTML"
                            )
                        )
                    else:
                        media_group.append(InputMediaPhoto(media=InputFile(photo_path[1])))

                # Media group yuborish va file_id larni saqlash
                sent_messages = await callback.message.answer_media_group(media=media_group)

                # File_id larni cache ga saqlash
                for idx, msg in enumerate(sent_messages):
                    if msg.photo:
                        file_id = msg.photo[-1].file_id
                        db.save_cached_file_id(f'career_{idx+1}', file_id)
            else:
                await callback.message.answer(
                    texts.get(lang, texts['uz']),
                    parse_mode="HTML",
                    reply_markup=keyboard,
                    disable_web_page_preview=True
                )
                return

        # Tugma bilan alohida xabar yuborish
        await callback.message.answer(
            "⬇️",
            reply_markup=keyboard
        )
    except Exception as e:
        # Har qanday xatolik - faqat matn
        await callback.message.answer(
            texts.get(lang, texts['uz']),
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


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
        # Agar edit_text ishlamasa (masalan, xabar rasm bo'lsa),
        # eski xabarni o'chirib, yangi xabar yuboramiz
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(
            texts.get(lang, texts['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )

    try:
        await callback.answer()
    except Exception:
        pass


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

    try:
        await callback.answer()
    except Exception:
        pass


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
    dp.register_message_handler(process_direction, state=ScheduleStates.waiting_for_direction)
    dp.register_message_handler(process_course, state=ScheduleStates.waiting_for_course)
    dp.register_message_handler(process_group, state=ScheduleStates.waiting_for_group)

    # Kutubxona - redirect to new library system
    dp.register_message_handler(
        library_resources_info,
        lambda message: message.text in [
            '📚 Kutubxona / resurslar',
            '📚 Библиотека / ресурсы',
            '📚 Library / resources'
        ],
        state='*'
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