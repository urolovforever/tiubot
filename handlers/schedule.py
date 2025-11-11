from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_direction_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
from database.db import Database
from states.forms import ScheduleStates
from utils.helpers import t

db = Database()


async def schedule_start_handler(message: types.Message, state: FSMContext):
    """Step 1: Choose faculty"""
    user_id = message.from_user.id

    await message.answer(
        t(user_id, 'choose_faculty'),
        reply_markup=get_faculty_keyboard(user_id)
    )
    await ScheduleStates.waiting_for_faculty.set()


async def process_faculty(message: types.Message, state: FSMContext):
    """Step 2: Choose course"""
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
        t(user_id, 'choose_course'),
        reply_markup=get_course_keyboard(user_id, faculty)
    )
    await ScheduleStates.waiting_for_course.set()


async def process_course(message: types.Message, state: FSMContext):
    """Step 3: Choose direction or group (for Yurisprudensiya)"""
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_faculty'),
            reply_markup=get_faculty_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_faculty.set()
        return

    course = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    await state.update_data(course=course)

    # Check if this is Yurisprudensiya (groups directly) or other faculty (directions first)
    from config import FACULTIES
    lang = db.get_user_language(user_id)
    faculties_lang = FACULTIES.get(lang, FACULTIES['uz'])

    if faculty in faculties_lang and course in faculties_lang[faculty]:
        course_data = faculties_lang[faculty][course]

        # If it's a list, then it's Yurisprudensiya - show schedule directly
        if isinstance(course_data, list):
            # This is Yurisprudensiya - the data is groups list
            # Show schedule directly (groups are in the direction keyboard)
            # We need to go to direction state, but it will act as group selection
            await message.answer(
                t(user_id, 'choose_group'),
                reply_markup=get_direction_keyboard(user_id, faculty, course)
            )
            await ScheduleStates.waiting_for_direction.set()
        else:
            # This is other faculty - show directions
            await message.answer(
                t(user_id, 'choose_direction'),
                reply_markup=get_direction_keyboard(user_id, faculty, course)
            )
            await ScheduleStates.waiting_for_direction.set()


async def process_direction(message: types.Message, state: FSMContext):
    """Step 4: Choose group (or show schedule for Yurisprudensiya)"""
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        await message.answer(
            t(user_id, 'choose_course'),
            reply_markup=get_course_keyboard(user_id, faculty)
        )
        await ScheduleStates.waiting_for_course.set()
        return

    direction_or_group = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    course = data.get('course')

    # Check if this is Yurisprudensiya or other faculty
    from config import FACULTIES
    lang = db.get_user_language(user_id)
    faculties_lang = FACULTIES.get(lang, FACULTIES['uz'])

    if faculty in faculties_lang and course in faculties_lang[faculty]:
        course_data = faculties_lang[faculty][course]

        if isinstance(course_data, list):
            # This is Yurisprudensiya - direction_or_group is actually a group
            # Show schedule directly (no direction in DB for Yurisprudensiya)
            group = direction_or_group

            # For Yurisprudensiya, direction field can be empty or same as faculty
            schedule_image = db.get_schedule_with_direction(faculty, '', course, group)

            if not schedule_image:
                # Try with faculty name as direction
                schedule_image = db.get_schedule_with_direction(faculty, faculty, course, group)

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
        else:
            # This is other faculty - direction_or_group is a direction
            direction = direction_or_group
            await state.update_data(direction=direction)

            # Get groups for this direction
            groups = course_data.get(direction, [])

            if not groups:
                # Try database
                groups = db.get_groups_by_faculty_direction_course(faculty, direction, course)

            await message.answer(
                t(user_id, 'choose_group'),
                reply_markup=get_group_keyboard(user_id, groups)
            )
            await ScheduleStates.waiting_for_group.set()


async def process_group(message: types.Message, state: FSMContext):
    """Step 5: Show schedule for selected group"""
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        data = await state.get_data()
        faculty = data.get('faculty')
        course = data.get('course')
        await message.answer(
            t(user_id, 'choose_direction'),
            reply_markup=get_direction_keyboard(user_id, faculty, course)
        )
        await ScheduleStates.waiting_for_direction.set()
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

