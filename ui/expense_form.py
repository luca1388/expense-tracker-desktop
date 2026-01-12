"""
Docstring for ui.expense_form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from domain.models import Expense


class ExpenseFormFrame(ttk.Frame):
    """
    Docstring for ExpenseFormFrame
    Frame to add a new expense.
    """

    def __init__(self, parent, expense_repo, category_repo, on_expense_added):
        super().__init__(parent, padding=10)

        self.expense_repo = expense_repo
        self.category_repo = category_repo
        self.on_expense_added = on_expense_added

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Add Expense", font=("Arial", 12, "bold")).pack(anchor="w")

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        categories = self.category_repo.get_all()
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
        try:
            exp = Expense(
                id=None,
                created_at=date.fromisoformat(self.date_var.get()),
                date=date.fromisoformat(self.date_var.get()),
                amount=float(self.amount_var.get()),
                category_id=self.categories[self.category_cb.get()],
                description=self.desc_var.get(),
                is_recurring=False,
                attachment_path=None,
                attachment_type=None,
                analysis_data=None,
                analysis_summary=None,
            )

            self.expense_repo.add(exp)
            self.on_expense_added()

            self.amount_var.set("")
            self.desc_var.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))
