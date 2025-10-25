from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.helpers import t
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

db = Database()


def get_about_submenu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = db.get_user_language(user_id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = {
        'uz': [
            '🎓 Universitet haqida qisqacha ma\'lumot',
            '🌍 Xalqaro hamkorliklar',
            '📚 Fakultetlar va dasturlar',
            '🎥 3D sayohat'
        ],
        'ru': [
            '🎓 Краткая информация об университете',
            '🌍 Международное сотрудничество',
            '📚 Факультеты и программы',
            '🎥 3D-тур'
        ],
        'en': [
            '🎓 Brief information about university',
            '🌍 International partnerships',
            '📚 Faculties and programs',
            '🎥 3D tour'
        ]
    }

    for btn in buttons.get(lang, buttons['uz']):
        keyboard.insert(KeyboardButton(btn))

    keyboard.add(KeyboardButton(t(user_id, 'back')))
    return keyboard


async def about_tiu_handler(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': 'Bu yerda universitetimiz va hamkor universitetlar, fakultet va dasturlar haqida ma\'lumot olishingiz mumkin.\n\nTo\'liq ma\'lumot olish uchun quyidagi bo\'limlardan birini tanlang:',
        'ru': 'Здесь вы можете получить информацию о нашем университете, университетах-партнерах, факультетах и программах.\n\nДля получения полной информации выберите один из разделов:',
        'en': 'Here you can get information about our university, partner universities, faculties and programs.\n\nFor complete information, please select one of the sections:'
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def about_university_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''
<b>🏛 Tashkil topgan sanasi va hujjatlar</b>

Tashkent International University O'zbekiston Respublikasi Vazirlar Mahkamasining 02.11.2019 yildagi <a href="https://lex.uz/uz/docs/-4584249">900-son qarori</a> asosida tashkil etilgan.

Universitet faoliyati O'zbekiston Respublikasi Oliy ta'lim, fan va innovatsiyalar vazirligi tomonidan berilgan <a href="https://license.gov.uz/registry/beb55034-934b-4754-b2e0-92364d5916b2">304988-sonli litsenziya</a> bilan amalga oshiriladi.

<b>🎯 Asosiy maqsad va vazifalar</b>

TIU ning asosiy maqsadi — xalqaro standartlarga mos, amaliy bilim va ko'nikmalarga ega mutaxassislarni tayyorlashdir.

Universitet:
- ta'lim, fan va innovatsiyalarni integratsiyalash,
- xorijiy universitetlar bilan qo'shma dasturlarni joriy etish,
- raqamli texnologiyalar, sun'iy intellekt va biznes boshqaruvi sohalarida yangi avlod kadrlarni tayyorlash,
- talabalarning xalqaro almashinuvini kengaytirish kabi vazifalarni amalga oshiradi.

<b>🎓 Ta'lim shakllari va tillari</b>

TIUda ta'lim:
- Kunduzgi,
- Sirtqi,
- Masofaviy shakllarda olib boriladi.

Ta'lim o'zbek va rus tillarida amalga oshiriladi.

<b>🏆 Afzalliklar</b>

✅ 100% grant va chegirma tizimi
✅ Masofaviy ta'lim imkoniyati
✅ Talabalar yotoqxonasi
✅ Markaziy joylashuv (Toshkent markazi)
✅ Xalqaro professor-o'qituvchilar tarkibi
✅ Qo'shma diplom dasturlari va almashinuv imkoniyati''',

    'ru': '''
<b>🏛 Дата основания и документы</b>

Tashkent International University был создан на основании <a href="https://lex.uz/uz/docs/-4584249">постановления Кабинета Министров Республики Узбекистан № 900</a> от 02.11.2019 года.

Деятельность университета осуществляется на основании <a href="https://license.gov.uz/registry/beb55034-934b-4754-b2e0-92364d5916b2">лицензии № 304988</a>, выданной Министерством высшего образования, науки и инноваций Республики Узбекистан.

<b>🎯 Основные цели и задачи</b>

Основная цель TIU — подготовка специалистов, соответствующих международным стандартам, обладающих практическими знаниями и навыками.

Университет:
- интеграция образования, науки и инноваций,
- внедрение совместных программ с зарубежными университетами,
- подготовка кадров нового поколения в области цифровых технологий, искусственного интеллекта и бизнес-управления,
- расширение международного обмена студентов.

<b>🎓 Формы и языки обучения</b>

В TIU обучение проводится в формах:
- Дневная,
- Заочная,
- Дистанционная.

Обучение ведется на узбекском и русском языках.

<b>🏆 Преимущества</b>

✅ Система 100% грантов и скидок
✅ Возможность дистанционного обучения
✅ Студенческое общежитие
✅ Центральное расположение (центр Ташкента)
✅ Международный профессорско-преподавательский состав
✅ Программы двойного диплома и возможности обмена''',

     'en': '''

<b>🏛 Foundation Date and Documents</b>

Tashkent International University was established based on <a href="https://lex.uz/uz/docs/-4584249">Resolution No. 900 of the Cabinet of Ministers of the Republic of Uzbekistan</a> dated November 2, 2019.

The university operates under <a href="https://license.gov.uz/registry/beb55034-934b-4754-b2e0-92364d5916b2">license No. 304988</a> issued by the Ministry of Higher Education, Science and Innovation of the Republic of Uzbekistan.

<b>🎯 Main Goals and Objectives</b>

The main goal of TIU is to train specialists who meet international standards and possess practical knowledge and skills.

The university:
- integrates education, science and innovation,
- implements joint programs with foreign universities,
- trains a new generation of specialists in digital technologies, artificial intelligence and business management,
- expands international student exchange.

<b>🎓 Forms and Languages of Education</b>

At TIU, education is provided in:
- Full-time,
- Part-time,
- Distance learning formats.

Education is conducted in Uzbek and Russian languages.

<b>🏆 Advantages</b>

✅ 100% grant and discount system
✅ Distance learning opportunities
✅ Student dormitory
✅ Central location (Tashkent city center)
✅ International faculty
✅ Double degree programs and exchange opportunities'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def partner_universities_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)
    texts = {
        'uz': '''🤝 <b>Toshkent Xalqaro Universitetining xalqaro hamkorlari</b>

Toshkent Xalqaro Universiteti (TIU) bugungi kunda Koreya, AQSh, Rossiya va Turkiyaning yetakchi oliy ta'lim muassasalari bilan hamkorlikda ishlaydi. Ushbu hamkorliklar doirasida qo'shma ta'lim dasturlari, professor-o'qituvchilar almashinuvi, xalqaro konferensiyalar, ilmiy loyihalar va talabalar almashinuvi yo'lga qo'yilgan.

<b>🇰🇷 Koreya Respublikasi universitetlari</b>

<a href="https://sejong.ac.kr">Sejong University</a> — qo'shma ta'lim dasturlari va talaba almashinuvi
<a href="https://ssu.ac.kr">Soongsil University</a> — IT va menejment yo'nalishlarida hamkorlik
<a href="https://sookmyung.ac.kr">Sookmyung Women's University</a> — gender ta'limi va psixologiya sohasida hamkorlik
<a href="https://dgist.ac.kr">DGIST</a> — texnologik tadqiqot loyihalari
<a href="https://hufs.ac.kr">HUFS</a> — xorijiy tillar va tarjima sohasida qo'shma dasturlar
<a href="https://konkuk.ac.kr">Konkuk University</a>, <a href="https://kookmin.ac.kr">Kookmin University</a> va <a href="https://kduniv.ac.kr">Kyungdong University</a> — talabalar uchun almashinuv dasturlari

<b>🇺🇸 AQSh universitetlari</b>

<a href="https://lewisu.edu">Lewis University</a> — biznes boshqaruvi va IT bo'yicha qo'shma dasturlar
<a href="https://goucher.edu">Goucher College</a> — ta'lim va ijtimoiy fanlar sohasida ilmiy almashuv
<a href="https://bridgeport.edu">University of Bridgeport</a> — onlayn o'qish va ilmiy loyihalar

<b>🇷🇺 Rossiya universitetlari</b>

<a href="https://ranepa.ru">RANHiGS</a> — iqtisodiyot va davlat boshqaruvi bo'yicha qo'shma dastur
<a href="https://rudn.ru">RUDN University</a> — magistratura bosqichida ilmiy almashinuv
<a href="https://susu.ru">Janubiy Ural davlat universiteti</a> — texnik ta'lim yo'nalishlarida hamkorlik

<b>🇹🇷 Turkiya universitetlari</b>

<a href="https://aydin.edu.tr">Istanbul Aydın University</a> — qo'shma seminarlar va ilmiy tadqiqotlar
<a href="https://ybu.edu.tr">Ankara Yildirim Beyazit University</a> — xalqaro huquq va tibbiyot

<b>🌍 Boshqa hamkor tashkilotlar</b>

<a href="https://koica.go.kr">KOICA</a> — Sun'iy intellekt markazi uchun 1 million dollar grant
<a href="https://www.turkicstates.org/en">TURKUNIB</a> — TIU 2025-2026 yillarda rais universiteti
<a href="https://erasmus-plus.ec.europa.eu">Erasmus+</a> — talabalar almashinuvi dasturi

<b>🌐 Hamkorlik yo'nalishlari</b>

✅ Qo'shma bakalavriat va magistratura dasturlari
✅ Talaba va professor almashinuvi
✅ Ilmiy-tadqiqot va innovatsion loyihalar
✅ Xalqaro konferensiyalar va forumlar
✅ Masofaviy ta'lim va onlayn kurslar''',

        'ru': '''🤝 <b>Международные партнеры Ташкентского международного университета</b>

Ташкентский международный университет (TIU) сегодня сотрудничает с ведущими высшими учебными заведениями Кореи, США, России и Турции. В рамках этого сотрудничества реализуются совместные образовательные программы, обмен преподавателями, международные конференции, научные проекты и студенческий обмен.

<b>🇰🇷 Университеты Республики Корея</b>

<a href="https://sejong.ac.kr">Sejong University</a> — совместные образовательные программы и студенческий обмен
<a href="https://ssu.ac.kr">Soongsil University</a> — сотрудничество в области IT и менеджмента
<a href="https://sookmyung.ac.kr">Sookmyung Women's University</a> — сотрудничество в области гендерного образования и психологии
<a href="https://dgist.ac.kr">DGIST</a> — технологические исследовательские проекты
<a href="https://hufs.ac.kr">HUFS</a> — совместные программы в области иностранных языков и перевода
<a href="https://konkuk.ac.kr">Konkuk University</a>, <a href="https://kookmin.ac.kr">Kookmin University</a> и <a href="https://kduniv.ac.kr">Kyungdong University</a> — программы обмена и стажировки

<b>🇺🇸 Университеты США</b>

<a href="https://lewisu.edu">Lewis University</a> — совместные программы по бизнес-управлению и IT
<a href="https://goucher.edu">Goucher College</a> — научный обмен в области образования и социальных наук
<a href="https://bridgeport.edu">University of Bridgeport</a> — сотрудничество в области онлайн-обучения

<b>🇷🇺 Университеты России</b>

<a href="https://ranepa.ru">РАНХиГС</a> — совместная программа по экономике и государственному управлению
<a href="https://rudn.ru">RUDN University</a> — научный обмен на уровне магистратуры
<a href="https://susu.ru">Южно-Уральский государственный университет</a> — сотрудничество в области технического образования

<b>🇹🇷 Университеты Турции</b>

<a href="https://aydin.edu.tr">Istanbul Aydın University</a> — совместные семинары и научные исследования
<a href="https://ybu.edu.tr">Ankara Yildirim Beyazit University</a> — сотрудничество в области международного права и медицины

<b>🌍 Другие партнерские организации</b>

<a href="https://koica.go.kr">KOICA</a> — грант в 1 млн долларов для создания Центра ИИ
<a href="https://www.turkicstates.org/en">TURKUNIB</a> — TIU университет-председатель в 2025–2026 годах
<a href="https://erasmus-plus.ec.europa.eu">Erasmus+</a> — программы студенческого обмена

<b>🌐 Направления сотрудничества</b>

✅ Совместные программы бакалавриата и магистратуры
✅ Обмен студентами и преподавателями
✅ Научно-исследовательские и инновационные проекты
✅ Международные конференции и форумы
✅ Дистанционное обучение и онлайн-курсы''',

        'en': '''🤝 <b>International Partners of Tashkent International University</b>

Tashkent International University (TIU) today collaborates with leading higher education institutions in Korea, the USA, Russia, and Turkey. Within the framework of this cooperation, joint educational programs, faculty exchange, international conferences, research projects, and student exchange are implemented.

<b>🇰🇷 Universities of the Republic of Korea</b>

<a href="https://sejong.ac.kr">Sejong University</a> — joint educational programs and student exchange
<a href="https://ssu.ac.kr">Soongsil University</a> — cooperation in IT and management
<a href="https://sookmyung.ac.kr">Sookmyung Women's University</a> — cooperation in gender education and psychology
<a href="https://dgist.ac.kr">DGIST</a> — technological research projects
<a href="https://hufs.ac.kr">HUFS</a> — joint programs in foreign languages and translation
<a href="https://konkuk.ac.kr">Konkuk University</a>, <a href="https://kookmin.ac.kr">Kookmin University</a>, and <a href="https://kduniv.ac.kr">Kyungdong University</a> — exchange programs and internships

<b>🇺🇸 Universities of the USA</b>

<a href="https://lewisu.edu">Lewis University</a> — joint programs in business management and IT
<a href="https://goucher.edu">Goucher College</a> — academic exchange in education and social sciences
<a href="https://bridgeport.edu">University of Bridgeport</a> — cooperation in online learning and research

<b>🇷🇺 Universities of Russia</b>

<a href="https://ranepa.ru">RANEPA</a> — joint program in economics and public administration
<a href="https://rudn.ru">RUDN University</a> — academic exchange at master's level
<a href="https://susu.ru">South Ural State University</a> — cooperation in technical education

<b>🇹🇷 Universities of Turkey</b>

<a href="https://aydin.edu.tr">Istanbul Aydın University</a> — joint seminars and research
<a href="https://ybu.edu.tr">Ankara Yildirim Beyazit University</a> — cooperation in international law and medicine

<b>🌍 Other Partner Organizations</b>

<a href="https://koica.go.kr">KOICA</a> — 1 million USD grant for AI Center establishment
<a href="https://www.turkicstates.org/en">TURKUNIB</a> — TIU as Chair University in 2025–2026
<a href="https://erasmus-plus.ec.europa.eu">Erasmus+</a> — student exchange programs

<b>🌐 Areas of Cooperation</b>

✅ Joint bachelor's and master's programs
✅ Student and faculty exchange
✅ Research and innovation projects
✅ International conferences and forums
✅ Distance learning and online courses'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def faculties_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)
    texts = {
        'uz': '''📚 <b>Fakultetlar va yo'nalishlar</b>

<b>🏢 1. Biznes va innovatsion ta'lim fakulteti</b>

Maqsad: zamonaviy iqtisodiyot, boshqaruv va ta'lim sohalarida xalqaro standartlarga javob beradigan malakali mutaxassislarni tayyorlash.

<b>Bakalavriat yo'nalishlari:</b>
- Biznes boshqaruvi (Business Administration)
- Xalqaro iqtisodiyot (International Economics)
- Menejment (Management)
- Marketing va reklama (Marketing and Advertising)
- Buxgalteriya hisobi va audit (Accounting and Auditing)
- Psixologiya (Psychology)
- Axborot texnologiyalari (Information Technologies)
- Ingliz tili (English Language and Literature)
- Koreys tili (Korean Language and Literature)
- Ta'lim (Pedagogy)

<b>Magistratura yo'nalishlari:</b>
- Biznes boshqaruvi (MBA)
- Jahon iqtisodiyoti va XIM

<b>⚖️ 2. Yurisprudensiya fakulteti</b>

Maqsad: huquqiy davlat qurilishi, xalqaro hamkorlik va adolatli jamiyat tamoyillariga xizmat qiluvchi yuridik mutaxassislarni tayyorlash.

<b>Bakalavriat yo'nalishlari:</b>
- Yurisprudensiya (Law)
- Xalqaro huquq (International Law)

<b>📘 Qo'shimcha ma'lumot</b>

✅ Ta'lim shakllari: kunduzgi, sirtqi, masofaviy
✅ Ta'lim tillari: o'zbek va rus
✅ O'qish muddati: bakalavriat — 4 yil, magistratura — 2 yil
✅ Diplom: TIU diplomi, hamda qo'shma dasturlar orqali xorijiy universitet diplomi olish imkoniyati mavjud''',

        'ru': '''📚 <b>Факультеты и направления</b>

<b>🏢 1. Факультет бизнеса и инновационного образования</b>

Цель: подготовка квалифицированных специалистов в области современной экономики, управления и образования, соответствующих международным стандартам.

<b>Направления бакалавриата:</b>
- Бизнес-администрирование (Business Administration)
- Международная экономика (International Economics)
- Менеджмент (Management)
- Маркетинг и реклама (Marketing and Advertising)
- Бухгалтерский учет и аудит (Accounting and Auditing)
- Психология (Psychology)
- Информационные технологии (Information Technologies)
- Английский язык (English Language and Literature)
- Корейский язык (Korean Language and Literature)
- Педагогика (Pedagogy)

<b>Направления магистратуры:</b>
- Бизнес-администрирование (MBA)
- Мировая экономика и МЭО

<b>⚖️ 2. Юридический факультет</b>

Цель: подготовка юридических специалистов, служащих принципам правового государства, международного сотрудничества и справедливого общества.

<b>Направления бакалавриата:</b>
- Юриспруденция (Law)
- Международное право (International Law)

<b>📘 Дополнительная информация</b>

✅ Формы обучения: дневная, заочная, дистанционная
✅ Языки обучения: узбекский и русский
✅ Срок обучения: бакалавриат — 4 года, магистратура — 2 года
✅ Диплом: диплом TIU, а также возможность получения диплома зарубежного университета через совместные программы''',

        'en': '''📚 <b>Faculties and Programs</b>

<b>🏢 1. Faculty of Business and Innovative Education</b>

Goal: training qualified specialists in modern economics, management and education that meet international standards.

<b>Bachelor's programs:</b>
- Business Administration
- International Economics
- Management
- Marketing and Advertising
- Accounting and Auditing
- Psychology
- Information Technologies
- English Language and Literature
- Korean Language and Literature
- Pedagogy

<b>Master's programs:</b>
- Business Administration (MBA)
- World Economy and International Economic Relations

<b>⚖️ 2. Faculty of Law</b>

Goal: training legal specialists who serve the principles of the rule of law, international cooperation and a just society.

<b>Bachelor's programs:</b>
- Law
- International Law

<b>📘 Additional Information</b>

✅ Forms of education: full-time, part-time, distance learning
✅ Languages of instruction: Uzbek and Russian
✅ Duration: bachelor's degree — 4 years, master's degree — 2 years
✅ Diploma: TIU diploma, as well as the opportunity to obtain a diploma from a foreign university through joint programs'''
    }

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_about_submenu_keyboard(user_id)
    )


