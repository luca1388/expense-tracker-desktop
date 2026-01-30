"""
Docstring for persistence.repositories
Handles data access for the expense tracker application.

This module provides repository classes to interact with the database
for managing expense categories.
"""

import sqlite3
from typing import Optional
from domain.models import Category


class CategoryRepository:
    """Repository for managing expense categories in the database."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def get_all(self) -> list[Category]:
        """
        Docstring for get_all

        :param self: Description
        :return: Description
        :rtype: list[Category]
        """
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, is_custom FROM categories")
            rows = cursor.fetchall()

        return [
            Category(id=row[0], name=row[1], is_custom=bool(row[2])) for row in rows
        ]

    def add(self, category: Category) -> None:
        """Adds a new category to the database"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, is_custom) VALUES (?, ?)",
                (category.name, int(category.is_custom)),
            )
            conn.commit()

    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Returns a category by its name, if it exists.
        """
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Category(id=row[0], name=row[1], is_custom=bool(row[2]))
