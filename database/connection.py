"""Secure MySQL connection helpers for PromptWall."""

import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()


def get_connection() -> Any:
    """Create a MySQL connection using environment variables only.

    The connector is imported lazily so authorization/unit tests can run in an
    environment where MySQL client dependencies are not installed yet.
    """
    import mysql.connector

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "promptwall_db"),
        user=os.getenv("DB_USER", "promptwall_app"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def test_connection() -> bool:
    """Return True when the configured database can be reached."""
    connection: Optional[Any] = None
    try:
        connection = get_connection()
        return bool(connection.is_connected())
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
