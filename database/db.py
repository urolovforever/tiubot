import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_name: str = 'tiu_bot.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()

        # Users table (5 ustun)
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY, 
                      username TEXT, 
                      full_name TEXT,
                      language TEXT DEFAULT 'uz',
                      registration_date TEXT)''')

        # Applications table (12 ustun - username, phone_number, user_type, app_type, is_anonymous bilan)
        c.execute('''CREATE TABLE IF NOT EXISTS applications
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      username TEXT,
                      full_name TEXT,
                      phone_number TEXT,
                      message TEXT,
                      file_id TEXT,
                      status TEXT DEFAULT 'new',
                      created_at TEXT,
                      admin_response TEXT,
                      user_type TEXT,
                      app_type TEXT,
                      is_anonymous INTEGER DEFAULT 0)''')

        # Migration: Yangi column lar qo'shish (agar mavjud table da bo'lmasa)
        try:
            c.execute("ALTER TABLE applications ADD COLUMN user_type TEXT")
        except:
            pass  # Column allaqachon mavjud

        try:
            c.execute("ALTER TABLE applications ADD COLUMN app_type TEXT")
        except:
            pass

        try:
            c.execute("ALTER TABLE applications ADD COLUMN is_anonymous INTEGER DEFAULT 0")
        except:
            pass

        # Events table
        c.execute('''CREATE TABLE IF NOT EXISTS events
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      description TEXT,
                      date TEXT,
                      location TEXT,
                      image_id TEXT,
                      created_at TEXT)''')

        # Schedules table
        c.execute('''CREATE TABLE IF NOT EXISTS schedules
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      faculty TEXT,
                      direction TEXT,
                      course TEXT,
                      group_name TEXT,
                      image_id TEXT,
                      created_at TEXT)''')

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def save_user(self, user_id: int, username: str, full_name: str, language: str = 'uz'):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT OR REPLACE INTO users VALUES (?,?,?,?,?)",
                (user_id, username, full_name, language,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving user: {e}")
        finally:
            conn.close()

    def get_user(self, user_id: int) -> Optional[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
        finally:
            conn.close()

    def get_all_users(self) -> List[int]:
        """Barcha foydalanuvchilar ID larini olish (broadcast uchun)"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT user_id FROM users")
            return [row[0] for row in c.fetchall()]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
        finally:
            conn.close()

    def get_user_language(self, user_id: int) -> str:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
            result = c.fetchone()
            return result[0] if result else 'uz'
        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            return 'uz'
        finally:
            conn.close()

    def update_user_language(self, user_id: int, language: str):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating language: {e}")
        finally:
            conn.close()

    # Applications
    def create_application(self, user_id: int, username: str, full_name: str,
                           phone_number: str, message: str, file_id: Optional[str] = None,
                           user_type: str = '', app_type: str = '', is_anonymous: bool = False) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO applications
                   (user_id, username, full_name, phone_number, message, file_id, status, created_at, admin_response, user_type, app_type, is_anonymous)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (user_id, username, full_name, phone_number, message, file_id, 'new',
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, user_type, app_type, 1 if is_anonymous else 0)
            )
            app_id = c.lastrowid
            conn.commit()
            return app_id
        except Exception as e:
            logger.error(f"Error creating application: {e}")
            return 0
        finally:
            conn.close()

    def get_new_applications(self) -> List[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT * FROM applications WHERE status='new' ORDER BY created_at DESC"
            )
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting applications: {e}")
            return []
        finally:
            conn.close()

    def get_answered_applications(self) -> List[Tuple]:
        """Javob berilgan murojaatlar"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT * FROM applications WHERE status='answered' ORDER BY created_at DESC"
            )
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting answered applications: {e}")
            return []
        finally:
            conn.close()

    def get_application(self, app_id: int) -> Optional[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM applications WHERE id=?", (app_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting application: {e}")
            return None
        finally:
            conn.close()

    def get_user_applications(self, user_id: int, limit: int = 10) -> List[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                """SELECT id, message, status, created_at 
                   FROM applications 
                   WHERE user_id=? 
                   ORDER BY created_at DESC 
                   LIMIT ?""",
                (user_id, limit)
            )
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting user applications: {e}")
            return []
        finally:
            conn.close()

    def update_application_response(self, app_id: int, response: str):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "UPDATE applications SET admin_response=?, status='answered' WHERE id=?",
                (response, app_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating application: {e}")
        finally:
            conn.close()

    def get_statistics(self, period: str = 'week') -> dict:
        """Statistika olish"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            if period == 'week':
                days = 7
            elif period == 'month':
                days = 30
            else:
                days = 7

            # Yangi foydalanuvchilar
            c.execute(f"""
                SELECT COUNT(*) FROM users 
                WHERE date(registration_date) >= date('now', '-{days} days')
            """)
            new_users = c.fetchone()[0]

            # Yangi murojaatlar
            c.execute(f"""
                SELECT COUNT(*) FROM applications 
                WHERE date(created_at) >= date('now', '-{days} days')
            """)
            new_applications = c.fetchone()[0]

            # Javob berilgan murojaatlar
            c.execute(f"""
                SELECT COUNT(*) FROM applications 
                WHERE status='answered' AND date(created_at) >= date('now', '-{days} days')
            """)
            answered = c.fetchone()[0]

            # Javob berilmagan
            c.execute("SELECT COUNT(*) FROM applications WHERE status='new'")
            pending = c.fetchone()[0]

            # Jami foydalanuvchilar
            c.execute("SELECT COUNT(*) FROM users")
            total_users = c.fetchone()[0]

            # Jami murojaatlar
            c.execute("SELECT COUNT(*) FROM applications")
            total_apps = c.fetchone()[0]

            return {
                'new_users': new_users,
                'new_applications': new_applications,
                'answered': answered,
                'pending': pending,
                'total_users': total_users,
                'total_applications': total_apps
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
        finally:
            conn.close()

    # Events
    def create_event(self, title: str, description: str, date: str,
                     location: str, image_id: Optional[str] = None) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO events (title, description, date, location, image_id, created_at)
                   VALUES (?,?,?,?,?,?)''',
                (title, description, date, location, image_id,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            event_id = c.lastrowid
            conn.commit()
            return event_id
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return 0
        finally:
            conn.close()

    def get_all_events(self) -> List[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM events ORDER BY date DESC")
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []
        finally:
            conn.close()

    def get_event(self, event_id: int) -> Optional[Tuple]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM events WHERE id=?", (event_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting event: {e}")
            return None
        finally:
            conn.close()

    def delete_event(self, event_id: int):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("DELETE FROM events WHERE id=?", (event_id,))
            conn.commit()
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
        finally:
            conn.close()

    # Schedules
    def save_schedule(self, faculty: str, course: str, group_name: str, image_id: str) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Check if exists
            c.execute(
                "SELECT id FROM schedules WHERE faculty=? AND course=? AND group_name=?",
                (faculty, course, group_name)
            )
            existing = c.fetchone()

            if existing:
                c.execute(
                    "UPDATE schedules SET image_id=? WHERE id=?",
                    (image_id, existing[0])
                )
                schedule_id = existing[0]
            else:
                c.execute(
                    '''INSERT INTO schedules (faculty, course, group_name, image_id, created_at)
                       VALUES (?,?,?,?,?)''',
                    (faculty, course, group_name, image_id,
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                schedule_id = c.lastrowid

            conn.commit()
            return schedule_id
        except Exception as e:
            logger.error(f"Error saving schedule: {e}")
            return 0
        finally:
            conn.close()

    def get_schedule(self, faculty: str, course: str, group_name: str) -> Optional[str]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT image_id FROM schedules WHERE faculty=? AND course=? AND group_name=?",
                (faculty, course, group_name)
            )
            result = c.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting schedule: {e}")
            return None
        finally:
            conn.close()

    def get_groups_by_faculty_course(self, faculty: str, course: str) -> List[str]:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT DISTINCT group_name FROM schedules WHERE faculty=? AND course=?",
                (faculty, course)
            )
            return [row[0] for row in c.fetchall()]
        except Exception as e:
            logger.error(f"Error getting groups: {e}")
            return []
        finally:
            conn.close()