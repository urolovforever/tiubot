"""
Universal Broadcast - Admin nima yuborsa shuni yuborish
Telegram'dagi kabi tabiiy: text, photo, video, audio, document, poll, sticker, va h.k.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from states.forms import BroadcastState
from utils.helpers import is_admin
from datetime import datetime
import asyncio
import logging

db = Database()
logger = logging.getLogger(__name__)


async def broadcast_command(message: types.Message, state: FSMContext):
    """
    /broadcast komandasi - Universal broadcast rejimini yoqish
    """
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.answer("❌ Sizda broadcast yuborish huquqi yo'q")
        return

    # Har qanday oldingi stateni tozalash
    await state.finish()

    # Foydalanuvchilar sonini ko'rsatish
    users = db.get_all_users()
    users_count = len(users)

    await message.answer(
        f"📢 <b>Broadcast rejimi yoqildi!</b>\n\n"
        f"Endi siz nima yuborsangiz, barcha foydalanuvchilarga yuboriladi:\n\n"
        f"📝 Matn\n"
        f"🖼️ Rasm (caption bilan yoki yo'qsiz)\n"
        f"🎥 Video (caption bilan yoki yo'qsiz)\n"
        f"📄 Fayl\n"
        f"🎵 Audio\n"
        f"🎬 Video xabar (круг)\n"
        f"🎤 Ovozli xabar\n"
        f"📊 So'rovnoma\n"
        f"📍 Joylashuv\n"
        f"📞 Kontakt\n"
        f"🎲 Dice/Dart emoji\n"
        f"🎨 Sticker\n"
        f"🎬 GIF/Animation\n\n"
        f"👥 <b>Jami foydalanuvchilar: {users_count} ta</b>\n\n"
        f"<i>Xabarni yuboring yoki /cancel tugating.</i>",
        parse_mode='HTML'
    )

    await BroadcastState.waiting_for_content.set()


async def broadcast_cancel(message: types.Message, state: FSMContext):
    """
    /cancel komandasi - Broadcast rejimini to'xtatish
    """
    await state.finish()
    await message.answer(
        "❌ <b>Broadcast bekor qilindi</b>\n\n"
        "Yangi broadcast uchun: /broadcast",
        parse_mode='HTML'
    )


async def broadcast_receive_content(message: types.Message, state: FSMContext):
    """
    Admin yuborgan har qanday content'ni qabul qilish
    Text, Photo, Video, Audio, Document, Poll, Sticker, Voice, Video Note, va h.k.
    """
    user_id = message.from_user.id

    # Content turini aniqlash va saqlash
    content_data = {
        'message_id': message.message_id,
        'chat_id': message.chat.id
    }

    # Har bir content type uchun ma'lumotlarni saqlash
    if message.text:
        content_data['type'] = 'text'
        content_data['text'] = message.text
        content_data['entities'] = message.entities
    elif message.photo:
        content_data['type'] = 'photo'
        content_data['photo'] = message.photo[-1].file_id
        content_data['caption'] = message.caption
        content_data['caption_entities'] = message.caption_entities
    elif message.video:
        content_data['type'] = 'video'
        content_data['video'] = message.video.file_id
        content_data['caption'] = message.caption
        content_data['caption_entities'] = message.caption_entities
    elif message.audio:
        content_data['type'] = 'audio'
        content_data['audio'] = message.audio.file_id
        content_data['caption'] = message.caption
        content_data['caption_entities'] = message.caption_entities
    elif message.document:
        content_data['type'] = 'document'
        content_data['document'] = message.document.file_id
        content_data['caption'] = message.caption
        content_data['caption_entities'] = message.caption_entities
    elif message.voice:
        content_data['type'] = 'voice'
        content_data['voice'] = message.voice.file_id
        content_data['caption'] = message.caption
    elif message.video_note:
        content_data['type'] = 'video_note'
        content_data['video_note'] = message.video_note.file_id
    elif message.sticker:
        content_data['type'] = 'sticker'
        content_data['sticker'] = message.sticker.file_id
    elif message.animation:
        content_data['type'] = 'animation'
        content_data['animation'] = message.animation.file_id
        content_data['caption'] = message.caption
        content_data['caption_entities'] = message.caption_entities
    elif message.poll:
        content_data['type'] = 'poll'
        content_data['poll'] = {
            'question': message.poll.question,
            'options': [opt.text for opt in message.poll.options],
            'is_anonymous': message.poll.is_anonymous,
            'allows_multiple_answers': message.poll.allows_multiple_answers,
            'type': message.poll.type
        }
    elif message.location:
        content_data['type'] = 'location'
        content_data['location'] = {
            'latitude': message.location.latitude,
            'longitude': message.location.longitude
        }
    elif message.contact:
        content_data['type'] = 'contact'
        content_data['contact'] = {
            'phone_number': message.contact.phone_number,
            'first_name': message.contact.first_name,
            'last_name': message.contact.last_name
        }
    elif message.dice:
        content_data['type'] = 'dice'
        content_data['dice'] = message.dice.emoji
    else:
        await message.answer(
            "❌ Bu xabar turini broadcast qilish mumkin emas.\n\n"
            "Yangi xabar yuboring yoki /cancel tugating."
        )
        return

    # Ma'lumotlarni saqlash
    await state.update_data(content_data=content_data)

    # Tasdiqlash uchun inline keyboard
    users_count = len(db.get_all_users())

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="✅ Yuborish", callback_data="broadcast_confirm"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast_cancel")
    )

    # Content type'ga qarab preview
    content_type_names = {
        'text': '📝 Matn',
        'photo': '🖼️ Rasm',
        'video': '🎥 Video',
        'audio': '🎵 Audio',
        'document': '📄 Fayl',
        'voice': '🎤 Ovozli xabar',
        'video_note': '🎬 Video xabar',
        'sticker': '🎨 Sticker',
        'animation': '🎬 GIF',
        'poll': '📊 So\'rovnoma',
        'location': '📍 Joylashuv',
        'contact': '📞 Kontakt',
        'dice': '🎲 Dice'
    }

    content_type_display = content_type_names.get(content_data['type'], content_data['type'])

    await message.answer(
        f"✅ <b>Xabar qabul qilindi!</b>\n\n"
        f"📌 Tur: {content_type_display}\n"
        f"👥 Qabul qiluvchilar: {users_count} ta\n\n"
        f"<i>Preview:</i>",
        parse_mode='HTML'
    )

    # Xabarni forward qilib ko'rsatish (eng aniq preview)
    try:
        await message.forward(message.chat.id)
    except:
        pass

    await message.answer(
        "Yuborishni tasdiqlaymi?",
        reply_markup=keyboard
    )

    await BroadcastState.waiting_for_confirmation.set()


async def broadcast_confirm_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Tasdiqlash callback - Broadcast yuborish
    """
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer("❌ Ruxsat yo'q")
        return

    data = await state.get_data()
    content_data = data.get('content_data')

    if not content_data:
        await callback.message.edit_text("❌ Xato: Content topilmadi")
        await state.finish()
        return

    # Yuborishni boshlash
    users = db.get_all_users()
    total = len(users)

    await callback.message.edit_text(
        f"📤 <b>Broadcast boshlanmoqda...</b>\n\n"
        f"👥 Jami: {total} ta\n"
        f"⏳ Kuting...",
        parse_mode='HTML'
    )

    success = 0
    failed = 0
    blocked = 0
    start_time = datetime.now()

    # Progress message
    progress_msg = await callback.message.answer("⏳ 0%")

    for idx, user_id_target in enumerate(users, 1):
        try:
            # Har bir content type uchun yuborish
            if content_data['type'] == 'text':
                await callback.bot.send_message(
                    user_id_target,
                    content_data['text'],
                    entities=content_data.get('entities')
                )
            elif content_data['type'] == 'photo':
                await callback.bot.send_photo(
                    user_id_target,
                    content_data['photo'],
                    caption=content_data.get('caption'),
                    caption_entities=content_data.get('caption_entities')
                )
            elif content_data['type'] == 'video':
                await callback.bot.send_video(
                    user_id_target,
                    content_data['video'],
                    caption=content_data.get('caption'),
                    caption_entities=content_data.get('caption_entities')
                )
            elif content_data['type'] == 'audio':
                await callback.bot.send_audio(
                    user_id_target,
                    content_data['audio'],
                    caption=content_data.get('caption'),
                    caption_entities=content_data.get('caption_entities')
                )
            elif content_data['type'] == 'document':
                await callback.bot.send_document(
                    user_id_target,
                    content_data['document'],
                    caption=content_data.get('caption'),
                    caption_entities=content_data.get('caption_entities')
                )
            elif content_data['type'] == 'voice':
                await callback.bot.send_voice(
                    user_id_target,
                    content_data['voice'],
                    caption=content_data.get('caption')
                )
            elif content_data['type'] == 'video_note':
                await callback.bot.send_video_note(
                    user_id_target,
                    content_data['video_note']
                )
            elif content_data['type'] == 'sticker':
                await callback.bot.send_sticker(
                    user_id_target,
                    content_data['sticker']
                )
            elif content_data['type'] == 'animation':
                await callback.bot.send_animation(
                    user_id_target,
                    content_data['animation'],
                    caption=content_data.get('caption'),
                    caption_entities=content_data.get('caption_entities')
                )
            elif content_data['type'] == 'poll':
                poll = content_data['poll']
                await callback.bot.send_poll(
                    user_id_target,
                    question=poll['question'],
                    options=poll['options'],
                    is_anonymous=poll['is_anonymous'],
                    allows_multiple_answers=poll.get('allows_multiple_answers', False)
                )
            elif content_data['type'] == 'location':
                loc = content_data['location']
                await callback.bot.send_location(
                    user_id_target,
                    latitude=loc['latitude'],
                    longitude=loc['longitude']
                )
            elif content_data['type'] == 'contact':
                cont = content_data['contact']
                await callback.bot.send_contact(
                    user_id_target,
                    phone_number=cont['phone_number'],
                    first_name=cont['first_name'],
                    last_name=cont.get('last_name')
                )
            elif content_data['type'] == 'dice':
                await callback.bot.send_dice(
                    user_id_target,
                    emoji=content_data['dice']
                )

            success += 1

        except Exception as e:
            error_str = str(e).lower()
            if 'blocked' in error_str or 'bot was blocked' in error_str:
                blocked += 1
            else:
                failed += 1
            logger.error(f'Broadcast error for user {user_id_target}: {e}')

        # Progress update har 50 ta user da
        if idx % 50 == 0 or idx == total:
            percentage = int((idx / total) * 100)
            try:
                await progress_msg.edit_text(
                    f"⏳ {percentage}% ({idx}/{total})\n"
                    f"✅ Yuborildi: {success}\n"
                    f"❌ Xato: {failed}\n"
                    f"🚫 Bloklagan: {blocked}"
                )
            except:
                pass

        # Spam prevention
        await asyncio.sleep(0.04)

    # Tugallash
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    minutes = int(duration // 60)
    seconds = int(duration % 60)
    time_str = f"{minutes} daqiqa {seconds} sekund" if minutes > 0 else f"{seconds} sekund"

    success_rate = (success / total * 100) if total > 0 else 0

    await progress_msg.edit_text(
        f"✅ <b>Broadcast yakunlandi!</b>\n\n"
        f"📊 <b>Natijalar:</b>\n"
        f"• Yuborilgan: {success} ta ({success_rate:.1f}%)\n"
        f"• Muvaffaqiyatli: {success} ta\n"
        f"• Bloklagan: {blocked} ta\n"
        f"• Xato: {failed} ta\n"
        f"• Jami: {total} ta\n"
        f"• Vaqt: {time_str}\n\n"
        f"💡 Yangi broadcast uchun: /broadcast",
        parse_mode='HTML'
    )

    await state.finish()
    await callback.answer("✅ Broadcast yakunlandi!")


async def broadcast_cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Bekor qilish callback
    """
    await state.finish()
    await callback.message.edit_text(
        "❌ <b>Broadcast bekor qilindi</b>\n\n"
        "Yangi broadcast uchun: /broadcast",
        parse_mode='HTML'
    )
    await callback.answer("Bekor qilindi")


def register_universal_broadcast_handlers(dp: Dispatcher):
    """
    Universal broadcast handler'larini ro'yxatdan o'tkazish
    """

    # /broadcast komandasi
    dp.register_message_handler(
        broadcast_command,
        commands=['broadcast'],
        state='*'
    )

    # Broadcast button handler (admin panel)
    dp.register_message_handler(
        broadcast_command,
        lambda message: message.text in ['📢 Broadcast', '📢 Рассылка'] and is_admin(message.from_user.id),
        state='*'
    )

    # /cancel komandasi broadcast rejimida
    dp.register_message_handler(
        broadcast_cancel,
        commands=['cancel'],
        state=BroadcastState.waiting_for_content
    )

    # Har qanday content qabul qilish
    dp.register_message_handler(
        broadcast_receive_content,
        content_types=types.ContentTypes.ANY,
        state=BroadcastState.waiting_for_content
    )

    # Tasdiqlash va bekor qilish callback'lari
    dp.register_callback_query_handler(
        broadcast_confirm_callback,
        lambda c: c.data == 'broadcast_confirm' and is_admin(c.from_user.id),
        state=BroadcastState.waiting_for_confirmation
    )

    dp.register_callback_query_handler(
        broadcast_cancel_callback,
        lambda c: c.data == 'broadcast_cancel' and is_admin(c.from_user.id),
        state=BroadcastState.waiting_for_confirmation
    )
