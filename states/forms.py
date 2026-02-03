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
    waiting_for_time = State()
    waiting_for_location = State()
    waiting_for_registration_link = State()
    waiting_for_image = State()

class EventDeleteState(StatesGroup):
    waiting_for_event_choice = State()

class EventEditState(StatesGroup):
    waiting_for_field_value = State()
    waiting_for_event_choice = State()

# YANGI - Sodda tadbir yuklash (nom, rasm+caption, sana)
class EventQuickCreateState(StatesGroup):
    waiting_for_title = State()  # Tadbir nomi
    waiting_for_post = State()  # Rasm + caption (tavsif)
    waiting_for_date = State()  # Sana
    waiting_for_confirmation = State()  # Tasdiqlash

# UNIVERSAL BROADCAST STATE - Har qanday Telegram content type uchun
class BroadcastState(StatesGroup):
    waiting_for_content = State()  # Har qanday content type: text, photo, video, audio, document, poll, etc.
    waiting_for_confirmation = State()  # Tasdiqlash

# Boshlang'ich til tanlash uchun state
class OnboardingState(StatesGroup):
    waiting_for_language = State()

# Schedule upload states (admin)
class ScheduleUploadState(StatesGroup):
    waiting_for_faculty = State()
    waiting_for_course = State()
    waiting_for_direction = State()
    waiting_for_group = State()
    waiting_for_image = State()

# Contract lookup states (student)
class ContractLookupState(StatesGroup):
    waiting_for_passport = State()

# Contract upload states (admin)
class ContractUploadState(StatesGroup):
    waiting_for_excel = State()