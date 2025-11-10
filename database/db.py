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

        # Library categories table
        c.execute('''CREATE TABLE IF NOT EXISTS library_categories
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name_uz TEXT,
                      name_ru TEXT,
                      name_en TEXT,
                      emoji TEXT,
                      channel_id TEXT,
                      channel_username TEXT,
                      is_active INTEGER DEFAULT 1,
                      created_at TEXT)''')

        # Library books table
        c.execute('''CREATE TABLE IF NOT EXISTS library_books
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      category_id INTEGER,
                      title_uz TEXT,
                      title_ru TEXT,
                      title_en TEXT,
                      author TEXT,
                      year INTEGER,
                      pages INTEGER,
                      language TEXT,
                      description TEXT,
                      file_id TEXT,
                      channel_message_id INTEGER,
                      download_count INTEGER DEFAULT 0,
                      is_featured INTEGER DEFAULT 0,
                      created_at TEXT,
                      FOREIGN KEY (category_id) REFERENCES library_categories (id))''')

        # Library downloads table (statistics)
        c.execute('''CREATE TABLE IF NOT EXISTS library_downloads
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      book_id INTEGER,
                      user_id INTEGER,
                      downloaded_at TEXT,
                      FOREIGN KEY (book_id) REFERENCES library_books (id))''')

        # Library favorites table
        c.execute('''CREATE TABLE IF NOT EXISTS library_favorites
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      book_id INTEGER,
                      user_id INTEGER,
                      added_at TEXT,
                      UNIQUE(book_id, user_id),
                      FOREIGN KEY (book_id) REFERENCES library_books (id))''')

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
                     location: str, image_id: Optional[str] = None,
                     time: Optional[str] = None, registration_link: Optional[str] = None) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO events (title, description, date, time, location, registration_link, image_id, created_at)
                   VALUES (?,?,?,?,?,?,?,?)''',
                (title, description, date, time, location, registration_link, image_id,
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

    def get_all_events(self, upcoming_only: bool = False) -> List[Tuple]:
        """Get all events, optionally filter upcoming events only, sorted by date (nearest first)"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Barcha tadbirlarni olish
            c.execute("SELECT * FROM events")
            all_events = c.fetchall()

            # Agar faqat kelajakdagi tadbirlar kerak bo'lsa, Python'da filter qilamiz
            if upcoming_only:
                from datetime import datetime
                today = datetime.now().date()

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
                        # Agar sana parse bo'lmasa, o'sha tadbirni ham qo'shamiz (xatolikni oldini olish)
                        logger.warning(f"Event #{event[0]}: Could not parse date '{event_date_str}': {e}")
                        filtered_events.append(event)

                # Sana bo'yicha tartiblash (yaqindan uzoqqa)
                filtered_events.sort(key=lambda e: self._parse_event_date(e[3]))
                return filtered_events
            else:
                # Barcha tadbirlarni sana bo'yicha tartiblash
                all_events_sorted = sorted(all_events, key=lambda e: self._parse_event_date(e[3]))
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
                (event_id, user_id, reminder_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        """Get events that need reminders (1 day or 1 hour before)"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT * FROM events
                WHERE datetime(date || ' ' || COALESCE(time, '00:00'))
                      BETWEEN datetime('now')
                      AND datetime('now', '+{hours_before} hours', '+30 minutes')
            """)
            return c.fetchall()
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
                (channel_id, message_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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

    # === LIBRARY METHODS ===

    def get_all_library_categories(self, lang: str = 'uz') -> List[Tuple]:
        """Get all active library categories with book counts"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT c.id, c.name_{lang}, c.emoji, COUNT(b.id) as book_count
                FROM library_categories c
                LEFT JOIN library_books b ON c.id = b.category_id
                WHERE c.is_active = 1
                GROUP BY c.id
                ORDER BY c.id
            """)
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting library categories: {e}")
            return []
        finally:
            conn.close()

    def get_library_category(self, category_id: int) -> Optional[Tuple]:
        """Get a single library category"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM library_categories WHERE id=?", (category_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting library category: {e}")
            return None
        finally:
            conn.close()

    def get_books_by_category(self, category_id: int, limit: int = 15, offset: int = 0, lang: str = 'uz') -> List[Tuple]:
        """Get books by category with pagination"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT id, title_{lang}, author, year, file_id, download_count
                FROM library_books
                WHERE category_id = ?
                ORDER BY id
                LIMIT ? OFFSET ?
            """, (category_id, limit, offset))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting books by category: {e}")
            return []
        finally:
            conn.close()

    def get_books_count_by_category(self, category_id: int) -> int:
        """Get total count of books in a category"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM library_books WHERE category_id=?", (category_id,))
            return c.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting books count: {e}")
            return 0
        finally:
            conn.close()

    def get_book(self, book_id: int) -> Optional[Tuple]:
        """Get a single book by ID"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM library_books WHERE id=?", (book_id,))
            return c.fetchone()
        except Exception as e:
            logger.error(f"Error getting book: {e}")
            return None
        finally:
            conn.close()

    def search_books(self, query: str, category_id: Optional[int] = None, lang: str = 'uz') -> List[Tuple]:
        """Search books by title or author"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            search_pattern = f"%{query}%"
            if category_id:
                c.execute(f"""
                    SELECT id, title_{lang}, author, year, file_id
                    FROM library_books
                    WHERE category_id = ? AND (title_{lang} LIKE ? OR author LIKE ?)
                    ORDER BY download_count DESC
                    LIMIT 20
                """, (category_id, search_pattern, search_pattern))
            else:
                c.execute(f"""
                    SELECT id, title_{lang}, author, year, file_id
                    FROM library_books
                    WHERE title_{lang} LIKE ? OR author LIKE ?
                    ORDER BY download_count DESC
                    LIMIT 20
                """, (search_pattern, search_pattern))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error searching books: {e}")
            return []
        finally:
            conn.close()

    def increment_book_download(self, book_id: int, user_id: int):
        """Increment book download count and save to statistics"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Increment counter
            c.execute("UPDATE library_books SET download_count = download_count + 1 WHERE id=?", (book_id,))

            # Save to downloads table
            c.execute(
                "INSERT INTO library_downloads (book_id, user_id, downloaded_at) VALUES (?,?,?)",
                (book_id, user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Error incrementing book download: {e}")
        finally:
            conn.close()

    def toggle_favorite_book(self, book_id: int, user_id: int) -> bool:
        """Toggle favorite status for a book. Returns True if added, False if removed"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Check if already in favorites
            c.execute("SELECT id FROM library_favorites WHERE book_id=? AND user_id=?", (book_id, user_id))
            existing = c.fetchone()

            if existing:
                # Remove from favorites
                c.execute("DELETE FROM library_favorites WHERE book_id=? AND user_id=?", (book_id, user_id))
                conn.commit()
                return False
            else:
                # Add to favorites
                c.execute(
                    "INSERT INTO library_favorites (book_id, user_id, added_at) VALUES (?,?,?)",
                    (book_id, user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error toggling favorite: {e}")
            return False
        finally:
            conn.close()

    def get_user_favorites(self, user_id: int, lang: str = 'uz') -> List[Tuple]:
        """Get user's favorite books"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT b.id, b.title_{lang}, b.author, b.year, b.file_id
                FROM library_books b
                JOIN library_favorites f ON b.id = f.book_id
                WHERE f.user_id = ?
                ORDER BY f.added_at DESC
            """, (user_id,))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting user favorites: {e}")
            return []
        finally:
            conn.close()

    def get_featured_books(self, lang: str = 'uz', limit: int = 20) -> List[Tuple]:
        """Get featured/recommended books"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT id, title_{lang}, author, year, file_id, download_count
                FROM library_books
                WHERE is_featured = 1
                ORDER BY download_count DESC
                LIMIT ?
            """, (limit,))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Error getting featured books: {e}")
            return []
        finally:
            conn.close()

    def get_library_statistics(self) -> dict:
        """Get library statistics for admin"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Total books
            c.execute("SELECT COUNT(*) FROM library_books")
            total_books = c.fetchone()[0]

            # Total downloads
            c.execute("SELECT COUNT(*) FROM library_downloads")
            total_downloads = c.fetchone()[0]

            # Unique users who downloaded
            c.execute("SELECT COUNT(DISTINCT user_id) FROM library_downloads")
            active_users = c.fetchone()[0]

            # Top categories
            c.execute("""
                SELECT c.name_uz, COUNT(d.id) as download_count
                FROM library_categories c
                JOIN library_books b ON c.id = b.category_id
                JOIN library_downloads d ON b.id = d.book_id
                GROUP BY c.id
                ORDER BY download_count DESC
                LIMIT 5
            """)
            top_categories = c.fetchall()

            # Top books
            c.execute("""
                SELECT title_uz, download_count
                FROM library_books
                ORDER BY download_count DESC
                LIMIT 5
            """)
            top_books = c.fetchall()

            return {
                'total_books': total_books,
                'total_downloads': total_downloads,
                'active_users': active_users,
                'top_categories': top_categories,
                'top_books': top_books
            }
        except Exception as e:
            logger.error(f"Error getting library statistics: {e}")
            return {}
        finally:
            conn.close()