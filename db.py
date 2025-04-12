from sqlalchemy import create_engine, inspect
from sqlalchemy import text

import os
from dotenv import load_dotenv


def initdb():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

    engine = create_engine(DATABASE_URL, client_encoding="utf8")

    conn = engine.connect()

    conn.execute(
        text("""
    CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );
    """)
    )
    conn.execute(
        text("""
    CREATE TABLE IF NOT EXISTS tasks ( id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    deadline DATE NOT NULL,
    user VARCHAR(255) NOT NULL,
    FOREIGN KEY (user) REFERENCES users(username)
    );
    """)
    )

    return conn
