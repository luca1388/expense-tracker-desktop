"""
Docstring for main
"""

from datetime import date
from domain.models import RecurrenceFrequency, RecurringExpense
from persistence.db import init_db
from persistence.category_repository import CategoryRepository
from persistence.expense_repository import ExpenseRepository
from persistence.recurring_expense_repository import RecurringExpenseRepository
from services.category_service import CategoryService
from services.expense_service import ExpenseService
from services.recurring_expense_service import RecurringExpenseService


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    repository = CategoryRepository()
    service = CategoryService(repository)

    service.bootstrap_default_categories()


def bootstrap_recurring_expense(category_id: int) -> None:
    """
    Creates a recurring expense if it does not already exist.
    """
    recurring_repo = RecurringExpenseRepository()

    existing = recurring_repo.get_by_name("Electricity Bill")
    if existing:
        return

    recurring = RecurringExpense(
        id=None,
        name="Electricity Bill",
        amount=120.0,
        category_id=category_id,
        frequency=RecurrenceFrequency.MONTHLY,
        start_date=date(2024, 1, 1),
        end_date=None,
        description="Monthly electricity bill",
        attachment_path=None,
        attachment_type=None,
        last_generated_date=None,
        # created_at=None,  # Will be set by the repository
    )

    recurring_repo.add(recurring)


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

    category_repo = CategoryRepository()
    electricity_category = category_repo.get_by_name("Luce")

    if not electricity_category:
        raise RuntimeError("Electricity category not found")

    print(electricity_category)

    bootstrap_recurring_expense(electricity_category.id)

    # Run recurring expense generation
    recurring_repo = RecurringExpenseRepository()
    expense_repo = ExpenseRepository()
    service = RecurringExpenseService(recurring_repo, expense_repo)

    today = date.today()
    generated = service.generate_missing_expenses(up_to=today)

    print(f"Generated {len(generated)} expenses:")
    for expense in generated:
        print(
            f"- {expense.date} | {expense.amount}€ | "
            f"category_id={expense.category_id}"
        )


if __name__ == "__main__":
    main()
