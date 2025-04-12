from sqlalchemy import create_engine, inspect

from backend.config import DATABASE_URL, logger
from backend.ddl import CREATE, DROP  # noqa: F401


def initdb():
    """
    Initializes the database by creating the necessary tables
    and establishing a connection.

    This function performs the following steps:
    1. Creates a database engine using the provided `DATABASE_URL`.

    2. Logs the connection process and the database URL

    3. Creates the required tables (`userTable` and `taskTable`)
       using the `CREATE` object.
    4. Inspects the database to retrieve and log the list of table names.

    5. Logs a success message upon successful initialization.

    Returns:
        sqlalchemy.engine.Engine: The database engine instance.
                                  with all necessary configuration.
    Raises:
        SystemExit: If an error occurs while creating the database engine.
    """
    try:
        ENGINE = create_engine(DATABASE_URL, client_encoding="utf8")
    except Exception as e:
        logger.error(f"Error creating DB engine {e}")
        exit(1)

    logger.info("Connecting to the database...")
    logger.info(f"Database URL: {DATABASE_URL}")

    create = CREATE(ENGINE)

    # DROP(ENGINE).drop_all()
    create.userTable()
    create.taskTable()

    inspector = inspect(ENGINE)

    logger.info(inspector.get_table_names())
    logger.info("Database initialized successfully.")

    return ENGINE
