"""
Docstring for ui.expense_form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from domain.models import Expense
from utils.frequency_constants import FREQUENCY_FORM_OPTIONS


class ExpenseFormFrame(ttk.Frame):
    """
    Docstring for ExpenseFormFrame
    Frame to add a new expense.
    """

    def __init__(
        self,
        parent,
        expense_service,
        category_service,
        recurring_expense_service,
        on_expense_added,
        on_update_requested,
        expense_to_modify=None,
    ):
        super().__init__(parent, padding=10)

        self.expense_service = expense_service
        self.category_service = category_service
        self.recurring_expense_service = recurring_expense_service
        self.on_expense_added = on_expense_added
        self.on_update_requested = on_update_requested

        # None → ADD mode
        # int → EDIT mode
        self._expense_to_modify: Expense | None = expense_to_modify

        self._configure_styles()

        self._build_ui()

    def _build_ui(self):
        # Configure parent frame to expand
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        form = ttk.Frame(self)
        form.grid(row=0, column=0, sticky="nsew")

        form.columnconfigure(0, weight=0)  # label
        form.columnconfigure(1, weight=1)  # input

        self.date_var = tk.StringVar(
            value=(
                self._expense_to_modify.date
                if self._expense_to_modify
                else date.today().isoformat()
            )
        )
        self.amount_var = tk.StringVar(
            value=(
                str(self._expense_to_modify.amount) if self._expense_to_modify else ""
            )
        )
        self.desc_var = tk.StringVar(
            value=(
                self._expense_to_modify.description if self._expense_to_modify else ""
            )
        )

        categories = sorted(
            self.category_service.get_all_categories(), key=lambda c: c.name
        )
        self.categories = {c.name: c.id for c in categories}

        self.is_recurring_var = tk.BooleanVar(value=False)
        self.frequency_var = tk.StringVar(value="Spesa singola")

        self.category_combo = ttk.Combobox(
            form, values=list(self.categories.keys()), state="readonly"
        )
        self.category_combo.current(0)

        self.date_entry = ttk.Entry(form, textvariable=self.date_var)
        self.amount_entry = ttk.Entry(form, textvariable=self.amount_var)
        self.description_entry = ttk.Entry(form, textvariable=self.desc_var)

        self.date_error = ttk.Label(form, text="", foreground="red")
        self.amount_error = ttk.Label(form, text="", foreground="red")
        self.category_error = ttk.Label(form, text="", foreground="red")
        self.desc_error = ttk.Label(form, text="", foreground="red")

        self._add_row(form, 0, "Data", self.date_entry, self.date_error)
        self._add_row(form, 1, "Importo", self.amount_entry, self.amount_error)
        self._add_row(form, 2, "Category", self.category_combo, self.category_error)
        self._add_row(form, 3, "Descrizione", self.description_entry, self.desc_error)

        self.frequency_combo = ttk.Combobox(
            form,
            textvariable=self.frequency_var,
            values=[FREQUENCY_FORM_OPTIONS[key] for key in FREQUENCY_FORM_OPTIONS],
            state="readonly",
        )

        self._update_frequency_combo_state(self._expense_to_modify)

        self._add_row(form, 4, "Frequenza spesa", self.frequency_combo)

    def submit(self):
        """
        Docstring for submit

        :param self: Description
        """

        if not self._validate_form():
            return

        is_recurring = self.frequency_var.get() != "Spesa singola"

        if self._expense_to_modify:
            # EDIT mode
            data = {
                "date": date.fromisoformat(self.date_var.get()),
                "amount": float(self.amount_var.get()),
                "category_id": self.categories[self.category_combo.get()],
                "description": self.desc_var.get(),
                "attachment_path": None,
                "attachment_type": None,
            }

            try:
                self.expense_service.update_expense(
                    self._expense_to_modify.id,
                    **data,
                )

                self._clear_errors()

                messagebox.showinfo("Success", "Spesa aggiornata con successo!")

                self.on_expense_added()

            except ValueError as e:
                messagebox.showerror(
                    "Error", f"Impossibile aggiornare la spesa: {str(e)}"
                )

            return

        try:
            if is_recurring:
                print(f"category: {self.categories[self.category_combo.get()]}")
                frequency_key = [
                    key
                    for key, value in FREQUENCY_FORM_OPTIONS.items()
                    if value == self.frequency_var.get()
                ][0]
                self.recurring_expense_service.create_recurring_expense(
                    name=self.desc_var.get(),
                    amount=float(self.amount_var.get()),
                    category_id=self.categories[self.category_combo.get()],
                    frequency=frequency_key,
                    description=self.desc_var.get(),
                    attachment_path=None,
                    attachment_type=None,
                    start_date=date.fromisoformat(self.date_var.get()),
                )
            else:
                # Single expense: create it directly
                self.expense_service.create_expense(
                    date_=date.fromisoformat(self.date_var.get()),
                    amount=float(self.amount_var.get()),
                    category_id=self.categories[self.category_combo.get()],
                    description=self.desc_var.get(),
                    is_recurring=is_recurring,
                    attachment_path=None,
                    attachment_type=None,
                    analysis_data=None,
                    analysis_summary=None,
                )

            self.amount_var.set("")
            self.desc_var.set("")
            self.category_combo.current(0)
            self._clear_errors()

            # messagebox.showinfo("Success", "Expense added successfully!")

            self.recurring_expense_service.generate_missing_expenses(date.today())

            self.on_expense_added()

        except ValueError as e:
            messagebox.showerror("Error", f"Impossibile aggiungere la spesa: {str(e)}")

    def _validate_form(self):
        self._clear_errors()
        valid = True

        # Date
        try:
            date.fromisoformat(self.date_var.get())
        except ValueError:
            self.date_entry.configure(style="Error.TEntry")
            self.date_error.config(text="Formato YYYY-MM-DD")
            valid = False

        # Amount
        try:
            if float(self.amount_var.get()) <= 0:
                raise ValueError
        except ValueError:
            self.amount_entry.configure(style="Error.TEntry")
            self.amount_error.config(text="Inserisci un importo valido")
            valid = False

        # Category
        if not self.category_combo.get():
            self.category_combo.configure(style="Error.TCombobox")
            self.category_error.config(text="Seleziona una categoria")
            valid = False

        # Description
        desc = self.desc_var.get().strip()
        if not desc:
            self.description_entry.configure(style="Error.TEntry")
            self.desc_error.config(text="Descrizione obbligatoria")
            valid = False
        elif len(desc) > 100:
            self.description_entry.configure(style="Error.TEntry")
            self.desc_error.config(text="Max 100 caratteri")
            valid = False

        return valid

    def _add_row(self, parent, row, label_text, widget, error_label=None):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row * 2, column=0, sticky="w", padx=(0, 10), pady=(6, 0))

        widget.grid(row=row * 2, column=1, sticky="ew", pady=(6, 0))

        if error_label:
            error_label.grid(row=row * 2 + 1, column=1, sticky="w", pady=(0, 4))

    def _configure_styles(self):
        style = ttk.Style()
        style.configure("Error.TEntry", foreground="black")
        style.configure("Error.TCombobox", foreground="black")

    def _clear_errors(self):
        widgets = [
            (self.date_entry, self.date_error),
            (self.amount_entry, self.amount_error),
            (self.category_combo, self.category_error),
            (self.description_entry, self.desc_error),
        ]

        for widget, error_label in widgets:
            widget.configure(style="")
            error_label.config(text="")

    def _update_frequency_combo_state(self, condition):
        """
        Updates the state of the frequency combobox based on the given condition.

        :param condition: A boolean indicating whether to disable the combobox.
        """
        if condition:
            self.frequency_combo.configure(state="disabled")
        else:
            self.frequency_combo.configure(state="readonly")
