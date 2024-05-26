import pytest

from unittest.mock import Mock, AsyncMock


@pytest.fixture()
def db_mock():
    """Mock for testing interaction with database."""
    return Mock(
        delete_habit=Mock(),
        get_habits=Mock()
    )


@pytest.fixture()
def state_mock():
    """Mock for testing current state."""
    return AsyncMock()
