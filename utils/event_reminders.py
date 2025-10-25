"""
Event Reminder System

This module handles sending reminders to users about upcoming events:
- 1 day before the event
- 1 hour before the event
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List
from aiogram import Bot
from database.db import Database
from utils.helpers import t

logger = logging.getLogger(__name__)


async def send_event_reminders(bot: Bot):
    """
    Send reminders for upcoming events
    Checks for events happening in 24 hours and 1 hour
    """
    db = Database()

    try:
        # Get events needing 1-day reminders (between 23-25 hours from now)
        events_1day = db.get_events_needing_reminders(24)

        for event in events_1day:
            await send_reminder_to_all_users(bot, db, event, '1day')

        # Get events needing 1-hour reminders (between 55 minutes - 65 minutes from now)
        events_1hour = db.get_events_needing_reminders(1)

        for event in events_1hour:
            await send_reminder_to_all_users(bot, db, event, '1hour')

    except Exception as e:
        logger.error(f"Error sending event reminders: {e}")


async def send_reminder_to_all_users(bot: Bot, db: Database, event: tuple, reminder_type: str):
    """
    Send a reminder about an event to all users who haven't received it yet

    Args:
        bot: Telegram Bot instance
        db: Database instance
        event: Event tuple from database
        reminder_type: '1day' or '1hour'
    """
    # Parse event data
    # event structure: (id, title, description, date, time, location, registration_link, image_id, created_at)
    event_id = event[0]
    title = event[1]
    description = event[2]
    date = event[3]
    time = event[4] if event[4] else "TBA"
    location = event[5]
    registration_link = event[6]
    image_id = event[7]

    # Get all users
    users = db.get_all_users()

    sent_count = 0
    failed_count = 0

    for user_id in users:
        try:
            # Check if reminder was already sent to this user
            if db.check_reminder_sent(event_id, user_id, reminder_type):
                continue

            # Get user's language
            lang = db.get_user_language(user_id)

            # Prepare reminder message
            if reminder_type == '1day':
                message_key = 'event_reminder_1day'
            else:
                message_key = 'event_reminder_1hour'

            # Format the reminder message
            reminder_text = t(user_id, message_key).format(
                title=title,
                location=location,
                time=time
            )

            # Add registration link if available
            if registration_link:
                link_text = {
                    'uz': f"\n\n🔗 Ro'yxatdan o'tish: {registration_link}",
                    'ru': f"\n\n🔗 Регистрация: {registration_link}",
                    'en': f"\n\n🔗 Registration: {registration_link}"
                }
                reminder_text += link_text.get(lang, link_text['uz'])

            # Send reminder
            if image_id:
                await bot.send_photo(
                    user_id,
                    photo=image_id,
                    caption=reminder_text
                )
            else:
                await bot.send_message(
                    user_id,
                    reminder_text
                )

            # Mark reminder as sent
            db.save_reminder(event_id, user_id, reminder_type)
            sent_count += 1

            # Small delay to avoid hitting rate limits
            await asyncio.sleep(0.05)

        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to send reminder to user {user_id}: {e}")

    logger.info(f"Event reminder sent: {event_id} ({reminder_type}) - Success: {sent_count}, Failed: {failed_count}")


async def start_reminder_scheduler(bot: Bot, interval_minutes: int = 30):
    """
    Start background task that checks and sends event reminders periodically

    Args:
        bot: Telegram Bot instance
        interval_minutes: How often to check for reminders (default: 30 minutes)
    """
    logger.info(f"Event reminder scheduler started (checking every {interval_minutes} minutes)")

    while True:
        try:
            await send_event_reminders(bot)
            await asyncio.sleep(interval_minutes * 60)  # Convert minutes to seconds
        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying


def format_event_datetime(date_str: str, time_str: str = None) -> datetime:
    """
    Parse date and time strings to datetime object

    Args:
        date_str: Date string (e.g., "15.02.2025" or "2025-02-15")
        time_str: Time string (e.g., "10:00" or "10:00 - 16:00")

    Returns:
        datetime object
    """
    try:
        # Parse date
        if '.' in date_str:
            # Format: DD.MM.YYYY
            day, month, year = date_str.split('.')
            date_obj = datetime(int(year), int(month), int(day))
        elif '-' in date_str:
            # Format: YYYY-MM-DD
            year, month, day = date_str.split('-')
            date_obj = datetime(int(year), int(month), int(day))
        else:
            logger.error(f"Invalid date format: {date_str}")
            return None

        # Parse time if provided
        if time_str:
            # Extract first time if range is given (e.g., "10:00 - 16:00" -> "10:00")
            if '-' in time_str:
                time_str = time_str.split('-')[0].strip()

            if ':' in time_str:
                hour, minute = time_str.split(':')
                date_obj = date_obj.replace(hour=int(hour), minute=int(minute))

        return date_obj

    except Exception as e:
        logger.error(f"Error parsing datetime: {e}")
        return None
