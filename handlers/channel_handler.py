"""
Channel post handler - kanaldagi postlarni kuzatish va saqlash
Bot kanalga admin sifatida qo'shilgan bo'lishi kerak
"""

from aiogram import types, Dispatcher
from database.db import Database
from config import DIGEST_CHANNEL_ID
import logging

db = Database()
logger = logging.getLogger(__name__)


async def channel_post_handler(message: types.Message):
    """
    Kanaldan kelgan yangi postlarni database'ga saqlash
    """
    try:
        channel_id = str(message.chat.id)

        # Faqat bizning kanal postlarini saqlash
        if channel_id == DIGEST_CHANNEL_ID:
            db.save_channel_post(channel_id, message.message_id)
            logger.info(f'Saved channel post: {message.message_id} from channel {channel_id}')

    except Exception as e:
        logger.error(f'Error handling channel post: {e}')


def register_channel_handlers(dp: Dispatcher):
    """
    Channel post handler'larini ro'yxatdan o'tkazish
    """
    # Kanal postlarini kuzatish
    dp.register_channel_post_handler(
        channel_post_handler,
        content_types=types.ContentTypes.ANY
    )
