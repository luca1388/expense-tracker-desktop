"""
Docstring for ui.expense_list
Defines the ExpenseListFrame for displaying a list of expenses.
"""

import tkinter as tk
from tkinter import ttk
from utils.frequency_constants import FREQUENCY_LABELS


class ExpenseListFrame(ttk.Frame):
    """
    Frame to display a list of expenses.

    """

    def __init__(
        self,
        parent,
        expense_service,
        recurring_expense_service=None,
        on_selection_changed=None,
    ):
        super().__init__(parent)
        self.expense_service = expense_service
        self.recurring_expense_service = recurring_expense_service
        self.on_selection_changed = on_selection_changed

        self._build_ui()
        # Improvement: insert the current month expenses by default
        # self.refresh(start_date=None, end_date=None)

    def _build_ui(self):
        # Header frame with title and total
        header_frame = ttk.Frame(self)
        header_frame.pack(anchor="w", fill=tk.X, pady=(0, 5))

        ttk.Label(header_frame, text="Spese", font=("Arial", 12, "bold")).pack(
            side=tk.LEFT
        )

        self.total_label = ttk.Label(
            header_frame, text="Totale: € 0.00", font=("Arial", 10, "bold")
        )
        self.total_label.pack(side=tk.RIGHT)

        columns = ("id", "data", "importo", "categoria", "descrizione", "frequenza")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.tag_configure("recurring", background="#F5FAFF")

        self.tree.heading("id", text="ID")
        self.tree.heading("data", text="Data")
        self.tree.heading("importo", text="Importo")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("descrizione", text="Descrizione")
        self.tree.heading("frequenza", text="Frequenza")

        self.tree.column("id", width=0)
        self.tree.column("data", width=90)
        self.tree.column("importo", width=80, anchor="e")
        self.tree.column("categoria", width=120)
        self.tree.column("descrizione", width=250)
        self.tree.column("frequenza", width=120)

        # Enable / disable buttons based on selection
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_changed)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def refresh(self, start_date, end_date) -> float:
        """Refreshes the expense list from the repository."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0.0
        if not start_date or not end_date:
            expenses = self.expense_service.get_all_expenses()
        else:
            expenses = self.expense_service.get_expenses_for_period(
                start_date, end_date
            )

        for exp in expenses:
            total += exp.amount

            # Get frequency if this is a recurring expense
            frequency_display = "-"
            if exp.recurring_expense_id:

                # Fetch the recurring expense to get its frequency
                recurring = self.recurring_expense_service.get_recurring_expense_by_id(
                    exp.recurring_expense_id
                )
                if recurring:
                    frequency_display = FREQUENCY_LABELS.get(recurring.frequency, "")

            self.tree.insert(
                "",
                tk.END,
                values=(
                    exp.id,
                    exp.date.isoformat(),
                    f"{exp.amount:.2f}",
                    exp.category_id,  # miglioreremo con join o cache
                    exp.description or "",
                    frequency_display,
                ),
                tags=("recurring",) if exp.recurring_expense_id else (),
            )

        self.total_label.config(text=f"Totale: € {total:.2f}")
        return total

    def _on_selection_changed(self, _event) -> None:
        """Notify parent when selection changes."""
        has_selection = bool(self.tree.selection())
        selected_id = self.get_selected_expense_id()
        if self.on_selection_changed:
            self.on_selection_changed(selected_id if has_selection else None)

    def get_selected_expense_id(self) -> int | None:
        """
        Return the ID of the currently selected expense, if any.
        """
        selection = self.tree.selection()
        if not selection:
            return None

        # Get the tree item and extract the ID from the first value column
        item = selection[0]
        values = self.tree.item(item, "values")
        return int(values[0]) if values else None
