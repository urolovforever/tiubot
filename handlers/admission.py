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
        'uz': '''📋 <b>TIUga qabul quyidagi talablarga asosan amalga oshiriladi:</b>

<b>1. Ta’lim darajasi:</b>
11-sinf yoki kollej/litsey bitiruvchisi

<b>2. Hujjatlar ro‘yxati:</b>
- Passport yoki ID karta
- Attestat/Diplom (ilovasi bilan)
- 3×4 rasm (elektron ko‘rinishda)
- IELTS / TOPIK / boshqa sertifikat (mavjud bo‘lsa — ustunlik beradi)

<b>3. Qabul jarayoni:</b>
- Onlayn ariza topshirish
- Ichki test yoki suhbat (yo‘nalishdan kelib chiqib)
- Natijalar test yakunlangach e'lon qilinadi

<b>4. O‘qish shakllari:</b>
Kunduzgi / Sirtqi / Masofaviy

<b>5. To‘lov turi:</b>
Kontrakt yoki grant (cheklangan kvota)

ℹ️ <b>Eslatma:</b>
Til sertifikati majburiy emas, mavjud bo‘lsa imtihondan ozod qilinishi yoki chegirma berilishi mumkin.

Qabul kvotalari cheklangan, joylar to‘ldirilgandan so‘ng qabul yopiladi.
''',

        'ru': '''📋 <b>Приём в ТИУ осуществляется на основе следующих требований:</b>

<b>1. Уровень образования:</b>
Выпускник 11 класса или колледжа/лицея

<b>2. Список документов:</b>
- Паспорт или ID-карта
- Аттестат/диплом (с приложением)
- Фото 3×4 (в электронном виде)
- IELTS / TOPIK / другие сертификаты (если есть — дают преимущество)

<b>3. Процесс поступления:</b>
- Подача онлайн-заявки
- Внутренний тест или собеседование (в зависимости от направления)
- Результаты объявляются после завершения тестов

<b>4. Формы обучения:</b>
Очная / Заочная / Дистанционная

<b>5. Тип оплаты:</b>
Контракт или грант (ограниченная квота)

ℹ️ <b>Примечание:</b>
Языковой сертификат не обязателен, но если он есть — можно получить освобождение от экзамена или скидку.

Количество мест ограничено — прием закрывается после заполнения квоты.
''',

        'en': '''📋 <b>Admission to TIU is carried out based on the following requirements:</b>

<b>1. Education Level:</b>
High school or college/lyceum graduate

<b>2. Required Documents:</b>
- Passport or ID card
- Certificate/Diploma (with transcript)
- 3×4 photo (digital format)
- IELTS / TOPIK / other certificates (if available — gives an advantage)

<b>3. Admission Process:</b>
- Submit online application
- Internal test or interview (depending on program)
- Results are announced after testing

<b>4. Study Formats:</b>
Full-time / Part-time / Online

<b>5. Payment Type:</b>
Contract or scholarship (limited quota)

ℹ️ <b>Note:</b>
A language certificate is not mandatory. If available, it may provide exam exemption or a discount.

Seats are limited — admission closes once the quota is filled.
'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id),
        parse_mode="HTML"
    )




async def payment_grant_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    # 1-XABAR: Yo'nalishlar va kontrakt narxlari
    texts_1 = {
        'uz': '''📚 <b>TIU'da mavjud yo'nalishlar va kontrakt narxlari</b>

<b>Kunduzgi ta’lim:</b>
• Yurisprudensiya — 25,000,000 so‘m
• Bank ishi — 19,000,000 so‘m
• Buxgalteriya hisobi — 19,000,000 so‘m
• Iqtisodiyot — 19,000,000 so‘m
• Marketing — 19,000,000 so‘m
• Menejment — 19,000,000 so‘m
• Moliya va moliyaviy texnologiyalar — 19,000,000 so‘m
• Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar — 19,000,000 so‘m
• Axborot tizimlari va texnologiyalari — 19,000,000 so‘m
• Kiberxavfsizlik injiniringi — 19,000,000 so‘m
• Kompyuter injiniringi — 19,000,000 so‘m
• Dasturiy injiniring — 19,000,000 so‘m
• Maktabgacha ta’lim — 16,000,000 so‘m
• Boshlang‘ich ta’lim — 16,000,000 so‘m
• Psixologiya — 16,000,000 so‘m
• Ingliz tili va adabiyoti — 19,000,000 so‘m
• Koreys tili va adabiyoti — 19,000,000 so‘m

