from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from states.forms import ApplicationForm
from keyboards.reply import get_cancel_keyboard, get_phone_keyboard, get_main_keyboard
from utils.helpers import t
from config import ADMIN_IDS, ADMIN_GROUP_ID
import logging

db = Database()
logger = logging.getLogger(__name__)


def get_applications_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['✍️ Murojaat yuborish', '🔎 Mening murojaatlarim'],
        'ru': ['✍️ Отправить обращение', '🔎 Мои обращения'],
        'en': ['✍️ Submit application', '🔎 My applications']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


def get_user_type_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['👨‍🎓 Talaba', '👨‍💼 Xodim', '👤 Abituriyent', '🧑‍💼 Boshqa'],
        'ru': ['👨‍🎓 Студент', '👨‍💼 Сотрудник', '👤 Абитуриент', '🧑‍💼 Другое'],
        'en': ['👨‍🎓 Student', '👨‍💼 Staff', '👤 Applicant', '🧑‍💼 Other']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_application_type_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['📝 Ariza', '❓ Savol', '💡 Taklif', '😠 Shikoyat'],
        'ru': ['📝 Заявление', '❓ Вопрос', '💡 Предложение', '😠 Жалоба'],
        'en': ['📝 Application', '❓ Question', '💡 Suggestion', '😠 Complaint']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_anonymity_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Anonim yoki ochiq murojaat tanlash"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['🕶 Anonim murojaat', '📱 Ochiq murojaat'],
        'ru': ['🕶 Анонимное обращение', '📱 Открытое обращение'],
        'en': ['🕶 Anonymous request', '📱 Public request']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.add(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_yes_no_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Ha/Yo'q tugmalari (fayl biriktirish uchun)"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['✅ Ha', '❌ Yo\'q'],
        'ru': ['✅ Да', '❌ Нет'],
        'en': ['✅ Yes', '❌ No']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    return keyboard


