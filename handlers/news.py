from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t
from keyboards.inline import get_events_inline_keyboard
from config import DIGEST_CHANNEL_ID
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

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


async def video_news_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''

Tashkent International Universityning rasmiy yangilik va e’lonlarini quyidagi platformalarda kuzatib boring:
''',
        'ru': '''

Следите за официальными новостями и объявлениями Tashkent International University на следующих платформах:
''',
        'en': '''

Follow the official news and announcements of Tashkent International University on the following platforms:
'''
    }

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Telegram", url="https://t.me/tiu_edu")],
        [InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/tiuofficial/")],
        [InlineKeyboardButton(text="Facebook", url="https://www.facebook.com/profile.php?id=100095487825640")],
        [InlineKeyboardButton(text="YouTube", url="https://www.youtube.com/@tiu_uz")],
        [InlineKeyboardButton(text="Twitter", url="https://x.com/tiuofficial_")],
        [InlineKeyboardButton(text="Web-site", url="http://www.tiu.uz/")]
    ])

    photo_path = "/home/nizomjon/PycharmProjects/Tiu_bot/photos/ck.jpg"  # Rasm joylashgan joy

    try:
        await message.answer_photo(
            photo=InputFile(photo_path),
            caption=texts.get(lang, texts['uz']),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    except:
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=keyboard,
            parse_mode="HTML"
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
            'uz': '📭 Hozircha rejalashtirilgan tadbirlar yo\'q.',
            'ru': '📭 Пока нет запланированных мероприятий.',
            'en': '📭 No scheduled events yet.'
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

    dp.register_message_handler(
        weekly_digest_handler,
        lambda message: message.text in [
            '🆕 Hafta dayjesti',
            '🆕 Недельный дайджест',
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

    dp.register_message_handler(
        events_calendar_handler,
        lambda message: message.text in [
            '🗓 Tadbirlar taqvimi',
            '🗓 Календарь мероприятий',
            '🗓 Events calendar'
        ]
    )

