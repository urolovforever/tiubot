"""
Tez tadbir qo'shish - Telegram post formatida
Admin rasm + caption yuklaydi, bot faqat sanani so'raydi
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from states.forms import EventQuickCreateState
from utils.helpers import t, is_admin
from keyboards.reply import get_admin_keyboard, get_cancel_keyboard
import re
from datetime import datetime

db = Database()


def extract_title_from_caption(caption: str) -> str:
    """
    Caption'dan tadbir nomini ajratib olish
    Birinchi qator yoki 50 belgidan keyin ...
    """
    if not caption:
        return "Tadbir"

    # Birinchi qatorni olish
    first_line = caption.split('\n')[0].strip()

    # HTML teglarini olib tashlash
    first_line = re.sub('<[^<]+?>', '', first_line)

    # Emoji'larni saqlagan holda qisqartirish
    if len(first_line) > 50:
        return first_line[:50] + "..."

    return first_line if first_line else "Tadbir"


def parse_date_from_text(text: str) -> str:
    """
    Turli formatdagi sanalarni parse qilish
    Masalan: 15.02.2025, 15-02-2025, 15/02/2025
    """
    # Raqamlarni topish
    numbers = re.findall(r'\d+', text)

    if len(numbers) >= 3:
        day, month, year = numbers[0], numbers[1], numbers[2]

        # Yilni to'ldirish (25 -> 2025)
        if len(year) == 2:
            year = "20" + year

        # Format: DD.MM.YYYY
        return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

    return text  # Parse qila olmasa, o'zi qaytaradi


async def quick_event_start(message: types.Message, state: FSMContext):
    """Admin tadbir qo'shishni boshlaydi"""
    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    await message.answer(
        "📝 <b>Tadbir qo'shish</b>\n\n"
        "1️⃣ Tadbir nomini kiriting:\n\n"
        "Masalan:\n"
        "• Ochiq eshiklar kuni\n"
        "• Yuridik kitoblar yarmarkasi\n"
        "• Startup tanlov",
        parse_mode='HTML',
        reply_markup=get_cancel_keyboard(user_id)
    )

    await EventQuickCreateState.waiting_for_title.set()


async def process_event_title(message: types.Message, state: FSMContext):
    """Tadbir nomini qabul qilish"""
    user_id = message.from_user.id

    # Bekor qilish
    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            "❌ Bekor qilindi",
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    # Nomni saqlash
    title = message.text.strip()
    await state.update_data(title=title)

    # Rasm + caption so'rash
    await message.answer(
        "📸 <b>2️⃣ Rasm va tavsif yuboring</b>\n\n"
        "Tadbir haqida to'liq ma'lumot:\n"
        "• Rasm yuklang\n"
        "• Caption'da tavsif yozing\n\n"
        "Caption'da:\n"
        "• Tadbir haqida batafsil\n"
        "• Vaqt, manzil\n"
        "• Link (kerak bo'lsa)\n"
        "• Emoji va hashtag ishlatish mumkin\n\n"
        "Telegram post formatida yuboring.",
        parse_mode='HTML'
    )

    await EventQuickCreateState.waiting_for_post.set()


async def process_event_post(message: types.Message, state: FSMContext):
    """Admin yuborgan rasm + caption'ni qabul qilish"""
    user_id = message.from_user.id

    # Bekor qilish
    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            "❌ Bekor qilindi",
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    # Rasm bo'lishi kerak
    if not message.photo:
        await message.answer(
            "❌ Rasm yuborish kerak!\n\n"
            "Rasm + Caption formatida yuboring.\n\n"
            "Qaytadan yuboring yoki bekor qiling."
        )
        return

    # Caption bo'lishi kerak
    if not message.caption:
        await message.answer(
            "❌ Caption (tadbir tavsifi) yozish kerak!\n\n"
            "Rasm bilan birga caption yozing.\n\n"
            "Qaytadan yuboring yoki bekor qiling."
        )
        return

    # Ma'lumotlarni saqlash
    photo_id = message.photo[-1].file_id

    # HTML formatda caption olish (formatting saqlanadi)
    # aiogram 2.x da caption_html yo'q, shuning uchun caption va entities ishlatamiz
    caption = message.caption or ""

    # Agar caption_entities bo'lsa, HTML formatga o'tkazish
    if message.caption_entities:
        # aiogram'ning HTML formatter'idan foydalanish
        from aiogram.utils.markdown import html_decoration
        caption = message.html_text or message.caption

    await state.update_data(
        photo_id=photo_id,
        caption=caption
    )

    # Sanani so'rash
    await message.answer(
        "📅 <b>3️⃣ Tadbir sanasini kiriting</b>\n\n"
        "Format: DD.MM.YYYY\n\n"
        "Masalan:\n"
        "• 15.02.2025\n"
        "• 27.10.2025\n"
        "• 01.12.2025",
        parse_mode='HTML'
    )

    await EventQuickCreateState.waiting_for_date.set()