<b>Masofaviy ta’lim:</b>
• Yurisprudensiya — 20,000,000 so‘m
• Bank ishi — 16,000,000 so‘m
• Jahon iqtisodiyoti — 16,000,000 so‘m
• Buxgalteriya hisobi — 16,000,000 so‘m
• Marketing — 16,000,000 so‘m
• Menejment — 16,000,000 so‘m
• Moliya va moliyaviy texnologiyalar — 16,000,000 so‘m
• Iqtisodiyot — 16,000,000 so‘m
• Dasturiy injiniring — 16,000,000 so‘m
• Kompyuter injiniringi — 16,000,000 so‘m
• Kiberxavfsizlik injiniringi — 16,000,000 so‘m
• Axborot tizimlari va texnologiyalari — 16,000,000 so‘m
• Psixologiya — 16,000,000 so‘m
• Maktabgacha ta’lim — 15,000,000 so‘m
• Boshlang‘ich ta’lim — 15,000,000 so‘m''',

        'ru': '''📚 <b>Направления и стоимость обучения в TIU</b>

<b>Очная форма:</b>
• Юриспруденция — 25,000,000 сум
• Банковское дело — 19,000,000 сум
• Бухгалтерский учет — 19,000,000 сум
• Экономика — 19,000,000 сум
• Маркетинг — 19,000,000 сум
• Менеджмент — 19,000,000 сум
• Финансы и финансовые технологии — 19,000,000 сум
• Мировая экономика и международные экономические отношения — 19,000,000 сум
• Информационные системы и технологии — 19,000,000 сум
• Кибербезопасность — 19,000,000 сум
• Компьютерная инженерия — 19,000,000 сум
• Программная инженерия — 19,000,000 сум
• Дошкольное образование — 16,000,000 сум
• Начальное образование — 16,000,000 сум
• Психология — 16,000,000 сум
• Английский язык и литература — 19,000,000 сум
• Корейский язык и литература — 19,000,000 сум

<b>Дистанционная форма:</b>
• Юриспруденция — 20,000,000 сум
• Банковское дело — 16,000,000 сум
• Мировая экономика — 16,000,000 сум
• Бухгалтерский учет — 16,000,000 сум
• Маркетинг — 16,000,000 сум
• Менеджмент — 16,000,000 сум
• Финансы и финансовые технологии — 16,000,000 сум
• Экономика — 16,000,000 сум
• Программная инженерия — 16,000,000 сум
• Компьютерная инженерия — 16,000,000 сум
• Кибербезопасность — 16,000,000 сум
• Информационные системы и технологии — 16,000,000 сум
• Психология — 16,000,000 сум
• Дошкольное образование — 15,000,000 сум
• Начальное образование — 15,000,000 сум''',

        'en': '''📚 <b>TIU Programs and Tuition Fees</b>

<b>Full-time Programs:</b>
• Law — 25,000,000 UZS
• Banking — 19,000,000 UZS
• Accounting — 19,000,000 UZS
• Economics — 19,000,000 UZS
• Marketing — 19,000,000 UZS
• Management — 19,000,000 UZS
• Finance and Financial Technologies — 19,000,000 UZS
• World Economy and International Relations — 19,000,000 UZS
• Information Systems and Technologies — 19,000,000 UZS
• Cybersecurity Engineering — 19,000,000 UZS
• Computer Engineering — 19,000,000 UZS
• Software Engineering — 19,000,000 UZS
• Preschool Education — 16,000,000 UZS
• Primary Education — 16,000,000 UZS
• Psychology — 16,000,000 UZS
• English Language and Literature — 19,000,000 UZS
• Korean Language and Literature — 19,000,000 UZS

