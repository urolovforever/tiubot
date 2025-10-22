from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.reply import get_faculty_keyboard, get_course_keyboard, get_group_keyboard, get_main_keyboard
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
        t(user_id, 'choose_course'),
        reply_markup=get_course_keyboard(user_id)
    )
    await ScheduleStates.waiting_for_course.set()


async def process_course(message: types.Message, state: FSMContext):
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

    groups = db.get_groups_by_faculty_course(faculty, course)

    if not groups:
        groups = [f'{course[0]}01-20', f'{course[0]}02-20', f'{course[0]}03-20', f'{course[0]}04-20']

    await message.answer(
        t(user_id, 'choose_group'),
        reply_markup=get_group_keyboard(user_id, groups)
    )
    await ScheduleStates.waiting_for_group.set()


async def process_group(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['⬅️ Orqaga', '⬅️ Назад', '⬅️ Back']:
        await message.answer(
            t(user_id, 'choose_course'),
            reply_markup=get_course_keyboard(user_id)
        )
        await ScheduleStates.waiting_for_course.set()
        return

    group = message.text
    data = await state.get_data()
    faculty = data.get('faculty')
    course = data.get('course')

    schedule_image = db.get_schedule(faculty, course, group)

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
    dp.register_message_handler(process_course, state=ScheduleStates.waiting_for_course)
    dp.register_message_handler(process_group, state=ScheduleStates.waiting_for_group)

