"""
Docstring for persistence.repositories
Handles data access for the expense tracker application.

This module provides repository classes to interact with the database
for managing expense categories.
"""

from domain.models import Category
from persistence.db import get_connection


class CategoryRepository:
    """Repository for managing expense categories in the database."""

    def get_all(self) -> list[Category]:
        """
        Docstring for get_all

        :param self: Description
        :return: Description
        :rtype: list[Category]
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, is_custom FROM categories")
            rows = cursor.fetchall()

        return [
            Category(id=row[0], name=row[1], is_custom=bool(row[2])) for row in rows
        ]

    def add(self, category: Category) -> None:
        """Adds a new category to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, is_custom) VALUES (?, ?)",
                (category.name, int(category.is_custom)),
            )
            conn.commit()
