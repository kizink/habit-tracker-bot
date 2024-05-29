import os
import psycopg

from dataclasses import dataclass
from datetime import time
from datetime import datetime
from psycopg.rows import class_row


@dataclass
class Habit:
    """Representation of row from table habit."""

    id: int
    user_id: int
    name: str
    description: str
    notification_time: time


@dataclass
class Action:
    """Representation of row from table action."""

    habit_id: int
    action_time: datetime
    is_complited: bool


class DataBase:
    """BD class."""

    def __init__(self):
        """Configure db."""
        self.conn = psycopg.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]
        )

    def user_exists(self, user_id) -> bool:
        """Return True if the user exists in the database."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM \"user\" WHERE id = %s",
                (user_id,)
            )
            records = cursor.fetchall()
        return len(records) > 0

    def add_user(self, user_id, user_name) -> bool:
        """Add a user to the database."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO \"user\" (id, name) VALUES (%s, %s);",
                    (user_id, user_name,)
                )
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
        return False

    def add_habit(self, user_id, name, description, notificationTime) -> None:
        """Add a habit to the database."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO habit
                    (user_id, name, description, notification_time)
                    VALUES (%s, %s, %s, %s)
                """,
                (user_id, name, description, notificationTime)
            )
        self.conn.commit()

    def get_habits(self, user_id) -> list[Habit]:
        """Get habits from db."""
        with self.conn.cursor(row_factory=class_row(Habit)) as cursor:
            cursor.execute(
                """
                    SELECT * FROM habit
                    WHERE user_id = %s
                """,
                (user_id,)
            )
            records = cursor.fetchall()
        return records

    def get_habits_for_notification(
        self,
        notify_from: time,
        notify_to: time
    ) -> list[Habit]:
        """Get habits which need to be notificated."""
        with self.conn.cursor(row_factory=class_row(Habit)) as cursor:
            cursor.execute(
                """
                    SELECT * FROM habit
                    WHERE
                        notification_time >= %s
                    AND
                        notification_time <= %s
                """,
                (notify_from, notify_to)
            )
            records = cursor.fetchall()
        return records

    def delete_habit(self, habit_id) -> None:
        """Delete a habit from db."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                    DELETE FROM habit
                    WHERE id = %s;
                """,
                (habit_id,)
            )
        self.conn.commit()

    def add_action(self, action: Action) -> bool:
        """Add an action to the database."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO action
                        (habit_id, action_time, is_complited)
                        VALUES (%s, %s, %s)
                    """,
                    (action.habit_id, action.action_time, action.is_complited)
                )
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False

    def get_actions(self, habit_id: int) -> list[Action]:
        """Get actions for specific user habit."""
        with self.conn.cursor(row_factory=class_row(Action)) as cursor:
            cursor.execute(
                """
                    SELECT * FROM action
                    WHERE habit_id = %s
                """,
                (habit_id,)
            )
            records = cursor.fetchall()
        return records
