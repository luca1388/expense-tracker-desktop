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
    connection = sqlite3.connect(DB_PATH)
    # Senza questa riga:
    # potresti inserire una spesa con category_id inesistente
    # nessun errore verrebbe lanciato
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


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

        # Recurring expenses table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,
            amount REAL NOT NULL,

            category_id INTEGER NOT NULL,

            frequency TEXT NOT NULL,

            start_date TEXT NOT NULL,
            end_date TEXT,

            description TEXT,

            attachment_path TEXT,
            attachment_type TEXT,

            last_generated_date TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """
        )

        # Tabella spese
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT NOT NULL,
            amount REAL NOT NULL,

            category_id INTEGER NOT NULL,
            description TEXT,

            is_recurring INTEGER NOT NULL DEFAULT 0,

            attachment_path TEXT,
            attachment_type TEXT,
            
            analysis_data TEXT,
            analysis_summary TEXT,

            created_at TEXT NOT NULL,
            
            recurring_expense_id INTEGER,

            FOREIGN KEY (category_id) REFERENCES categories(id)
            FOREIGN KEY (recurring_expense_id) REFERENCES recurring_expenses(id)
        )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_expenses_recurring_id
ON expenses(recurring_expense_id);
            """
        )

        conn.commit()
