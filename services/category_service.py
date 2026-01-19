"""
services/category_service.py

Service layer responsible for category-related business logic,
including initial bootstrap of default categories.
"""

import json
from pathlib import Path
from domain.models import Category
from persistence.category_repository import CategoryRepository


# DEFAULT_CATEGORIES = [
#     "Electricity",
#     "Gas",
#     "Water",
#     "Internet",
#     "Rent",
#     "Groceries",
#     "Transport",
#     "Subscriptions",
# ]


class CategoryService:
    """
    Service responsible for category management.
    """

    def __init__(self, repository: CategoryRepository) -> None:
        """
        Initializes the service with a category repository.
        """
        self._repository = repository

        json_path = Path("resources/default_categories.json")

        if not json_path.exists():
            raise FileNotFoundError("Default categories JSON file not found")

        with json_path.open("r", encoding="utf-8") as file:
            self._categories = json.load(file)

    def bootstrap_default_categories(self) -> None:
        """
        Ensures that default categories exist in the database.
        This operation is idempotent.
        """
        existing_categories = self._repository.get_all()
        existing_names = {category.name for category in existing_categories}

        for category in self._categories:
            if category["name"] not in existing_names:
                category = Category(
                    id=None,
                    name=category["name"],
                    is_custom=False,
                )
                self._repository.add(category)

    def get_all_categories(self) -> list[Category]:
        """
        Retrieves all categories from the repository.

        Returns:
            list[Category]: List of all categories.
        """
        return self._repository.get_all()
