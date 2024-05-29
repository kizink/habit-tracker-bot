import pytest
from datetime import time


@pytest.mark.parametrize(
        "user_id, is_exists",
        [
            (1, True),
            (2, True),
            (100500, False),
        ]
)
async def test_user_exists(db_with_data, user_id, is_exists):
    """Check user in db."""
    assert db_with_data.user_exists(user_id) == is_exists


@pytest.mark.parametrize(
        "notify_from, notify_to, expected_count",
        [
            (time(11, 25), time(11, 29), 0),
            (time(11, 25), time(11, 30), 1),
            (time(11, 30, 1), time(11, 31), 0),
            (time(8, 50), time(16, 30), 3),
            (time(19, 15), time(19, 15), 1),
            (time(19, 15, 0, 1), time(19, 15, 0, 2), 0),
        ]
)
async def test_get_habits_for_notification(
        db_with_data, notify_from, notify_to, expected_count
):
    records = db_with_data.get_habits_for_notification(
        notify_from, notify_to
    )
    assert len(records) == expected_count


@pytest.mark.parametrize(
        "user_id, user_name, expected_success",
        [
            (100500, 'Petr', True),
            (1, 'Ivan', False),
        ]
)
async def test_add_user(db_with_data, user_id, user_name, expected_success):
    """Check saving new user."""
    result = db_with_data.add_user(user_id, user_name)
    assert result == expected_success

    with db_with_data.conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT * FROM "user" WHERE id = %s
            """,
            (user_id, )
        )
        records = cursor.fetchall()
    assert len(records) == 1
    if expected_success:
        assert records[0][1] == user_name
    else:
        assert records[0][1] != user_name
