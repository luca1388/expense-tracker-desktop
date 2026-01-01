"""
Docstring for main
"""

import json

from datetime import date
from domain.models import Category
from persistence.db import init_db
from persistence.category_repository import CategoryRepository
from persistence.expense_repository import ExpenseRepository
from services.category_service import CategoryService
from services.expense_service import ExpenseService


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    repository = CategoryRepository()
    service = CategoryService(repository)

    service.bootstrap_default_categories()


def main() -> None:
    """
    Runs a simple manual test of the expense service.
    """
    # Initialize the database schema
    init_db()

    load_base_categories()

    # Create repository and service instances
    expense_repository = ExpenseRepository()
    expense_service = ExpenseService(expense_repository)

    # Create a test expense
    expense = expense_service.create_expense(
        date_=date.today(),
        amount=49.99,
        category_id=1,
        description="Test electricity bill",
        is_recurring=True,
        attachment_path="documents/electricity_bill.pdf",
        attachment_type="pdf",
    )

    print("Expense created:")
    print(expense)

    # Retrieve and print all expenses
    expenses = expense_service.get_all_expenses()

    print("\nAll expenses:")
    for exp in expenses:
        print(exp)


if __name__ == "__main__":
    main()
