from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from utils.helpers import t


async def contact_handler(message: types.Message):
    user_id = message.from_user.id
    lang = t(user_id, 'lang')

    text = {
        'uz': """📞 <b>Aloqa ma'lumotlari</b>

📱 Telefon: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Fakultetlar bo'yicha aloqaga chiqish uchun tanlang ↓""",
        'ru': """📞 <b>Контактная информация</b>

📱 Телефон: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Выберите факультет для связи ↓""",
        'en': """📞 <b>Contact Information</b>

📱 Phone: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Choose a faculty to contact ↓"""
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("⚖️ Yurisprudensiya fakulteti", callback_data="faculty_law"),
        InlineKeyboardButton("🏛 Biznes va innovatsion ta'lim fakulteti", callback_data="faculty_business"),
        InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")
    )

    photo_path = "media/contact.jpg"
    try:
        await message.answer_photo(
            photo=InputFile(photo_path),
            caption=text.get(lang, text['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except:
        await message.answer(
            text.get(lang, text['uz']),
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


# ---- Fakultet matnlari ----
faculty_texts = {
    "law": {
        "uz": """⚖️ <b>YURISPRUDENSIYA FAKULTETI</b>

📌 Masofaviy ta'lim (Hemis, Hero tizimi) bo'yicha murojaatlar — @tiu_studentservis
📌 Sirtqi ta'lim shakli bo'yicha murojaatlar — @tiu_studentservis
📌 Kunduzgi ta'lim shakli bo'yicha murojaatlar — +998 55 517 53 53 (ichki raqam 1007)

📢 Fakultet rasmiy telegram kanali — https://t.me/TIU_Faculty_of_Law
📢 Masofaviy ta'lim rasmiy kanali — https://t.me/masofaviytalim_TIU

📞 Fakultet telefon raqami — +998 55 517 53 53 (ichki raqam 1007)
📄 Kontrakt shartnomasi bo'yicha murojaatlar — @Mahkamjonov""",

        "ru": """⚖️ <b>ФАКУЛЬТЕТ ЮРИСПРУДЕНЦИИ</b>

📌 По вопросам дистанционного обучения (Hemis, Hero система) — @tiu_studentservis
📌 По вопросам заочного обучения — @tiu_studentservis
📌 По вопросам очного обучения — +998 55 517 53 53 (внутр. 1007)

📢 Официальный telegram канал факультета — https://t.me/TIU_Faculty_of_Law
📢 Официальный канал дистанционного обучения — https://t.me/masofaviytalim_TIU

📞 Телефон факультета — +998 55 517 53 53 (внутр. 1007)
📄 По вопросам контракта — @Mahkamjonov""",

        "en": """⚖️ <b>FACULTY OF LAW</b>

📌 Distance learning inquiries (Hemis, Hero system) — @tiu_studentservis
📌 Part-time learning inquiries — @tiu_studentservis
📌 Full-time learning inquiries — +998 55 517 53 53 (ext. 1007)

📢 Official faculty telegram channel — https://t.me/TIU_Faculty_of_Law
📢 Official distance learning channel — https://t.me/masofaviytalim_TIU

📞 Faculty phone — +998 55 517 53 53 (ext. 1007)
📄 Contract inquiries — @Mahkamjonov"""
    },

    "business": {
        "uz": """🏛 <b>BIZNES VA INNOVATSION TA'LIM FAKULTETI</b>

📌 Masofaviy ta'lim (Hemis, Hero tizimi) bo'yicha murojaatlar — @tiu_deans
📌 Kunduzgi ta'lim shakli bo'yicha murojaatlar — @tiu_deans
📌 Sirtqi ta'lim shakli bo'yicha murojaatlar — @tiu_deans

📢 Fakultet rasmiy telegram kanali — https://t.me/tiu_businessfaculty
📢 Masofaviy ta'lim rasmiy kanali — https://t.me/masofaviytalim_TIU

📞 Fakultet telefon raqami — +998 55 517 53 53 (ichki raqam 1008)
📄 Kontrakt shartnomasi bo'yicha murojaatlar — @Mahkamjonov""",

        "ru": """🏛 <b>ФАКУЛЬТЕТ БИЗНЕСА И ИННОВАЦИОННОГО ОБРАЗОВАНИЯ</b>

📌 По вопросам дистанционного обучения (Hemis, Hero система) — @tiu_deans
📌 По вопросам очного обучения — @tiu_deans
📌 По вопросам заочного обучения — @tiu_deans

📢 Официальный telegram канал факультета — https://t.me/tiu_businessfaculty
📢 Официальный канал дистанционного обучения — https://t.me/masofaviytalim_TIU

📞 Телефон факультета — +998 55 517 53 53 (внутр. 1008)
📄 По вопросам контракта — @Mahkamjonov""",

        "en": """🏛 <b>FACULTY OF BUSINESS AND INNOVATIVE EDUCATION</b>

📌 Distance learning inquiries (Hemis, Hero system) — @tiu_deans
📌 Full-time learning inquiries — @tiu_deans
📌 Part-time learning inquiries — @tiu_deans

📢 Official faculty telegram channel — https://t.me/tiu_businessfaculty
📢 Official distance learning channel — https://t.me/masofaviytalim_TIU

📞 Faculty phone — +998 55 517 53 53 (ext. 1008)
📄 Contract inquiries — @Mahkamjonov"""
    }
}


async def faculty_law_callback(callback: types.CallbackQuery):
    lang = t(callback.from_user.id, 'lang')
    if lang not in ['uz', 'ru', 'en']:
        lang = 'uz'

    # Orqaga qaytish tugmasi
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back",
                             callback_data="back_to_contact")
    )

    # Xabarni yangilash (yangi xabar yubormaslik)
    try:
        await callback.message.edit_caption(
            caption=faculty_texts["law"].get(lang, faculty_texts["law"]['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except:
        await callback.message.edit_text(
            text=faculty_texts["law"].get(lang, faculty_texts["law"]['uz']),
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    await callback.answer()


async def faculty_business_callback(callback: types.CallbackQuery):
    lang = t(callback.from_user.id, 'lang')
    if lang not in ['uz', 'ru', 'en']:
        lang = 'uz'

    # Orqaga qaytish tugmasi
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔙 Orqaga" if lang == 'uz' else "🔙 Назад" if lang == 'ru' else "🔙 Back",
                             callback_data="back_to_contact")
    )

    # Xabarni yangilash
    try:
        await callback.message.edit_caption(
            caption=faculty_texts["business"].get(lang, faculty_texts["business"]['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except:
        await callback.message.edit_text(
            text=faculty_texts["business"].get(lang, faculty_texts["business"]['uz']),
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    await callback.answer()


async def back_to_contact_callback(callback: types.CallbackQuery):
    lang = t(callback.from_user.id, 'lang')

    text = {
        'uz': """📞 <b>Aloqa ma'lumotlari</b>

📱 Telefon: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Fakultetlar bo'yicha aloqaga chiqish uchun tanlang ↓""",
        'ru': """📞 <b>Контактная информация</b>

📱 Телефон: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Выберите факультет для связи ↓""",
        'en': """📞 <b>Contact Information</b>

📱 Phone: <b>+998 95 131 55 55</b>
📱 Telegram: https://t.me/tiuqabul

Choose a faculty to contact ↓"""
    }

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("⚖️ Yurisprudensiya fakulteti", callback_data="faculty_law"),
        InlineKeyboardButton("🏛 Biznes va innovatsion ta'lim fakulteti", callback_data="faculty_business"),
        InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")
    )

    # Xabarni yangilash
    try:
        await callback.message.edit_caption(
            caption=text.get(lang, text['uz']),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except:
        await callback.message.edit_text(
            text=text.get(lang, text['uz']),
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    await callback.answer()


def register_contact_handlers(dp: Dispatcher):
    dp.register_message_handler(contact_handler, lambda msg: msg.text in ['📞 Aloqa', '📞 Контакты', '📞 Contact'])
    dp.register_callback_query_handler(faculty_law_callback, lambda c: c.data == "faculty_law")
    dp.register_callback_query_handler(faculty_business_callback, lambda c: c.data == "faculty_business")
    dp.register_callback_query_handler(back_to_contact_callback, lambda c: c.data == "back_to_contact")