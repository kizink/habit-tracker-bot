import pytest
import datetime

from unittest.mock import Mock, AsyncMock
from routers.save_history import handle_save_history
from db.db_scripts import Action


@pytest.mark.parametrize(
        'habit_id, is_complited, expected_success',
        [
            (1, True, True),
            (1, False, True),
            (4, True, True),
            (4, False, True),
            (10, True, False)
        ]
)
@pytest.mark.asyncio
async def test_save_history(
    state_mock, db_with_data, habit_id, is_complited, expected_success
):
    n = len(db_with_data.get_actions(habit_id))
    date = datetime.datetime(year=2040, month=1, day=14, hour=14)

    callback = AsyncMock(
        answer=AsyncMock(),
        message=Mock(
            bot=AsyncMock(),
            date=date,
            text="some text"
        ),
        data='notify_' + str(habit_id) + ('_yes' if is_complited else '_no')
    )

    await handle_save_history(callback, db_with_data)

    actions = db_with_data.get_actions(habit_id)
    if expected_success:
        assert len(actions) == n + 1
    else:
        assert len(actions) == n
    action = Action(
        habit_id, date, is_complited
    )
    if expected_success:
        assert action in actions
    else:
        assert action not in actions
    callback.answer.assert_awaited_once()
