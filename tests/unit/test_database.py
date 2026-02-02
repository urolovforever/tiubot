"""
Unit tests for database operations.
Tests cover all CRUD operations for users, applications, events, contracts, and library.
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.db import Database, get_tashkent_now, TASHKENT_TZ


class TestDatabaseInitialization:
    """Test database initialization and table creation."""

    def test_database_creates_tables(self, temp_db):
        """Test that all required tables are created."""
        conn = temp_db.get_connection()
        cursor = conn.cursor()

        # Check all expected tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        expected_tables = {
            'users', 'applications', 'events', 'event_reminders',
            'schedules', 'channel_posts', 'library_categories',
            'library_books', 'library_downloads', 'library_favorites',
            'media_cache', 'student_contracts'
        }

        for table in expected_tables:
            assert table in tables, f"Table '{table}' should exist"


class TestUserOperations:
    """Test user-related database operations."""

    def test_save_user(self, temp_db, sample_user):
        """Test saving a new user."""
        temp_db.save_user(**sample_user)
        user = temp_db.get_user(sample_user['user_id'])

        assert user is not None
        assert user[0] == sample_user['user_id']
        assert user[1] == sample_user['username']
        assert user[2] == sample_user['full_name']
        assert user[3] == sample_user['language']

    def test_save_user_updates_existing(self, temp_db, sample_user):
        """Test that saving user with same ID updates existing record."""
        temp_db.save_user(**sample_user)

        # Update the user
        updated_user = sample_user.copy()
        updated_user['full_name'] = 'Updated Name'
        updated_user['language'] = 'ru'
        temp_db.save_user(**updated_user)

        user = temp_db.get_user(sample_user['user_id'])
        assert user[2] == 'Updated Name'
        assert user[3] == 'ru'

    def test_get_user_returns_none_for_nonexistent(self, temp_db):
        """Test that get_user returns None for non-existent user."""
        user = temp_db.get_user(999999999)
        assert user is None

    def test_get_all_users(self, temp_db, sample_user, sample_user_ru):
        """Test getting all user IDs."""
        temp_db.save_user(**sample_user)
        temp_db.save_user(**sample_user_ru)

        all_users = temp_db.get_all_users()

        assert len(all_users) == 2
        assert sample_user['user_id'] in all_users
        assert sample_user_ru['user_id'] in all_users

    def test_get_user_language(self, temp_db, sample_user):
        """Test getting user language."""
        temp_db.save_user(**sample_user)
        language = temp_db.get_user_language(sample_user['user_id'])
        assert language == sample_user['language']

    def test_get_user_language_default_for_nonexistent(self, temp_db):
        """Test that default language is returned for non-existent user."""
        language = temp_db.get_user_language(999999999)
        assert language == 'uz'  # Default language

    def test_update_user_language(self, temp_db, sample_user):
        """Test updating user language."""
        temp_db.save_user(**sample_user)
        temp_db.update_user_language(sample_user['user_id'], 'en')

        language = temp_db.get_user_language(sample_user['user_id'])
        assert language == 'en'


class TestApplicationOperations:
    """Test application-related database operations."""

    def test_create_application(self, temp_db, sample_application):
        """Test creating a new application."""
        app_id = temp_db.create_application(**sample_application)

        assert app_id > 0

        app = temp_db.get_application(app_id)
        assert app is not None
        assert app[1] == sample_application['user_id']
        assert app[5] == sample_application['message']

    def test_create_anonymous_application(self, temp_db, sample_application):
        """Test creating an anonymous application."""
        anon_app = sample_application.copy()
        anon_app['is_anonymous'] = True
        anon_app['phone_number'] = ''  # Anonymous apps don't have phone

        app_id = temp_db.create_application(**anon_app)
        app = temp_db.get_application(app_id)

        assert app is not None
        # is_anonymous column (index 12)
        assert app[12] == 1

    def test_get_new_applications(self, temp_db, sample_application):
        """Test getting new (unanswered) applications."""
        temp_db.create_application(**sample_application)
        temp_db.create_application(**sample_application)

        new_apps = temp_db.get_new_applications()

        assert len(new_apps) == 2
        for app in new_apps:
            assert app[7] == 'new'  # status column

    def test_update_application_response(self, temp_db, sample_application):
        """Test responding to an application."""
        app_id = temp_db.create_application(**sample_application)

        temp_db.update_application_response(app_id, "This is the admin response")

        app = temp_db.get_application(app_id)
        assert app[7] == 'answered'  # status
        assert app[9] == "This is the admin response"  # admin_response

    def test_get_user_applications(self, temp_db, sample_application):
        """Test getting applications by user."""
        # Create multiple applications
        for i in range(3):
            app = sample_application.copy()
            app['message'] = f'Application {i}'
            temp_db.create_application(**app)

        user_apps = temp_db.get_user_applications(sample_application['user_id'], limit=5)

        assert len(user_apps) == 3

    def test_cleanup_old_user_applications(self, temp_db, sample_application):
        """Test cleaning up old user applications."""
        # Create 7 applications
        for i in range(7):
            app = sample_application.copy()
            app['message'] = f'Application {i}'
            temp_db.create_application(**app)

        # Cleanup keeping only last 5
        deleted = temp_db.cleanup_old_user_applications(
            sample_application['user_id'],
            keep_last=5
        )

        assert deleted == 2  # 7 - 5 = 2 deleted

        remaining = temp_db.get_user_applications(sample_application['user_id'], limit=10)
        assert len(remaining) == 5

    def test_save_and_get_application_by_message_id(self, temp_db, sample_application):
        """Test saving and retrieving application by group message ID."""
        app_id = temp_db.create_application(**sample_application)
        message_id = 12345

        temp_db.save_application_message_id(app_id, message_id)

        app = temp_db.get_application_by_message_id(message_id)
        assert app is not None
        assert app[0] == app_id


class TestEventOperations:
    """Test event-related database operations."""

    def test_create_event(self, temp_db, sample_event):
        """Test creating a new event."""
        event_id = temp_db.create_event(**sample_event)

        assert event_id > 0

        event = temp_db.get_event(event_id)
        assert event is not None
        assert event[1] == sample_event['title']
        assert event[2] == sample_event['description']
        assert event[3] == sample_event['date']

    def test_get_all_events(self, temp_db, sample_event):
        """Test getting all events."""
        temp_db.create_event(**sample_event)

        event2 = sample_event.copy()
        event2['title'] = 'Second Event'
        temp_db.create_event(**event2)

        events = temp_db.get_all_events()

        assert len(events) == 2

    def test_get_upcoming_events_only(self, temp_db, sample_event):
        """Test filtering for upcoming events."""
        # Create a future event
        temp_db.create_event(**sample_event)

        # Create a past event
        past_event = sample_event.copy()
        past_event['title'] = 'Past Event'
        past_event['date'] = '01.01.2020'  # Past date
        temp_db.create_event(**past_event)

        upcoming = temp_db.get_all_events(upcoming_only=True)

        # Only future event should be returned
        assert len(upcoming) == 1
        assert upcoming[0][1] == sample_event['title']

    def test_update_event(self, temp_db, sample_event):
        """Test updating an event."""
        event_id = temp_db.create_event(**sample_event)

        temp_db.update_event(
            event_id,
            title='Updated Title',
            description='Updated description',
            date=sample_event['date'],
            time='15:00',
            location='New Location',
            registration_link='https://new-link.com'
        )

        event = temp_db.get_event(event_id)
        assert event[1] == 'Updated Title'
        assert event[4] == '15:00'  # time column
        assert event[5] == 'New Location'

    def test_delete_event(self, temp_db, sample_event):
        """Test deleting an event."""
        event_id = temp_db.create_event(**sample_event)

        temp_db.delete_event(event_id)

        event = temp_db.get_event(event_id)
        assert event is None

    def test_delete_event_removes_reminders(self, temp_db, sample_event, sample_user):
        """Test that deleting event also removes its reminders."""
        temp_db.save_user(**sample_user)
        event_id = temp_db.create_event(**sample_event)

        # Add a reminder
        temp_db.save_reminder(event_id, sample_user['user_id'], '24h')

        # Delete event
        temp_db.delete_event(event_id)

        # Check reminder is also deleted
        reminder_sent = temp_db.check_reminder_sent(
            event_id, sample_user['user_id'], '24h'
        )
        assert reminder_sent is False


class TestEventReminders:
    """Test event reminder operations."""

    def test_save_and_check_reminder(self, temp_db, sample_event, sample_user):
        """Test saving and checking reminder status."""
        temp_db.save_user(**sample_user)
        event_id = temp_db.create_event(**sample_event)

        # Initially no reminder sent
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '24h') is False

        # Save reminder
        temp_db.save_reminder(event_id, sample_user['user_id'], '24h')

        # Now should return True
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '24h') is True

        # Different reminder type should still be False
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '1h') is False

    def test_get_events_needing_reminders_24h(self, temp_db):
        """Test getting events that need 24-hour reminders."""
        # Create an event for ~24 hours from now
        now = get_tashkent_now()
        event_time = now + timedelta(hours=24)

        event = {
            'title': 'Tomorrow Event',
            'description': 'Test',
            'date': event_time.strftime('%d.%m.%Y'),
            'time': event_time.strftime('%H:%M'),
            'location': 'Test Location'
        }
        temp_db.create_event(**event)

        events = temp_db.get_events_needing_reminders(hours_before=24)

        # The event should be in the list
        assert len(events) >= 1


class TestScheduleOperations:
    """Test schedule-related database operations."""

    def test_save_schedule(self, temp_db):
        """Test saving a schedule."""
        schedule_id = temp_db.save_schedule(
            faculty='Business',
            course='1-kurs',
            group_name='EK-1-25',
            image_id='AgACAgIAAxkBAAI...'
        )

        assert schedule_id > 0

    def test_get_schedule(self, temp_db):
        """Test getting a schedule."""
        temp_db.save_schedule(
            faculty='Business',
            course='1-kurs',
            group_name='EK-1-25',
            image_id='test_image_id'
        )

        image_id = temp_db.get_schedule('Business', '1-kurs', 'EK-1-25')

        assert image_id == 'test_image_id'

    def test_get_schedule_returns_none_for_nonexistent(self, temp_db):
        """Test that non-existent schedule returns None."""
        image_id = temp_db.get_schedule('NonExistent', '1-kurs', 'XX-1-25')
        assert image_id is None

    def test_save_schedule_updates_existing(self, temp_db):
        """Test that saving schedule with same key updates the record."""
        temp_db.save_schedule('Faculty', '1-kurs', 'G1', 'old_image')
        temp_db.save_schedule('Faculty', '1-kurs', 'G1', 'new_image')

        image_id = temp_db.get_schedule('Faculty', '1-kurs', 'G1')
        assert image_id == 'new_image'

    def test_get_groups_by_faculty_course(self, temp_db):
        """Test getting groups by faculty and course."""
        temp_db.save_schedule('Business', '1-kurs', 'EK-1-25', 'img1')
        temp_db.save_schedule('Business', '1-kurs', 'EK-2-25', 'img2')
        temp_db.save_schedule('Business', '2-kurs', 'EK-1-24', 'img3')

        groups = temp_db.get_groups_by_faculty_course('Business', '1-kurs')

        assert len(groups) == 2
        assert 'EK-1-25' in groups
        assert 'EK-2-25' in groups


class TestContractOperations:
    """Test student contract database operations."""

    def test_save_contracts_from_excel(self, temp_db, sample_contracts_list):
        """Test bulk saving contracts from Excel data."""
        inserted = temp_db.save_contracts_from_excel(
            sample_contracts_list,
            'test_contracts.xlsx'
        )

        assert inserted == 3
        assert temp_db.get_contracts_count() == 3

    def test_save_contracts_replaces_existing(self, temp_db, sample_contracts_list):
        """Test that new upload replaces all existing contracts."""
        # First upload
        temp_db.save_contracts_from_excel(sample_contracts_list, 'file1.xlsx')

        # Second upload with fewer contracts
        new_contracts = [sample_contracts_list[0]]
        temp_db.save_contracts_from_excel(new_contracts, 'file2.xlsx')

        assert temp_db.get_contracts_count() == 1

    def test_get_contract_by_passport(self, temp_db, sample_contracts_list):
        """Test looking up contract by passport."""
        temp_db.save_contracts_from_excel(sample_contracts_list, 'test.xlsx')

        contract = temp_db.get_contract_by_passport('BB2222222')

        assert contract is not None
        assert contract[2] == 'Student Two'  # full_name
        assert contract[5] == 12000000.0  # total_amount

    def test_get_contract_by_passport_returns_none(self, temp_db, sample_contracts_list):
        """Test that non-existent passport returns None."""
        temp_db.save_contracts_from_excel(sample_contracts_list, 'test.xlsx')

        contract = temp_db.get_contract_by_passport('ZZ9999999')
        assert contract is None

    def test_get_last_contract_upload_date(self, temp_db, sample_contracts_list):
        """Test getting the last upload date."""
        temp_db.save_contracts_from_excel(sample_contracts_list, 'test.xlsx')

        upload_date = temp_db.get_last_contract_upload_date()

        assert upload_date is not None
        # Should be today's date
        assert datetime.now().strftime('%Y-%m-%d') in upload_date


class TestStatistics:
    """Test statistics-related operations."""

    def test_get_statistics_empty_db(self, temp_db):
        """Test statistics on empty database."""
        stats = temp_db.get_statistics()

        assert stats['total_users'] == 0
        assert stats['total_applications'] == 0
        assert stats['pending'] == 0

    def test_get_statistics_with_data(self, populated_db):
        """Test statistics with data."""
        stats = populated_db.get_statistics()

        assert stats['total_users'] == 2
        assert stats['total_applications'] == 1
        assert stats['pending'] == 1  # New app is pending


class TestMediaCache:
    """Test media cache operations."""

    def test_save_and_get_cached_file_id(self, temp_db):
        """Test caching and retrieving file IDs."""
        temp_db.save_cached_file_id('campus_photo_1', 'AgACAgIAAxkBAAI...')

        file_id = temp_db.get_cached_file_id('campus_photo_1')

        assert file_id == 'AgACAgIAAxkBAAI...'

    def test_get_cached_file_id_returns_none(self, temp_db):
        """Test that non-existent cache key returns None."""
        file_id = temp_db.get_cached_file_id('nonexistent_key')
        assert file_id is None

    def test_get_cached_media_group(self, temp_db):
        """Test getting a group of cached media files."""
        temp_db.save_cached_file_id('campus_1', 'file1')
        temp_db.save_cached_file_id('campus_2', 'file2')
        temp_db.save_cached_file_id('campus_3', 'file3')
        temp_db.save_cached_file_id('other_1', 'file4')

        campus_files = temp_db.get_cached_media_group('campus')

        assert len(campus_files) == 3
        assert 'file1' in campus_files
        assert 'file4' not in campus_files


class TestChannelPosts:
    """Test channel post tracking operations."""

    def test_save_and_get_channel_post(self, temp_db):
        """Test saving and retrieving channel post."""
        channel_id = '-1001234567890'
        message_id = 12345

        temp_db.save_channel_post(channel_id, message_id)

        retrieved_id = temp_db.get_channel_post(channel_id)

        assert retrieved_id == message_id

    def test_channel_post_updates_existing(self, temp_db):
        """Test that saving channel post updates existing record."""
        channel_id = '-1001234567890'

        temp_db.save_channel_post(channel_id, 100)
        temp_db.save_channel_post(channel_id, 200)

        message_id = temp_db.get_channel_post(channel_id)
        assert message_id == 200


class TestTimezoneOperations:
    """Test timezone-related functionality."""

    def test_get_tashkent_now(self):
        """Test that get_tashkent_now returns Tashkent timezone."""
        now = get_tashkent_now()

        assert now.tzinfo is not None
        # Tashkent is UTC+5
        assert now.utcoffset().total_seconds() == 5 * 3600

    def test_event_date_parsing(self, temp_db):
        """Test that event dates are correctly parsed."""
        event = {
            'title': 'Date Test Event',
            'description': 'Testing date parsing',
            'date': '25.12.2025',
            'time': '10:30',
            'location': 'Test'
        }
        event_id = temp_db.create_event(**event)

        retrieved = temp_db.get_event(event_id)
        assert retrieved[3] == '25.12.2025'  # date
        assert retrieved[4] == '10:30'  # time
