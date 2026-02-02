"""
Unit tests for translation system.
Tests verify that all translation keys exist and are consistent across languages.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.translations import TRANSLATIONS, get_text


class TestTranslationStructure:
    """Test the structure and completeness of translations."""

    def test_all_languages_exist(self):
        """Test that all required languages are defined."""
        required_languages = ['uz', 'ru', 'en']

        for lang in required_languages:
            assert lang in TRANSLATIONS, f"Language '{lang}' should exist in translations"

    def test_all_keys_exist_in_all_languages(self):
        """Test that all translation keys exist in all languages."""
        # Get keys from Uzbek (base language)
        uz_keys = set(TRANSLATIONS['uz'].keys())
        ru_keys = set(TRANSLATIONS['ru'].keys())
        en_keys = set(TRANSLATIONS['en'].keys())

        # Check Russian has all Uzbek keys
        missing_in_ru = uz_keys - ru_keys
        assert not missing_in_ru, f"Keys missing in Russian: {missing_in_ru}"

        # Check English has all Uzbek keys
        missing_in_en = uz_keys - en_keys
        assert not missing_in_en, f"Keys missing in English: {missing_in_en}"

        # Check Uzbek has all Russian keys (reverse check)
        extra_in_ru = ru_keys - uz_keys
        assert not extra_in_ru, f"Extra keys in Russian: {extra_in_ru}"

        # Check Uzbek has all English keys (reverse check)
        extra_in_en = en_keys - uz_keys
        assert not extra_in_en, f"Extra keys in English: {extra_in_en}"

    def test_no_empty_translations(self):
        """Test that no translation value is empty."""
        for lang, translations in TRANSLATIONS.items():
            for key, value in translations.items():
                assert value, f"Translation for '{key}' in '{lang}' should not be empty"
                assert value.strip(), f"Translation for '{key}' in '{lang}' should not be whitespace only"


class TestGetTextFunction:
    """Test the get_text helper function."""

    def test_get_text_returns_correct_translation(self):
        """Test that get_text returns correct translation for given language and key."""
        uz_welcome = get_text('uz', 'welcome')
        ru_welcome = get_text('ru', 'welcome')
        en_welcome = get_text('en', 'welcome')

        # Check they're different (translations should differ)
        assert uz_welcome != ru_welcome
        assert ru_welcome != en_welcome

        # Check they contain expected content
        assert 'Tashkent International University' in uz_welcome
        assert 'Добро пожаловать' in ru_welcome
        assert 'Welcome' in en_welcome

    def test_get_text_default_language_fallback(self):
        """Test that invalid language falls back to Uzbek."""
        result = get_text('invalid_lang', 'welcome')
        uz_result = get_text('uz', 'welcome')

        assert result == uz_result

    def test_get_text_returns_key_for_missing_key(self):
        """Test that missing key returns the key itself."""
        result = get_text('uz', 'nonexistent_key_xyz')

        # Should return the key name when key doesn't exist
        assert result == 'nonexistent_key_xyz'

    def test_get_text_with_all_essential_keys(self):
        """Test that essential keys work in all languages."""
        essential_keys = [
            'welcome', 'main_menu', 'back', 'cancel',
            'settings', 'admin_panel', 'statistics',
            'events', 'applications', 'schedule'
        ]

        for lang in ['uz', 'ru', 'en']:
            for key in essential_keys:
                result = get_text(lang, key)
                assert result != key, f"Key '{key}' should have translation in '{lang}'"


class TestTranslationContent:
    """Test specific translation content requirements."""

    def test_menu_buttons_have_emojis(self):
        """Test that main menu buttons have emojis for visual appeal."""
        emoji_keys = [
            'about_tiu', 'admission', 'students', 'schedule',
            'events', 'applications', 'news', 'contact', 'settings'
        ]

        for lang in ['uz', 'ru', 'en']:
            for key in emoji_keys:
                value = get_text(lang, key)
                # Check that value contains at least one emoji-like character
                # Emojis are typically in certain Unicode ranges
                has_emoji = any(ord(c) > 127 for c in value)
                assert has_emoji, f"'{key}' in '{lang}' should have emoji"

    def test_contact_info_consistency(self):
        """Test that contact info is consistent across languages."""
        # All languages should have same phone number and email
        for lang in ['uz', 'ru', 'en']:
            contact = get_text(lang, 'contact_text')
            assert '+998 71 200 09 09' in contact, f"Phone number missing in {lang}"
            assert 'info@tiu.uz' in contact, f"Email missing in {lang}"
            assert 'www.tiu.uz' in contact, f"Website missing in {lang}"

    def test_error_messages_exist(self):
        """Test that error/not found messages exist."""
        error_keys = [
            'schedule_not_found', 'no_events', 'event_not_found',
            'library_book_not_found', 'library_no_search_results',
            'library_no_favorites'
        ]

        for lang in ['uz', 'ru', 'en']:
            for key in error_keys:
                value = get_text(lang, key)
                assert value != key, f"Error message '{key}' should exist in '{lang}'"

    def test_success_messages_exist(self):
        """Test that success/confirmation messages exist."""
        success_keys = [
            'application_sent', 'event_created', 'event_updated',
            'event_deleted', 'response_sent', 'language_changed',
            'broadcast_completed'
        ]

        for lang in ['uz', 'ru', 'en']:
            for key in success_keys:
                value = get_text(lang, key)
                assert value != key, f"Success message '{key}' should exist in '{lang}'"

    def test_library_translations_complete(self):
        """Test that all library-related translations exist."""
        library_keys = [
            'library', 'library_title', 'library_category_books',
            'library_books_list', 'library_book_downloading',
            'library_book_details', 'library_book_sent',
            'library_book_not_found', 'library_search_prompt',
            'library_search_results', 'library_no_search_results',
            'library_favorite_added', 'library_favorite_removed',
            'library_favorites', 'library_no_favorites', 'library_featured'
        ]

        for lang in ['uz', 'ru', 'en']:
            for key in library_keys:
                value = get_text(lang, key)
                assert value != key, f"Library key '{key}' should exist in '{lang}'"

    def test_event_reminder_translations(self):
        """Test that event reminder message templates exist and have placeholders."""
        reminder_keys = ['event_reminder_1day', 'event_reminder_1hour']

        for lang in ['uz', 'ru', 'en']:
            for key in reminder_keys:
                value = get_text(lang, key)
                assert '{title}' in value, f"'{key}' in '{lang}' should have {{title}} placeholder"
                assert '{location}' in value, f"'{key}' in '{lang}' should have {{location}} placeholder"
                assert '{time}' in value, f"'{key}' in '{lang}' should have {{time}} placeholder"

    def test_broadcast_translations_have_placeholders(self):
        """Test that broadcast messages have required placeholders."""
        # broadcast_confirm should have {count} and {message}
        for lang in ['uz', 'ru', 'en']:
            confirm = get_text(lang, 'broadcast_confirm')
            assert '{count}' in confirm, f"broadcast_confirm in '{lang}' should have {{count}}"
            assert '{message}' in confirm, f"broadcast_confirm in '{lang}' should have {{message}}"

            # broadcast_completed should have {success} and {failed}
            completed = get_text(lang, 'broadcast_completed')
            assert '{success}' in completed, f"broadcast_completed in '{lang}' should have {{success}}"
            assert '{failed}' in completed, f"broadcast_completed in '{lang}' should have {{failed}}"


class TestTranslationCount:
    """Test translation statistics and coverage."""

    def test_minimum_translation_count(self):
        """Test that we have a minimum number of translations."""
        min_expected_keys = 50  # Minimum expected translations

        for lang in ['uz', 'ru', 'en']:
            key_count = len(TRANSLATIONS[lang])
            assert key_count >= min_expected_keys, \
                f"Language '{lang}' should have at least {min_expected_keys} keys, has {key_count}"

    def test_translation_counts_match(self):
        """Test that all languages have the same number of translations."""
        uz_count = len(TRANSLATIONS['uz'])
        ru_count = len(TRANSLATIONS['ru'])
        en_count = len(TRANSLATIONS['en'])

        assert uz_count == ru_count, \
            f"Uzbek ({uz_count}) and Russian ({ru_count}) should have same key count"
        assert ru_count == en_count, \
            f"Russian ({ru_count}) and English ({en_count}) should have same key count"