<b>Online Programs:</b>
• Law — 20,000,000 UZS
• Banking — 16,000,000 UZS
• World Economy — 16,000,000 UZS
• Accounting — 16,000,000 UZS
• Marketing — 16,000,000 UZS
• Management — 16,000,000 UZS
• Finance and Financial Technologies — 16,000,000 UZS
• Economics — 16,000,000 UZS
• Software Engineering — 16,000,000 UZS
• Computer Engineering — 16,000,000 UZS
• Cybersecurity Engineering — 16,000,000 UZS
• Information Systems and Technologies — 16,000,000 UZS
• Psychology — 16,000,000 UZS
• Preschool Education — 15,000,000 UZS
• Primary Education — 15,000,000 UZS'''
    }

    # 2-XABAR: Grant tizimi
    texts_2 = {
        'uz': '''🎓 <b>TIU Grant Tizimi</b>

🏆 100% — To‘liq grant  
🥇 75% — Yuqori chegirma  
🥈 50% — O‘rtacha chegirma  
🥉 25% — Qisman chegirma  

<b>Grantlar quyidagilarga beriladi:</b>
• Imtihon natijalari
• IELTS / TOPIK / Xalqaro sertifikatlar
• Iqtidor, portfel, diplom va medallar

🎓 TIU talabalari davlat grantlarida ham ishtirok etishlari mumkin.
''',

        'ru': '''🎓 <b>Грантовая система TIU</b>

🏆 100% — Полный грант  
🥇 75% — Высокая скидка  
🥈 50% — Средняя скидка  
🥉 25% — Частичная скидка  

<b>Гранты предоставляются на основе:</b>
• Результатов экзамена
• IELTS / TOPIK / международных сертификатов
• Таланта, портфолио, дипломов и медалей

🎓 Студенты TIU могут участвовать в государственных грантах.
''',

        'en': '''🎓 <b>TIU Grant System</b>

🏆 100% — Full Scholarship  
🥇 75% — High Scholarship  
🥈 50% — Medium Scholarship  
🥉 25% — Partial Scholarship  

<b>Grants are awarded based on:</b>
• Entrance exam performance
• IELTS / TOPIK / international certificates
• Talent, portfolio, awards, and achievements

