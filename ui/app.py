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
from ui.month_selector import MonthFilterFrame
from utils.dates import month_date_range


class ExpenseTrackerApp(tk.Tk):
    """
    Docstring for ExpenseTrackerApp
    """

    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("900x500")

        # Repositories
        self.expense_repo = ExpenseRepository()
        self.category_repo = CategoryRepository()

        self._build_ui()

    def _build_ui(self):
        # --- TOP: Month selector + total
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.filter_frame = MonthFilterFrame(
            main_frame, on_month_changed=self._on_month_changed
        )
        self.filter_frame.pack(fill=tk.X)

        # --- BOTTOM: content frame (Expense list + Add form)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Expense list
        self.expense_list = ExpenseListFrame(
            content_frame, expense_repo=self.expense_repo
        )
        self.expense_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: Add expense form
        self.expense_form = ExpenseFormFrame(
            content_frame,
            expense_repo=self.expense_repo,
            category_repo=self.category_repo,
            on_expense_added=self.expense_list.refresh,
        )
        self.expense_form.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_month_changed(self, year: int, month: int):
        """Callback triggered when the month selection changes."""
        if not hasattr(self, "filter_frame") or not hasattr(self, "expense_list"):
            return
        start_date, end_date = month_date_range(year, month)

        total = self.expense_list.refresh(start_date=start_date, end_date=end_date)
        self.filter_frame.update_total(total)
