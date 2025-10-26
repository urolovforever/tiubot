from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t
from keyboards.inline import get_events_inline_keyboard

db = Database()


def get_news_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
    '🆕 Hafta dayjesti',
    '🎥 So‘nggi yangiliklar',
    '🗓 Tadbirlar taqvimi'
],

'ru': [
    '🆕 Еженедельный дайджест',
    '🎥 Последние новости',
    '🗓 Календарь мероприятий'
],

'en': [
    '🆕 Weekly digest',
    '🎥 Latest news',
    '🗓 Events calendar'
]

    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.insert(KeyboardButton(t(user_id, 'back')))
    return keyboard


async def news_menu_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '📢 Yangiliklar\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '📢 Новости\n\nВыберите один из разделов:',
        'en': '📢 News\n\nChoose one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_news_submenu_keyboard(user_id)
    )


async def latest_news_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🆕 So'nggi yangiliklar

📱 Telegram: @tiuofficial
📷 Instagram: @tiuofficial

Obuna bo'ling!

🌐 www.tiu.uz/news''',

        'ru': '''🆕 Последние новости

📱 Telegram: @tiuofficial
📷 Instagram: @tiuofficial

Подпишитесь!

🌐 www.tiu.uz/news''',

        'en': '''🆕 Latest News

📱 Telegram: @tiuofficial
📷 Instagram: @tiuofficial

Subscribe!

🌐 www.tiu.uz/news'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_news_submenu_keyboard(user_id)
    )


async def video_news_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🎥 Video yangiliklar

📺 YouTube: @tiuofficial
📷 Instagram Reels
🎬 TikTok: @tiuofficial

Obuna bo'ling!''',

        'ru': '''🎥 Видео новости

📺 YouTube: @tiuofficial
📷 Instagram Reels
🎬 TikTok: @tiuofficial

Подпишитесь!''',

        'en': '''🎥 Video News

📺 YouTube: @tiuofficial
📷 Instagram Reels
🎬 TikTok: @tiuofficial

Subscribe!'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_news_submenu_keyboard(user_id)
    )


async def events_calendar_handler(message: types.Message):
    """
    Yangiliklar menyusidan Tadbirlar taqvimini ko'rsatish
    Yangi inline keyboard formatida
    """
    user_id = message.from_user.id

    # Yaqinlashib kelayotgan tadbirlarni olish (sanasi bo'yicha tartiblangan)
    events = db.get_all_events(upcoming_only=True)

    if not events:
        texts = {
            'uz': '📭 Hozircha rejalashtirilgan tadbirlar yo\'q.\n\n📱 @tiuofficial',
            'ru': '📭 Пока нет запланированных мероприятий.\n\n📱 @tiuofficial',
            'en': '📭 No scheduled events yet.\n\n📱 @tiuofficial'
        }
        lang = db.get_user_language(user_id)
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_news_submenu_keyboard(user_id)
        )
        return

    # Inline keyboard bilan tadbirlar ro'yxatini ko'rsatish
    await message.answer(
        t(user_id, 'events_calendar_title'),
        reply_markup=get_events_inline_keyboard(events)
    )


def register_news_handlers(dp: Dispatcher):
    dp.register_message_handler(
        news_menu_handler,
        lambda message: message.text in ['📰 Yangiliklar', '📰 Новости', '📰 News']
    )

    # 🆕 Hafta dayjesti (Weekly digest)
    dp.register_message_handler(
        latest_news_handler,
        lambda message: message.text in [
            '🆕 Hafta dayjesti',
            '🆕 Еженедельный дайджест',
            '🆕 Weekly digest'
        ]
    )

    # 🎥 Video yangiliklar (Video news)
    dp.register_message_handler(
        video_news_handler,
        lambda message: message.text in [
            '🎥 So‘nggi yangiliklar',
            '🎥 Последние новости',
            '🎥 Latest news'
        ]
    )

    # 🗓 Tadbirlar taqvimi (Events calendar)
    dp.register_message_handler(
        events_calendar_handler,
        lambda message: message.text in [
            '🗓 Tadbirlar taqvimi',
            '🗓 Календарь мероприятий',
            '🗓 Events calendar'
        ]
    )

