import tkinter as tk
from tkinter import ttk
from datetime import date
from ui.add_expense_modal import AddExpenseModal


class ExpenseActions(ttk.Frame):
    """
    Unified toolbar containing:
    - Month/year filter selector with prev/next navigation
    - Edit/delete action buttons for expenses
    """

    def __init__(
        self,
        parent,
        *,
        expense_service=None,
        category_service=None,
        recurring_expense_service=None,
        on_delete_expense_requested=None,
        on_expense_added=None,
        update_expense_requested=None,
        create_expense_requested=None,
        delete_expense_requested=None,
        on_refresh=None,
    ):
        super().__init__(parent)

        self.on_delete_expense_requested = on_delete_expense_requested
        self.on_expense_added = on_expense_added
        self.expense_service = expense_service
        self.category_service = category_service
        self.recurring_expense_service = recurring_expense_service
        self.update_expense_requested = update_expense_requested
        self.create_expense_requested = create_expense_requested
        self.delete_expense_requested = delete_expense_requested
        self.on_refresh = on_refresh

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(side=tk.LEFT, fill=tk.X, expand=False, pady=(5, 0))

        self.add_button = ttk.Button(
            frame,
            text="Nuova spesa",
            command=self.create_expense_requested,
        )
        self.add_button.pack(side=tk.LEFT)

        self.edit_button = ttk.Button(
            frame,
            text="Modifica",
            command=self.update_expense_requested,
            state=tk.DISABLED,
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(
            frame,
            text="Elimina",
            command=self.delete_expense_requested,
            state=tk.DISABLED,
        )
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))

    def enable_actions(self):
        """Enable action buttons."""
        self.edit_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)

    def disable_actions(self):
        """Disable action buttons."""
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
