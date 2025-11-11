from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import (get_admin_keyboard, get_cancel_keyboard, get_events_keyboard,
                             get_main_keyboard, get_statistics_keyboard,
                             get_skip_keyboard)
# get_broadcast_confirm_keyboard endi ishlatilmaydi
from database.db import Database, get_tashkent_now
from states.forms import AdminReplyState, EventCreateState, EventDeleteState
# BroadcastState endi universal_broadcast.py da ishlatiladi
from utils.helpers import t, is_admin
from datetime import datetime
from config import ADMIN_IDS
import logging
import asyncio

db = Database()
logger = logging.getLogger(__name__)


# ==================== ADMIN PANEL ASOSIY ====================

async def admin_panel_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    await state.finish()

    lang = db.get_user_language(user_id)
    texts = {
        'uz': '👨‍💼 Admin panel\n\nKerakli bo\'limni tanlang:',
        'ru': '👨‍💼 Админ панель\n\nВыберите нужный раздел:',
        'en': '👨‍💼 Admin Panel\n\nChoose the section:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admin_keyboard(user_id)
    )


# ==================== YANGI MUROJAATLAR ====================

async def view_new_applications_handler(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    applications = db.get_new_applications()

    if not applications:
        lang = db.get_user_language(user_id)
        texts = {
            'uz': '📭 Yangi murojaatlar yo\'q',
            'ru': '📭 Новых обращений нет',
            'en': '📭 No new applications'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    await message.answer(f'📬 Yangi murojaatlar: {len(applications)} ta\n\n')

    for app in applications:
        text = f'''📬 Murojaat #{app[0]}
🆕 Status: Yangi

👤 Foydalanuvchi:
  • Ism: {app[3]}
  • Username: @{app[2] if app[2] else "yo'q"}
  • Telefon: {app[4]}
  • Link: tg://user?id={app[1]}

💬 Murojaat:
{app[5]}

📅 Sana: {app[8]}

📌 Javob berish: /reply_{app[0]}'''

        if app[6]:  # file_id
            try:
                await message.answer_photo(app[6], caption=text)
            except:
                try:
                    await message.answer_document(app[6], caption=text)
                except:
                    await message.answer(text)
        else:
            await message.answer(text)

        await asyncio.sleep(0.3)  # Spam oldini olish


# ==================== JAVOB BERILGAN MUROJAATLAR ====================

async def view_answered_applications_handler(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    # Oxirgi 7 kunlik murojaatlarni olish
    applications = db.get_answered_applications(days=7)

    if not applications:
        lang = db.get_user_language(user_id)
        texts = {
            'uz': '📭 Oxirgi 7 kunda javob berilgan murojaatlar yo\'q',
            'ru': '📭 Нет отвеченных обращений за последние 7 дней',
            'en': '📭 No answered applications in the last 7 days'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    await message.answer(f'✅ Javob berilgan murojaatlar (oxirgi 7 kun): {len(applications)} ta\n\n')

    for app in applications[:20]:  # Oxirgi 20 ta
        text = f'''📬 Murojaat #{app[0]}
✅ Status: Javob berilgan

👤 Foydalanuvchi:
  • Ism: {app[3]}
  • Telefon: {app[4]}
  • ID: {app[1]}

💬 Murojaat:
{app[5]}

💬 Javob:
{app[9] if app[9] else "Yo'q"}

📅 Sana: {app[8]}'''

        await message.answer(text)
        await asyncio.sleep(0.3)


# ==================== MUROJAATGA JAVOB BERISH ====================

async def reply_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    try:
        app_id = int(message.text.split('_')[1])

        # Murojaat mavjudligini tekshirish
        app = db.get_application(app_id)
        if not app:
            await message.answer('❌ Murojaat topilmadi')
            return

        await state.update_data(app_id=app_id)

        lang = db.get_user_language(user_id)
        texts = {
            'uz': f'💬 Murojaat #{app_id} uchun javob yozing:',
            'ru': f'💬 Напишите ответ для обращения #{app_id}:',
            'en': f'💬 Write reply for application #{app_id}:'
        }

        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await AdminReplyState.waiting_for_reply.set()
    except Exception as e:
        logger.error(f'Error in reply command: {e}')
        await message.answer('❌ Xatolik yuz berdi')


async def process_admin_reply(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            '❌ Bekor qilindi',
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    data = await state.get_data()
    app_id = data.get('app_id')
    response = message.text

    app = db.get_application(app_id)

    if app:
        # Update database
        db.update_application_response(app_id, response)

        # Foydalanuvchiga xabar yuborish
        user_lang = db.get_user_language(app[1])

        response_texts = {
            'uz': f'''✅ Murojaatingizga javob keldi!

📬 Sizning murojaat #{app_id}:
{app[5]}

💬 Javob:
{response}

📅 {get_tashkent_now().strftime("%Y-%m-%d %H:%M")}''',

            'ru': f'''✅ Получен ответ на ваше обращение!

📬 Ваше обращение #{app_id}:
{app[5]}

💬 Ответ:
{response}

📅 {get_tashkent_now().strftime("%Y-%m-%d %H:%M")}''',

            'en': f'''✅ Response received for your application!

📬 Your application #{app_id}:
{app[5]}

💬 Response:
{response}

📅 {get_tashkent_now().strftime("%Y-%m-%d %H:%M")}'''
        }

        try:
            await message.bot.send_message(
                app[1],
                response_texts.get(user_lang, response_texts['uz'])
            )

            await message.answer(
                f'✅ Javob yuborildi!\n\nMurojaat #{app_id} holati "Javob berilgan" ga o\'zgartirildi',
                reply_markup=get_admin_keyboard(user_id)
            )
        except Exception as e:
            logger.error(f'Error sending response to user: {e}')
            await message.answer(
                f'❌ Xatolik: Foydalanuvchiga javob yuborib bo\'lmadi\n\nLekin javob database\'ga saqlandi',
                reply_markup=get_admin_keyboard(user_id)
            )
    else:
        await message.answer(
            '❌ Murojaat topilmadi',
            reply_markup=get_admin_keyboard(user_id)
        )

    await state.finish()


# ==================== STATISTIKA ====================

async def statistics_handler(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    lang = db.get_user_language(user_id)
    texts = {
        'uz': '📊 Statistika\n\nDavrni tanlang:',
        'ru': '📊 Статистика\n\nВыберите период:',
        'en': '📊 Statistics\n\nChoose period:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_statistics_keyboard(user_id)
    )


async def show_weekly_statistics(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    stats = db.get_statistics('week')

    text = f'''📊 Haftalik statistika (oxirgi 7 kun)

👥 Yangi foydalanuvchilar: {stats.get('new_users', 0)}
📬 Yangi murojaatlar: {stats.get('new_applications', 0)}
✅ Javob berilgan: {stats.get('answered', 0)}
⏳ Kutilmoqda: {stats.get('pending', 0)}

📈 Umumiy:
👥 Jami foydalanuvchilar: {stats.get('total_users', 0)}
📬 Jami murojaatlar: {stats.get('total_applications', 0)}

📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}'''

    await message.answer(text, reply_markup=get_admin_keyboard(user_id))


async def show_monthly_statistics(message: types.Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    stats = db.get_statistics('month')

    text = f'''📊 Oylik statistika (oxirgi 30 kun)

👥 Yangi foydalanuvchilar: {stats.get('new_users', 0)}
📬 Yangi murojaatlar: {stats.get('new_applications', 0)}
✅ Javob berilgan: {stats.get('answered', 0)}
⏳ Kutilmoqda: {stats.get('pending', 0)}

📈 Umumiy:
👥 Jami foydalanuvchilar: {stats.get('total_users', 0)}
📬 Jami murojaatlar: {stats.get('total_applications', 0)}

📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}'''

    await message.answer(text, reply_markup=get_admin_keyboard(user_id))


# ==================== BROADCAST ====================
# ESKI BUTTON-BASED BROADCAST O'CHIRILDI
# Endi /broadcast komandasi ishlatiladi (universal_broadcast.py)
# Eski handler'lar git history'dan topish mumkin


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
    await message.answer(t(user_id, 'enter_event_time'))
    await EventCreateState.waiting_for_time.set()


async def process_event_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(time=message.text)
    await message.answer(t(user_id, 'enter_event_location'))
    await EventCreateState.waiting_for_location.set()


async def process_event_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(location=message.text)
    await message.answer(
        t(user_id, 'enter_event_registration_link'),
        reply_markup=get_skip_keyboard(user_id)
    )
    await EventCreateState.waiting_for_registration_link.set()


async def process_event_registration_link(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Check if user wants to skip
    if message.text in ['⏭ O\'tkazib yuborish', '⏭ Пропустить', '⏭ Skip']:
        await state.update_data(registration_link=None)
    else:
        await state.update_data(registration_link=message.text)

    await message.answer(
        t(user_id, 'send_event_image'),
        reply_markup=get_skip_keyboard(user_id)
    )
    await EventCreateState.waiting_for_image.set()


async def process_event_image(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    image_id = None

    if message.photo:
        image_id = message.photo[-1].file_id
    elif message.document:
        image_id = message.document.file_id
    elif message.text and (message.text.lower() in ['skip', 'yo\'q', 'нет', 'no'] or
                          message.text in ['⏭ O\'tkazib yuborish', '⏭ Пропустить', '⏭ Skip']):
        image_id = None

    data = await state.get_data()

    # Create event with new fields
    db.create_event(
        title=data['title'],
        description=data['description'],
        date=data['date'],
        location=data['location'],
        image_id=image_id,
        time=data.get('time'),
        registration_link=data.get('registration_link')
    )

    await message.answer(
        t(user_id, 'event_created'),
        reply_markup=get_admin_keyboard(user_id)
    )
    await state.finish()


async def manage_events_handler(message: types.Message, state: FSMContext):
    """Admin event management - shows inline keyboard with edit/delete options"""
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

    from keyboards.inline import get_admin_events_keyboard

    await message.answer(
        t(user_id, 'manage_events_title'),
        reply_markup=get_admin_events_keyboard(events)
    )


# Event edit callback handlers
# EDIT FUNKSIYASI O'CHIRILDI - FAQAT DELETE QOLDIRILDI
# async def edit_event_callback(callback: types.CallbackQuery, state: FSMContext):
#     """Handle edit event button click"""
#     user_id = callback.from_user.id
#
#     if not is_admin(user_id):
#         await callback.answer("❌ Ruxsat yo'q")
#         return
#
#     try:
#         event_id = int(callback.data.split('_')[-1])
#         from keyboards.inline import get_event_edit_options_keyboard
#
#         await callback.message.edit_text(
#             t(user_id, 'choose_field_to_edit'),
#             reply_markup=get_event_edit_options_keyboard(event_id)
#         )
#     except Exception as e:
#         await callback.answer(f"❌ Xatolik: {str(e)}")
#
#     await callback.answer()


async def delete_event_callback(callback: types.CallbackQuery):
    """Handle delete event button click - show confirmation"""
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer("❌ Ruxsat yo'q")
        return

    try:
        event_id = int(callback.data.split('_')[-1])
        event = db.get_event(event_id)

        if not event:
            await callback.answer(t(user_id, 'event_not_found'))
            return

        from keyboards.inline import get_delete_confirm_keyboard

        await callback.message.edit_text(
            f"{t(user_id, 'confirm_delete_event')}\n\n<b>{event[1]}</b>",
            parse_mode='HTML',
            reply_markup=get_delete_confirm_keyboard(event_id)
        )
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {str(e)}")

    await callback.answer()


async def confirm_delete_event_callback(callback: types.CallbackQuery):
    """Confirm and delete the event"""
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer("❌ Ruxsat yo'q")
        return

    try:
        event_id = int(callback.data.split('_')[-1])
        db.delete_event(event_id)

        await callback.message.edit_text(
            t(user_id, 'event_deleted')
        )
        await callback.answer("✅ O'chirildi")
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {str(e)}")


async def admin_back_callback(callback: types.CallbackQuery):
    """Handle admin back button"""
    user_id = callback.from_user.id

    await callback.message.delete()
    await callback.message.answer(
        t(user_id, 'admin_panel'),
        reply_markup=get_admin_keyboard(user_id)
    )
    await callback.answer()


async def admin_manage_events_callback(callback: types.CallbackQuery):
    """Go back to manage events list"""
    user_id = callback.from_user.id

    events = db.get_all_events()

    if not events:
        await callback.message.edit_text(t(user_id, 'no_events'))
        await callback.answer()
        return

    from keyboards.inline import get_admin_events_keyboard

    await callback.message.edit_text(
        t(user_id, 'manage_events_title'),
        reply_markup=get_admin_events_keyboard(events)
    )
    await callback.answer()


# EDIT FUNKSIYALARI O'CHIRILDI - FAQAT DELETE QOLDIRILDI
# async def edit_field_callback(callback: types.CallbackQuery, state: FSMContext):
#     """Handle field edit button click"""
#     user_id = callback.from_user.id
#
#     if not is_admin(user_id):
#         await callback.answer("❌ Ruxsat yo'q")
#         return
#
#     # Parse callback data: edit_<field>_<event_id>
#     parts = callback.data.split('_')
#     field = parts[1]
#     event_id = int(parts[2])
#
#     # Store event_id and field in state
#     await state.update_data(event_id=event_id, field=field)
#
#     # Get field name in user's language
#     field_names = {
#         'title': 'nomini',
#         'desc': 'tavsifini',
#         'date': 'sanasini',
#         'time': 'vaqtini',
#         'location': 'manzilini',
#         'link': 'havolasini',
#         'image': 'rasmini'
#     }
#
#     await callback.message.edit_text(
#         f"Tadbirning {field_names.get(field, field)} yangi qiymatini kiriting:",
#         reply_markup=get_cancel_keyboard(user_id)
#     )
#
#     from states.forms import EventEditState
#     await EventEditState.waiting_for_field_value.set()
#     await callback.answer()
#
#
# async def process_field_edit(message: types.Message, state: FSMContext):
#     """Process the new field value"""
#     user_id = message.from_user.id
#
#     if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
#         await state.finish()
#         await message.answer(
#             t(user_id, 'admin_panel'),
#             reply_markup=get_admin_keyboard(user_id)
#         )
#         return
#
#     data = await state.get_data()
#     event_id = data.get('event_id')
#     field = data.get('field')
#
#     # Get current event data
#     event = db.get_event(event_id)
#     if not event:
#         await message.answer(t(user_id, 'event_not_found'))
#         await state.finish()
#         return
#
#     # Update the specific field
#     if field == 'title':
#         db.update_event(event_id, message.text, event[2], event[3], event[4], event[5], event[6], event[7])
#     elif field == 'desc':
#         db.update_event(event_id, event[1], message.text, event[3], event[4], event[5], event[6], event[7])
#     elif field == 'date':
#         db.update_event(event_id, event[1], event[2], message.text, event[4], event[5], event[6], event[7])
#     elif field == 'time':
#         db.update_event(event_id, event[1], event[2], event[3], message.text, event[5], event[6], event[7])
#     elif field == 'location':
#         db.update_event(event_id, event[1], event[2], event[3], event[4], message.text, event[6], event[7])
#     elif field == 'link':
#         db.update_event(event_id, event[1], event[2], event[3], event[4], event[5], message.text, event[7])
#     elif field == 'image':
#         if message.photo:
#             image_id = message.photo[-1].file_id
#             db.update_event(event_id, event[1], event[2], event[3], event[4], event[5], event[6], image_id)
#         elif message.document:
#             image_id = message.document.file_id
#             db.update_event(event_id, event[1], event[2], event[3], event[4], event[5], event[6], image_id)
#
#     await message.answer(
#         "✅ Tadbir yangilandi!",
#         reply_markup=get_admin_keyboard(user_id)
#     )
#     await state.finish()


def register_admin_handlers(dp: Dispatcher):
    # Admin panel asosiy
    dp.register_message_handler(
        admin_panel_handler,
        lambda message: message.text in ['👨‍💼 Admin panel', '👨‍💼 Админ панель', '👨‍💼 Admin Panel'],
        state='*'
    )

    # Yangi murojaatlar
    dp.register_message_handler(
        view_new_applications_handler,
        lambda message: message.text in ['📬 Yangi murojaatlar', '📬 Новые обращения', '📬 New Applications'] and is_admin(
            message.from_user.id)
    )

    # Javob berilgan murojaatlar
    dp.register_message_handler(
        view_answered_applications_handler,
        lambda message: message.text in ['✅ Javob berilganlar', '✅ Отвеченные', '✅ Answered'] and is_admin(
            message.from_user.id)
    )

    # Murojaatga javob
    dp.register_message_handler(
        reply_command_handler,
        lambda message: message.text.startswith('/reply_'),
        state='*'
    )
    dp.register_message_handler(process_admin_reply, state=AdminReplyState.waiting_for_reply)

    # Statistika
    dp.register_message_handler(
        statistics_handler,
        lambda message: message.text in ['📊 Statistika', '📊 Статистика', '📊 Statistics'] and is_admin(
            message.from_user.id)
    )
    dp.register_message_handler(
        show_weekly_statistics,
        lambda message: message.text in ['📅 Haftalik', '📅 Недельная', '📅 Weekly'] and is_admin(message.from_user.id)
    )
    dp.register_message_handler(
        show_monthly_statistics,
        lambda message: message.text in ['📆 Oylik', '📆 Месячная', '📆 Monthly'] and is_admin(message.from_user.id)
    )

    # Broadcast - ESKI BUTTON-BASED METHOD O'CHIRILDI
    # Endi /broadcast komandasi ishlatiladi (universal_broadcast.py)
    # dp.register_message_handler(
    #     broadcast_start_handler,
    #     lambda message: message.text in ['📢 Broadcast', '📢 Рассылка'] and is_admin(message.from_user.id),
    #     state='*'
    # )
    # dp.register_message_handler(
    #     broadcast_process_message,
    #     content_types=['text', 'photo', 'video', 'document'],
    #     state=BroadcastState.waiting_for_content
    # )
    # dp.register_message_handler(
    #     broadcast_confirm,
    #     state=BroadcastState.waiting_for_confirmation
    # )

    dp.register_message_handler(process_admin_reply, state=AdminReplyState.waiting_for_reply)

    # ESKI USUL - O'CHIRILDI (event_quick_create.py ishlatiladi)
    # dp.register_message_handler(
    #     add_event_handler,
    #     lambda message: message.text in ['➕ Tadbir qo\'shish', '➕ Добавить мероприятие'] and is_admin(
    #         message.from_user.id),
    #     state='*'
    # )
    # dp.register_message_handler(process_event_title, state=EventCreateState.waiting_for_title)
    # dp.register_message_handler(process_event_description, state=EventCreateState.waiting_for_description)
    # dp.register_message_handler(process_event_date, state=EventCreateState.waiting_for_date)
    # dp.register_message_handler(process_event_time, state=EventCreateState.waiting_for_time)
    # dp.register_message_handler(process_event_location, state=EventCreateState.waiting_for_location)
    # dp.register_message_handler(process_event_registration_link, state=EventCreateState.waiting_for_registration_link)
    # dp.register_message_handler(
    #     process_event_image,
    #     content_types=['text', 'photo', 'document'],
    #     state=EventCreateState.waiting_for_image
    # )

    dp.register_message_handler(
        manage_events_handler,
        lambda message: message.text in ['📝 Tadbirlarni boshqarish', '📝 Управление мероприятиями'] and is_admin(
            message.from_user.id),
        state='*'
    )

    # Event delete callback handlers (Edit handlers o'chirildi)
    # dp.register_callback_query_handler(
    #     edit_event_callback,
    #     lambda c: c.data.startswith('edit_event_') and is_admin(c.from_user.id),
    #     state='*'
    # )
    dp.register_callback_query_handler(
        delete_event_callback,
        lambda c: c.data.startswith('delete_event_') and is_admin(c.from_user.id)
    )
    dp.register_callback_query_handler(
        confirm_delete_event_callback,
        lambda c: c.data.startswith('confirm_delete_') and is_admin(c.from_user.id)
    )
    dp.register_callback_query_handler(
        admin_back_callback,
        lambda c: c.data == 'admin_back' and is_admin(c.from_user.id)
    )
    dp.register_callback_query_handler(
        admin_manage_events_callback,
        lambda c: c.data == 'admin_manage_events' and is_admin(c.from_user.id)
    )
    # dp.register_callback_query_handler(
    #     edit_field_callback,
    #     lambda c: c.data.startswith('edit_') and not c.data.startswith('edit_event_') and is_admin(c.from_user.id),
    #     state='*'
    # )

    # Event edit state handler - O'CHIRILDI
    # from states.forms import EventEditState
    # dp.register_message_handler(
    #     process_field_edit,
    #     content_types=['text', 'photo', 'document'],
    #     state=EventEditState.waiting_for_field_value
    # )