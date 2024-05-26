import psycopg2


class DataBase:
    """BD class."""

    def __init__(self) -> None:
        """Configure db."""
        from .db_secrets.db_pass import PASS
        self.conn = psycopg2.connect(
            dbname="habits_db",
            user="pguser",
            password=PASS,
            host="0.0.0.0",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id) -> bool:
        """Return True if the user exists in the database."""
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = %s",
            (user_id,)
        )
        records = self.cursor.fetchall()
        if len(records):
            return True
        return False

    def add_user(self, user_id, user_name) -> None:
        """Add a user to the database."""
        self.cursor.execute(
            "INSERT INTO users (user_id, name) VALUES (%s, %s)",
            (user_id, user_name,)
        )

    def add_habit(self, user_id, name, description, notificationTime) -> None:
        """Add a habit to the database."""
        self.cursor.execute(
            """
                INSERT INTO habits
                (user_id, name, description, notification_time)
                VALUES (%s, %s, %s, %s)
            """,
            (user_id, name, description, notificationTime)
        )

    def get_habits(self, user_id):
        """Get habits from db."""
        self.cursor.execute(
            """
                SELECT habit_id, name, description, notification_time
                FROM habits WHERE user_id = %s
            """,
            (user_id,)
        )
        records = self.cursor.fetchall()
        return records

    def delete_habit(self, habit_id):
        """Delete a habit from db."""
        self.cursor.execute(
            """
                DELETE FROM habits
                WHERE habits.habit_id = %s;
            """,
            (habit_id,)
        )
