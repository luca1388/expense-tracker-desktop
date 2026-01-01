"""
services/expense_service.py

Service layer for managing expenses.
Contains business logic and coordinates repositories.
"""

from datetime import date, datetime
from typing import Optional

from domain.models import Expense
from persistence.expense_repository import ExpenseRepository


class ExpenseService:
    """
    Service responsible for expense-related business logic.
    """

    def __init__(self, repository: ExpenseRepository) -> None:
        """
        Initializes the service with a repository dependency.
        """
        self._repository = repository

    def create_expense(
        self,
        *,
        date_: date,
        amount: float,
        category_id: int,
        description: Optional[str] = None,
        is_recurring: bool = False,
        attachment_path: Optional[str] = None,
        attachment_type: Optional[str] = None,
        analysis_data: Optional[str] = None,
        analysis_summary: Optional[str] = None,
    ) -> Expense:
        """
        Creates and persists a new expense.

        Returns:
            Expense: The newly created expense
        """
        self._validate_amount(amount)

        expense = Expense(
            id=None,
            date=date_,
            amount=amount,
            category_id=category_id,
            description=description,
            is_recurring=is_recurring,
            attachment_path=attachment_path,
            attachment_type=attachment_type,
            analysis_data=analysis_data,
            analysis_summary=analysis_summary,
            created_at=datetime.now(),
        )

        return self._repository.add(expense)

    def get_expenses_for_period(
        self,
        start_date: date,
        end_date: date,
    ) -> list[Expense]:
        """
        Retrieves expenses within a specific time period.
        """
        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        return self._repository.get_by_period(start_date, end_date)

    def get_all_expenses(self) -> list[Expense]:
        """
        Retrieves all expenses.
        """
        return self._repository.get_all()

    def _validate_amount(self, amount: float) -> None:
        """
        Validates that the expense amount is positive.
        """
        if amount <= 0:
            raise ValueError("Expense amount must be greater than zero")