🎓 TIU students are also eligible for state scholarship competitions.
'''
    }

    # Xabarlar ketma-ket yuboriladi
    await message.answer(
        texts_1.get(lang, texts_1['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id),
        parse_mode="HTML"
    )

    await message.answer(
        texts_2.get(lang, texts_2['uz']),
        parse_mode="HTML"
    )



async def online_registration_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''📢 Hurmatli abituriyentlar!

Toshkent Xalqaro Universitetining joriy yil uchun qabul jarayonlari rasman yakunlandi. Ariza topshirgan barcha nomzodlarga minnatdorchilik bildiramiz. Qabul natijalari shaxsiy kabinet orqali bosqichma-bosqich e’lon qilib boriladi.

Keyingi o‘quv yili uchun qabul sanalari qo‘shimcha ravishda e’lon qilinadi.''',

        'ru': '''📢 Уважаемые абитуриенты!

Процесс приема в Ташкентский Международный Университет на текущий год официально завершён. Благодарим всех подавших заявки. Результаты приёма будут объявляться поэтапно через личный кабинет.

Даты приема на следующий учебный год будут объявлены дополнительно.''',

        'en': '''📢 Dear applicants!

The admission process for this academic year at Tashkent International University has officially been completed. We thank all applicants who submitted their applications. Admission results will be gradually announced through the personal account.

The admission dates for the next academic year will be announced additionally.'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_admission_submenu_keyboard(user_id)
    )



async def admission_contact_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''❓ Savolingiz bormi?
TIU Qabul bo‘limi sizga yordam beradi.

📞 Telefon: +998 (95) 131-55-55
✉️ Telegram: https://t.me/tiuqabul

🌐 www.tiu.uz''',

        'ru': '''❓ У вас есть вопросы?
Приемная комиссия TIU поможет вам.

📞 Телефон: +998 (95) 131-55-55
✉️ Telegram: https://t.me/tiuqabul

🌐 www.tiu.uz''',

        'en': '''❓ Got questions?
TIU Admissions Office is here to help.

📞 Phone: +998 (95) 131-55-55
✉️ Telegram: https://t.me/tiuqabul

🌐 www.tiu.uz'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_admission_submenu_keyboard(user_id)
    )



async def faq_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': """❓ Tez-tez so'raladigan savollar

1. TIUga qabul qachon boshlanadi?
Qabul onlayn tarzda <a href="https://qabul.tiu.uz">qabul.tiu.uz</a> portali orqali amalga oshiriladi. Yangi qabul sanalari rasmiy sahifalarda e’lon qilinadi.

2. Qanday hujjatlar kerak bo‘ladi?
- Passport yoki ID
- Attestat yoki Diplom (ilova bilan)
- IELTS/TOPIK (bo‘lsa — ustunlik beradi)

3. Qabul qanday shaklda? Test bormi yoki suhbatmi?
Yo‘nalishga qarab ichki test yoki suhbat o‘tkaziladi. Ba’zi hollarda sertifikatga ega abituriyentlar imtihondan ozod qilinishi mumkin.

4. Ta’lim shakllari qanaqa?
- Kunduzgi
- Masofaviy (online)
TIUda sirtqi ta’lim yo‘q, uning o‘rnini masofaviy ta’lim to‘liq qoplaydi.

5. Masofaviy ta’lim qanday o‘qitiladi?
Onlayn platforma orqali video darslar, testlar, vebinarlar va semestr yakunida 1–2 marta oflayn nazoratlar asosida o‘qitiladi. Diplom kunduzgi bilan teng kuchga ega.

6. Kontrakt narxlari qancha?
Yo‘nalishlarga qarab 15 mln dan 25 mln so‘mgacha.
To‘liq ro‘yxat: https://qabul.tiu.uz/

7. Grantlar bormi?
Ha. TIUda 25%, 50%, 75% va 100% universitet grantlari mavjud.
Bundan tashqari, davlat grantlarida ishtirok etish imkoniyati ham bor.

8. Chet tili sertifikati bo‘lsa nima bo‘ladi?
B2 va undan yuqori darajadagi sertifikat bo‘lsa, abituriyent chet tili testidan ozod etiladi.

9. Yotoqxona bormi?
Ha, 300 o‘rinli talabalar yotoqxonasi mavjud.
Batafsil ma’lumot uchun qo‘ng‘iroq orqali murojaat qilinadi.

10. TIU diplomi tan olinadimi?
TIU litsenziyaga ega va diplom davlat tomonidan tan olinadi.
Litsenziya havolasi: https://www.tiu.uz/regulations

11. Qaysi yo‘nalishlar mavjud?
Kunduzgi va masofaviy ta’lim uchun bir nechta yo‘nalishlar mavjud.
To‘liq ro‘yxat bot ichida alohida bo‘lim sifatida ko‘rsatilgan.

12. O‘qish qayerda joylashgan?
📍 Manzil: Toshkent shahar, Yunusobod tumani, Kichik halqa yo‘li, 7-uy

13. Qanday ro‘yxatdan o‘tsam bo‘ladi?
Onlayn ro‘yxatdan o‘tish havolasi: https://qabul.tiu.uz/

14. Bir yo‘nalish yopilgan bo‘lsa, boshqa variant bormi?
Ha. Agar kunduzgi kvotalar to‘lib qolgan bo‘lsa, abituriyent masofaviy ta’lim yoki boshqa kunduzgi yo‘nalishni tanlashi mumkin.
""",

        'ru': """❓ Часто задаваемые вопросы

1. Когда начинается прием в TIU?
Прием осуществляется онлайн через портал <a href="https://qabul.tiu.uz">qabul.tiu.uz</a>. Новые даты приема публикуются на официальных страницах.

2. Какие документы необходимы?
- Паспорт или ID-карта
- Аттестат или Диплом (с приложением)
- IELTS/TOPIK (при наличии — дает преимущество)

3. Как проходит прием? Тест или собеседование?
В зависимости от направления проводится внутренний тест или собеседование. В некоторых случаях абитуриенты с сертификатами могут быть освобождены от экзамена.

4. Формы обучения:
- Очная
- Дистанционная (online)
В TIU нет заочного обучения, его полностью заменяет дистанционная форма.

5. Как проходит дистанционное обучение?
Через онлайн-платформу: видео-уроки, тесты, вебинары и 1–2 офлайн контроля в конце семестра. Диплом имеет такую же силу, как и очный.

6. Стоимость контракта?
От 15 до 25 млн сум в зависимости от направления.
Полный список: https://qabul.tiu.uz/

7. Есть ли гранты?
Да. В TIU доступны 25%, 50%, 75% и 100% университетские гранты, а также возможность участия в государственных грантах.

8. Что если есть сертификат по иностранному языку?
С уровнем B2 и выше абитуриент освобождается от теста по иностранному языку.

9. Есть ли общежитие?
Да, есть общежитие на 300 мест.
Подробности уточняются по телефону.

10. Признается ли диплом TIU?
TIU имеет государственную лицензию, диплом признается государством.
Лицензия: https://www.tiu.uz/regulations

11. Какие направления доступны?
Список направлений для очной и дистанционной формы указан в отдельном разделе бота.

12. Где находится университет?
📍 Адрес: г. Ташкент, Юнусабадский район, Кичик Халка Йули, дом 7

13. Как зарегистрироваться?
Онлайн регистрация: https://qabul.tiu.uz/

14. Если направление закрыто, есть ли альтернатива?
Да. Можно выбрать другое очное направление или дистанционную форму.
""",

        'en': """❓ Frequently Asked Questions

1. When does admission to TIU start?
Admission is conducted online via <a href="https://qabul.tiu.uz">qabul.tiu.uz</a>. New admission dates are announced on official pages.

2. What documents are required?
- Passport or ID card
- High school certificate or Diploma (with transcript)
- IELTS/TOPIK (if available — it gives an advantage)

3. How is the admission process? Test or interview?
Depending on the program, there may be an internal test or interview. Applicants with certain certificates may be exempt from exams.

4. Modes of study:
- Full-time (On-campus)
- Distance (Online)
TIU does not offer part-time study; distance learning fully replaces it.

5. How is distance learning conducted?
Through an online platform: video lessons, tests, webinars, and 1–2 offline assessments per semester. The diploma is fully equivalent to full-time.

6. Tuition fees:
From 15 million to 25 million UZS depending on the program.
Full list: https://qabul.tiu.uz/

7. Are scholarships available?
Yes. TIU offers 25%, 50%, 75% and 100% university scholarships. There is also an opportunity to participate in state scholarships.

8. What if I have a foreign language certificate?
If the certificate is B2 level or higher, the applicant is exempt from the foreign language exam.

9. Is there a dormitory?
Yes, a dormitory for 300 students is available.
Details can be clarified by phone.

10. Is the TIU diploma recognized?
TIU has a state license and its diploma is officially recognized.
License link: https://www.tiu.uz/regulations

11. Which programs are available?
The full list of programs for full-time and distance study is shown in the bot in a separate section.

12. Where is the university located?
📍 Address: Tashkent city, Yunusabad district, Kichik Halqa Yo‘li, 7

13. How do I apply?
Online application: https://qabul.tiu.uz/

14. If a program is full, are there alternatives?
Yes. You may choose another full-time program or distance study.
"""
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_admission_submenu_keyboard(user_id),
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