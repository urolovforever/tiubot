from aiogram import types, Dispatcher
from keyboards.reply import get_back_keyboard
from utils.helpers import t

async def contact_handler(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        t(user_id, 'contact_text'),
        reply_markup=get_back_keyboard(user_id)
    )

def register_contact_handlers(dp: Dispatcher):
    dp.register_message_handler(
        contact_handler,
        lambda message: message.text in ['📞 Aloqa', '📞 Контакты', '📞 Contact']
    )
