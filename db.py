from sqlalchemy import create_engine, inspect

from backend.config import DATABASE_URL, logger
from backend.ddl import CREATE, DROP


def initdb():
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
