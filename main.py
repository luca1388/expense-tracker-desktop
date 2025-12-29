"""
Docstring for main
"""

import json
from domain.models import Category
from persistence.db import init_db
from persistence.repositories import CategoryRepository


def load_base_categories():
    """Loads base categories from a JSON file into the database."""
    repo = CategoryRepository()
    existing = {c.name for c in repo.get_all()}

    with open("resources/categories.json", "r", encoding="utf-8") as f:
        base_categories = json.load(f)

    for name in base_categories:
        if name not in existing:
            repo.add(Category(id=None, name=name, is_custom=False))


def main():
    """
    Docstring for main
    """
    init_db()
    load_base_categories()
    print("Database e categorie inizializzati correttamente.")


if __name__ == "__main__":
    main()
