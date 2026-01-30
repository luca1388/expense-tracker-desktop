from datetime import date

import pytest

from domain.models import RecurrenceFrequency, RecurringExpense


def test_stop_recurring_sets_end_date_today(recurring_repository, recurring_service):
    """
    Docstring for test_stop_recurring_sets_end_date_today

    :param tmp_path: Description
    :type tmp_path: Path
    """
    # --- setup ---
    # done with fixtures passed from conftest.py

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

    recurring = recurring_repository.add(recurring)

    # --- action ---
    recurring_service.stop_recurring_expense(recurring.id, end_date=date.today())

    # --- assert ---
    updated = recurring_repository.get_by_id(recurring.id)

    assert updated.end_date == date.today()


def test_stop_recurring_sets_end_date_today_no_date_provided(
    recurring_repository, recurring_service
):
    """
    Docstring for test_stop_recurring_sets_end_date_today

    :param tmp_path: Description
    :type tmp_path: Path
    """

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

    recurring = recurring_repository.add(recurring)

    # --- action ---
    recurring_service.stop_recurring_expense(recurring.id)

    # --- assert ---
    updated = recurring_repository.get_by_id(recurring.id)

    assert updated.end_date == date.today()


def test_stop_recurring_already_stopped(recurring_repository, recurring_service):
    """
    Docstring for test_stop_recurring_already_stopped

    :param db_connection_test: Description
    """

    # --- create recurring already stopped ---
    stopped_date = date(2025, 1, 1)
    recurring = RecurringExpense(
        id=None,
        name="Netflix",
        amount=9.99,
        category_id=1,
        frequency=RecurrenceFrequency.MONTHLY,
        start_date=date(2024, 1, 1),
        end_date=stopped_date,  # già stoppata
        description=None,
        attachment_path=None,
        attachment_type=None,
        last_generated_date=None,
        created_at=date.today(),
    )
    recurring = recurring_repository.add(recurring)

    # --- action & assert: ci aspettiamo ValueError ---
    with pytest.raises(ValueError):  # , match="Recurring expense is already stopped"
        recurring_service.stop_recurring_expense(recurring.id)


def test_stop_recurring_nonexistent_raises(recurring_service):
    """
    Docstring for test_stop_recurring_nonexistent_raises

    :param db_connection_test: Description
    :type db_connection_test: Connection
    """

    non_existent_id = 9999  # id che sicuramente non esiste

    # ci aspettiamo un ValueError chiaro
    with pytest.raises(ValueError):
        recurring_service.stop_recurring_expense(non_existent_id)
