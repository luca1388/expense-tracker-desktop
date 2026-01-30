"""Initialization module for loading base categories into the system."""

from persistence.db import get_connection
from services.category_service import CategoryService
from persistence.category_repository import CategoryRepository


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    connection = get_connection()
    repository = CategoryRepository(connection=connection)
    service = CategoryService(repository)

    service.bootstrap_default_categories()
