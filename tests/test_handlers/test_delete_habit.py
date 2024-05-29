import pytest

from unittest.mock import Mock, AsyncMock
from routers.delete_habit import handle_delete_habit, handle_choice_habits
from routers.FSM_states import DeleteHabitStates, Form


@pytest.mark.asyncio
async def test_delete_habit(state_mock, db_with_data):
    """Get user habits and remove one of them."""
    user_id = 3
    message_mock = AsyncMock(
        from_user=Mock(
            id=user_id
        ),
        answer=AsyncMock()
    )
    await handle_delete_habit(
        message_mock,
        state_mock,
        db_with_data
    )
    state_mock.set_state.assert_called_with(DeleteHabitStates.ChoiceHabits)

    habit_id = 0
    message_mock = AsyncMock(
        text=str(habit_id),
        answer=AsyncMock()
    )
    state_mock.get_data = AsyncMock(
        return_value={
            'habit_list': [Mock(id=6)]
        }
    )
    await handle_choice_habits(
        message_mock,
        state_mock,
        db_with_data
    )
    state_mock.set_state.assert_called_with(Form.buttons)
    with db_with_data.conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT * FROM habit WHERE id = 6
            """
        )
        records = cursor.fetchall()
    assert len(records) == 0


@pytest.mark.asyncio
async def test_no_habits_to_delete(state_mock, db_with_data):
    """User with no habits."""
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
        db_with_data
    )
    state_mock.assert_not_awaited()
