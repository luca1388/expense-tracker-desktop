from datetime import date

from persistence.recurring_expense_repository import RecurringExpenseRepository
from services.recurring_expense_service import RecurringExpenseService
from domain.models import RecurrenceFrequency, RecurringExpense


def test_stop_recurring_sets_end_date_today(db_connection_test):
    """
    Docstring for test_stop_recurring_sets_end_date_today

    :param tmp_path: Description
    :type tmp_path: Path
    """
    # --- setup ---
    repository = RecurringExpenseRepository(connection=db_connection_test)
    service = RecurringExpenseService(
        recurring_repository=repository, expense_repository=None
    )

    # --- create recurring ---
    recurring = RecurringExpense(
        id=None,
        name="Netflix",
        amount=9.99,
        category_id=1,
        frequency=RecurrenceFrequency.MONTHLY,
        start_date=date(2024, 1, 1),
        end_date=None,
        description=None,
        attachment_path=None,
        attachment_type=None,
        last_generated_date=None,
        created_at=date.today(),
    )

    recurring = repository.add(recurring)

    # --- action ---
    service.stop_recurring_expense(recurring.id, end_date=date.today())

    # --- assert ---
    updated = repository.get_by_id(recurring.id)

    assert updated.end_date == date.today()


def test_stop_recurring_sets_end_date_today_no_date_provided(db_connection_test):
    """
    Docstring for test_stop_recurring_sets_end_date_today

    :param tmp_path: Description
    :type tmp_path: Path
    """
    # --- setup ---
    repository = RecurringExpenseRepository(connection=db_connection_test)
    service = RecurringExpenseService(
        recurring_repository=repository, expense_repository=None
    )

    # --- create recurring ---
    recurring = RecurringExpense(
        id=None,
        name="Netflix",
        amount=9.99,
        category_id=1,
        frequency=RecurrenceFrequency.MONTHLY,
        start_date=date(2024, 1, 1),
        end_date=None,
        description=None,
        attachment_path=None,
        attachment_type=None,
        last_generated_date=None,
        created_at=date.today(),
    )

    recurring = repository.add(recurring)

    # --- action ---
    service.stop_recurring_expense(recurring.id)

    # --- assert ---
    updated = repository.get_by_id(recurring.id)

    assert updated.end_date == date.today()
