from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_main_keyboard
from database.db import Database
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
            '💼 Kontrakt',
            '🎉 Talabalar hayoti / klublar'
        ],
        'ru': [
            '📅 Расписание занятий',
            '📚 Библиотека / ресурсы',
            '💼 Контракт',
            '🎉 Студенческая жизнь / клубы'
        ],
        'en': [
            '📅 Class schedule',
            '📚 Library / resources',
            '💼 Contract',
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

async def library_resources_info(message: types.Message, state: FSMContext):
    """Show library e-library link"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # Clear any previous state
    await state.finish()

    texts = {
        'uz': '''📚 <b>Kutubxona / Resurslar</b>

Elektron kutubxonaga kirish uchun quyidagi havoladan foydalaning:

🔗 <a href="https://www.tiu.uz/elibrary">https://www.tiu.uz/elibrary</a>

Bu yerda darsliklar, ilmiy maqolalar va boshqa ta'lim resurslari mavjud.''',
        'ru': '''📚 <b>Библиотека / Ресурсы</b>

Для доступа к электронной библиотеке используйте следующую ссылку:

🔗 <a href="https://www.tiu.uz/elibrary">https://www.tiu.uz/elibrary</a>

Здесь доступны учебники, научные статьи и другие образовательные ресурсы.''',
        'en': '''📚 <b>Library / Resources</b>

To access the e-library, use the following link:

🔗 <a href="https://www.tiu.uz/elibrary">https://www.tiu.uz/elibrary</a>

Here you can find textbooks, scientific articles and other educational resources.'''
    }

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back",
            callback_data="back_to_students_menu"
        )
    )

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=keyboard,
        disable_web_page_preview=True
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

Quyidagi bo'limlardan birini tanlang''',
        'ru': '''🎉 <b>Студенческая жизнь</b>

Выберите раздел''',
        'en': '''🎉 <b>Student Life</b>

Choose a section'''
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

📚 <b>Kitobxonlik & Mushoira Klubi</b>
🔗 @KMK_TIU_official

⚖️ <b>Yuristlar klubi</b>
🔗 @Yuristlar_klubi_TIU

🧠 <b>Zakovat Klubi</b>
👤 @Shamsiddin_Sherzodbekvich

👑 <b>"Miss Yurist"</b>
🔗 @missyuristqizlarklubi0107

💼 <b>Yosh Iqtisodchilar Klubi</b>
🔗 @XKB000

🎭 <b>TIU Ijodkor Yoshlari</b>
👤 @Abrorjon_4033

🎯 <b>Yosh Analitiklar Klubi</b>
👤 @Habibullo_Nazarov""",

    "ru": """🎉 <b>СТУДЕНЧЕСКИЕ КЛУБЫ</b>

📚 <b>Клуб чтения и поэзии</b>
🔗 @KMK_TIU_official

⚖️ <b>Клуб юристов</b>
🔗 @Yuristlar_klubi_TIU

🧠 <b>Клуб интеллектуальных игр</b>
👤 @Shamsiddin_Sherzodbekvich

👑 <b>"Мисс Юрист"</b>
🔗 @missyuristqizlarklubi0107

💼 <b>Клуб молодых экономистов</b>
🔗 @XKB000

🎭 <b>Творческая молодежь TIU</b>
👤 @Abrorjon_4033

🎯 <b>Клуб молодых аналитиков</b>
👤 @Habibullo_Nazarov""",

    "en": """🎉 <b>STUDENT CLUBS</b>

📚 <b>Reading & Poetry Club</b>
🔗 @KMK_TIU_official

⚖️ <b>Law Club</b>
🔗 @Yuristlar_klubi_TIU

🧠 <b>Intellectual Games Club</b>
👤 @Shamsiddin_Sherzodbekvich

👑 <b>"Miss Lawyer"</b>
🔗 @missyuristqizlarklubi0107

💼 <b>Young Economists Club</b>
🔗 @XKB000

🎭 <b>TIU Creative Youth</b>
👤 @Abrorjon_4033

🎯 <b>Young Analysts Club</b>
👤 @Habibullo_Nazarov"""
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

🔗 https://youtu.be/oSepaRSf9_8?si=-UTVmrL2TeWS1I2c

📱 Ko'proq videolar: https://www.youtube.com/@tiu_uz''',

        'ru': '''☕️ <b>Один день из жизни студента</b>

🎬 Посмотрите один день из жизни наших студентов:

🔗 https://youtu.be/oSepaRSf9_8?si=-UTVmrL2TeWS1I2c

📱 Больше видео: https://www.youtube.com/@tiu_uz''',

        'en': '''☕️ <b>A Day in Student Life</b>

🎬 Watch a day in the life of our students:

🔗 https://youtu.be/oSepaRSf9_8?si=-UTVmrL2TeWS1I2c

📱 More videos: https://www.youtube.com/@tiu_uz'''
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
        'uz': '''
🇰🇷 <b>TIU talabalari Koreyada!</b>

40 kunlik amaliyot davomida TIU talabalari Seul shahrining mashhur diqqatga sazovor joylariga, jumladan tarixiy Gyeongbokgung saroyiga tashrif buyurishdi. 🏯✨

📍 Bugun esa ular Koreyaning nufuzli kompaniyalaridan biri — Hyundai Heavy Industries – Engine & Machinery Division ga tashrif buyurib, muhandislik jarayonlari haqida qiziqarli ma'lumotlarga ega bo'lishdi.

Shuningdek, talabalar Koreyaning dengiz bo'yidagi go'zal shahri Busan ga yo'l olishmoqda. 🌊🚆

Bu safar davomida ular nafaqat bilim va tajriba orttirmoqda, balki Koreya madaniyati va sanoati bilan yaqindan tanishishmoqda. 🇺🇿🤝🇰🇷
''',

        'ru': '''
🇰🇷 <b>Студенты TIU в Корее!</b>

В течение 40-дневной стажировки студенты TIU посетили знаменитые достопримечательности Сеула, включая исторический дворец Кёнбоккун. 🏯✨

📍 Сегодня они также посетили одну из престижных компаний Кореи — Hyundai Heavy Industries – Engine & Machinery Division и получили интересную информацию об инженерных процессах.

Кроме того, студенты направляются в прекрасный прибрежный город Корея - Пусан. 🌊🚆

Во время этой поездки они не только увеличивают знания и опыт, но и знакомятся с культурой и промышленностью Кореи. 🇺🇿🤝🇰🇷
''',

        'en': '''
🇰🇷 <b>TIU Students in Korea!</b>

During a 40-day internship, TIU students visited Seoul's famous attractions, including the historic Gyeongbokgung Palace. 🏯✨

📍 Today they also visited one of Korea's prestigious companies — Hyundai Heavy Industries – Engine & Machinery Division and gained interesting insights into engineering processes.

Additionally, students are heading to Korea's beautiful coastal city - Busan. 🌊🚆

During this trip, they are not only increasing their knowledge and experience, but also getting closely acquainted with Korean culture and industry. 🇺🇿🤝🇰🇷

'''
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

Quyidagi bo'limlardan birini tanlang:''',
        'ru': '''🎉 <b>Студенческая жизнь</b>

Выберите раздел:''',
        'en': '''🎉 <b>Student Life</b>

Choose a section:'''
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
# KONTRAKT BO'LIMI
# ===============================

async def contract_info_handler(message: types.Message, state: FSMContext):
    """Contract menu handler - ask for passport series"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # Clear any previous state
    await state.finish()

    texts = {
        'uz': '''💼 <b>Kontrakt ma'lumotlari</b>

Kontrakt ma'lumotlaringizni ko'rish uchun pasport seriangizni kiriting.

<i>Misol: AA1234567</i>''',
        'ru': '''💼 <b>Информация о контракте</b>

Для просмотра информации о контракте введите серию вашего паспорта.

<i>Пример: AA1234567</i>''',
        'en': '''💼 <b>Contract Information</b>

To view your contract information, please enter your passport series.

<i>Example: AA1234567</i>'''
    }

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(t(user_id, 'back')))

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=keyboard,
        parse_mode='HTML'
    )

    from states.forms import ContractLookupState
    await ContractLookupState.waiting_for_passport.set()


async def process_passport_lookup(message: types.Message, state: FSMContext):
    """Process passport series and show contract information"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # Check if user wants to go back
    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await state.finish()
        await students_handler(message)
        return

    passport_series = message.text.strip().upper()

    # Lookup contract in database
    contract = db.get_contract_by_passport(passport_series)

    if not contract:
        # Contract not found
        texts = {
            'uz': f'''❌ <b>Topilmadi</b>

Pasport seriya <code>{passport_series}</code> bo'yicha kontrakt ma'lumotlari topilmadi.

Iltimos, pasport seriangizni to'g'ri kiriting yoki administrator bilan bog'laning.''',
            'ru': f'''❌ <b>Не найдено</b>

По серии паспорта <code>{passport_series}</code> информация о контракте не найдена.

Пожалуйста, введите правильную серию паспорта или свяжитесь с администратором.''',
            'en': f'''❌ <b>Not Found</b>

Contract information for passport series <code>{passport_series}</code> was not found.

Please enter the correct passport series or contact the administrator.'''
        }

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(t(user_id, 'back')))

        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        return

    # Contract found - display information
    # contract[0] = id, contract[1] = passport_series, contract[2] = full_name,
    # contract[3] = jshshir, contract[4] = course, contract[5] = total_amount,
    # contract[6] = paid_amount, contract[7] = remaining_amount, contract[8] = upload_date, contract[9] = excel_filename

    full_name = contract[2]
    jshshir = contract[3]
    course = contract[4]
    total_amount = contract[5]
    paid_amount = contract[6]
    remaining_amount = contract[7]

    # Calculate payment percentage
    payment_percentage = 0
    if total_amount and total_amount > 0:
        payment_percentage = (paid_amount / total_amount) * 100

    # Format amounts with thousand separators
    def format_amount(amount):
        if amount:
            return f"{amount:,.2f}".replace(',', ' ')
        return "0.00"

    texts = {
        'uz': f'''✅ <b>Kontrakt ma'lumotlari</b>

👤 <b>Talaba:</b> {full_name}
📚 <b>Kurs:</b> {course}

💰 <b>Kontrakt summasi:</b> {format_amount(total_amount)} so'm
💳 <b>To'langan:</b> {format_amount(paid_amount)} so'm
📊 <b>To'lov foizi:</b> {payment_percentage:.1f}%
💵 <b>Qoldiq:</b> {format_amount(remaining_amount)} so'm''',

        'ru': f'''✅ <b>Информация о контракте</b>

👤 <b>Студент:</b> {full_name}
📚 <b>Курс:</b> {course}

💰 <b>Сумма контракта:</b> {format_amount(total_amount)} сум
💳 <b>Оплачено:</b> {format_amount(paid_amount)} сум
📊 <b>Процент оплаты:</b> {payment_percentage:.1f}%
💵 <b>Остаток:</b> {format_amount(remaining_amount)} сум''',

        'en': f'''✅ <b>Contract Information</b>

👤 <b>Student:</b> {full_name}
📚 <b>Course:</b> {course}

💰 <b>Contract amount:</b> {format_amount(total_amount)} sum
💳 <b>Paid:</b> {format_amount(paid_amount)} sum
📊 <b>Payment percentage:</b> {payment_percentage:.1f}%
💵 <b>Remaining:</b> {format_amount(remaining_amount)} sum'''
    }

    await state.finish()
    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_students_submenu_keyboard(user_id),
        parse_mode='HTML'
    )


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

    # Contract menu
    dp.register_message_handler(
        contract_info_handler,
        lambda message: message.text in [
            '💼 Kontrakt',
            '💼 Контракт',
            '💼 Contract'
        ],
        state='*'
    )

    # Contract passport lookup
    from states.forms import ContractLookupState
    dp.register_message_handler(
        process_passport_lookup,
        state=ContractLookupState.waiting_for_passport
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