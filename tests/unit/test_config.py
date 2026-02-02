"""
Unit tests for configuration validation.
Tests verify the structure and integrity of configuration data.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import FACULTIES, ADMIN_IDS, BOT_TOKEN, ADMIN_GROUP_ID, LIBRARY_CHANNELS


class TestAdminConfiguration:
    """Test admin-related configuration."""

    def test_admin_ids_is_list(self):
        """Test that ADMIN_IDS is a list."""
        assert isinstance(ADMIN_IDS, list)

    def test_admin_ids_not_empty(self):
        """Test that there is at least one admin."""
        assert len(ADMIN_IDS) > 0, "At least one admin ID should be configured"

    def test_admin_ids_are_integers(self):
        """Test that all admin IDs are integers."""
        for admin_id in ADMIN_IDS:
            assert isinstance(admin_id, int), f"Admin ID {admin_id} should be an integer"

    def test_admin_ids_are_positive(self):
        """Test that all admin IDs are positive numbers."""
        for admin_id in ADMIN_IDS:
            assert admin_id > 0, f"Admin ID {admin_id} should be positive"


class TestBotConfiguration:
    """Test bot token and group configuration."""

    def test_bot_token_exists(self):
        """Test that BOT_TOKEN is defined."""
        assert BOT_TOKEN is not None
        assert len(BOT_TOKEN) > 0

    def test_bot_token_format(self):
        """Test that BOT_TOKEN has expected format."""
        # Telegram bot tokens are in format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
        assert ':' in BOT_TOKEN, "Bot token should contain a colon"
        parts = BOT_TOKEN.split(':')
        assert len(parts) == 2, "Bot token should have two parts separated by colon"
        assert parts[0].isdigit(), "First part of bot token should be numeric"

    def test_admin_group_id_exists(self):
        """Test that admin group ID is configured."""
        assert ADMIN_GROUP_ID is not None


class TestLibraryChannelsConfiguration:
    """Test library channels configuration."""

    def test_library_channels_is_dict(self):
        """Test that LIBRARY_CHANNELS is a dictionary."""
        assert isinstance(LIBRARY_CHANNELS, dict)

    def test_library_channels_not_empty(self):
        """Test that there are library channels configured."""
        assert len(LIBRARY_CHANNELS) > 0

    def test_library_channel_structure(self):
        """Test that each library channel has required fields."""
        for channel_id, channel_data in LIBRARY_CHANNELS.items():
            assert isinstance(channel_id, int), f"Channel key {channel_id} should be integer"
            assert 'username' in channel_data, f"Channel {channel_id} should have 'username'"
            assert channel_data['username'].startswith('@'), \
                f"Channel {channel_id} username should start with @"


class TestFacultiesStructure:
    """Test the faculties configuration structure."""

    def test_faculties_has_all_languages(self):
        """Test that faculties are defined for all languages."""
        required_languages = ['uz', 'ru', 'en']

        for lang in required_languages:
            assert lang in FACULTIES, f"FACULTIES should have '{lang}' language"

    def test_faculties_not_empty(self):
        """Test that each language has faculties defined."""
        for lang, faculties in FACULTIES.items():
            assert len(faculties) > 0, f"Language '{lang}' should have at least one faculty"

    def test_faculty_has_courses(self):
        """Test that each faculty has courses defined."""
        for lang, faculties in FACULTIES.items():
            for faculty_name, courses in faculties.items():
                assert len(courses) > 0, \
                    f"Faculty '{faculty_name}' in '{lang}' should have courses"

    def test_courses_have_groups_or_directions(self):
        """Test that each course has either groups (list) or directions (dict)."""
        for lang, faculties in FACULTIES.items():
            for faculty_name, courses in faculties.items():
                for course_name, course_data in courses.items():
                    # Course data should be either list (direct groups) or dict (directions)
                    assert isinstance(course_data, (list, dict)), \
                        f"Course '{course_name}' in '{faculty_name}' ({lang}) should be list or dict"

                    if isinstance(course_data, list):
                        # If it's a list, it should have group names
                        assert len(course_data) > 0, \
                            f"Course '{course_name}' should have at least one group"
                    elif isinstance(course_data, dict):
                        # If it's a dict, each direction should have groups
                        for direction_name, groups in course_data.items():
                            assert isinstance(groups, list), \
                                f"Direction '{direction_name}' should have groups list"
                            assert len(groups) > 0, \
                                f"Direction '{direction_name}' should have at least one group"

    def test_group_names_not_empty(self):
        """Test that group names are non-empty strings."""
        for lang, faculties in FACULTIES.items():
            for faculty_name, courses in faculties.items():
                for course_name, course_data in courses.items():
                    groups = []
                    if isinstance(course_data, list):
                        groups = course_data
                    elif isinstance(course_data, dict):
                        for direction_groups in course_data.values():
                            groups.extend(direction_groups)

                    for group in groups:
                        assert isinstance(group, str), f"Group name should be string"
                        assert len(group) > 0, f"Group name should not be empty"


class TestFacultiesConsistency:
    """Test consistency between language versions of faculties."""

    def test_same_number_of_faculties_per_language(self):
        """Test that all languages have the same number of faculties."""
        uz_count = len(FACULTIES['uz'])
        ru_count = len(FACULTIES['ru'])
        en_count = len(FACULTIES['en'])

        assert uz_count == ru_count, \
            f"UZ ({uz_count}) and RU ({ru_count}) should have same faculty count"
        assert ru_count == en_count, \
            f"RU ({ru_count}) and EN ({en_count}) should have same faculty count"

    def test_group_names_consistent_across_languages(self):
        """Test that group names are identical across all languages."""
        # Collect all group names per language
        groups_by_lang = {}

        for lang, faculties in FACULTIES.items():
            all_groups = set()
            for faculty_name, courses in faculties.items():
                for course_name, course_data in courses.items():
                    if isinstance(course_data, list):
                        all_groups.update(course_data)
                    elif isinstance(course_data, dict):
                        for groups in course_data.values():
                            all_groups.update(groups)
            groups_by_lang[lang] = all_groups

        # All languages should have the same groups
        uz_groups = groups_by_lang['uz']
        ru_groups = groups_by_lang['ru']
        en_groups = groups_by_lang['en']

        assert uz_groups == ru_groups, "UZ and RU should have same group names"
        assert ru_groups == en_groups, "RU and EN should have same group names"


class TestCourseNamingConvention:
    """Test course naming conventions."""

    def test_uz_course_names_format(self):
        """Test that Uzbek course names follow expected format."""
        expected_patterns = ['1-kurs', '2-kurs', '3-kurs', '4-kurs']

        for faculty_name, courses in FACULTIES['uz'].items():
            for course_name in courses.keys():
                assert course_name in expected_patterns or 'kurs' in course_name.lower(), \
                    f"Uzbek course '{course_name}' should contain 'kurs'"

    def test_ru_course_names_format(self):
        """Test that Russian course names follow expected format."""
        for faculty_name, courses in FACULTIES['ru'].items():
            for course_name in courses.keys():
                assert 'курс' in course_name.lower(), \
                    f"Russian course '{course_name}' should contain 'курс'"

    def test_en_course_names_format(self):
        """Test that English course names follow expected format."""
        for faculty_name, courses in FACULTIES['en'].items():
            for course_name in courses.keys():
                assert 'year' in course_name.lower(), \
                    f"English course '{course_name}' should contain 'year'"


class TestGroupNamingConvention:
    """Test group naming conventions."""

    def test_group_names_follow_pattern(self):
        """Test that group names follow expected patterns."""
        # Group names should match patterns like: XX-N-YY or XX-N-YYr
        import re
        pattern = re.compile(r'^[A-Z]{2,3}-\d+-\d{2}r?$')

        for lang, faculties in FACULTIES.items():
            for faculty_name, courses in faculties.items():
                for course_name, course_data in courses.items():
                    groups = []
                    if isinstance(course_data, list):
                        groups = course_data
                    elif isinstance(course_data, dict):
                        for direction_groups in course_data.values():
                            groups.extend(direction_groups)

                    for group in groups:
                        assert pattern.match(group), \
                            f"Group '{group}' should match pattern XX-N-YY or XX-N-YYr"

    def test_group_year_codes_valid(self):
        """Test that year codes in group names are valid (23, 24, 25)."""
        valid_years = {'23', '24', '25', '26'}  # Valid year codes

        for lang, faculties in FACULTIES.items():
            for faculty_name, courses in faculties.items():
                for course_name, course_data in courses.items():
                    groups = []
                    if isinstance(course_data, list):
                        groups = course_data
                    elif isinstance(course_data, dict):
                        for direction_groups in course_data.values():
                            groups.extend(direction_groups)

                    for group in groups:
                        # Extract year code (last 2 digits before optional 'r')
                        year_code = group.rstrip('r').split('-')[-1]
                        assert year_code in valid_years, \
                            f"Group '{group}' has invalid year code '{year_code}'"
