import os
import pytest

from unittest.mock import AsyncMock

from db.db_scripts import DataBase


@pytest.fixture()
def empty_db(request):
    """Create empty DataBase instance."""
    db_instance = DataBase()
    with db_instance.conn.cursor() as cursor:
        cursor.execute(
            """
                TRUNCATE "action", habit, "user";
            """
        )
    db_instance.conn.commit()

    def clear_db():
        with db_instance.conn.cursor() as cursor:
            cursor.execute(
                """
                    TRUNCATE "action", habit, "user";
                """
            )
        db_instance.conn.commit()

    request.addfinalizer(clear_db)
    return db_instance


@pytest.fixture()
def db_with_data(empty_db):
    """Create DataBase instance with test data."""
    with empty_db.conn.cursor() as cursor:
        cursor.execute(
            """
                INSERT INTO "user"
                    (id, name)
                VALUES
                    (1, 'Vasya'),
                    (2, 'Petya'),
                    (3, 'Petya2');

                INSERT INTO habit
                    (id, user_id, name, description, notification_time)
                VALUES
                    (1, 1, 'Пить', 'очень важно пить', '11:30:00'),
                    (2, 1, 'Зарядка', 'это нам надо', '09:00:00'),
                    (3, 1, 'Таблетки', 'это приходится', '21:45:00'),
                    (4, 2, 'Код писать', 'зачем это', '15:00:00'),
                    (5, 2, 'Гулять', 'люблю такое', '19:15:00'),
                    (6, 3, 'Гулять', 'люблю такое', '23:15:00');

                INSERT INTO action
                    (habit_id, action_time, is_complited)
                VALUES
                    (1, '2024-05-20 12:40:00', TRUE),
                    (1, '2024-05-21 12:40:00', TRUE),
                    (1, '2024-05-22 12:40:00', FALSE),
                    (1, '2024-05-23 12:40:00', TRUE),
                    (2, '2024-05-27 12:40:00', FALSE);
            """
        )
    empty_db.conn.commit()
    return empty_db


@pytest.fixture()
def state_mock():
    """Mock for testing current state."""
    return AsyncMock()


@pytest.fixture(scope="session", autouse=True)
def setup_credentials(request):
    """Set up environment variables."""
    os.environ["DB_NAME"] = "test_habits_db"
    os.environ["DB_USER"] = "test_pguser"
    os.environ["DB_PASS"] = "test_password"
    os.environ["DB_HOST"] = "0.0.0.0"
    os.environ["DB_PORT"] = "5432"
