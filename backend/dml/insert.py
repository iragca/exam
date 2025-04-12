from sqlalchemy import text


class INSERT:
    """
    Class to handle INSERT requests to the database.
    """

    def __init__(self, engine):
        self.engine = engine

    def user(self, username: str, password: str) -> None:
        """
        Inserts a new user into the users table.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            None
        """
        query = text(
            "INSERT INTO users (username, password) "
            "VALUES (:username, :password)"
        )

        conn = self.engine.connect()
        result = conn.execute(
            query,
            {"username": username, "password": password},
        )
        conn.commit()
        conn.close()

        return result

    def task(self, task: str, deadline: str, username: str) -> None:
        """
        Inserts a new task into the tasks table.

        Args:
            task (str): The task description.
            deadline (str): The deadline for the task.
            user (str): The user associated with the task.

        Returns:
            None
        """
        query = text(
            "INSERT INTO tasks (task, deadline, username) "
            "VALUES (:task, :deadline, :username)"
        ).bindparams(
            task=task, deadline=deadline, username=username
        )

        conn = self.engine.connect()
        result = conn.execute(query)
        conn.commit()
        conn.close()

        return result
