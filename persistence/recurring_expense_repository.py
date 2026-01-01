from datetime import date, datetime
from typing import List, Optional

from domain.models import RecurringExpense, RecurrenceFrequency
from persistence.db import get_connection


class RecurringExpenseRepository:
    """
    Repository responsible for persistence of RecurringExpense entities.
    """

    def add(self, recurring_expense: RecurringExpense) -> RecurringExpense:
        """
        Persists a new RecurringExpense into the database.
        """
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO recurring_expenses (
                    name,
                    amount,
                    category_id,
                    frequency,
                    start_date,
                    end_date,
                    description,
                    attachment_path,
                    attachment_type,
                    last_generated_date,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    recurring_expense.name,
                    recurring_expense.amount,
                    recurring_expense.category_id,
                    recurring_expense.frequency.value,
                    recurring_expense.start_date.isoformat(),
                    (
                        recurring_expense.end_date.isoformat()
                        if recurring_expense.end_date
                        else None
                    ),
                    recurring_expense.description,
                    recurring_expense.attachment_path,
                    recurring_expense.attachment_type,
                    (
                        recurring_expense.last_generated_date.isoformat()
                        if recurring_expense.last_generated_date
                        else None
                    ),
                    recurring_expense.created_at.isoformat(),
                ),
            )

            recurring_expense.id = cursor.lastrowid
            return recurring_expense

    def get_all(self) -> List[RecurringExpense]:
        """
        Returns all recurring expenses.
        """
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM recurring_expenses")
            rows = cursor.fetchall()

            return [self._map_row_to_entity(row) for row in rows]

    def get_by_id(self, recurring_expense_id: int) -> Optional[RecurringExpense]:
        """
        Returns a recurring expense by its ID, if found.
        """
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM recurring_expenses WHERE id = ?",
                (recurring_expense_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return self._map_row_to_entity(row)

    def get_by_name(self, name: str) -> Optional[RecurringExpense]:
        """
        Returns a recurring expense by its name, if found.
        """
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM recurring_expenses WHERE name = ?",
                (name,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return self._map_row_to_entity(row)

    def update_last_generated_date(
        self, recurring_expense_id: int, generated_date: date
    ) -> None:
        """
        Updates the last_generated_date field for a recurring expense.
        """
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE recurring_expenses
                SET last_generated_date = ?
                WHERE id = ?
                """,
                (generated_date.isoformat(), recurring_expense_id),
            )

    def _map_row_to_entity(self, row) -> RecurringExpense:
        """
        Maps a database row to a RecurringExpense domain entity.
        """
        return RecurringExpense(
            id=row[0],
            name=row[1],
            amount=row[2],
            category_id=row[3],
            frequency=RecurrenceFrequency(row[4]),
            start_date=date.fromisoformat(row[5]),
            end_date=date.fromisoformat(row[6]) if row[6] else None,
            description=row[7],
            attachment_path=row[8],
            attachment_type=row[9],
            last_generated_date=date.fromisoformat(row[10]) if row[10] else None,
            created_at=datetime.fromisoformat(row[11]),
        )
