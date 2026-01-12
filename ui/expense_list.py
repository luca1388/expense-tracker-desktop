"""
Docstring for ui.expense_list
Defines the ExpenseListFrame for displaying a list of expenses.
"""

import tkinter as tk
from tkinter import ttk


class ExpenseListFrame(ttk.Frame):
    """
    Frame to display a list of expenses.

    """

    def __init__(self, parent, expense_repo):
        super().__init__(parent)
        self.expense_repo = expense_repo

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ttk.Label(self, text="Expenses", font=("Arial", 12, "bold")).pack(anchor="w")

        columns = ("date", "amount", "category", "description")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")

        self.tree.column("date", width=90)
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("category", width=120)
        self.tree.column("description", width=250)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def refresh(self):
        """Refreshes the expense list from the repository."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        expenses = self.expense_repo.get_all()

        for exp in expenses:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    exp.date.isoformat(),
                    f"{exp.amount:.2f}",
                    exp.category_id,  # miglioreremo con join o cache
                    exp.description or "",
                ),
            )
