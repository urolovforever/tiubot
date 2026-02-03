import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Tashkent timezone (UTC+5)
try:
    from zoneinfo import ZoneInfo
    TASHKENT_TZ = ZoneInfo("Asia/Tashkent")
except ImportError:
    # Fallback for Python < 3.9
    from datetime import timezone
    TASHKENT_TZ = timezone(timedelta(hours=5))


def get_tashkent_now():
    """Tashkent vaqti bo'yicha hozirgi vaqtni qaytaradi"""
    return datetime.now(TASHKENT_TZ)


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

        # Migration: Add group_message_id column for tracking messages in admin group
        try:
            c.execute("ALTER TABLE applications ADD COLUMN group_message_id INTEGER")
        except:
            pass

        # Migration: Add answered_at column for tracking when response was sent
        try:
            c.execute("ALTER TABLE applications ADD COLUMN answered_at TEXT")
        except:
            pass

        # Events table
        c.execute('''CREATE TABLE IF NOT EXISTS events
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      description TEXT,
                      date TEXT,
                      time TEXT,
                      location TEXT,
                      registration_link TEXT,
                      image_id TEXT,
                      created_at TEXT)''')

        # Migration: Add time and registration_link columns to events table
        try:
            c.execute("ALTER TABLE events ADD COLUMN time TEXT")
        except:
            pass  # Column already exists

        try:
            c.execute("ALTER TABLE events ADD COLUMN registration_link TEXT")
        except:
            pass  # Column already exists

        # Event reminders table - to track sent reminders
        c.execute('''CREATE TABLE IF NOT EXISTS event_reminders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      event_id INTEGER,
                      user_id INTEGER,
                      reminder_type TEXT,
                      sent_at TEXT,
                      FOREIGN KEY (event_id) REFERENCES events (id))''')

        # Schedules table
        c.execute('''CREATE TABLE IF NOT EXISTS schedules
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      faculty TEXT,
                      direction TEXT,
                      course TEXT,
                      group_name TEXT,
                      image_id TEXT,
                      created_at TEXT)''')

        # Channel posts table - to store latest digest post
        c.execute('''CREATE TABLE IF NOT EXISTS channel_posts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      channel_id TEXT,
                      message_id INTEGER,
                      post_date TEXT,
                      UNIQUE(channel_id))''')

        # Media cache table - to store file_ids for faster loading
        c.execute('''CREATE TABLE IF NOT EXISTS media_cache
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      media_key TEXT UNIQUE,
                      file_id TEXT,
                      cached_at TEXT)''')

        # Student contracts table - stores contract information from Excel
        c.execute('''CREATE TABLE IF NOT EXISTS student_contracts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      passport_series TEXT UNIQUE,
                      full_name TEXT,
                      jshshir TEXT,
                      course TEXT,
                      total_amount REAL,
                      paid_amount REAL,
                      remaining_amount REAL,
                      upload_date TEXT,
                      excel_filename TEXT)''')

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
                 get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
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
                 get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"), None, user_type, app_type, 1 if is_anonymous else 0)
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

    def get_answered_applications(self, days: int = 7) -> List[Tuple]:
        """
        Javob berilgan murojaatlar (faqat oxirgi N kun)
        Default: 7 kun
        """
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Tashkent vaqti bo'yicha N kun oldingi sana
            cutoff_date = (get_tashkent_now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

            c.execute(
                """SELECT * FROM applications
                   WHERE status='answered'
                   AND created_at >= ?
                   ORDER BY created_at DESC""",
                (cutoff_date,)
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

    def get_user_applications(self, user_id: int, limit: int = 5) -> List[Tuple]:
        """
        Foydalanuvchining murojaatlarini olish (oxirgi N ta)
        Returns: (id, message, status, created_at, admin_response, answered_at)
        """
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                """SELECT id, message, status, created_at, admin_response, answered_at
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

    def cleanup_old_user_applications(self, user_id: int, keep_last: int = 5) -> int:
        """
        Foydalanuvchining eski murojaatlarini o'chirish (faqat oxirgi N ta saqlanadi)
        Returns: O'chirilgan murojaatlar soni
        """
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Oxirgi N ta murojaatni saqlash, qolganlarini o'chirish
            c.execute(
                """DELETE FROM applications
                   WHERE user_id=?
                   AND id NOT IN (
                       SELECT id FROM applications
                       WHERE user_id=?
                       ORDER BY created_at DESC
                       LIMIT ?
                   )""",
                (user_id, user_id, keep_last)
            )
            deleted_count = c.rowcount
            conn.commit()
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old applications for user {user_id}")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up user applications: {e}")
            return 0
        finally:
            conn.close()

    def update_application_response(self, app_id: int, response: str):
        """Murojaatga javob berish va javob berilgan vaqtni saqlash"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            answered_at = get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "UPDATE applications SET admin_response=?, status='answered', answered_at=? WHERE id=?",
                (response, answered_at, app_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating application: {e}")
        finally:
            conn.close()

    def save_application_message_id(self, app_id: int, message_id: int):
        """Guruhda yuborilgan murojaat message ID sini saqlash"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "UPDATE applications SET group_message_id=? WHERE id=?",
                (message_id, app_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving message ID: {e}")
        finally:
            conn.close()

    def get_application_by_message_id(self, message_id: int) -> Optional[Tuple]:
        """Guruh message ID bo'yicha murojaatni topish"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM applications WHERE group_message_id=?", (message_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting application by message ID: {e}")
            return None
        finally:
            conn.close()

    def cleanup_old_answered_applications(self, days: int = 7) -> int:
        """
        N kundan eski javob berilgan murojaatlarni o'chirish
        Default: 7 kun
        Returns: O'chirilgan murojaatlar soni
        """
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Tashkent vaqti bo'yicha N kun oldingi sana
            cutoff_date = (get_tashkent_now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

            # Avval nechta o'chirilishini sanash
            c.execute(
                """SELECT COUNT(*) FROM applications
                   WHERE status='answered'
                   AND created_at < ?""",
                (cutoff_date,)
            )
            count = c.fetchone()[0]

            # O'chirish
            if count > 0:
                c.execute(
                    """DELETE FROM applications
                       WHERE status='answered'
                       AND created_at < ?""",
                    (cutoff_date,)
                )
                conn.commit()
                logger.info(f"Cleaned up {count} old answered applications (older than {days} days)")

            return count
        except Exception as e:
            logger.error(f"Error cleaning up old applications: {e}")
            return 0
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

            # Tashkent vaqti bo'yicha cutoff sanani hisoblash
            cutoff_date = (get_tashkent_now() - timedelta(days=days)).strftime("%Y-%m-%d")

            # Yangi foydalanuvchilar
            c.execute("""
                SELECT COUNT(*) FROM users
                WHERE date(registration_date) >= ?
            """, (cutoff_date,))
            new_users = c.fetchone()[0]

            # Yangi murojaatlar
            c.execute("""
                SELECT COUNT(*) FROM applications
                WHERE date(created_at) >= ?
            """, (cutoff_date,))
            new_applications = c.fetchone()[0]

            # Javob berilgan murojaatlar
            c.execute("""
                SELECT COUNT(*) FROM applications
                WHERE status='answered' AND date(created_at) >= ?
            """, (cutoff_date,))
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
                     location: str, image_id: Optional[str] = None,
                     time: Optional[str] = None, registration_link: Optional[str] = None) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO events (title, description, date, time, location, registration_link, image_id, created_at)
                   VALUES (?,?,?,?,?,?,?,?)''',
                (title, description, date, time, location, registration_link, image_id,
                 get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            event_id = c.lastrowid
            conn.commit()
            return event_id
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return 0
        finally:
            conn.close()

    def get_all_events(self, upcoming_only: bool = False) -> List[Tuple]:
        """Get all events, optionally filter upcoming events only, sorted by creation time (newest first)"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Barcha tadbirlarni olish
            c.execute("SELECT * FROM events")
            all_events = c.fetchall()

            # Agar faqat kelajakdagi tadbirlar kerak bo'lsa, Python'da filter qilamiz
            if upcoming_only:
                # Tashkent vaqti bo'yicha bugungi sana
                today = datetime.now(TASHKENT_TZ).date()

                filtered_events = []
                for event in all_events:
                    # event[3] = date (DD.MM.YYYY formatida)
                    event_date_str = event[3]
                    try:
                        # DD.MM.YYYY formatidan datetime.date ga o'tkazish
                        event_date = datetime.strptime(event_date_str, '%d.%m.%Y').date()
                        # Bugungi yoki kelajakdagi tadbirlar
                        if event_date >= today:
                            filtered_events.append(event)
                    except Exception as e:
                        # Agar sana parse bo'lmasa, xatolik log qilamiz va tadbir qo'shilmaydi
                        logger.warning(f"Event #{event[0]}: Could not parse date '{event_date_str}': {e}")

                # Created_at bo'yicha tartiblash (eng yangi birinchi)
                # event[8] = created_at
                filtered_events.sort(key=lambda e: e[8], reverse=True)
                return filtered_events
            else:
                # Barcha tadbirlarni created_at bo'yicha tartiblash (eng yangi birinchi)
                all_events_sorted = sorted(all_events, key=lambda e: e[8], reverse=True)
                return all_events_sorted

        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []
        finally:
            conn.close()

    def _parse_event_date(self, date_str: str):
        """Helper function to parse event date for sorting"""
        from datetime import datetime
        try:
            return datetime.strptime(date_str, '%d.%m.%Y')
        except:
            # Agar parse qilib bo'lmasa, katta sana qaytaramiz (oxirga qo'yish uchun)
            return datetime(9999, 12, 31)

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
            # Also delete related reminders
            c.execute("DELETE FROM event_reminders WHERE event_id=?", (event_id,))
            conn.commit()
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
        finally:
            conn.close()

    def update_event(self, event_id: int, title: str, description: str, date: str,
                     time: str, location: str, registration_link: Optional[str] = None,
                     image_id: Optional[str] = None):
        """Update an existing event"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            if image_id:
                c.execute(
                    """UPDATE events SET title=?, description=?, date=?, time=?, location=?,
                       registration_link=?, image_id=? WHERE id=?""",
                    (title, description, date, time, location, registration_link, image_id, event_id)
                )
            else:
                c.execute(
                    """UPDATE events SET title=?, description=?, date=?, time=?, location=?,
                       registration_link=? WHERE id=?""",
                    (title, description, date, time, location, registration_link, event_id)
                )
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating event: {e}")
        finally:
            conn.close()

    # Event reminders
    def save_reminder(self, event_id: int, user_id: int, reminder_type: str):
        """Save that a reminder was sent to a user"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO event_reminders (event_id, user_id, reminder_type, sent_at)
                   VALUES (?,?,?,?)''',
                (event_id, user_id, reminder_type, get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving reminder: {e}")
        finally:
            conn.close()

    def check_reminder_sent(self, event_id: int, user_id: int, reminder_type: str) -> bool:
        """Check if a reminder was already sent"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT id FROM event_reminders WHERE event_id=? AND user_id=? AND reminder_type=?",
                (event_id, user_id, reminder_type)
            )
            return c.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking reminder: {e}")
            return False
        finally:
            conn.close()

    def get_events_needing_reminders(self, hours_before: int) -> List[Tuple]:
        """
        Get events that need reminders (24 hours or 1 hour before)
        Uses Tashkent timezone for comparison
        """
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Barcha tadbirlarni olish
            c.execute("SELECT * FROM events")
            all_events = c.fetchall()

            # Tashkent vaqti bo'yicha hozirgi vaqt
            now = get_tashkent_now()

            # hours_before soatdan keyin bo'ladigan tadbirlarni topish
            if hours_before == 24:
                # 1 kun oldin: 23-25 soat orasida
                min_time = now + timedelta(hours=23)
                max_time = now + timedelta(hours=25)
            elif hours_before == 1:
                # 1 soat oldin: 55 daqiqa - 65 daqiqa orasida
                min_time = now + timedelta(minutes=55)
                max_time = now + timedelta(minutes=65)
            else:
                min_time = now + timedelta(hours=hours_before - 0.5)
                max_time = now + timedelta(hours=hours_before + 0.5)

            events_needing_reminder = []
            for event in all_events:
                # event[3] = date (DD.MM.YYYY), event[4] = time (HH:MM)
                date_str = event[3]
                time_str = event[4] if event[4] else "00:00"

                try:
                    # DD.MM.YYYY HH:MM formatidan datetime ga o'tkazish
                    day, month, year = date_str.split('.')

                    # Vaqtni parse qilish
                    if ':' in time_str:
                        # Agar vaqt range bo'lsa (10:00-12:00), birinchisini olish
                        if '-' in time_str:
                            time_str = time_str.split('-')[0].strip()
                        hour, minute = time_str.split(':')[:2]
                    else:
                        hour, minute = 0, 0

                    # Tashkent timezone bilan datetime yaratish
                    event_datetime = datetime(
                        int(year), int(month), int(day),
                        int(hour), int(minute),
                        tzinfo=TASHKENT_TZ
                    )

                    # Agar tadbir kerakli vaqt oralig'ida bo'lsa
                    if min_time <= event_datetime <= max_time:
                        events_needing_reminder.append(event)

                except Exception as e:
                    logger.warning(f"Event #{event[0]}: Could not parse datetime '{date_str} {time_str}': {e}")

            return events_needing_reminder

        except Exception as e:
            logger.error(f"Error getting events for reminders: {e}")
            return []
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
                     get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
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

    def get_groups_by_faculty_direction_course(self, faculty: str, direction: str, course: str) -> List[str]:
        """Get groups by faculty, direction, and course"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT DISTINCT group_name FROM schedules WHERE faculty=? AND direction=? AND course=?",
                (faculty, direction, course)
            )
            return [row[0] for row in c.fetchall()]
        except Exception as e:
            logger.error(f"Error getting groups by faculty, direction, course: {e}")
            return []
        finally:
            conn.close()

    def get_schedule_with_direction(self, faculty: str, direction: str, course: str, group_name: str) -> Optional[str]:
        """Get schedule image by faculty, direction, course, and group"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT image_id FROM schedules WHERE faculty=? AND direction=? AND course=? AND group_name=?",
                (faculty, direction, course, group_name)
            )
            result = c.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting schedule with direction: {e}")
            return None
        finally:
            conn.close()

    def save_channel_post(self, channel_id: str, message_id: int):
        """Save or update the latest channel post message ID"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT OR REPLACE INTO channel_posts (channel_id, message_id, post_date)
                   VALUES (?, ?, ?)''',
                (channel_id, message_id, get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving channel post: {e}")
        finally:
            conn.close()

    def get_channel_post(self, channel_id: str) -> Optional[int]:
        """Get the latest channel post message ID"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT message_id FROM channel_posts WHERE channel_id=?",
                (channel_id,)
            )
            result = c.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting channel post: {e}")
            return None
        finally:
            conn.close()

    # ==================== MEDIA CACHE ====================

    def get_cached_file_id(self, media_key: str) -> Optional[str]:
        """Get cached file_id by media key"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT file_id FROM media_cache WHERE media_key=?", (media_key,))
            result = c.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting cached file_id: {e}")
            return None
        finally:
            conn.close()

    def save_cached_file_id(self, media_key: str, file_id: str):
        """Save file_id to cache"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT OR REPLACE INTO media_cache (media_key, file_id, cached_at) VALUES (?, ?, ?)",
                (media_key, file_id, get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving cached file_id: {e}")
        finally:
            conn.close()

    def get_cached_media_group(self, group_key: str) -> Optional[List[str]]:
        """Get all file_ids for a media group (e.g., 'campus' or 'career')"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "SELECT file_id FROM media_cache WHERE media_key LIKE ? ORDER BY media_key",
                (f"{group_key}_%",)
            )
            results = c.fetchall()
            return [r[0] for r in results] if results else None
        except Exception as e:
            logger.error(f"Error getting cached media group: {e}")
            return None
        finally:
            conn.close()

    # ==================== CONTRACT METHODS ====================

    def save_contracts_from_excel(self, contracts_data: List[dict], excel_filename: str) -> int:
        """Save contract data from Excel file, replacing all existing data"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Delete all existing contract data
            c.execute("DELETE FROM student_contracts")

            # Insert new data
            upload_date = get_tashkent_now().strftime("%Y-%m-%d %H:%M:%S")
            inserted_count = 0

            for contract in contracts_data:
                try:
                    c.execute(
                        '''INSERT INTO student_contracts
                           (passport_series, full_name, jshshir, course, total_amount, paid_amount, remaining_amount, upload_date, excel_filename)
                           VALUES (?,?,?,?,?,?,?,?,?)''',
                        (
                            contract.get('passport_series'),
                            contract.get('full_name'),
                            contract.get('jshshir'),
                            contract.get('course'),
                            contract.get('total_amount'),
                            contract.get('paid_amount'),
                            contract.get('remaining_amount'),
                            upload_date,
                            excel_filename
                        )
                    )
                    inserted_count += 1
                except Exception as e:
                    logger.warning(f"Error inserting contract {contract.get('passport_series')}: {e}")
                    continue

            conn.commit()
            return inserted_count
        except Exception as e:
            logger.error(f"Error saving contracts: {e}")
            return 0
        finally:
            conn.close()

    def get_contract_by_passport(self, passport_series: str) -> Optional[Tuple]:
        """Get contract information by passport series"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM student_contracts WHERE passport_series=?", (passport_series,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting contract: {e}")
            return None
        finally:
            conn.close()

    def get_contracts_count(self) -> int:
        """Get total number of contracts in database"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM student_contracts")
            return c.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting contracts count: {e}")
            return 0
        finally:
            conn.close()

    def get_last_contract_upload_date(self) -> Optional[str]:
        """Get the date of last contract upload"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT upload_date FROM student_contracts ORDER BY upload_date DESC LIMIT 1")
            result = c.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting last upload date: {e}")
            return None
        finally:
            conn.close()