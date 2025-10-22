from database.db import Database

db = Database()

def t(user_id: int, key: str) -> str:
    '''Get translated text for user'''
    lang = db.get_user_language(user_id)
    from utils.translations import get_text
    return get_text(lang, key)

def is_admin(user_id: int) -> bool:
    '''Check if user is admin'''
    from config import ADMIN_IDS
    return user_id in ADMIN_IDS