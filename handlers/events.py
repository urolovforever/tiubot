from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from keyboards.reply import get_back_keyboard, get_main_keyboard
from keyboards.inline import (
    get_events_inline_keyboard,
    get_event_details_inline_keyboard
)
from database.db import Database
from utils.helpers import t

db = Database()


async def events_handler(message: types.Message):
    """
    Main events handler - shows list of upcoming events
    Uses inline keyboard with event buttons
    """
    user_id = message.from_user.id

    # Get all upcoming events (sorted by date, nearest first)
    events = db.get_all_events(upcoming_only=True)

    if not events:
        await message.answer(
            t(user_id, 'no_events'),
            reply_markup=get_back_keyboard(user_id)
        )
        return

    # Show events list with inline keyboard
    await message.answer(
        t(user_id, 'events_calendar_title'),
        reply_markup=get_events_inline_keyboard(events)
    )


async def event_callback_handler(callback: CallbackQuery):
    """
    Handle event button clicks from inline keyboard
    Shows detailed information about the selected event
    """
    user_id = callback.from_user.id

    # Parse event_id from callback data
    try:
        event_id = int(callback.data.split('_')[1])
    except:
        await callback.answer("❌ Xatolik yuz berdi")
        return

    # Get event details
    event = db.get_event(event_id)

    if not event:
        await callback.answer(t(user_id, 'event_not_found'))
        return

    # Parse event data
    # event structure: (id, title, description, date, time, location, registration_link, image_id, created_at)
    event_id = event[0]
    title = event[1]
    description = event[2]
    date = event[3]
    time = event[4]
    location = event[5]
    registration_link = event[6]
    image_id = event[7]

    # Format event details in Telegram post style
    text = f"<b>{title}</b>\n\n"
    text += f"📝 <b>Tavsif:</b>\n{description}\n\n"
    text += f"📅 <b>Sana:</b> {date}\n"

    if time:
        text += f"⏰ <b>Vaqt:</b> {time}\n"

    text += f"📍 <b>Joylashuv:</b> {location}\n"

    if registration_link:
        text += f"\n🔗 <b>Ro'yxatdan o'tish:</b> <a href='{registration_link}'>Bu yerga bosing</a>\n"

    text += f"\n#TIUevents"

    # Send event details
    if image_id:
        # Send with image
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=image_id,
            caption=text,
            parse_mode='HTML',
            reply_markup=get_event_details_inline_keyboard(event_id, registration_link)
        )
    else:
        # Send without image
        await callback.message.delete()
        await callback.message.answer(
            text,
            parse_mode='HTML',
            reply_markup=get_event_details_inline_keyboard(event_id, registration_link)
        )

    await callback.answer()


async def back_to_events_handler(callback: CallbackQuery):
    """Handle back to events list button"""
    user_id = callback.from_user.id

    # Get all upcoming events
    events = db.get_all_events(upcoming_only=True)

    if not events:
        await callback.message.delete()
        await callback.message.answer(
            t(user_id, 'no_events'),
            reply_markup=get_back_keyboard(user_id)
        )
        await callback.answer()
        return

    # Show events list
    await callback.message.delete()
    await callback.message.answer(
        t(user_id, 'events_calendar_title'),
        reply_markup=get_events_inline_keyboard(events)
    )
    await callback.answer()


async def event_details_handler(message: types.Message):
    """
    Legacy handler for backward compatibility
    Redirects to main menu if user clicks back button
    """
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'main_menu'),
            reply_markup=get_main_keyboard(user_id)
        )
        return


def register_events_handlers(dp: Dispatcher):
    """Register all event-related handlers"""

    # Main events handler (button click)
    dp.register_message_handler(
        events_handler,
        lambda message: message.text in [
            '📅 Tadbirlar taqvimi',
            '📅 Календарь событий',
            '📅 Events Calendar',
            '📢 Tadbirlar',
            '📢 Мероприятия',
            '📢 Events'
        ]
    )

    # Callback query handlers
    dp.register_callback_query_handler(
        event_callback_handler,
        lambda c: c.data.startswith('event_')
    )

    dp.register_callback_query_handler(
        back_to_events_handler,
        lambda c: c.data == 'back_to_events'
    )

    # Legacy handler for back button
    dp.register_message_handler(
        event_details_handler,
        lambda message: message.text and message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']
    )