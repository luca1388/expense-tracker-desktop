"""
Docstring for ui.app
Defines the main application window for the Expense Tracker desktop app.
"""

import tkinter as tk
from tkinter import ttk

from persistence.expense_repository import ExpenseRepository
from persistence.category_repository import CategoryRepository

from ui.expense_list import ExpenseListFrame

from ui.expense_form import ExpenseFormFrame


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("900x500")

        # Repositories
        self.expense_repo = ExpenseRepository()
        self.category_repo = CategoryRepository()

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Expense list
        self.expense_list = ExpenseListFrame(main_frame, expense_repo=self.expense_repo)
        self.expense_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: Add expense form
        self.expense_form = ExpenseFormFrame(
            main_frame,
            expense_repo=self.expense_repo,
            category_repo=self.category_repo,
            on_expense_added=self.expense_list.refresh,
        )
        self.expense_form.pack(side=tk.RIGHT, fill=tk.Y)
