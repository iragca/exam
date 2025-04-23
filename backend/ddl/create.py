from sqlalchemy import text


class CREATE:
    """
    Class to handle CREATE requests to the database.
    """

    def __init__(self, engine):
        self.engine = engine

    def userTable(self) -> None:
        """
        Creates the USER Table
        """

        conn = self.engine.connect()
        result = conn.execute(
            text(
                """
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );
    """
            )
        )
        conn.commit()
        conn.close()

        return result

    def taskTable(self) -> None:
        """
        Creates the TASK Table
        """

        conn = self.engine.connect()
        result = conn.execute(
            text(
                """
    CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    deadline DATE NOT NULL,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
    );
    """
            )
        )
        conn.commit()
        conn.close()

        return result

    def iragTable(self) -> None:
        """
        Creates the IRAG Table
        """

        conn = self.engine.connect()
        result = conn.execute(
            text(
                """
    CREATE TABLE IF NOT EXISTS irag (
    id SERIAL PRIMARY KEY
    );
    """
            )
        )

        conn.commit()
        conn.close()

        return result
