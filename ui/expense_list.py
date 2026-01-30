"""
Docstring for ui.expense_list
Defines the ExpenseListFrame for displaying a list of expenses.
"""

from datetime import date
import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox
from services.category_service import CategoryService
from services.expense_service import ExpenseService, ExpenseSortField
from services.recurring_expense_service import RecurringExpenseService
from utils.frequency_constants import FREQUENCY_LABELS


COLUMN_SORT_MAPPING = {
    "date": ExpenseSortField.DATE,
    "amount": ExpenseSortField.AMOUNT,
    "category": ExpenseSortField.CATEGORY,
}

SORT_FIELD_TO_COLUMN_ID = {
    ExpenseSortField.DATE: "date",
    ExpenseSortField.AMOUNT: "amount",
    ExpenseSortField.CATEGORY: "category",
}


class ExpenseListFrame(ttk.Frame):
    """
    Frame to display a list of expenses.

    """

    def __init__(
        self,
        parent,
        expense_service: ExpenseService,
        recurring_expense_service: RecurringExpenseService | None = None,
        category_service: CategoryService | None = None,
        on_selection_changed=None,
        on_refresh_requested=None,
        on_sort_requested=None,
    ):
        super().__init__(parent)
        self.expense_service = expense_service
        self.recurring_expense_service = recurring_expense_service
        self.category_service = category_service
        self.on_selection_changed = on_selection_changed
        self._selected_recurring_id = None
        self._on_refresh_requested = on_refresh_requested
        self._on_sort_requested = on_sort_requested

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

        # self.total_label = ttk.Label(
        #     header_frame, text="Totale: € 0.00", font=("Arial", 10, "bold")
        # )
        # self.total_label.pack(side=tk.RIGHT)

        columns = ("id", "data", "importo", "categoria", "descrizione", "frequenza")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.column("id", width=0, stretch=False)

        self.tree.tag_configure("recurring", background="#F5FAFF")
        # self.tree.tag_configure(
        #     "recurring_stopped", foreground="#888888"  # grigio soft
        # )

        self.tree.bind("<Button-3>", self._on_right_click)

        # Menu contestuale
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="Interrompi spesa ricorrente",
            command=self._on_stop_recurring_selected,
        )

        self.tree.heading(
            "id",
            text="ID",
            anchor="w",
            command=lambda: self._on_column_header_clicked("id"),
        )
        self.tree.heading(
            "data",
            text="Data",
            anchor="w",
            command=lambda: self._on_column_header_clicked("date"),
        )
        self.tree.heading(
            "importo",
            text="Importo",
            anchor="w",
            command=lambda: self._on_column_header_clicked("amount"),
        )
        self.tree.heading(
            "categoria",
            text="Categoria",
            anchor="w",
            command=lambda: self._on_column_header_clicked("category"),
        )
        self.tree.heading(
            "descrizione",
            text="Descrizione",
            anchor="w",
            command=lambda: self._on_column_header_clicked("description"),
        )
        self.tree.heading(
            "frequenza",
            text="Frequenza",
            anchor="w",
            command=lambda: self._on_column_header_clicked("frequency"),
        )

        self.tree.column("id", width=0, anchor="w")
        self.tree.column("data", width=90, anchor="w")
        self.tree.column("importo", width=80, anchor="w")
        self.tree.column("categoria", width=120, anchor="w")
        self.tree.column("descrizione", width=250, anchor="w")
        self.tree.column("frequenza", width=120, anchor="w")

        # Enable / disable buttons based on selection
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_changed)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 2. FOOTER FISSO (La riga grigia)
        self.footer = tk.Frame(self, bg="#f0f0f0", height=30)  # Grigio chiaro
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer.pack_propagate(False)  # Forza l'altezza fissa

        self.total_label_footer = ttk.Label(
            self.footer,
            text="Totale: € 0.00",
            background="#f0f0f0",
            font=("TkDefaultFont", 10, "bold"),
        )
        # Il padding a destra dovrebbe idealmente corrispondere alla larghezza
        # della scrollbar + eventuali margini per allinearsi alla colonna Amount
        self.total_label_footer.pack(side=tk.LEFT, padx=(10, 0))

    def refresh(self, start_date, end_date, sort_field, sort_direction) -> float:
        """Refreshes the expense list from the repository."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0.0
        if not start_date or not end_date:
            expenses = self.expense_service.get_all_expenses_sorted(
                sort_by=sort_field, direction=sort_direction
            )
        else:
            expenses = self.expense_service.get_expenses_for_month_sorted(
                start_date,
                end_date,
                sort_by=sort_field,
                direction=sort_direction,
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

            # Get category name
            category_name = (
                self.category_service.get_category_by_id(exp.category_id).name
                if self.category_service
                else "N/A"
            )

            self.tree.insert(
                "",
                tk.END,
                iid=str(exp.id),  # ID come iid
                values=(
                    exp.id,
                    exp.date.isoformat(),
                    f"{exp.amount:.2f}",
                    category_name,
                    exp.description or "",
                    frequency_display,
                ),
                tags=("recurring",) if exp.recurring_expense_id else (),
            )

        # self.total_label.config(text=f"Totale: € {total:.2f}")
        self.total_label_footer.config(text=f"Totale: € {total:.2f}")
        return total

    def _on_selection_changed(self, _event) -> None:
        """Notify parent when selection changes."""
        has_selection = bool(self.tree.selection())
        selected_id = self.get_selected_expense_id()
        print(f"Expense selection changed: {selected_id}")
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

    def _on_right_click(self, event):
        # 🔹 Seleziona esplicitamente la riga
        # Individua riga sotto il click
        item_id = self.tree.identify_row(event.y)
        self.tree.selection_set(item_id)
        self.tree.focus(item_id)

        if not item_id:
            return  # click su vuoto

        # Salva ID per callback menu
        expense = self.tree.item(item_id, "values")

        # print(f"Right-clicked expense: {expense}")
        is_recurring = True if expense[-1] != "-" else False
        expense_id = int(expense[0])
        expense = self.expense_service.get_by_id(expense_id)

        if not is_recurring:
            return  # menu disponibile solo per recurring

        self._selected_recurring_id = expense.recurring_expense_id
        self.context_menu.post(event.x_root, event.y_root)

    def _on_stop_recurring_selected(self):
        if self._selected_recurring_id is None:
            return

        confirm = messagebox.askyesno(
            "Interrompi spesa ricorrente",
            "Vuoi interrompere questa spesa ricorrente? Le spese già registrate non verranno modificate.",
        )
        if not confirm:
            return

        try:
            # print(f"Stopping recurring expense ID {self._selected_recurring_id}")
            self.recurring_expense_service.stop_recurring_expense(
                self._selected_recurring_id, end_date=date.today()
            )
            messagebox.showinfo(
                "Operazione completata", "Spesa ricorrente interrotta correttamente."
            )
            self._on_refresh_requested()
        except ValueError as e:
            print(f"error stopping recurring expense: {e}")
            messagebox.showerror("Attenzione", "Questa spesa risulta già interrotta.")

    def _on_column_header_clicked(self, column_id: str) -> None:
        # print(f"Column header clicked: {column_id}")
        sort_field = COLUMN_SORT_MAPPING.get(column_id)
        # print(f"Mapped sort field: {sort_field}")
        if sort_field is None:
            return

        self._on_sort_requested(sort_field)

    def set_sorted_column(self, sort_field: ExpenseSortField) -> None:
        """
        Docstring for set_sorted_column

        :param self: Description
        :param sort_field: Description
        :type sort_field: ExpenseSortField
        """
        return
        active_column = SORT_FIELD_TO_COLUMN_ID.get(sort_field)

        for column_id in self.tree["columns"]:
            style = (
                "Sorted.Treeview.Heading"
                if column_id == active_column
                else "Treeview.Heading"
            )
            print(f"Setting style for column {column_id}: {style}")
            self.tree.heading(column_id, style=style)
