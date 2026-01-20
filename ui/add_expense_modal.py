"""
Docstring for ui.add_expense_modal
Defines a reusable modal window for adding a new expense.
"""

import tkinter as tk
from tkinter import ttk

from ui.expense_form import ExpenseFormFrame


class AddExpenseModal(tk.Toplevel):
    """
    A modal window for adding a new expense.
    Encapsulates the modal creation, layout, and form handling.
    """

    def __init__(self, parent, expense_service, category_service, on_expense_added):
        """
        Initialize the add expense modal.

        Args:
            parent: The parent window
            expense_service: Service for managing expenses
            category_service: Service for managing categories
            on_expense_added: Callback function invoked when expense is successfully added
        """
        super().__init__(parent)

        self.title("Nuova spesa")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.bind("<Escape>", lambda e: self.destroy())
        # self.bind("<Return>", lambda e: self.submit())

        # Position modal relative to parent window
        self._position_modal(parent)

        # Build the modal UI
        self._build_ui(expense_service, category_service, on_expense_added)

    def _position_modal(self, parent):
        """Position the modal window at the center of the screen."""
        # Set explicit modal dimensions
        modal_width = 400
        modal_height = 300
        self.geometry(f"{modal_width}x{modal_height}")

        self.update_idletasks()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        x = (screen_width - modal_width) // 2
        y = (screen_height - modal_height) // 2

        self.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

    def _build_ui(self, expense_service, category_service, on_expense_added):
        """Build the modal UI with form and buttons."""
        # Content frame for the form
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Footer frame for buttons
        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Create the expense form
        form = ExpenseFormFrame(
            content,
            expense_service=expense_service,
            category_service=category_service,
            on_expense_added=lambda: on_expense_added(self),
        )
        form.pack(fill=tk.BOTH, padx=10, pady=10)

        # Cancel button
        ttk.Button(
            footer,
            text="Annulla",
            command=self.destroy,
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Save button
        ttk.Button(
            footer,
            text="Salva",
            command=form.submit,
        ).pack(side=tk.RIGHT)
