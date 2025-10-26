from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_direction_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
from database.db import Database
from states.forms import ScheduleStates
from utils.helpers import t

db = Database()


async def schedule_start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        t(user_id, 'choose_faculty'),
        reply_markup=get_faculty_keyboard(user_id)
    )
    await ScheduleStates.waiting_for_faculty.set()


async def process_faculty(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await state.finish()
        await message.answer(
            t(user_id, 'main_menu'),
            reply_markup=get_main_keyboard(user_id)
        )
        return

    faculty = message.text
    await state.update_data(faculty=faculty)

    await message.answer(
        t(user_id, 'choose_direction'),
        reply_markup=get_direction_keyboard(user_id, faculty)
    )
    await ScheduleStates.waiting_for_direction.set()


async def process_direction(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_faculty'),
            reply_markup=get_faculty_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_faculty.set()
        return

    direction = message.text
    data = await state.get_data()
    faculty = data.get('faculty')

    await state.update_data(direction=direction)

    await message.answer(
        t(user_id, 'choose_course'),
        reply_markup=get_course_keyboard(user_id, faculty, direction)
    )
    await ScheduleStates.waiting_for_course.set()


async def process_course(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        await message.answer(
            t(user_id, 'choose_direction'),
            reply_markup=get_direction_keyboard(user_id, faculty)
        )
        await ScheduleStates.waiting_for_direction.set()
        return

    course = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    direction = data.get('direction')

    await state.update_data(course=course)

    # Get groups from FACULTIES config
    from config import FACULTIES
    lang = db.get_user_language(user_id)
    faculties_lang = FACULTIES.get(lang, FACULTIES['uz'])

    groups = []
    if faculty in faculties_lang and direction in faculties_lang[faculty] and course in faculties_lang[faculty][direction]:
        groups = faculties_lang[faculty][direction][course]

    # If no groups found in config, try database
    if not groups:
        groups = db.get_groups_by_faculty_direction_course(faculty, direction, course)

    # If still no groups, use empty list (will show message)
    if not groups:
        groups = []

    await message.answer(
        t(user_id, 'choose_group'),
        reply_markup=get_group_keyboard(user_id, groups)
    )
    await ScheduleStates.waiting_for_group.set()


async def process_group(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        direction = data.get('direction')
        await message.answer(
            t(user_id, 'choose_course'),
            reply_markup=get_course_keyboard(user_id, faculty, direction)
        )
        await ScheduleStates.waiting_for_course.set()
        return

    group = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    direction = data.get('direction')
    course = data.get('course')

    schedule_image = db.get_schedule_with_direction(faculty, direction, course, group)

    if schedule_image:
        await message.answer_photo(
            schedule_image,
            caption=t(user_id, 'schedule_success')
        )
    else:
        await message.answer(t(user_id, 'schedule_not_found'))

    await state.finish()
    await message.answer(
        t(user_id, 'main_menu'),
        reply_markup=get_main_keyboard(user_id)
    )


def register_schedule_handlers(dp: Dispatcher):
    dp.register_message_handler(
        schedule_start_handler,
        lambda message: message.text in ['📅 Dars jadvali', '📅 Расписание', '📅 Schedule'],
        state='*'
    )
    dp.register_message_handler(process_faculty, state=ScheduleStates.waiting_for_faculty)
    dp.register_message_handler(process_direction, state=ScheduleStates.waiting_for_direction)
    dp.register_message_handler(process_course, state=ScheduleStates.waiting_for_course)
    dp.register_message_handler(process_group, state=ScheduleStates.waiting_for_group)

