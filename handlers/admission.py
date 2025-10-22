from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t

db = Database()


def get_admission_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '📋 Qabul shartlari',
            '💰 To\'lov va grant tizimi',
            '🌐 Online ro\'yxatdan o\'tish',
            '📞 Qabul bo\'limi bilan bog\'lanish',
            '❓ Tez-tez so\'raladigan savollar'
        ],
        'ru': [
            '📋 Условия поступления',
            '💰 Оплата и система грантов',
            '🌐 Онлайн регистрация',
            '📞 Связаться с приемной комиссией',
            '❓ Часто задаваемые вопросы'
        ],
        'en': [
            '📋 Admission requirements',
            '💰 Payment and grant system',
            '🌐 Online registration',
            '📞 Contact admissions office',
            '❓ Frequently asked questions'
        ]
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.insert(KeyboardButton(t(user_id, 'back')))
    return keyboard


async def admission_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '🧑‍🎓 Qabul (Abituriyentlar uchun)\n\nQuyidagi bo\'limlardan birini tanlang:',
        'ru': '🧑‍🎓 Поступление (Для абитуриентов)\n\nВыберите один из разделов:',
        'en': '🧑‍🎓 Admission (For applicants)\n\nChoose one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


async def admission_requirements_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''📋 Qabul shartlari

Hujjatlar:
✅ O'rta ma'lumot hujjati
✅ Pasport nusxasi
✅ 3x4 fotosurat (6 ta)
✅ Kirish imtihonlari natijasi

Imtihonlar:
📝 Matematika / Ingliz / Mantiq
📅 Iyun - Avgust

Ariza muddati:
🗓 1-iyun - 20-avgust

