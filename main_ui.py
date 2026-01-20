"""
Docstring for main_ui
"""

from init import load_base_categories
from persistence.db import init_db
from ui.app import ExpenseTrackerApp

if __name__ == "__main__":
    init_db()
    load_base_categories()

    app = ExpenseTrackerApp()
    app.mainloop()
