"""
Docstring for ui.expense_form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class ExpenseFormFrame(ttk.Frame):
    """
    Docstring for ExpenseFormFrame
    Frame to add a new expense.
    """

    def __init__(self, parent, expense_service, category_service, on_expense_added):
        super().__init__(parent, padding=10)

        self.expense_service = expense_service
        self.category_service = category_service
        self.on_expense_added = on_expense_added

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Add Expense", font=("Arial", 12, "bold")).pack(anchor="w")

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        categories = self.category_service.get_all_categories()
        self.categories = {c.name: c.id for c in categories}

        ttk.Label(self, text="Date (YYYY-MM-DD)").pack(anchor="w")
        ttk.Entry(self, textvariable=self.date_var).pack(fill=tk.X)

        ttk.Label(self, text="Amount").pack(anchor="w")
        ttk.Entry(self, textvariable=self.amount_var).pack(fill=tk.X)

        ttk.Label(self, text="Category").pack(anchor="w")
        self.category_cb = ttk.Combobox(
            self, values=list(self.categories.keys()), state="readonly"
        )
        self.category_cb.pack(fill=tk.X)
        self.category_cb.current(0)

        ttk.Label(self, text="Description").pack(anchor="w")
        ttk.Entry(self, textvariable=self.desc_var).pack(fill=tk.X)

        ttk.Button(self, text="Add Expense", command=self._submit).pack(pady=10)

    def _submit(self):
        validation_error = self._validate_form()
        if validation_error:
            messagebox.showerror("Validation Error", validation_error)
            return

        try:
            self.expense_service.create_expense(
                date_=date.fromisoformat(self.date_var.get()),
                amount=float(self.amount_var.get()),
                category_id=self.categories[self.category_cb.get()],
                description=self.desc_var.get(),
                is_recurring=False,
                attachment_path=None,
                attachment_type=None,
                analysis_data=None,
                analysis_summary=None,
            )
            self.on_expense_added()

            self.amount_var.set("")
            self.desc_var.set("")
            self.category_cb.current(0)
            messagebox.showinfo("Success", "Expense added successfully!")

        except ValueError as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

    def _validate_form(self):
        """Validate all form fields. Returns error message if validation fails, None otherwise."""

        # Validate date
        date_str = self.date_var.get().strip()
        if not date_str:
            return "Date cannot be empty."
        try:
            date.fromisoformat(date_str)
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-13)."

        # Validate amount
        amount_str = self.amount_var.get().strip()
        if not amount_str:
            return "Amount cannot be empty."
        try:
            amount = float(amount_str)
            if amount <= 0:
                return "Amount must be a positive number."
        except ValueError:
            return "Invalid amount. Please enter a valid number."

        # Validate category
        if not self.category_cb.get():
            return "Please select a category."

        # Validate description
        description = self.desc_var.get().strip()
        if not description:
            return "Description cannot be empty."
        if len(description) > 100:
            return "Description is too long (max 100 characters)."

        return None
