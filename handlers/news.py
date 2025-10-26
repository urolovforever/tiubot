from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t
from keyboards.inline import get_events_inline_keyboard
from config import DIGEST_CHANNEL_ID
import logging

db = Database()
logger = logging.getLogger(__name__)


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


async def weekly_digest_handler(message: types.Message):
    """
    Hafta dayjesti - kanaldagi eng so'nggi postni foydalanuvchiga yuborish
    """
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    try:
        # Database'dan eng so'nggi post message ID ni olish
        message_id = db.get_channel_post(DIGEST_CHANNEL_ID)

        # Agar post ID mavjud bo'lmasa
        if not message_id:
            error_texts = {
                'uz': '⚠️ Hozircha dayjest mavjud emas.',
                'ru': '⚠️ Дайджест пока недоступен.',
                'en': '⚠️ Digest is not available yet.'
            }
            await message.answer(
                error_texts.get(lang, error_texts['uz']),
                reply_markup=get_news_submenu_keyboard(user_id)
            )
            return

        # Postni copy qilib yuborish (forward emas!)
        await message.bot.copy_message(
            chat_id=user_id,
            from_chat_id=DIGEST_CHANNEL_ID,
            message_id=message_id
        )

        # Menyuni qayta yuborish
        await message.answer(
            "📱 @tiuofficial",
            reply_markup=get_news_submenu_keyboard(user_id)
        )

    except Exception as e:
        logger.error(f'Weekly digest error for user {user_id}: {e}')

        error_texts = {
            'uz': '⚠️ Hozircha dayjest mavjud emas.',
            'ru': '⚠️ Дайджест пока недоступен.',
            'en': '⚠️ Digest is not available yet.'
        }

        await message.answer(
            error_texts.get(lang, error_texts['uz']),
            reply_markup=get_news_submenu_keyboard(user_id)
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
        weekly_digest_handler,
        lambda message: message.text in [
            '📰 Hafta dayjesti',
            '📰 Недельный дайджест',
            '📰 Weekly digest'
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

