"""
Docstring for ui.app
Defines the main application window for the Expense Tracker desktop app.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from persistence.expense_repository import ExpenseRepository
from persistence.category_repository import CategoryRepository

from services.category_service import CategoryService
from services.expense_service import ExpenseService
from ui.expense_list import ExpenseListFrame
from ui.toolbar import ToolbarFrame
from ui.add_expense_modal import AddExpenseModal
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
        self.expense_service = ExpenseService(ExpenseRepository())
        self.category_service = CategoryService(CategoryRepository())

        self._build_ui()

    def _build_ui(self):
        # --- TOP: Unified toolbar
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbar = ToolbarFrame(
            main_frame,
            on_month_changed=self._on_month_changed,
            on_edit_expense_requested=self._on_edit_expense_requested,
            on_delete_expense_requested=self._on_delete_expense_requested,
            on_add_expense_requested=self._on_add_expense_requested,
        )
        self.toolbar.pack(fill=tk.X)

        # --- BOTTOM: content frame (Expense list + Add form)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Expense list
        self.expense_list = ExpenseListFrame(
            content_frame,
            expense_service=self.expense_service,
            on_selection_changed=self._on_expense_selection_changed,
        )
        self.expense_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._on_month_changed(
            self.toolbar.year_var.get(), self.toolbar.get_selected_month_number()
        )

    def _on_expense_added(self, modal):
        """Refresh the expense list with the currently selected month after adding an expense."""

        start_date, end_date = month_date_range(
            self.toolbar.year_var.get(), self.toolbar.get_selected_month_number()
        )
        self.expense_list.refresh(start_date=start_date, end_date=end_date)
        self.toolbar.disable_actions()

        modal.destroy()

    def _on_month_changed(self, year: int, month: int):
        """Callback triggered when the month selection changes."""
        if not hasattr(self, "toolbar") or not hasattr(self, "expense_list"):
            return
        start_date, end_date = month_date_range(year, month)

        self.expense_list.refresh(start_date=start_date, end_date=end_date)
        self.toolbar.disable_actions()

    def _on_expense_selection_changed(self, has_selection: bool):
        """Callback triggered when expense selection changes."""
        if has_selection:
            self.toolbar.enable_actions()
        else:
            self.toolbar.disable_actions()

    def _on_edit_expense_requested(self):
        """Handle edit button click."""
        pass

    def _on_add_expense_requested(self):
        """Handle add expense action from the toolbar."""
        AddExpenseModal(
            self,
            expense_service=self.expense_service,
            category_service=self.category_service,
            on_expense_added=self._on_expense_added,
        )

    def _on_delete_expense_requested(self):
        """
        Handle delete expense action from the toolbar.
        """
        expense_id = self.expense_list.get_selected_expense_id()
        if expense_id is None:
            return

        confirmed = messagebox.askyesno(
            title="Conferma eliminazione",
            message="Sei sicuro di voler eliminare la spesa selezionata?",
        )
        if not confirmed:
            return

        self.expense_service.delete_expense(expense_id)

        # Refresh current month
        year = self.toolbar.year_var.get()
        month = self.toolbar.get_selected_month_number()
        start_date, end_date = month_date_range(year, month)

        self.expense_list.refresh(start_date=start_date, end_date=end_date)
