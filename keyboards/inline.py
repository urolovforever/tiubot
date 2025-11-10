from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from datetime import datetime

db = Database()


def parse_event_date(date_str: str) -> str:
    """Parse event date and return formatted short version (e.g., '15.02')"""
    try:
        # Try to parse different date formats
        if '.' in date_str:
            parts = date_str.split('.')
            if len(parts) >= 2:
                day = parts[0].strip()
                month = parts[1].strip()
                return f"{day.zfill(2)}.{month.zfill(2)}"
        elif '-' in date_str:
            parts = date_str.split('-')
            if len(parts) >= 3:
                # Format: YYYY-MM-DD
                month = parts[1].strip()
                day = parts[2].strip()
                return f"{day.zfill(2)}.{month.zfill(2)}"
    except:
        pass

    # Return as is if parsing fails
    return date_str[:5] if len(date_str) > 5 else date_str


def get_event_emoji(title: str) -> str:
    """Get appropriate emoji based on event title"""
    title_lower = title.lower()

    if any(word in title_lower for word in ['ochiq', 'eshik', 'open', 'door']):
        return '🎓'
    elif any(word in title_lower for word in ['startup', 'tanlov', 'konkurs', 'contest']):
        return '🏆'
    elif any(word in title_lower for word in ['bayram', 'festival', 'celebration', 'yangi yil']):
        return '🎭'
    elif any(word in title_lower for word in ['sport', 'futbol', 'basketbol']):
        return '⚽'
    elif any(word in title_lower for word in ['konferensiya', 'seminar', 'conference']):
        return '📊'
    elif any(word in title_lower for word in ['konsert', 'musiqa', 'concert']):
        return '🎵'
    elif any(word in title_lower for word in ['ko\'rgazma', 'exhibition']):
        return '🖼'
    else:
        return '📅'


def get_events_inline_keyboard(events: list) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for events list
    Each button shows event title with date
    Format: 📅 11.12.2025 | Ochiq eshiklar kuni
    """
    keyboard = InlineKeyboardMarkup(row_width=1)

    for event in events:
        # event structure: (id, title, description, date, time, location, registration_link, image_id, created_at)
        event_id = event[0]
        title = event[1]
        date = event[3]  # DD.MM.YYYY formatida

        # Sana va nom bilan tugma yaratish
        display_title = f"📅 {date} | {title}"

        # Truncate if too long (max 60 chars for button)
        max_length = 60
        if len(display_title) > max_length:
            # Nomni qisqartirish, sanani saqlab qolish
            available_for_title = max_length - len(f"📅 {date} | ") - 3
            short_title = title[:available_for_title] + "..."
            display_title = f"📅 {date} | {short_title}"

        # Add button with callback data
        keyboard.add(
            InlineKeyboardButton(
                text=display_title,
                callback_data=f"event_{event_id}"
            )
        )

    return keyboard


def get_event_details_inline_keyboard(event_id: int, registration_link: str = None) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for event details
    Includes registration link if available and back button
    """
    keyboard = InlineKeyboardMarkup(row_width=1)

    # Add registration button if link is provided and valid
    if registration_link:
        # Validate URL: must be a single valid URL without emojis or spaces (except %20)
        link = registration_link.strip()
        # Check if it's a valid single URL (starts with http/https and no newlines/emojis)
        if (link.startswith('http://') or link.startswith('https://')) and '\n' not in link and len(link.split()) == 1:
            keyboard.add(
                InlineKeyboardButton(
                    text="🔗 Ro'yxatdan o'tish",
                    url=link
                )
            )

    # Back to events list button
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Orqaga",
            callback_data="back_to_events"
        )
    )

    return keyboard


def get_admin_events_keyboard(events: list) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for admin to manage events
    Shows: Event name and Delete button for each event
    """
    keyboard = InlineKeyboardMarkup(row_width=2)

    for event in events:
        event_id = event[0]
        title = event[1]

        # Truncate title
        display_title = title if len(title) <= 30 else title[:30] + '...'

        keyboard.row(
            InlineKeyboardButton(
                text=f"📅 {display_title}",
                callback_data=f"view_event_{event_id}"
            ),
            InlineKeyboardButton(
                text="🗑 O'chirish",
                callback_data=f"delete_event_{event_id}"
            )
        )

    # Back button
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Orqaga",
            callback_data="admin_back"
        )
    )

    return keyboard


# EDIT FUNKSIYASI O'CHIRILDI - FAQAT DELETE QOLDIRILDI
# def get_event_edit_options_keyboard(event_id: int) -> InlineKeyboardMarkup:
#     """Keyboard with options to edit different fields of an event"""
#     keyboard = InlineKeyboardMarkup(row_width=1)
#
#     keyboard.add(
#         InlineKeyboardButton(text="📝 Nomini o'zgartirish", callback_data=f"edit_title_{event_id}"),
#         InlineKeyboardButton(text="📄 Tavsifni o'zgartirish", callback_data=f"edit_desc_{event_id}"),
#         InlineKeyboardButton(text="📅 Sanani o'zgartirish", callback_data=f"edit_date_{event_id}"),
#         InlineKeyboardButton(text="⏰ Vaqtni o'zgartirish", callback_data=f"edit_time_{event_id}"),
#         InlineKeyboardButton(text="📍 Manzilni o'zgartirish", callback_data=f"edit_location_{event_id}"),
#         InlineKeyboardButton(text="🔗 Havolani o'zgartirish", callback_data=f"edit_link_{event_id}"),
#         InlineKeyboardButton(text="🖼 Rasmni o'zgartirish", callback_data=f"edit_image_{event_id}"),
#         InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_manage_events")
#     )
#
#     return keyboard


def get_delete_confirm_keyboard(event_id: int) -> InlineKeyboardMarkup:
    """Confirmation keyboard for deleting an event"""
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm_delete_{event_id}"),
        InlineKeyboardButton(text="❌ Yo'q", callback_data="admin_manage_events")
    )

    return keyboard