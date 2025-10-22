from aiogram import types, Dispatcher
from keyboards.reply import get_settings_keyboard, get_language_keyboard, get_main_keyboard
from database.db import Database
from utils.helpers import t

db = Database()


async def settings_handler(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        t(user_id, 'settings_menu'),
        reply_markup=get_settings_keyboard(user_id)
    )


async def change_language_handler(message: types.Message):
    await message.answer(
        '🌐 Tilni tanlang / Выберите язык / Choose language:',
        reply_markup=get_language_keyboard()
    )


async def language_selected_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    language_map = {
        '🇺🇿 O\'zbek': 'uz',
        '🇷🇺 Русский': 'ru',
        '🇬🇧 English': 'en'
    }

    new_lang = language_map.get(text)
    if new_lang:
        db.update_user_language(user_id, new_lang)
        await message.answer(
            t(user_id, 'language_changed'),
            reply_markup=get_main_keyboard(user_id)
        )


def register_settings_handlers(dp: Dispatcher):
    dp.register_message_handler(
        settings_handler,
        lambda message: message.text in ['⚙️ Sozlamalar', '⚙️ Настройки', '⚙️ Settings']
    )
    dp.register_message_handler(
        change_language_handler,
        lambda message: message.text in ['🌐 Tilni o\'zgartirish', '🌐 Изменить язык', '🌐 Change Language']
    )
    dp.register_message_handler(
        language_selected_handler,
        lambda message: message.text in ['🇺🇿 O\'zbek', '🇷🇺 Русский', '🇬🇧 English']
    )
