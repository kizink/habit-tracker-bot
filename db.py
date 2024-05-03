import psycopg2


class DataBase:
    """BD class."""

    def __init__(self) -> None:
        """Configure db."""
        self.conn = psycopg2.connect(
            dbname="habits_db",
            user="pguser",
            password="bla_bla",
            host="0.0.0.0",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id) -> bool:
        """Return True if the user exists in the database."""
        self.cursor.execute("""
                            SELECT * FROM test_table WHERE user_id = %s
                            """,
                            (user_id,))
        records = self.cursor.fetchall()
        print(records)
        if len(records):
            return True
        return False

    def add_user(self, user_id, user_name) -> None:
        """Add a user to the database."""
        self.cursor.execute(
            "INSERT INTO test_table (user_id, user_name) VALUES (%s, %s)",
            (user_id, user_name,)
        )
