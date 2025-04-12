from sqlalchemy import text


class DROP:

    def __init__(self, engine):
        self.engine = engine

    def drop_all(self) -> None:
        """
        Drops all tables in the database.
        """
        conn = self.engine.connect()
        result = conn.execute(text("DROP TABLE IF EXISTS tasks;"))
        result = conn.execute(text("DROP TABLE IF EXISTS users;"))
        conn.commit()
        conn.close()

        return result
