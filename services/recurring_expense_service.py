from datetime import date, datetime
from typing import List

from domain.models import RecurringExpense, RecurrenceFrequency
from domain.models import Expense
from persistence.recurring_expense_repository import RecurringExpenseRepository
from persistence.expense_repository import ExpenseRepository


class RecurringExpenseService:
    """
    Service responsible for managing recurring expenses and generating
    actual Expense instances from them.
    """

    def __init__(
        self,
        recurring_repository: RecurringExpenseRepository,
        expense_repository: ExpenseRepository,
    ) -> None:
        self._recurring_repository = recurring_repository
        self._expense_repository = expense_repository

    def generate_missing_expenses(self, up_to: date) -> List[Expense]:
        """
        Generates all missing expenses for recurring expenses up to a given date.

        This method is deterministic and idempotent:
        calling it multiple times with the same date will not create duplicates.
        """
        generated_expenses: List[Expense] = []

        recurring_expenses = self._recurring_repository.get_all()

        for recurring in recurring_expenses:
            expenses = self._generate_for_recurring(recurring, up_to)
            generated_expenses.extend(expenses)

        return generated_expenses

    def _generate_for_recurring(
        self, recurring: RecurringExpense, up_to: date
    ) -> List[Expense]:
        """
        Generates missing Expense instances for a single RecurringExpense.
        """
        generated: List[Expense] = []

        current_date = self._get_generation_start_date(recurring)

        while current_date <= up_to:
            if recurring.end_date and current_date > recurring.end_date:
                break

            expense = Expense(
                id=None,
                date=current_date,
                amount=recurring.amount,
                category_id=recurring.category_id,
                description=recurring.description,
                is_recurring=True,
                attachment_path=recurring.attachment_path,
                attachment_type=recurring.attachment_type,
                analysis_data=None,
                analysis_summary=None,
                created_at=datetime.now(),
            )

            self._expense_repository.add(expense)

            generated.append(expense)

            recurring.last_generated_date = current_date
            self._recurring_repository.update_last_generated_date(
                recurring.id, current_date
            )

            current_date = self._get_next_date(current_date, recurring.frequency)

        return generated

    def _get_generation_start_date(self, recurring: RecurringExpense) -> date:
        """
        Determines the first date for which an expense should be generated.
        """
        if recurring.last_generated_date:
            return self._get_next_date(
                recurring.last_generated_date, recurring.frequency
            )

        return recurring.start_date

    def _get_next_date(
        self, current_date: date, frequency: RecurrenceFrequency
    ) -> date:
        """
        Calculates the next occurrence date based on the recurrence frequency.
        """
        if frequency == RecurrenceFrequency.MONTHLY:
            return self._add_month(current_date)

        if frequency == RecurrenceFrequency.YEARLY:
            return date(current_date.year + 1, current_date.month, current_date.day)

        raise ValueError(f"Unsupported frequency: {frequency}")

    def _add_month(self, current_date: date) -> date:
        """
        Adds one month to a date, keeping the day when possible.
        """
        year = current_date.year
        month = current_date.month + 1

        if month > 12:
            month = 1
            year += 1

        day = min(
            current_date.day,
            self._days_in_month(year, month),
        )

        return date(year, month, day)

    def _days_in_month(self, year: int, month: int) -> int:
        """
        Returns the number of days in a given month.
        """
        if month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                return 29
            return 28

        if month in {4, 6, 9, 11}:
            return 30

        return 31
