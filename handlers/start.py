from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_main_keyboard
from database.db import Database
from utils.helpers import t

db = Database()


async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''
    full_name = message.from_user.full_name

    await state.finish()
    db.save_user(user_id, username, full_name)

    await message.answer(
        t(user_id, 'welcome'),
        reply_markup=get_main_keyboard(user_id)
    )


async def back_to_main_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.finish()

    await message.answer(
        t(user_id, 'main_menu'),
        reply_markup=get_main_keyboard(user_id)
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(
        back_to_main_handler,
        lambda message: message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back'],
        state='*'
    )
