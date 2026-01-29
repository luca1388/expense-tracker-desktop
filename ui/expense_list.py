"""
Docstring for ui.expense_list
Defines the ExpenseListFrame for displaying a list of expenses.
"""

from datetime import date
import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox
from services.recurring_expense_service import RecurringExpenseService
from utils.frequency_constants import FREQUENCY_LABELS


class ExpenseListFrame(ttk.Frame):
    """
    Frame to display a list of expenses.

    """

    def __init__(
        self,
        parent,
        expense_service,
        recurring_expense_service: RecurringExpenseService | None = None,
        on_selection_changed=None,
        on_refresh_requested=None,
    ):
        super().__init__(parent)
        self.expense_service = expense_service
        self.recurring_expense_service = recurring_expense_service
        self.on_selection_changed = on_selection_changed
        self._selected_recurring_id = None
        self._on_refresh_requested = on_refresh_requested

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
            print(f"Stopping recurring expense ID {self._selected_recurring_id}")
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

        # try:
        #     self.recurring_service.stop_recurring_expense(self._selected_recurring_id)
        #     messagebox.showinfo("Success", "Recurring expense stopped.")
        #     self.refresh()  # aggiorna la lista
        # except ValueError as e:
        #     messagebox.showerror("Error", str(e))
