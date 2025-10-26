import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from database.db import Database

# Import all handler registration functions
from handlers.start import register_start_handlers
from handlers.settings import register_settings_handlers
from handlers.about import register_about_handlers
from handlers.contact import register_contact_handlers
from handlers.admission import register_admission_handlers
from handlers.students import register_students_handlers
from handlers.news import register_news_handlers
from handlers.schedule import register_schedule_handlers
from handlers.events import register_events_handlers
from handlers.event_quick_create import register_quick_event_handlers  # YANGI
from handlers.applications import register_applications_handlers
from handlers.library import register_library_handlers  # LIBRARY SYSTEM
from handlers.universal_broadcast import register_universal_broadcast_handlers  # UNIVERSAL BROADCAST
from handlers.channel_handler import register_channel_handlers  # CHANNEL POST TRACKER
from handlers.admin import register_admin_handlers

# Import event reminder system
from utils.event_reminders import start_reminder_scheduler

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Initialize database
db = Database()


def register_all_handlers(dp: Dispatcher):
    '''Register all handlers in correct order'''

    # Basic handlers (must be first)
    register_start_handlers(dp)
    register_settings_handlers(dp)

    # Main sections with submenus
    register_about_handlers(dp)
    register_contact_handlers(dp)
    register_admission_handlers(dp)
    register_students_handlers(dp)
    register_news_handlers(dp)

    # Complex handlers with FSM
    register_schedule_handlers(dp)
    register_events_handlers(dp)
    register_applications_handlers(dp)
    register_library_handlers(dp)  # LIBRARY SYSTEM - Kutubxona tizimi

    # Channel handlers (before admin to catch channel posts)
    register_channel_handlers(dp)  # CHANNEL POST TRACKER - Kanaldan postlarni saqlash

    # Admin handlers (must be last)
    register_quick_event_handlers(dp)  # YANGI - Tez tadbir qo'shish
    register_universal_broadcast_handlers(dp)  # UNIVERSAL BROADCAST - /broadcast command
    register_admin_handlers(dp)

    logger.info('✅ All handlers registered successfully')


async def on_startup(dp: Dispatcher):
    '''Actions on bot startup'''
    logger.info('🚀 Bot is starting...')
    logger.info(f'Bot name: {(await dp.bot.get_me()).full_name}')
    register_all_handlers(dp)

    # Start event reminder scheduler in background
    asyncio.create_task(start_reminder_scheduler(dp.bot, interval_minutes=30))
    logger.info('📅 Event reminder scheduler started')

    logger.info('✅ Bot started successfully!')


async def on_shutdown(dp: Dispatcher):
    '''Actions on bot shutdown'''
    logger.info('⏸ Bot is shutting down...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('✅ Bot stopped')


if __name__ == '__main__':
    try:
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )
    except KeyboardInterrupt:
        logger.info('Bot stopped by user')
    except Exception as e:
        logger.error(f'❌ Error starting bot: {e}')