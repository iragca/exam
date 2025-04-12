from sqlalchemy import text


class SELECT:
    """
    Class to handle SELECT queries to the database.
    """

    def __init__(self, engine):
        self.engine = engine

    def users(self) -> None:
        """
        Retrieves all records from a specified table in the database.

        Args:
            table (str): The name of the table to retrieve records from.
        """

        query = text("SELECT * FROM users")
        conn = self.engine.connect()
        result = conn.execute(query)
        conn.close()

        return result.fetchall()

    def users_by_username(self, username: str) -> None:
        """
        Retrieves a user record from the database based on the username.

        Args:
            username (str): The username of the user to retrieve.
        """
        query = text(
            "SELECT * FROM users WHERE username=:username"
        ).bindparams(username=username)

        conn = self.engine.connect()
        result = conn.execute(query)
        conn.close()

        return result.fetchone()

    def tasks_by_username(self, username: str) -> None:
        """
        Retrieves task records from the database based on the username.

        Args:
            username (str): The username of the user whose tasks to retrieve.
        """
        query = text(
            "SELECT * FROM tasks WHERE username=:username"
        ).bindparams(username=username)

        conn = self.engine.connect()
        result = conn.execute(query)
        conn.close()

        return result.fetchall()
