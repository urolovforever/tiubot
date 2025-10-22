from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_admin_keyboard, get_cancel_keyboard, get_events_keyboard
from database.db import Database
from states.forms import AdminReplyState, EventCreateState, EventDeleteState
from utils.helpers import t, is_admin
import logging

db = Database()
logger = logging.getLogger(__name__)


async def admin_panel_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    await state.finish()

    await message.answer(
        t(user_id, 'admin_panel'),
        reply_markup=get_admin_keyboard(user_id)
    )


async def view_applications_handler(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    applications = db.get_new_applications()

    if not applications:
        await message.answer(
            t(user_id, 'no_new_applications'),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    for app in applications:
        text = f'''📬 Murojaat #{app[0]}

👤 Foydalanuvchi:
  • Ism: {app[3]}
  • Username: @{app[2] if app[2] else "yo'q"}
  • Telefon: {app[4]}
  • ID: {app[1]}
  • Link: tg://user?id={app[1]}

💬 Murojaat:
{app[5]}

📅 Sana: {app[8]}

📌 Javob: /reply_{app[0]}'''

        if app[6]:
            try:
                await message.answer_photo(app[6], caption=text)
            except:
                await message.answer_document(app[6], caption=text)
        else:
            await message.answer(text)


async def reply_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    try:
        app_id = int(message.text.split('_')[1])
        await state.update_data(app_id=app_id)

        await message.answer(
            t(user_id, 'reply_to_application'),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await AdminReplyState.waiting_for_reply.set()
    except:
        pass


async def process_admin_reply(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'admin_panel'),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    data = await state.get_data()
    app_id = data.get('app_id')
    response = message.text

    app = db.get_application(app_id)

    if app:
        db.update_application_response(app_id, response)

        response_text = f'''✅ Murojaatingizga javob keldi!

Sizning murojaat #{app_id}:
{app[5]}

💬 Javob:
{response}'''

        try:
            await message.bot.send_message(app[1], response_text)
            await message.answer(
                t(user_id, 'response_sent'),
                reply_markup=get_admin_keyboard(user_id)
            )
        except Exception as e:
            logger.error(f'Error sending response: {e}')
            await message.answer(
                f'❌ Xatolik: Foydalanuvchiga javob yuborib bo\'lmadi',
                reply_markup=get_admin_keyboard(user_id)
            )

    await state.finish()


async def add_event_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    await message.answer(
        t(user_id, 'enter_event_title'),
        reply_markup=get_cancel_keyboard(user_id)
    )
    await EventCreateState.waiting_for_title.set()


async def process_event_title(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'admin_panel'),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    await state.update_data(title=message.text)
    await message.answer(t(user_id, 'enter_event_description'))
    await EventCreateState.waiting_for_description.set()


async def process_event_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(description=message.text)
    await message.answer(t(user_id, 'enter_event_date'))
    await EventCreateState.waiting_for_date.set()


async def process_event_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(date=message.text)
    await message.answer(t(user_id, 'enter_event_location'))
    await EventCreateState.waiting_for_location.set()


async def process_event_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(location=message.text)
    await message.answer(t(user_id, 'send_event_image'))
    await EventCreateState.waiting_for_image.set()


async def process_event_image(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    image_id = None

    if message.photo:
        image_id = message.photo[-1].file_id
    elif message.document:
        image_id = message.document.file_id
    elif message.text and message.text.lower() in ['skip', 'yo\'q', 'нет', 'no']:
        image_id = None

    data = await state.get_data()

    db.create_event(
        data['title'],
        data['description'],
        data['date'],
        data['location'],
        image_id
    )

    await message.answer(
        t(user_id, 'event_created'),
        reply_markup=get_admin_keyboard(user_id)
    )
    await state.finish()


async def manage_events_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    events = db.get_all_events()

    if not events:
        await message.answer(
            t(user_id, 'no_events'),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    await message.answer(
        t(user_id, 'choose_event_to_delete'),
        reply_markup=get_events_keyboard(user_id, events)
    )
    await EventDeleteState.waiting_for_event_choice.set()


async def process_event_delete(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await state.finish()
        await message.answer(
            t(user_id, 'admin_panel'),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    try:
        event_id = int(message.text.split('.')[0])
        db.delete_event(event_id)

        await message.answer(
            t(user_id, 'event_deleted'),
            reply_markup=get_admin_keyboard(user_id)
        )
    except:
        pass

    await state.finish()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_panel_handler,
        lambda message: message.text in ['👨‍💼 Admin panel', '👨‍💼 Админ панель'],
        state='*'
    )
    dp.register_message_handler(
        view_applications_handler,
        lambda message: message.text in ['📬 Murojaatlar', '📬 Обращения'] and is_admin(message.from_user.id)
    )
    dp.register_message_handler(
        reply_command_handler,
        lambda message: message.text.startswith('/reply_'),
        state='*'
    )
    dp.register_message_handler(process_admin_reply, state=AdminReplyState.waiting_for_reply)
    dp.register_message_handler(
        add_event_handler,
        lambda message: message.text in ['➕ Tadbir qo\'shish', '➕ Добавить мероприятие'] and is_admin(
            message.from_user.id),
        state='*'
    )
    dp.register_message_handler(process_event_title, state=EventCreateState.waiting_for_title)
    dp.register_message_handler(process_event_description, state=EventCreateState.waiting_for_description)
    dp.register_message_handler(process_event_date, state=EventCreateState.waiting_for_date)
    dp.register_message_handler(process_event_location, state=EventCreateState.waiting_for_location)
    dp.register_message_handler(
        process_event_image,
        content_types=['text', 'photo', 'document'],
        state=EventCreateState.waiting_for_image
    )
    dp.register_message_handler(
        manage_events_handler,
        lambda message: message.text in ['📝 Tadbirlarni boshqarish', '📝 Управление мероприятиями'] and is_admin(
            message.from_user.id),
        state='*'
    )
    dp.register_message_handler(process_event_delete, state=EventDeleteState.waiting_for_event_choice)