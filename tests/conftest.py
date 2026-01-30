import sqlite3
import pytest

from persistence.db import init_db


@pytest.fixture
def db_connection_test():
    """
    Provides a temporary in-memory database connection for testing.
    """
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()
