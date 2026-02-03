"""
Unit tests for FSM state definitions.
Tests verify that all state groups and states are properly defined.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from states.forms import (
    ApplicationForm, ScheduleStates, AdminReplyState,
    EventCreateState, EventDeleteState, EventEditState,
    EventQuickCreateState, BroadcastState, OnboardingState,
    ScheduleUploadState, ContractLookupState,
    ContractUploadState
)
from aiogram.dispatcher.filters.state import StatesGroup


class TestApplicationFormStates:
    """Test ApplicationForm state group."""

    def test_application_form_is_states_group(self):
        """Test that ApplicationForm inherits from StatesGroup."""
        assert issubclass(ApplicationForm, StatesGroup)

    def test_application_form_has_required_states(self):
        """Test that ApplicationForm has all required states."""
        required_states = [
            'waiting_for_user_type',
            'waiting_for_app_type',
            'waiting_for_anonymity',
            'waiting_for_phone',
            'waiting_for_message',
            'waiting_for_file_choice',
            'waiting_for_file',
            'waiting_for_confirmation'
        ]

        for state_name in required_states:
            assert hasattr(ApplicationForm, state_name), \
                f"ApplicationForm should have '{state_name}' state"

    def test_application_form_state_count(self):
        """Test that ApplicationForm has exactly 8 states."""
        states = ApplicationForm.all_states
        assert len(states) == 8, f"ApplicationForm should have 8 states, has {len(states)}"


class TestScheduleStates:
    """Test ScheduleStates state group."""

    def test_schedule_states_is_states_group(self):
        """Test that ScheduleStates inherits from StatesGroup."""
        assert issubclass(ScheduleStates, StatesGroup)

    def test_schedule_states_has_required_states(self):
        """Test that ScheduleStates has all required states."""
        required_states = [
            'waiting_for_faculty',
            'waiting_for_direction',
            'waiting_for_course',
            'waiting_for_group'
        ]

        for state_name in required_states:
            assert hasattr(ScheduleStates, state_name), \
                f"ScheduleStates should have '{state_name}' state"


class TestEventCreateStates:
    """Test EventCreateState state group."""

    def test_event_create_is_states_group(self):
        """Test that EventCreateState inherits from StatesGroup."""
        assert issubclass(EventCreateState, StatesGroup)

    def test_event_create_has_required_states(self):
        """Test that EventCreateState has all required states."""
        required_states = [
            'waiting_for_title',
            'waiting_for_description',
            'waiting_for_date',
            'waiting_for_time',
            'waiting_for_location',
            'waiting_for_registration_link',
            'waiting_for_image'
        ]

        for state_name in required_states:
            assert hasattr(EventCreateState, state_name), \
                f"EventCreateState should have '{state_name}' state"


class TestEventQuickCreateStates:
    """Test EventQuickCreateState state group."""

    def test_event_quick_create_is_states_group(self):
        """Test that EventQuickCreateState inherits from StatesGroup."""
        assert issubclass(EventQuickCreateState, StatesGroup)

    def test_event_quick_create_has_required_states(self):
        """Test that EventQuickCreateState has all required states."""
        required_states = [
            'waiting_for_title',
            'waiting_for_post',
            'waiting_for_date',
            'waiting_for_confirmation'
        ]

        for state_name in required_states:
            assert hasattr(EventQuickCreateState, state_name), \
                f"EventQuickCreateState should have '{state_name}' state"


class TestBroadcastStates:
    """Test BroadcastState state group."""

    def test_broadcast_is_states_group(self):
        """Test that BroadcastState inherits from StatesGroup."""
        assert issubclass(BroadcastState, StatesGroup)

    def test_broadcast_has_required_states(self):
        """Test that BroadcastState has all required states."""
        required_states = [
            'waiting_for_content',
            'waiting_for_confirmation'
        ]

        for state_name in required_states:
            assert hasattr(BroadcastState, state_name), \
                f"BroadcastState should have '{state_name}' state"


class TestContractStates:
    """Test contract-related state groups."""

    def test_contract_lookup_is_states_group(self):
        """Test that ContractLookupState inherits from StatesGroup."""
        assert issubclass(ContractLookupState, StatesGroup)

    def test_contract_lookup_has_passport_state(self):
        """Test that ContractLookupState has waiting_for_passport state."""
        assert hasattr(ContractLookupState, 'waiting_for_passport')

    def test_contract_upload_is_states_group(self):
        """Test that ContractUploadState inherits from StatesGroup."""
        assert issubclass(ContractUploadState, StatesGroup)

    def test_contract_upload_has_excel_state(self):
        """Test that ContractUploadState has waiting_for_excel state."""
        assert hasattr(ContractUploadState, 'waiting_for_excel')


class TestAdminStates:
    """Test admin-related state groups."""

    def test_admin_reply_is_states_group(self):
        """Test that AdminReplyState inherits from StatesGroup."""
        assert issubclass(AdminReplyState, StatesGroup)

    def test_admin_reply_has_reply_state(self):
        """Test that AdminReplyState has waiting_for_reply state."""
        assert hasattr(AdminReplyState, 'waiting_for_reply')

    def test_event_delete_is_states_group(self):
        """Test that EventDeleteState inherits from StatesGroup."""
        assert issubclass(EventDeleteState, StatesGroup)

    def test_event_edit_is_states_group(self):
        """Test that EventEditState inherits from StatesGroup."""
        assert issubclass(EventEditState, StatesGroup)


class TestOnboardingState:
    """Test OnboardingState state group."""

    def test_onboarding_is_states_group(self):
        """Test that OnboardingState inherits from StatesGroup."""
        assert issubclass(OnboardingState, StatesGroup)

    def test_onboarding_has_language_state(self):
        """Test that OnboardingState has waiting_for_language state."""
        assert hasattr(OnboardingState, 'waiting_for_language')


class TestScheduleUploadStates:
    """Test ScheduleUploadState state group."""

    def test_schedule_upload_is_states_group(self):
        """Test that ScheduleUploadState inherits from StatesGroup."""
        assert issubclass(ScheduleUploadState, StatesGroup)

    def test_schedule_upload_has_required_states(self):
        """Test that ScheduleUploadState has all required states."""
        required_states = [
            'waiting_for_faculty',
            'waiting_for_course',
            'waiting_for_direction',
            'waiting_for_group',
            'waiting_for_image'
        ]

        for state_name in required_states:
            assert hasattr(ScheduleUploadState, state_name), \
                f"ScheduleUploadState should have '{state_name}' state"


class TestAllStateGroupsExist:
    """Test that all expected state groups are defined."""

    def test_all_state_groups_importable(self):
        """Test that all state groups can be imported."""
        state_groups = [
            ApplicationForm, ScheduleStates, AdminReplyState,
            EventCreateState, EventDeleteState, EventEditState,
            EventQuickCreateState, BroadcastState, OnboardingState,
            ScheduleUploadState, ContractLookupState,
            ContractUploadState
        ]

        for state_group in state_groups:
            assert state_group is not None
            assert issubclass(state_group, StatesGroup)
