import pytest


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
