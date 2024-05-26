import pytest

from unittest.mock import Mock, AsyncMock
from routers.delete_habit import handle_delete_habit, handle_choice_habits
from routers.FSM_states import DeleteHabitStates, Form


@pytest.mark.asyncio
async def test_delete_habit(state_mock, db_mock):
    """Get user habits and remove one of them."""
    user_id = 100500
    message_mock = AsyncMock(
        from_user=Mock(
            id=user_id
        ),
        answer=AsyncMock()
    )
    await handle_delete_habit(
        message_mock,
        state_mock,
        db_mock
    )
    state_mock.set_state.assert_called_with(DeleteHabitStates.ChoiceHabits)
    db_mock.get_habits.assert_called_with(user_id)

    habit_id = 123
    message_mock = AsyncMock(
        text=str(habit_id),
        answer=AsyncMock()
    )
    await handle_choice_habits(
        message_mock,
        state_mock,
        db_mock
    )
    state_mock.set_state.assert_called_with(Form.buttons)
    db_mock.delete_habit.assert_called_with(habit_id)
