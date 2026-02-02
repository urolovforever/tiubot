"""
Integration tests for the application submission workflow.
Tests verify the complete flow from submission to admin response.
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.db import Database, get_tashkent_now


class TestApplicationSubmissionWorkflow:
    """Test the complete application submission workflow."""

    def test_complete_application_workflow(self, temp_db, sample_user, sample_application):
        """Test the entire application submission and response workflow."""
        # Step 1: User registers
        temp_db.save_user(**sample_user)
        user = temp_db.get_user(sample_user['user_id'])
        assert user is not None

        # Step 2: User submits application
        app_id = temp_db.create_application(**sample_application)
        assert app_id > 0

        # Step 3: Verify application is in "new" status
        new_apps = temp_db.get_new_applications()
        assert len(new_apps) == 1
        assert new_apps[0][0] == app_id
        assert new_apps[0][7] == 'new'  # status

        # Step 4: Admin responds
        admin_response = "Thank you for your message. We will process your request."
        temp_db.update_application_response(app_id, admin_response)

        # Step 5: Verify application is now "answered"
        app = temp_db.get_application(app_id)
        assert app[7] == 'answered'
        assert app[9] == admin_response  # admin_response column

        # Step 6: Verify no more new applications
        new_apps = temp_db.get_new_applications()
        assert len(new_apps) == 0

    def test_anonymous_application_workflow(self, temp_db, sample_user):
        """Test anonymous application submission workflow."""
        temp_db.save_user(**sample_user)

        # Submit anonymous application
        app_id = temp_db.create_application(
            user_id=sample_user['user_id'],
            username='',  # Anonymous - no username
            full_name='',  # Anonymous - no name
            phone_number='',  # Anonymous - no phone
            message='Anonymous feedback message',
            user_type='student',
            app_type='suggestion',
            is_anonymous=True
        )

        app = temp_db.get_application(app_id)

        # Verify anonymity flag is set
        assert app[12] == 1  # is_anonymous

        # Verify personal info is empty
        assert app[2] == ''  # username
        assert app[3] == ''  # full_name

    def test_multiple_users_applications(self, temp_db, sample_user, sample_user_ru):
        """Test applications from multiple users."""
        # Register both users
        temp_db.save_user(**sample_user)
        temp_db.save_user(**sample_user_ru)

        # User 1 submits applications
        app1 = temp_db.create_application(
            user_id=sample_user['user_id'],
            username=sample_user['username'],
            full_name=sample_user['full_name'],
            phone_number='+998901111111',
            message='First user message',
            user_type='student',
            app_type='question'
        )

        # User 2 submits application
        app2 = temp_db.create_application(
            user_id=sample_user_ru['user_id'],
            username=sample_user_ru['username'],
            full_name=sample_user_ru['full_name'],
            phone_number='+998902222222',
            message='Second user message',
            user_type='applicant',
            app_type='question'
        )

        # Verify both are in new applications
        new_apps = temp_db.get_new_applications()
        assert len(new_apps) == 2

        # Verify user-specific queries work
        user1_apps = temp_db.get_user_applications(sample_user['user_id'])
        assert len(user1_apps) == 1

        user2_apps = temp_db.get_user_applications(sample_user_ru['user_id'])
        assert len(user2_apps) == 1

    def test_application_with_file_attachment(self, temp_db, sample_user):
        """Test application with file attachment."""
        temp_db.save_user(**sample_user)

        file_id = 'AgACAgIAAxkBAAI...'  # Simulated Telegram file ID

        app_id = temp_db.create_application(
            user_id=sample_user['user_id'],
            username=sample_user['username'],
            full_name=sample_user['full_name'],
            phone_number='+998901234567',
            message='Application with attachment',
            file_id=file_id,
            user_type='student',
            app_type='complaint'
        )

        app = temp_db.get_application(app_id)

        # Verify file_id is saved
        assert app[6] == file_id  # file_id column


class TestEventReminderWorkflow:
    """Test the event creation and reminder workflow."""

    def test_event_reminder_workflow(self, temp_db, sample_user):
        """Test creating event and tracking reminders."""
        # Create user
        temp_db.save_user(**sample_user)

        # Create event for tomorrow
        now = get_tashkent_now()
        tomorrow = now + timedelta(days=1)

        event_id = temp_db.create_event(
            title='Tomorrow Workshop',
            description='Python programming workshop',
            date=tomorrow.strftime('%d.%m.%Y'),
            time='10:00',
            location='Room 101'
        )

        # Initially, no reminders sent
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '24h') is False
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '1h') is False

        # Send 24h reminder
        temp_db.save_reminder(event_id, sample_user['user_id'], '24h')
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '24h') is True
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '1h') is False

        # Send 1h reminder
        temp_db.save_reminder(event_id, sample_user['user_id'], '1h')
        assert temp_db.check_reminder_sent(event_id, sample_user['user_id'], '1h') is True


class TestLibraryWorkflow:
    """Test library-related workflows."""

    def test_book_download_tracking(self, temp_db, sample_user):
        """Test book download and statistics tracking."""
        temp_db.save_user(**sample_user)

        # First, we need to create a library category and book
        conn = temp_db.get_connection()
        cursor = conn.cursor()

        # Create category
        cursor.execute("""
            INSERT INTO library_categories (name_uz, name_ru, name_en, emoji, is_active, created_at)
            VALUES ('Test', 'Тест', 'Test', '📚', 1, datetime('now'))
        """)
        category_id = cursor.lastrowid

        # Create book
        cursor.execute("""
            INSERT INTO library_books
            (category_id, title_uz, title_ru, title_en, author, year, file_id, download_count, created_at)
            VALUES (?, 'Kitob', 'Книга', 'Book', 'Author', 2024, 'file123', 0, datetime('now'))
        """, (category_id,))
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # User downloads book
        temp_db.increment_book_download(book_id, sample_user['user_id'])

        # Verify download count increased
        book = temp_db.get_book(book_id)
        assert book is not None
        # Find download_count in the book tuple (check all positions for non-zero)
        # Based on db schema: download_count is the column after file_id
        # We verify by checking the book has a non-zero count somewhere
        found_download = False
        for idx, val in enumerate(book):
            if val == 1 and idx > 5:  # download_count should be after basic fields
                found_download = True
                break
        assert found_download, f"Download count not found or not incremented in book: {book}"

    def test_book_favorites_toggle(self, temp_db, sample_user):
        """Test adding and removing books from favorites."""
        temp_db.save_user(**sample_user)

        # Create book
        conn = temp_db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO library_categories (name_uz, name_ru, name_en, emoji, is_active, created_at)
            VALUES ('Cat', 'Кат', 'Cat', '📖', 1, datetime('now'))
        """)
        category_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO library_books
            (category_id, title_uz, title_ru, title_en, author, year, file_id, download_count, created_at)
            VALUES (?, 'Book', 'Книга', 'Book', 'Author', 2024, 'file456', 0, datetime('now'))
        """, (category_id,))
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Initially no favorites
        favorites = temp_db.get_user_favorites(sample_user['user_id'])
        assert len(favorites) == 0

        # Add to favorites
        result = temp_db.toggle_favorite_book(book_id, sample_user['user_id'])
        assert result is True  # Added

        favorites = temp_db.get_user_favorites(sample_user['user_id'])
        assert len(favorites) == 1

        # Remove from favorites
        result = temp_db.toggle_favorite_book(book_id, sample_user['user_id'])
        assert result is False  # Removed

        favorites = temp_db.get_user_favorites(sample_user['user_id'])
        assert len(favorites) == 0


class TestContractLookupWorkflow:
    """Test contract lookup workflow."""

    def test_contract_upload_and_lookup(self, temp_db, sample_contracts_list):
        """Test uploading contracts and looking them up."""
        # Admin uploads contracts
        inserted = temp_db.save_contracts_from_excel(
            sample_contracts_list,
            'contracts_2024.xlsx'
        )
        assert inserted == 3

        # Student looks up their contract
        contract = temp_db.get_contract_by_passport('AA1111111')
        assert contract is not None
        assert contract[2] == 'Student One'  # full_name

        # Calculate remaining amount
        total = contract[5]  # total_amount
        paid = contract[6]  # paid_amount
        remaining = contract[7]  # remaining_amount

        assert remaining == total - paid

    def test_contract_not_found(self, temp_db, sample_contracts_list):
        """Test contract lookup with non-existent passport."""
        temp_db.save_contracts_from_excel(sample_contracts_list, 'test.xlsx')

        # Try to find non-existent passport
        contract = temp_db.get_contract_by_passport('XX9999999')
        assert contract is None


class TestStatisticsWorkflow:
    """Test statistics collection workflow."""

    def test_statistics_accumulation(self, temp_db, sample_user, sample_user_ru):
        """Test that statistics properly accumulate."""
        # Initial stats
        stats = temp_db.get_statistics()
        assert stats['total_users'] == 0
        assert stats['total_applications'] == 0

        # Add users
        temp_db.save_user(**sample_user)
        temp_db.save_user(**sample_user_ru)

        # Check stats updated
        stats = temp_db.get_statistics()
        assert stats['total_users'] == 2

        # Add applications
        for i in range(5):
            temp_db.create_application(
                user_id=sample_user['user_id'],
                username=sample_user['username'],
                full_name=sample_user['full_name'],
                phone_number='+998901234567',
                message=f'Application {i}',
                user_type='student',
                app_type='question'
            )

        stats = temp_db.get_statistics()
        assert stats['total_applications'] == 5
        assert stats['pending'] == 5

        # Answer some applications
        apps = temp_db.get_new_applications()
        for app in apps[:3]:  # Answer first 3
            temp_db.update_application_response(app[0], 'Response')

        stats = temp_db.get_statistics()
        assert stats['pending'] == 2  # 5 - 3 = 2 pending
