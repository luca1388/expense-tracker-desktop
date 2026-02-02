"""
Configuration file for pytest fixtures.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3
import pytest
from persistence.db import init_db
from persistence.recurring_expense_repository import RecurringExpenseRepository
from services.recurring_expense_service import RecurringExpenseService


@pytest.fixture
def db_connection_test():
    """
    Provides a temporary in-memory database connection for testing.
    """
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()


@pytest.fixture
def recurring_repository(db_connection_test):
    """
    Provides a RecurringExpenseRepository using the test DB connection.
    """
    return RecurringExpenseRepository(connection=db_connection_test)


@pytest.fixture
def recurring_service(recurring_repository):
    """
    Provides a RecurringExpenseService with only the recurring repository.
    """
    return RecurringExpenseService(
        recurring_repository=recurring_repository,
        expense_repository=None,  # possiamo aggiungere una fixture expense_repository più avanti
    )
