"""
Docstring for persistence.db
Handles database connections and initialization.

This module provides functions to connect to the SQLite database
and initialize the required tables for the expense tracker application.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/expenses.db")


def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Initializes the database with the required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            is_custom INTEGER NOT NULL
        )
        """
        )

        conn.commit()