async def process_event_date_quick(message: types.Message, state: FSMContext):
    """Sana kiritildi - tasdiqlash"""
    user_id = message.from_user.id

    # Bekor qilish
    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            "❌ Bekor qilindi",
            reply_markup=get_admin_keyboard(user_id)
        )
        return

    # Sanani parse qilish
    date_str = parse_date_from_text(message.text)

    # Sanani tekshirish
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
    except:
        await message.answer(
            "❌ Noto'g'ri sana formati!\n\n"
            "To'g'ri format: DD.MM.YYYY\n"
            "Masalan: 15.02.2025\n\n"
            "Qaytadan kiriting:"
        )
        return

    # Sanani saqlash
    await state.update_data(date=date_str)

    # Tasdiqlash uchun preview ko'rsatish
    data = await state.get_data()

    # Tasdiqlash keyboard
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="✅ Tasdiqlash va e'lon qilish", callback_data="quick_event_confirm"),
        InlineKeyboardButton(text="📅 Sanani o'zgartirish", callback_data="quick_event_change_date"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="quick_event_cancel")
    )

    # Preview yuborish
    await message.answer_photo(
        photo=data['photo_id'],
        caption=f"{data['caption']}\n\n<b>📅 Sana: {date_str}</b>",
        parse_mode='HTML',
        reply_markup=keyboard
    )

    await message.answer(
        "👆 Tadbir shu ko'rinishda e'lon qilinadi.\n\n"
        "Tasdiqlaysizmi?",
        reply_markup=keyboard
    )

    await EventQuickCreateState.waiting_for_confirmation.set()


async def process_event_confirmation(callback: types.CallbackQuery, state: FSMContext):
    """Tasdiqlash callback'lari"""
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer("❌ Ruxsat yo'q")
        return

    data = await state.get_data()

    # Tasdiqlash
    if callback.data == "quick_event_confirm":
        # Database'ga saqlash
        # title, description (caption), date, time=None, location="", registration_link=None, image_id
        event_id = db.create_event(
            title=data['title'],
            description=data['caption'],  # Caption'ni description sifatida saqlash
            date=data['date'],
            location="",  # Caption ichida bor
            image_id=data['photo_id'],
            time=None,  # Caption ichida bor
            registration_link=None  # Caption ichida bor
        )

        if event_id:
            await callback.message.delete()
            await callback.message.answer(
                f"✅ <b>Tadbir muvaffaqiyatli qo'shildi!</b>\n\n"
                f"📅 Sana: {data['date']}\n"
                f"🆔 ID: {event_id}\n\n"
                f"Tadbir tadbirlar ro'yxatida ko'rinadi.",
                parse_mode='HTML',
                reply_markup=get_admin_keyboard(user_id)
            )
        else:
            await callback.message.answer(
                "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
                reply_markup=get_admin_keyboard(user_id)
            )

        await state.finish()
        await callback.answer("✅ Tadbir qo'shildi")

    # Sanani o'zgartirish
    elif callback.data == "quick_event_change_date":
        await callback.message.answer(
            "📅 Yangi sanani kiriting:\n\n"
            "Format: DD.MM.YYYY\n"
            "Masalan: 15.02.2025"
        )
        await EventQuickCreateState.waiting_for_date.set()
        await callback.answer("Sanani o'zgartirish")

    # Bekor qilish
    elif callback.data == "quick_event_cancel":
        await state.finish()
        await callback.message.delete()
        await callback.message.answer(
            "❌ Tadbir qo'shish bekor qilindi",
            reply_markup=get_admin_keyboard(user_id)
        )
        await callback.answer("Bekor qilindi")


def register_quick_event_handlers(dp: Dispatcher):
    """Tadbir qo'shish handler'larini ro'yxatdan o'tkazish"""

    # Boshlash
    dp.register_message_handler(
        quick_event_start,
        lambda message: message.text in [
            '➕ Tadbir qo\'shish',
            '➕ Tez tadbir qo\'shish',
            '➕ Добавить мероприятие',
            '➕ Быстро добавить событие',
            '➕ Add Event',
            '➕ Quick Add Event'
        ] and is_admin(message.from_user.id),
        state='*'
    )

    # Nom qabul qilish
    dp.register_message_handler(
        process_event_title,
        content_types=['text'],
        state=EventQuickCreateState.waiting_for_title
    )

    # Rasm + caption qabul qilish
    dp.register_message_handler(
        process_event_post,
        content_types=['photo', 'text'],
        state=EventQuickCreateState.waiting_for_post
    )

    # Sana qabul qilish
    dp.register_message_handler(
        process_event_date_quick,
        state=EventQuickCreateState.waiting_for_date
    )

    # Tasdiqlash callback'lari
    dp.register_callback_query_handler(
        process_event_confirmation,
        lambda c: c.data.startswith('quick_event_') and is_admin(c.from_user.id),
        state=EventQuickCreateState.waiting_for_confirmation
    )
