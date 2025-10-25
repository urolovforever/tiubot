from aiogram.dispatcher.filters.state import State, StatesGroup

class ApplicationForm(StatesGroup):
    waiting_for_user_type = State()
    waiting_for_app_type = State()
    waiting_for_anonymity = State()  # Anonim yoki ochiq
    waiting_for_phone = State()  # Faqat ochiq murojaat uchun
    waiting_for_message = State()
    waiting_for_file_choice = State()  # Ha/Yo'q - fayl biriktirish
    waiting_for_file = State()
    waiting_for_confirmation = State()  # Tasdiqlash

class ScheduleStates(StatesGroup):
    waiting_for_faculty = State()
    waiting_for_direction = State()
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

# YANGI STATE - Broadcast uchun
class BroadcastState(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()

# Boshlang'ich til tanlash uchun state
class OnboardingState(StatesGroup):
    waiting_for_language = State()