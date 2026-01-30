"""
Docstring for main_ui
"""

from init import load_base_categories
from persistence.db import get_connection, init_db
from ui.app import ExpenseTrackerApp

if __name__ == "__main__":
    try:
        init_db(get_connection())
        load_base_categories()

        app = ExpenseTrackerApp()
        app.mainloop()
    except KeyboardInterrupt as e:
        print("Application interrupted by user.")