📞 Ma'lumot: +998 71 200 09 09''',

        'ru': '''📋 Условия поступления

Документы:
✅ Документ о среднем образовании
✅ Копия паспорта
✅ Фото 3x4 (6 шт)
✅ Результаты экзаменов

Экзамены:
📝 Математика / Английский / Логика
📅 Июнь - Август

Срок подачи:
🗓 1 июня - 20 августа

📞 Информация: +998 71 200 09 09''',

        'en': '''📋 Admission Requirements

Documents:
✅ Secondary education certificate
✅ Passport copy
✅ 3x4 photos (6 pcs)
✅ Exam results

Exams:
📝 Math / English / Logic
📅 June - August

Application deadline:
🗓 June 1 - August 20

📞 Info: +998 71 200 09 09'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


async def payment_grant_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''💰 To'lov va grant tizimi

Kontrakt:
💳 12,000,000 - 20,000,000 so'm/yil

Grant:
🏆 100% - A'lo natija
🥈 50% - Yuqori ball
🥉 25% - Yaxshi natija

To'lov:
✅ Bir martalik (-5%)
✅ Yarim yillik
✅ Oylik

📞 +998 71 200 09 09''',

        'ru': '''💰 Оплата и гранты

Контракт:
💳 12,000,000 - 20,000,000 сум/год

Гранты:
🏆 100% - Отличный результат
🥈 50% - Высокий балл
🥉 25% - Хороший результат

Оплата:
✅ Единовременная (-5%)
✅ Полугодовая
✅ Ежемесячная

📞 +998 71 200 09 09''',

        'en': '''💰 Payment and Grants

Contract:
💳 12,000,000 - 20,000,000 UZS/year

Grants:
🏆 100% - Excellent result
🥈 50% - High score
🥉 25% - Good result

Payment:
✅ One-time (-5%)
✅ Semi-annual
✅ Monthly

📞 +998 71 200 09 09'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


async def online_registration_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🌐 Online ro'yxatdan o'tish

Qadamlar:
1️⃣ apply.tiu.uz ga kiring
2️⃣ Ma'lumotlarni kiriting
3️⃣ Yo'nalish tanlang
4️⃣ Hujjat yuklang
5️⃣ Tasdiqlang

🌐 apply.tiu.uz''',

        'ru': '''🌐 Онлайн регистрация

Шаги:
1️⃣ Зайдите на apply.tiu.uz
2️⃣ Введите данные
3️⃣ Выберите направление
4️⃣ Загрузите документы
5️⃣ Подтвердите

🌐 apply.tiu.uz''',

        'en': '''🌐 Online Registration

Steps:
1️⃣ Visit apply.tiu.uz
2️⃣ Enter information
3️⃣ Choose program
4️⃣ Upload documents
5️⃣ Confirm

🌐 apply.tiu.uz'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


async def admission_contact_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''📞 Qabul bo'limi

☎️ +998 71 200 09 09
📧 admission@tiu.uz
📱 @tiu_admission

Ish vaqti:
🕐 Dush-Juma: 9:00-18:00
🕐 Shanba: 9:00-13:00''',

        'ru': '''📞 Приемная комиссия

☎️ +998 71 200 09 09
📧 admission@tiu.uz
📱 @tiu_admission

Время работы:
🕐 Пн-Пт: 9:00-18:00
🕐 Суббота: 9:00-13:00''',

        'en': '''📞 Admissions Office

☎️ +998 71 200 09 09
📧 admission@tiu.uz
📱 @tiu_admission

Working hours:
🕐 Mon-Fri: 9:00-18:00
🕐 Saturday: 9:00-13:00'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


async def faq_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''❓ Tez-tez so'raladigan savollar

1️⃣ Qabul qachon?
   → 1-iyun - 20-avgust

2️⃣ Xalqaro diplom bormi?
   → Ha, qo'sh diplom dasturlari

3️⃣ Yotoqxona bormi?
   → Ha, zamonaviy turar joy

4️⃣ Grant minimal ball?
   → 100%: 180+, 50%: 160+

📞 +998 71 200 09 09''',

        'ru': '''❓ Частые вопросы

1️⃣ Когда прием?
   → 1 июня - 20 августа

2️⃣ Есть международный диплом?
   → Да, программы двойного диплома

3️⃣ Есть общежитие?
   → Да, современное жилье

4️⃣ Минимум для гранта?
   → 100%: 180+, 50%: 160+

📞 +998 71 200 09 09''',

        'en': '''❓ FAQ

1️⃣ When is admission?
   → June 1 - August 20

2️⃣ International diploma?
   → Yes, double degree programs

3️⃣ Dormitory available?
   → Yes, modern housing

4️⃣ Grant minimum score?
   → 100%: 180+, 50%: 160+

📞 +998 71 200 09 09'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )


def register_admission_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admission_handler,
        lambda message: message.text in ['🧑‍🎓 Qabul', '🧑‍🎓 Поступление', '🧑‍🎓 Admission']
    )
    dp.register_message_handler(
        admission_requirements_info,
        lambda message: message.text in [
            '📋 Qabul shartlari',
            '📋 Условия поступления',
            '📋 Admission requirements'
        ]
    )
    dp.register_message_handler(
        payment_grant_info,
        lambda message: message.text in [
            '💰 To\'lov va grant tizimi',
            '💰 Оплата и система грантов',
            '💰 Payment and grant system'
        ]
    )
    dp.register_message_handler(
        online_registration_info,
        lambda message: message.text in [
            '🌐 Online ro\'yxatdan o\'tish',
            '🌐 Онлайн регистрация',
            '🌐 Online registration'
        ]
    )
    dp.register_message_handler(
        admission_contact_info,
        lambda message: message.text in [
            '📞 Qabul bo\'limi bilan bog\'lanish',
            '📞 Связаться с приемной комиссией',
            '📞 Contact admissions office'
        ]
    )
    dp.register_message_handler(
        faq_info,
        lambda message: message.text in [
            '❓ Tez-tez so\'raladigan savollar',
            '❓ Часто задаваемые вопросы',
            '❓ Frequently asked questions'
        ]
    )