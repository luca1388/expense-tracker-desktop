"""
Module for database migrations.
"""

from db import get_connection


def main():
    """
    Docstring for main
    """
    print("DB migrations...")
    with get_connection() as conn:
        cursor = conn.cursor()

        # Example migration: add 'is_recurring' column to 'expenses' table
        cursor.execute(
            """
        ALTER TABLE expenses
        ADD COLUMN recurring_expense_id INTEGER;
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_expenses_recurring_id
ON expenses(recurring_expense_id);
            """
        )

        cursor.execute(
            """
            PRAGMA table_info(expenses);
            """
        )
        print("Migration completed.")


if __name__ == "__main__":
    main()
