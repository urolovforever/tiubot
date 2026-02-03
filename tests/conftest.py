"""
Shared test fixtures for the TIU Bot test suite.
"""

import os
import sys
import pytest
import tempfile
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import Database, get_tashkent_now, TASHKENT_TZ


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    db = Database(db_name=db_path)
    yield db

    # Cleanup
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def sample_user():
    """Sample user data for testing."""
    return {
        'user_id': 123456789,
        'username': 'test_user',
        'full_name': 'Test User',
        'language': 'uz'
    }


@pytest.fixture
def sample_user_ru():
    """Sample Russian-speaking user data."""
    return {
        'user_id': 987654321,
        'username': 'russian_user',
        'full_name': 'Тестовый Пользователь',
        'language': 'ru'
    }


@pytest.fixture
def sample_user_en():
    """Sample English-speaking user data."""
    return {
        'user_id': 111222333,
        'username': 'english_user',
        'full_name': 'English Test User',
        'language': 'en'
    }


@pytest.fixture
def sample_application():
    """Sample application data for testing."""
    return {
        'user_id': 123456789,
        'username': 'test_user',
        'full_name': 'Test User',
        'phone_number': '+998901234567',
        'message': 'Test application message',
        'file_id': None,
        'user_type': 'student',
        'app_type': 'question',
        'is_anonymous': False
    }


@pytest.fixture
def sample_event():
    """Sample event data for testing."""
    # Get a future date for the event
    future_date = (datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')
    return {
        'title': 'Test Event',
        'description': 'Test event description',
        'date': future_date,
        'time': '10:00',
        'location': 'Test Location',
        'registration_link': 'https://example.com/register',
        'image_id': None
    }


@pytest.fixture
def sample_event_tomorrow():
    """Sample event for tomorrow (for reminder testing)."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
    return {
        'title': 'Tomorrow Event',
        'description': 'Event happening tomorrow',
        'date': tomorrow,
        'time': '14:00',
        'location': 'Campus Hall A',
        'registration_link': None,
        'image_id': None
    }


@pytest.fixture
def sample_contract():
    """Sample contract data for testing."""
    return {
        'passport_series': 'AA1234567',
        'full_name': 'Test Student',
        'jshshir': '12345678901234',
        'course': '1-kurs',
        'total_amount': 10000000.0,
        'paid_amount': 5000000.0,
        'remaining_amount': 5000000.0
    }


@pytest.fixture
def sample_contracts_list():
    """Sample list of contracts for bulk import testing."""
    return [
        {
            'passport_series': 'AA1111111',
            'full_name': 'Student One',
            'jshshir': '11111111111111',
            'course': '1-kurs',
            'total_amount': 10000000.0,
            'paid_amount': 5000000.0,
            'remaining_amount': 5000000.0
        },
        {
            'passport_series': 'BB2222222',
            'full_name': 'Student Two',
            'jshshir': '22222222222222',
            'course': '2-kurs',
            'total_amount': 12000000.0,
            'paid_amount': 12000000.0,
            'remaining_amount': 0.0
        },
        {
            'passport_series': 'CC3333333',
            'full_name': 'Student Three',
            'jshshir': '33333333333333',
            'course': '3-kurs',
            'total_amount': 15000000.0,
            'paid_amount': 7500000.0,
            'remaining_amount': 7500000.0
        }
    ]


@pytest.fixture
def populated_db(temp_db, sample_user, sample_user_ru, sample_application, sample_event):
    """Database pre-populated with test data."""
    # Add users
    temp_db.save_user(**sample_user)
    temp_db.save_user(**sample_user_ru)

    # Add an application
    temp_db.create_application(**sample_application)

    # Add an event
    temp_db.create_event(**sample_event)

    return temp_db
