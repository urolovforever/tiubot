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
        'uz': ['👨‍🎓 Talaba', '🎓 Abituriyent', '👨‍👩‍👧 Ota-ona', '👔 Xodim'],
        'ru': ['👨‍🎓 Студент', '🎓 Абитуриент', '👨‍👩‍👧 Родитель', '👔 Сотрудник'],
        'en': ['👨‍🎓 Student', '🎓 Applicant', '👨‍👩‍👧 Parent', '👔 Staff']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
    return keyboard


def get_application_type_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': ['❓ Savol', '💡 Taklif', '⚠️ Shikoyat', '🙏 Tashakkur'],
        'ru': ['❓ Вопрос', '💡 Предложение', '⚠️ Жалоба', '🙏 Благодарность'],
        'en': ['❓ Question', '💡 Suggestion', '⚠️ Complaint', '🙏 Thanks']
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'cancel')))
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

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    await state.update_data(app_type=message.text)

    await message.answer(
        t(user_id, 'send_application'),
        reply_markup=get_cancel_keyboard(user_id)
    )
    await ApplicationForm.waiting_for_message.set()


async def process_application_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    await state.update_data(message=message.text)

    user = db.get_user(user_id)

    if user and user[3]:
        await state.update_data(phone=user[3])
        await message.answer(
            t(user_id, 'attach_file'),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_file.set()
    else:
        await message.answer(
            t(user_id, 'send_phone'),
            reply_markup=get_phone_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_phone.set()


async def process_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

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
        db.update_user_phone(user_id, phone)

        await message.answer(
            t(user_id, 'attach_file'),
            reply_markup=get_cancel_keyboard(user_id)
        )
        await ApplicationForm.waiting_for_file.set()


async def process_file_or_finish(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['❌ Bekor qilish', '❌ Отмена', '❌ Cancel']:
        await state.finish()
        await message.answer(
            t(user_id, 'application_cancelled'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id

    await state.update_data(file_id=file_id)

    data = await state.get_data()
    user = db.get_user(user_id)

    username = user[1] if user else message.from_user.username or ''
    full_name = user[2] if user else message.from_user.full_name
    phone = data.get('phone', '')

    app_id = db.create_application(
        user_id,
        username,
        full_name,
        phone,
        data['message'],
        file_id
    )

    await message.answer(
        t(user_id, 'application_sent'),
        reply_markup=get_main_keyboard(user_id)
    )

    # Notify admins
    admin_text = f'''🆕 Yangi murojaat #{app_id}

👤 Foydalanuvchi:
  • Ism: {full_name}
  • Username: @{username if username else "yo'q"}
  • ID: {user_id}
  • Link: tg://user?id={user_id}
  • Telefon: {phone}

📋 Murojaat:
  • Kim: {data.get('user_type', '')}
  • Turi: {data.get('app_type', '')}

💬 Matn:
{data['message']}

📌 Javob: /reply_{app_id}'''

    for admin_id in ADMIN_IDS:
        try:
            if file_id:
                await message.bot.send_photo(admin_id, file_id, caption=admin_text)
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
    dp.register_message_handler(process_application_message, state=ApplicationForm.waiting_for_message)
    dp.register_message_handler(process_phone, content_types=['text', 'contact'],
                                state=ApplicationForm.waiting_for_phone)
    dp.register_message_handler(process_file_or_finish, content_types=['text', 'photo', 'document'],
                                state=ApplicationForm.waiting_for_file)
