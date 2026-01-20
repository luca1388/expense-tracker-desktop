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

        form = ttk.Frame(self)
        form.grid(row=0, column=0, sticky="nsew")

        form.columnconfigure(0, weight=0)  # label
        form.columnconfigure(1, weight=1)  # input

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        categories = self.category_service.get_all_categories()
        self.categories = {c.name: c.id for c in categories}

        self.category_combo = ttk.Combobox(
            form, values=list(self.categories.keys()), state="readonly"
        )
        self.category_combo.current(0)

        self.date_entry = ttk.Entry(form, textvariable=self.date_var)
        self.amount_entry = ttk.Entry(form, textvariable=self.amount_var)
        self.description_entry = ttk.Entry(form, textvariable=self.desc_var)

        self._add_row(form, 0, "Data", self.date_entry)
        self._add_row(form, 1, "Importo", self.amount_entry)
        self._add_row(form, 2, "Category", self.category_combo)
        self._add_row(form, 3, "Descrizione", self.description_entry)

    def submit(self):
        """
        Docstring for submit

        :param self: Description
        """
        validation_error = self._validate_form()
        if validation_error:
            messagebox.showerror("Validation Error", validation_error)
            return

        try:
            self.expense_service.create_expense(
                date_=date.fromisoformat(self.date_var.get()),
                amount=float(self.amount_var.get()),
                category_id=self.categories[self.category_combo.get()],
                description=self.desc_var.get(),
                is_recurring=False,
                attachment_path=None,
                attachment_type=None,
                analysis_data=None,
                analysis_summary=None,
            )

            self.amount_var.set("")
            self.desc_var.set("")
            self.category_combo.current(0)
            messagebox.showinfo("Success", "Expense added successfully!")

            self.on_expense_added()

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
        if not self.category_combo.get():
            return "Please select a category."

        # Validate description
        description = self.desc_var.get().strip()
        if not description:
            return "Description cannot be empty."
        if len(description) > 100:
            return "Description is too long (max 100 characters)."

        return None

    def _add_row(self, parent, row, label_text, widget):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=6)

        widget.grid(row=row, column=1, sticky="ew", pady=6)