async def video_tours_info(message: types.Message):
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    texts = {
        'uz': '''🏫 <b>3D Kampus Turi</b>

TIU atmosferasini hoziroq his eting 👇''',
        'ru': '''🏫 <b>3D-тур по кампусу</b>

Почувствуйте атмосферу TIU прямо сейчас 👇''',
        'en': '''🏫 <b>3D Campus Tour</b>

Experience the TIU atmosphere right now 👇'''
    }

    # Inline keyboard yaratish
    button_texts = {
        'uz': '🎥 3D sayohatni boshlash',
        'ru': '🎥 Начать 3D-тур',
        'en': '🎥 Start 3D tour'
    }

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=button_texts.get(lang, button_texts['uz']),
            url="https://test.tiu.uz/tour/"  # 3D sayohat web sayt manzilini bu yerga qo'ying
        )]
    ])

    await message.answer(
        texts.get(lang, texts['uz']),
        parse_mode="HTML",
        reply_markup=keyboard
    )


def register_about_handlers(dp: Dispatcher):
    dp.register_message_handler(
        about_tiu_handler,
        lambda message: message.text in ['🏫 TIU haqida', '🏫 О TIU', '🏫 About TIU']
    )
    dp.register_message_handler(
        about_university_info,
        lambda message: message.text in [
            '🎓 Universitet haqida qisqacha ma\'lumot',
            '🎓 Краткая информация об университете',
            '🎓 Brief information about university'
        ]
    )
    dp.register_message_handler(
        partner_universities_info,
        lambda message: message.text in [
            '🌍 Xalqaro hamkorliklar',
            '🌍 Международное сотрудничество',
            '🌍 International partnerships'
        ]
    )
    dp.register_message_handler(
        faculties_info,
        lambda message: message.text in [
            '📚 Fakultetlar va dasturlar',
            '📚 Факультеты и программы',
            '📚 Faculties and programs'
        ]
    )
    dp.register_message_handler(
        video_tours_info,
        lambda message: message.text in [
            '🎥 3D sayohat',
            '🎥 3D-тур',
            '🎥 3D tour'
        ]
    )