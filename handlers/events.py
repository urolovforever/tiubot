from aiogram import types, Dispatcher
from keyboards.reply import get_events_keyboard, get_back_keyboard, get_main_keyboard
from database.db import Database
from utils.helpers import t

db = Database()


async def events_handler(message: types.Message):
    user_id = message.from_user.id

    events = db.get_all_events()

    if not events:
        await message.answer(
            t(user_id, 'no_events'),
            reply_markup=get_back_keyboard(user_id)
        )
        return

    await message.answer(
        t(user_id, 'events_list'),
        reply_markup=get_events_keyboard(user_id, events)
    )


async def event_details_handler(message: types.Message):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'main_menu'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    try:
        event_id = int(message.text.split('.')[0])
        event = db.get_event(event_id)

        if event:
            text = f'''📌 {t(user_id, 'event_details')}

📝 {event[1]}

📄 {event[2]}

📅 {event[3]}
📍 {event[4]}'''

            if event[5]:
                await message.answer_photo(
                    event[5],
                    caption=text,
                    reply_markup=get_back_keyboard(user_id)
                )
            else:
                await message.answer(
                    text,
                    reply_markup=get_back_keyboard(user_id)
                )
    except:
        pass


def register_events_handlers(dp: Dispatcher):
    dp.register_message_handler(
        events_handler,
        lambda message: message.text in ['📢 Tadbirlar', '📢 Мероприятия', '📢 Events']
    )
    dp.register_message_handler(
        event_details_handler,
        lambda message: message.text and (
                    message.text[0].isdigit() or message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back'])
    )