def get_confirmation_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Tasdiqlash keyboard - yuborish yoki bekor qilish"""
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['✅ Yuborish', '❌ Bekor qilish'],
        'ru': ['✅ Отправить', '❌ Отменить'],
        'en': ['✅ Send', '❌ Cancel']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    return keyboard


async def applications_menu_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '📬 Murojaatlar\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '📬 Обращения\n\nВыберите один из разделов:',
        'en': '📬 Applications\n\nChoose one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_applications_submenu_keyboard(user_id)
    )


async def start_application_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '✍️ Murojaat yuborish\n\nKim sifatida murojaat qilasiz?',
        'ru': '✍️ Отправить обращение\n\nКак вы обращаетесь?',
        'en': '✍️ Submit Application\n\nWho are you?'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_user_type_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_user_type.set()


async def process_user_type(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    await state.update_data(user_type=message.text)

    lang = db.get_user_language(user_id)
    texts = {
        'uz': 'Murojaat turini tanlang:',
        'ru': 'Выберите тип обращения:',
        'en': 'Choose application type:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_application_type_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_app_type.set()


async def process_app_type(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    await state.update_data(app_type=message.text)

    texts = {
        'uz': 'Murojaat turini tanlang:',
        'ru': 'Выберите тип обращения:',
        'en': 'Choose request type:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_anonymity_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_anonymity.set()


async def process_anonymity(message: types.Message, state: FSMContext):
    """Anonim yoki ochiq murojaat tanlanadi"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    # Anonim yoki ochiq?
    is_anonymous = message.text in ['🕶 Anonim murojaat', '🕶 Анонимное обращение', '🕶 Anonymous request']
    await state.update_data(is_anonymous=is_anonymous)

    if is_anonymous:
        # Anonim - to'g'ridan-to'g'ri matn so'raymiz
        texts = {
            'uz': '✍️ Murojaatingizni yozing:',
            'ru': '✍️ Напишите ваше обращение:',
            'en': '✍️ Write your request:'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_message.set()
    else:
        # Ochiq - telefon so'raymiz
        await message.answer(
            t(user_id, 'send_phone'),
            reply_markup=get_phone_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_phone.set()


async def process_phone(message: types.Message, state: FSMContext):
    """Telefon raqamni qabul qilish (faqat ochiq murojaat uchun)"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    phone = None

    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text

    if phone:
        await state.update_data(phone=phone)

        texts = {
            'uz': '✍️ Murojaatingizni yozing:',
            'ru': '✍️ Напишите ваше обращение:',
            'en': '✍️ Write your request:'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_message.set()


async def process_application_message(message: types.Message, state: FSMContext):
    """Murojaat matnini qabul qilish"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    await state.update_data(message=message.text)

    # Fayl biriktirmoqchimisiz?
    texts = {
        'uz': '📎 Fayl biriktirmoqchimisiz?',
        'ru': '📎 Хотите прикрепить файл?',
        'en': '📎 Do you want to attach a file?'
    }
    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_yes_no_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_file_choice.set()


async def process_file_choice(message: types.Message, state: FSMContext):
    """Fayl biriktirish: Ha yoki Yo'q"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel', '❌ Yo\'q', '❌ Нет', '❌ No']:
        # Yo'q - faylsiz davom etamiz
        await state.update_data(file_id=None)
        await show_confirmation(message, state)
        return

    if message.text in ['✅ Ha', '✅ Да', '✅ Yes']:
        # Ha - fayl yuborish
        texts = {
            'uz': '📎 Faylni yuboring (rasm yoki hujjat):',
            'ru': '📎 Отправьте файл (фото или документ):',
            'en': '📎 Send the file (photo or document):'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_file.set()
    else:
        # Noto'g'ri javob
        texts = {
            'uz': '❌ Iltimos, "Ha" yoki "Yo\'q" tugmasini bosing',
            'ru': '❌ Пожалуйста, нажмите кнопку "Да" или "Нет"',
            'en': '❌ Please press "Yes" or "No" button'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_yes_no_keyboard(user_id)
        )


async def process_file(message: types.Message, state: FSMContext):
    """Faylni qabul qilish"""
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    file_id = None

    # Fayl turini aniqlash
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id

    await state.update_data(file_id=file_id)
    await show_confirmation(message, state)


async def show_confirmation(message: types.Message, state: FSMContext):
    """Tasdiqlash ekranini ko'rsatish"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)
    data = await state.get_data()

    # Ma'lumotlarni formatlash
    is_anonymous = data.get('is_anonymous', False)

    anonymity_text = {
        'uz': '🕶 Anonim' if is_anonymous else '📱 Ochiq',
        'ru': '🕶 Анонимное' if is_anonymous else '📱 Открытое',
        'en': '🕶 Anonymous' if is_anonymous else '📱 Public'
    }

    file_text = {
        'uz': '✅ Biriktirilgan' if data.get('file_id') else '❌ Biriktirilmagan',
        'ru': '✅ Прикреплен' if data.get('file_id') else '❌ Не прикреплен',
        'en': '✅ Attached' if data.get('file_id') else '❌ Not attached'
    }

    confirmation_texts = {
        'uz': f'''📋 Murojaatingiz:

👤 Kim: {data.get('user_type', '')}
📝 Turi: {data.get('app_type', '')}
🔒 Holat: {anonymity_text['uz']}
{f"📱 Telefon: {data.get('phone', '')}" if not is_anonymous else ""}

💬 Matn:
{data.get('message', '')}

📎 Fayl: {file_text['uz']}

Yuborishni tasdiqlaysizmi?''',
        'ru': f'''📋 Ваше обращение:

👤 Кто: {data.get('user_type', '')}
📝 Тип: {data.get('app_type', '')}
🔒 Статус: {anonymity_text['ru']}
{f"📱 Телефон: {data.get('phone', '')}" if not is_anonymous else ""}

💬 Текст:
{data.get('message', '')}

📎 Файл: {file_text['ru']}

Подтвердить отправку?''',
        'en': f'''📋 Your request:

👤 Who: {data.get('user_type', '')}
📝 Type: {data.get('app_type', '')}
🔒 Status: {anonymity_text['en']}
{f"📱 Phone: {data.get('phone', '')}" if not is_anonymous else ""}

💬 Text:
{data.get('message', '')}

📎 File: {file_text['en']}

Confirm sending?'''
    }

    await message.answer(
        confirmation_texts.get(lang, confirmation_texts['uz']),
        reply_markup=get_confirmation_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_confirmation.set()


async def process_confirmation(message: types.Message, state: FSMContext):
    """Tasdiqlash va yuborish"""
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отменить', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    if message.text in ['✅ Yuborish', '✅ Отправить', '✅ Send']:
        await save_and_send_application(message, state)
    else:
        # Noto'g'ri javob
        lang = db.get_user_language(user_id)
        texts = {
            'uz': '❌ Iltimos, "Yuborish" yoki "Bekor qilish" tugmasini bosing',
            'ru': '❌ Пожалуйста, нажмите кнопку "Отправить" или "Отменить"',
            'en': '❌ Please press "Send" or "Cancel" button'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_confirmation_keyboard(user_id)
        )


async def save_and_send_application(message: types.Message, state: FSMContext):
    """Murojaatni saqlash va yuborish"""
    user_id = message.from_user.id
    data = await state.get_data()
    user = db.get_user(user_id)

    username = user[1] if user else message.from_user.username or ''
    full_name = user[2] if user else message.from_user.full_name
    phone = data.get('phone', '')
    is_anonymous = data.get('is_anonymous', False)

    app_id = db.create_application(
        user_id,
        username,
        full_name,
        phone,
        data['message'],
        data.get('file_id'),
        user_type=data.get('user_type', ''),
        app_type=data.get('app_type', ''),
        is_anonymous=is_anonymous
    )

    await message.answer(
        t(user_id, 'application_sent'),
        reply_markup=get_main_keyboard(user_id)
    )

    # Notify admins
    anonymity_status = '🕶 ANONIM (foydalanuvchi uchun)' if is_anonymous else '📱 OCHIQ'
    phone_display = f"  • Telefon: {phone}" if phone else "  • Telefon: -"

    admin_text = f'''🆕 Yangi murojaat

👤 Foydalanuvchi:
  • Ism: {full_name}
  • Username: @{username if username else "yo'q"}
  • ID: {user_id}
  • Link: tg://user?id={user_id}
{phone_display}

📋 Murojaat ma'lumotlari:
  • Kim: {data.get('user_type', '')}
  • Turi: {data.get('app_type', '')}
  • Holat: {anonymity_status}

💬 Matn:
{data['message']}'''

    # Adminlar guruhiga yuborish
    if ADMIN_GROUP_ID:
        try:
            if data.get('file_id'):
                sent_msg = await message.bot.send_photo(
                    ADMIN_GROUP_ID,
                    data['file_id'],
                    caption=admin_text
                )
            else:
                sent_msg = await message.bot.send_message(
                    ADMIN_GROUP_ID,
                    admin_text
                )

            # Message ID ni saqlash (keyin javob berish uchun)
            db.save_application_message_id(app_id, sent_msg.message_id)

        except Exception as e:
            logger.error(f'Error sending to admin group: {e}')
            # Agar guruhga yuborib bo'lmasa, adminlarga bitta-bitta yuborish
            for admin_id in ADMIN_IDS:
                try:
                    if data.get('file_id'):
                        await message.bot.send_photo(admin_id, data['file_id'], caption=admin_text)
                    else:
                        await message.bot.send_message(admin_id, admin_text)
                except Exception as e2:
                    logger.error(f'Error notifying admin {admin_id}: {e2}')
    else:
        # ADMIN_GROUP_ID bo'lmasa, eski usul - adminlarga bitta-bitta yuborish
        for admin_id in ADMIN_IDS:
            try:
                if data.get('file_id'):
                    await message.bot.send_photo(admin_id, data['file_id'], caption=admin_text)
                else:
                    await message.bot.send_message(admin_id, admin_text)
            except Exception as e:
                logger.error(f'Error notifying admin {admin_id}: {e}')

    await state.finish()


async def group_reply_handler(message: types.Message):
    """
    Adminlar guruhida reply orqali javob berish handler'i
    Admin murojaat xabariga reply qilganda ishga tushadi
    """
    # Faqat guruhda va reply bo'lsa ishlaydi
    if not message.reply_to_message or message.chat.type not in ['group', 'supergroup']:
        return

    # Faqat adminlar javob berishi mumkin
    if message.from_user.id not in ADMIN_IDS:
        return

    # Reply qilingan xabar ID bo'yicha murojaatni topish
    replied_msg_id = message.reply_to_message.message_id
    app = db.get_application_by_message_id(replied_msg_id)

    if not app:
        await message.reply("❌ Murojaat topilmadi yoki allaqachon javob berilgan.")
        return

    app_id = app[0]
    user_id = app[1]
    status = app[7]

    if status == 'answered':
        await message.reply("ℹ️ Bu murojaatga allaqachon javob berilgan.")
        return

    # Javobni saqlash
    response_text = message.text
    db.update_application_response(app_id, response_text)

    # Foydalanuvchiga javobni yuborish
    try:
        user_text = f'''✅ Sizning murojaatingizga javob berildi!

📬 Murojaat #{app_id}

💬 Javob:
{response_text}

Agar qo'shimcha savollaringiz bo'lsa, yana murojaat yuborishingiz mumkin.'''

        await message.bot.send_message(user_id, user_text)

        # Guruhda tasdiqlash xabari
        await message.reply(
            f"✅ Javob yuborildi!\n\n"
            f"Murojaat #{app_id}\n"
            f"Foydalanuvchi: {user_id}"
        )

        # Asl xabarni edit qilib, "Javob berilgan" statusini qo'shish
        try:
            original_text = message.reply_to_message.text or message.reply_to_message.caption
            updated_text = f"{original_text}\n\n✅ <b>JAVOB BERILGAN</b>"

            if message.reply_to_message.photo:
                await message.reply_to_message.edit_caption(
                    caption=updated_text,
                    parse_mode='HTML'
                )
            else:
                await message.reply_to_message.edit_text(
                    updated_text,
                    parse_mode='HTML'
                )
        except Exception as e:
            logger.error(f"Error updating message status: {e}")

    except Exception as e:
        logger.error(f'Error sending response to user {user_id}: {e}')
        await message.reply(f"❌ Xatolik: Foydalanuvchiga javob yuborib bo'lmadi.\n{e}")


async def my_applications_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # Avval eski murojaatlarni tozalash (faqat oxirgi 5 ta saqlanadi)
    db.cleanup_old_user_applications(user_id, keep_last=5)

    # Oxirgi 5 ta murojaatni olish
    apps = db.get_user_applications(user_id, limit=5)

    if not apps:
        texts = {
            'uz': 'Sizda hali murojaatlar yo\'q.',
            'ru': 'У вас пока нет обращений.',
            'en': 'You don\'t have any applications yet.'
        }
        await message.answer(
            texts.get(lang, texts['uz']),
            reply_markup=get_applications_submenu_keyboard(user_id)
        )
        return

    # Tarjimalar
    status_texts = {
        'answered': {'uz': '✅ Javob berildi', 'ru': '✅ Отвечено', 'en': '✅ Answered'},
        'new': {'uz': '⏳ Javob kutilmoqda', 'ru': '⏳ Ожидает ответа', 'en': '⏳ Waiting for response'}
    }

    sent_date_label = {'uz': '🕓 Yuborilgan sana:', 'ru': '🕓 Дата отправки:', 'en': '🕓 Sent date:'}
    message_label = {'uz': '💬 Murojaat:', 'ru': '💬 Обращение:', 'en': '💬 Application:'}
    status_label = {'uz': '📊 Status:', 'ru': '📊 Статус:', 'en': '📊 Status:'}
    answer_date_label = {'uz': '📅 Javob sanasi:', 'ru': '📅 Дата ответа:', 'en': '📅 Answer date:'}
    answer_label = {'uz': '✉️ Javob:', 'ru': '✉️ Ответ:', 'en': '✉️ Answer:'}

    header_texts = {
        'uz': '📋 Sizning murojaatlaringiz (oxirgi 5 ta):\n\n',
        'ru': '📋 Ваши обращения (последние 5):\n\n',
        'en': '📋 Your applications (last 5):\n\n'
    }

    text = header_texts.get(lang, header_texts['uz'])

    # app structure: (id, message, status, created_at, admin_response, answered_at)
    for i, app in enumerate(apps):
        app_id = app[0]
        app_message = app[1]
        status = app[2]
        created_at = app[3]
        admin_response = app[4]
        answered_at = app[5] if len(app) > 5 else None

        # Murojaat raqami yo'q, faqat ma'lumotlar
        text += f"{sent_date_label.get(lang, sent_date_label['uz'])} {created_at}\n"
        text += f"{message_label.get(lang, message_label['uz'])} {app_message}\n"

        status_text = status_texts.get(status, {}).get(lang, status)
        text += f"{status_label.get(lang, status_label['uz'])} {status_text}\n"

        # Agar javob berilgan bo'lsa
        if status == 'answered' and admin_response:
            # Javob sanasini ko'rsatish
            if answered_at:
                text += f"{answer_date_label.get(lang, answer_date_label['uz'])} {answered_at}\n"
            text += f"{answer_label.get(lang, answer_label['uz'])} {admin_response}\n"

        # Keyingi murojaat uchun separator
        if i < len(apps) - 1:
            text += "\n" + "─" * 30 + "\n\n"

    await message.answer(
        text,
        parse_mode='HTML',
        reply_markup=get_applications_submenu_keyboard(user_id)
    )


def register_applications_handlers(dp: Dispatcher):
    dp.register_message_handler(
        applications_menu_handler,
        lambda message: message.text in ['📬 Murojaatlar', '📬 Обращения', '📬 Applications']
    )
    dp.register_message_handler(
        start_application_handler,
        lambda message: message.text in [
            '✍️ Murojaat yuborish',
            '✍️ Отправить обращение',
            '✍️ Submit application'
        ],
        state='*'
    )
    dp.register_message_handler(
        my_applications_handler,
        lambda message: message.text in [
            '🔎 Mening murojaatlarim',
            '🔎 Мои обращения',
            '🔎 My applications'
        ]
    )
    dp.register_message_handler(process_user_type, state=ApplicationForm.waiting_for_user_type)
    dp.register_message_handler(process_app_type, state=ApplicationForm.waiting_for_app_type)
    dp.register_message_handler(process_anonymity, state=ApplicationForm.waiting_for_anonymity)
    dp.register_message_handler(process_phone, content_types=['text', 'contact'],
                                state=ApplicationForm.waiting_for_phone)
    dp.register_message_handler(process_application_message, state=ApplicationForm.waiting_for_message)
    dp.register_message_handler(process_file_choice, state=ApplicationForm.waiting_for_file_choice)
    dp.register_message_handler(process_file, content_types=['text', 'photo', 'document'],
                                state=ApplicationForm.waiting_for_file)
    dp.register_message_handler(process_confirmation, state=ApplicationForm.waiting_for_confirmation)

    # Guruhda reply orqali javob berish (oxirida bo'lishi kerak)
    dp.register_message_handler(
        group_reply_handler,
        lambda message: (
            message.chat.type in ['group', 'supergroup'] and
            message.reply_to_message is not None and
            message.from_user.id in ADMIN_IDS
        ),
        content_types=['text']
    )