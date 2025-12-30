"""
Docstring for main
"""

import json

from datetime import date
from domain.models import Category
from persistence.db import init_db
from persistence.category_repository import CategoryRepository
from persistence.expense_repository import ExpenseRepository
from services.expense_service import ExpenseService


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    repo = CategoryRepository()
    existing = {c.name for c in repo.get_all()}

    with open("resources/categories.json", "r", encoding="utf-8") as f:
        base_categories = json.load(f)

    for name in base_categories:
        if name not in existing:
            repo.add(Category(id=None, name=name, is_custom=False))


def main() -> None:
    """
    Runs a simple manual test of the expense service.
    """
    # Initialize the database schema
    init_db()

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
