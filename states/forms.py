from aiogram.dispatcher.filters.state import State, StatesGroup

class ApplicationForm(StatesGroup):
    waiting_for_user_type = State()
    waiting_for_app_type = State()
    waiting_for_message = State()
    waiting_for_phone = State()
    waiting_for_file = State()

class ScheduleStates(StatesGroup):
    waiting_for_faculty = State()
    waiting_for_course = State()
    waiting_for_group = State()

class AdminReplyState(StatesGroup):
    waiting_for_reply = State()

class EventCreateState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_date = State()
    waiting_for_location = State()
    waiting_for_image = State()

class EventDeleteState(StatesGroup):
    waiting_for_event_choice = State()