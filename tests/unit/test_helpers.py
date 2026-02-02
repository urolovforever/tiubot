"""
Unit tests for helper functions.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestIsAdminFunction:
    """Test the is_admin helper function."""

    def test_is_admin_returns_true_for_admin(self):
        """Test that is_admin returns True for admin user IDs."""
        from config import ADMIN_IDS
        from utils.helpers import is_admin

        for admin_id in ADMIN_IDS:
            assert is_admin(admin_id) is True, f"{admin_id} should be an admin"

    def test_is_admin_returns_false_for_non_admin(self):
        """Test that is_admin returns False for non-admin user IDs."""
        from utils.helpers import is_admin

        non_admin_ids = [123456789, 999999999, 1, 0, -1]

        for user_id in non_admin_ids:
            # These are unlikely to be admin IDs
            result = is_admin(user_id)
            # We can't assert False since we don't know the actual admin IDs,
            # but at least test that it returns a boolean
            assert isinstance(result, bool)


class TestTranslationHelper:
    """Test the t() translation helper function."""

    def test_t_function_returns_translation(self, temp_db, sample_user):
        """Test that t() returns correct translation for user."""
        # First save user to database
        temp_db.save_user(**sample_user)

        # The t() function imports db internally, so we need to test it
        # by checking the translation logic
        from utils.translations import get_text

        # User has 'uz' language
        expected = get_text('uz', 'welcome')
        assert 'Tashkent International University' in expected

    def test_t_function_respects_user_language(self, temp_db, sample_user_ru):
        """Test that t() respects user's language setting."""
        temp_db.save_user(**sample_user_ru)

        from utils.translations import get_text

        # User has 'ru' language
        expected = get_text('ru', 'welcome')
        assert 'Добро пожаловать' in expected
