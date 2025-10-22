from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t

db = Database()


def get_news_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '🆕 So\'nggi yangiliklar',
            '🎥 Video yangiliklar',
            '🗓 Tadbirlar taqvimi'
        ],
        'ru': [
            '🆕 Последние новости',
            '🎥 Видео новости',
            '🗓 Календарь мероприятий'
        ],
        'en': [
            '🆕 Latest news',
            '🎥 Video news',
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
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    events = db.get_all_events()

    texts = {
        'uz': '🗓 Tadbirlar taqvimi\n\nYaqinlashib kelayotgan tadbirlar:\n\n',
        'ru': '🗓 Календарь мероприятий\n\nПредстоящие мероприятия:\n\n',
        'en': '🗓 Events Calendar\n\nUpcoming events:\n\n'
    }

    text = texts.get(lang, texts['uz'])

    if events:
        for event in events[:5]:
            text += f'📌 {event[1]}\n📅 {event[3]}\n📍 {event[4]}\n\n'
    else:
        more_texts = {
            'uz': 'Hozircha rejalashtirilgan tadbirlar yo\'q.',
            'ru': 'Пока нет запланированных мероприятий.',
            'en': 'No scheduled events yet.'
        }
        text += more_texts.get(lang, more_texts['uz'])

    text += '\n📱 @tiuofficial'

    await message.answer(
        text,
        reply_markup=get_news_submenu_keyboard(user_id)
    )


def register_news_handlers(dp: Dispatcher):
    dp.register_message_handler(
        news_menu_handler,
        lambda message: message.text in ['📰 Yangiliklar', '📰 Новости', '📰 News']
    )
    dp.register_message_handler(
        latest_news_handler,
        lambda message: message.text in [
            '🆕 So\'nggi yangiliklar',
            '🆕 Последние новости',
            '🆕 Latest news'
        ]
    )
    dp.register_message_handler(
        video_news_handler,
        lambda message: message.text in [
            '🎥 Video yangiliklar',
            '🎥 Видео новости',
            '🎥 Video news'
        ]
    )
    dp.register_message_handler(
        events_calendar_handler,
        lambda message: message.text in [
            '🗓 Tadbirlar taqvimi',
            '🗓 Календарь мероприятий',
            '🗓 Events calendar'
        ]
    )
