"""
persistence/expense_repository.py

Repository responsible for persisting and retrieving Expense entities
from the SQLite database.
"""

import sqlite3
from datetime import date, datetime

from domain.models import Expense


class ExpenseRepository:
    """
    Repository for Expense entities.
    """

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def add(self, expense: Expense) -> Expense:
        """
        Persists a new Expense into the database.

        Args:
            expense (Expense): The expense to persist

        Returns:
            Expense: The persisted expense with the generated ID
        """
        with self.conn as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO expenses (
                    date,
                    amount,
                    category_id,
                    description,
                    is_recurring,        
                    attachment_path,
                    attachment_type,
                    analysis_data,
                    analysis_summary,
                    created_at,
                    recurring_expense_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    expense.date.isoformat(),
                    expense.amount,
                    expense.category_id,
                    expense.description,
                    int(expense.is_recurring),
                    expense.attachment_path,
                    expense.attachment_type,
                    expense.analysis_data,
                    expense.analysis_summary,
                    expense.created_at.isoformat(),
                    expense.recurring_expense_id,
                ),
            )

            expense.id = cursor.lastrowid

        return expense

    def update(self, expense: Expense) -> None:
        """
        Update an existing expense.
        """
        with self.conn as connection:
            connection.execute(
                """
                UPDATE expenses
                SET
                    date = ?,
                    amount = ?,
                    category_id = ?,
                    description = ?,
                    attachment_path = ?,
                    attachment_type = ?
                WHERE id = ?
                """,
                (
                    expense.date.isoformat(),
                    expense.amount,
                    expense.category_id,
                    expense.description,
                    expense.attachment_path,
                    expense.attachment_type,
                    expense.id,
                ),
            )
            connection.commit()

    def get_all(self) -> list[Expense]:
        """
        Retrieves all expenses from the database.

        Returns:
            list[Expense]: List of expenses
        """
        with self.conn as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM expenses")
            rows = cursor.fetchall()

        return [self._map_row_to_expense(row) for row in rows]

    def get_by_period(self, start_date: date, end_date: date) -> list[Expense]:
        """
        Retrieves all expenses within a given date range.

        Args:
            start_date (date): Start date (inclusive)
            end_date (date): End date (inclusive)

        Returns:
            list[Expense]: Filtered expenses
        """
        with self.conn as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT * FROM expenses
                WHERE date BETWEEN ? AND ?
                """,
                (
                    start_date.isoformat(),
                    end_date.isoformat(),
                ),
            )

            rows = cursor.fetchall()

        return [self._map_row_to_expense(row) for row in rows]

    def _map_row_to_expense(self, row: sqlite3.Row) -> Expense:
        """
        Maps a database row to an Expense domain object.

        Args:
            row (sqlite3.Row): Raw database row

        Returns:
            Expense: Mapped domain object
        """
        return Expense(
            id=row[0],
            date=date.fromisoformat(row[1]),
            amount=row[2],
            category_id=row[3],
            description=row[4],
            is_recurring=bool(row[5]),
            attachment_path=row[6],
            attachment_type=row[7],
            analysis_data=row[8],
            analysis_summary=row[9],
            created_at=datetime.fromisoformat(row[10]),
            recurring_expense_id=row[11],
        )

    def delete(self, expense_id: int) -> None:
        """
        Delete an expense by its ID.

        :param expense_id: ID of the expense to delete
        """
        with self.conn as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()

    def get_by_id(self, expense_id: int) -> Expense | None:
        """
        Retrieve an expense by its ID.
        """
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return self._map_row_to_expense(row)
