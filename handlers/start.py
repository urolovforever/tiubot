from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_main_keyboard, get_language_keyboard
from database.db import Database
from utils.helpers import t
from states.forms import OnboardingState

db = Database()


async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''
    full_name = message.from_user.full_name

    await state.finish()

    # Foydalanuvchi bazada bormi tekshirish
    existing_user = db.get_user(user_id)

    if existing_user is None:
        # Yangi foydalanuvchi - tilni so'raymiz
        # Foydalanuvchi ma'lumotlarini vaqtinchalik saqlaymiz (state da)
        await state.update_data(username=username, full_name=full_name)
        await OnboardingState.waiting_for_language.set()
        await message.answer(
            '👋 Assalomu aleykum! Tilni tanlang\n'
            '👋 Здравствуйте! Выберите язык\n'
            '👋 Hello! Choose your language',
            reply_markup=get_language_keyboard()
        )
    else:
        # Mavjud foydalanuvchi - oddiy welcome
        await message.answer(
            t(user_id, 'welcome'),
            reply_markup=get_main_keyboard(user_id)
        )


async def initial_language_selected(message: types.Message, state: FSMContext):
    """Yangi foydalanuvchi til tanlaganda"""
    user_id = message.from_user.id
    text = message.text

    language_map = {
        '🇺🇿 O\'zbek': 'uz',
        '🇷🇺 Русский': 'ru',
        '🇬🇧 English': 'en'
    }

    selected_lang = language_map.get(text)
    if selected_lang:
        # State dan foydalanuvchi ma'lumotlarini olish
        user_data = await state.get_data()
        username = user_data.get('username', '')
        full_name = user_data.get('full_name', '')

        # Foydalanuvchini tanlangan til bilan saqlash
        db.save_user(user_id, username, full_name, language=selected_lang)

        await state.finish()

        # Welcome xabarini tanlangan tilda ko'rsatish
        await message.answer(
            t(user_id, 'welcome'),
            reply_markup=get_main_keyboard(user_id)
        )
    else:
        # Noto'g'ri tanlash
        await message.answer(
            '❌ Iltimos, quyidagi tugmalardan birini tanlang\n'
            '❌ Пожалуйста, выберите одну из кнопок ниже\n'
            '❌ Please choose one of the buttons below',
            reply_markup=get_language_keyboard()
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
        initial_language_selected,
        state=OnboardingState.waiting_for_language
    )
    dp.register_message_handler(
        back_to_main_handler,
        lambda message: message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back'],
        state='*'
    )
