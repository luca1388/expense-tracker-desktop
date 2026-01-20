"""Initialization module for loading base categories into the system."""

from services.category_service import CategoryService
from persistence.category_repository import CategoryRepository


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    repository = CategoryRepository()
    service = CategoryService(repository)

    service.bootstrap_default_categories()
