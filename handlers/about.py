from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t

db = Database()


def get_about_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '🎓 Universitet haqida qisqacha ma\'lumot',
            '🌍 Hamkor universitetlar',
            '📚 Fakultetlar va dasturlar',
            '🎥 Video turlar'
        ],
        'ru': [
            '🎓 Краткая информация об университете',
            '🌍 Университеты-партнеры',
            '📚 Факультеты и программы',
            '🎥 Видео туры'
        ],
        'en': [
            '🎓 Brief information about university',
            '🌍 Partner universities',
            '📚 Faculties and programs',
            '🎥 Video tours'
        ]
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


async def about_tiu_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '🏫 TIU haqida\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '🏫 О TIU\n\nВыберите один из разделов:',
        'en': '🏫 About TIU\n\nChoose one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def about_university_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🎓 Tashkent International University

TIU — O'zbekistondagi yetakchi xalqaro universitetlardan biri. Zamonaviy ta'lim va xalqaro imkoniyatlar maskani.

✅ Xalqaro standartdagi ta'lim
✅ Zamonaviy kampus va infratuzilma
✅ Tajribali professor-o'qituvchilar
✅ Qo'sh diplom dasturlari
✅ Karyera markazi xizmatlari
✅ 100+ xalqaro hamkorliklar

🌐 www.tiu.uz''',

        'ru': '''🎓 Tashkent International University

TIU — один из ведущих международных университетов Узбекистана. Центр современного образования и международных возможностей.

✅ Образование международного стандарта
✅ Современный кампус и инфраструктура
✅ Опытные преподаватели
✅ Программы двойного диплома
✅ Услуги карьерного центра
✅ 100+ международных партнерств

🌐 www.tiu.uz''',

        'en': '''🎓 Tashkent International University

TIU — one of the leading international universities in Uzbekistan. A hub of modern education and international opportunities.

✅ International standard education
✅ Modern campus and infrastructure
✅ Experienced faculty
✅ Double degree programs
✅ Career center services
✅ 100+ international partnerships

🌐 www.tiu.uz'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def partner_universities_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🌍 Hamkor universitetlar

TIU dunyoning yetakchi universitetlari bilan hamkorlik qiladi:

🇬🇧 University of Westminster (Buyuk Britaniya)
🇰🇷 Inha University (Janubiy Koreya)
🇺🇸 Webster University (AQSH)
🇷🇺 MGU (Rossiya)
🇹🇷 Istanbul University (Turkiya)
🇩🇪 TU Dresden (Germaniya)

Va yana 100+ xalqaro hamkorlar!''',

        'ru': '''🌍 Университеты-партнеры

TIU сотрудничает с ведущими университетами мира:

🇬🇧 University of Westminster (Великобритания)
🇰🇷 Inha University (Южная Корея)
🇺🇸 Webster University (США)
🇷🇺 МГУ (Россия)
🇹🇷 Istanbul University (Турция)
🇩🇪 TU Dresden (Германия)

И еще 100+ международных партнеров!''',

        'en': '''🌍 Partner Universities

TIU collaborates with leading universities worldwide:

🇬🇧 University of Westminster (United Kingdom)
🇰🇷 Inha University (South Korea)
🇺🇸 Webster University (USA)
🇷🇺 MSU (Russia)
🇹🇷 Istanbul University (Turkey)
🇩🇪 TU Dresden (Germany)

And 100+ more international partners!'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def faculties_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''📚 Fakultetlar va yo'nalishlar

💼 Biznes va menejment
💻 Axborot texnologiyalari
🏗 Muhandislik
🎨 Dizayn va san'at
⚖️ Yuridik
🌍 Xalqaro munosabatlar

Batafsil: www.tiu.uz/faculties''',

        'ru': '''📚 Факультеты и направления

💼 Бизнес и менеджмент
💻 Информационные технологии
🏗 Инженерия
🎨 Дизайн и искусство
⚖️ Юриспруденция
🌍 Международные отношения

Подробнее: www.tiu.uz/faculties''',

        'en': '''📚 Faculties and Programs

💼 Business and Management
💻 Information Technology
🏗 Engineering
🎨 Design and Arts
⚖️ Law
🌍 International Relations

More details: www.tiu.uz/faculties'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def video_tours_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🎥 Video turlar

📺 YouTube: @tiuofficial
📷 Instagram: @tiuofficial
🎬 TikTok: @tiuofficial

Universitet kampusi, o'quv jarayoni va talabalar hayotidan videolar!''',

        'ru': '''🎥 Видео туры

📺 YouTube: @tiuofficial
📷 Instagram: @tiuofficial
🎬 TikTok: @tiuofficial

Видео о кампусе, учебном процессе и студенческой жизни!''',

        'en': '''🎥 Video Tours

📺 YouTube: @tiuofficial
📷 Instagram: @tiuofficial
🎬 TikTok: @tiuofficial

Videos about campus, educational process and student life!'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


def register_about_handlers(dp: Dispatcher):
    dp.register_message_handler(
        about_tiu_handler,
        lambda message: message.text in ['🏫 TIU haqida', '🏫 О TIU', '🏫 About TIU']
    )
    dp.register_message_handler(
        about_university_info,
        lambda message: message.text in [
            '🎓 Universitet haqida qisqacha ma\'lumot',
            '🎓 Краткая информация об университете',
            '🎓 Brief information about university'
        ]
    )
    dp.register_message_handler(
        partner_universities_info,
        lambda message: message.text in [
            '🌍 Hamkor universitetlar',
            '🌍 Университеты-партнеры',
            '🌍 Partner universities'
        ]
    )
    dp.register_message_handler(
        faculties_info,
        lambda message: message.text in [
            '📚 Fakultetlar va dasturlar',
            '📚 Факультеты и программы',
            '📚 Faculties and programs'
        ]
    )
    dp.register_message_handler(
        video_tours_info,
        lambda message: message.text in [
            '🎥 Video turlar',
            '🎥 Видео туры',
            '🎥 Video tours'
        ]
    )