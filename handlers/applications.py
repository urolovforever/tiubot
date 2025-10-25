from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from states.forms import ApplicationForm
from keyboards.reply import get_cancel_keyboard, get_phone_keyboard, get_main_keyboard
from utils.helpers import t
from config import ADMIN_IDS
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

    admin_text = f'''🆕 Yangi murojaat #{app_id}

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
{data['message']}

📌 Javob: /reply_{app_id}'''

    for admin_id in ADMIN_IDS:
        try:
            if data.get('file_id'):
                await message.bot.send_photo(admin_id, data['file_id'], caption=admin_text)
            else:
                await message.bot.send_message(admin_id, admin_text)
        except Exception as e:
            logger.error(f'Error notifying admin {admin_id}: {e}')

    await state.finish()


async def my_applications_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    apps = db.get_user_applications(user_id, 20)

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

    status_map = {
        'new': {'uz': '🆕 Yangi', 'ru': '🆕 Новое', 'en': '🆕 New'},
        'answered': {'uz': '✅ Javob berildi', 'ru': '✅ Отвечено', 'en': '✅ Answered'}
    }

    texts = {
        'uz': '📋 Sizning murojaatlaringiz:\n\n',
        'ru': '📋 Ваши обращения:\n\n',
        'en': '📋 Your applications:\n\n'
    }

    text = texts.get(lang, texts['uz'])
    for app in apps:
        status = status_map.get(app[2], {}).get(lang, app[2])
        text += f'#{app[0]} - {status}\n📅 {app[3]}\n\n'

    await message.answer(
        text,
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


