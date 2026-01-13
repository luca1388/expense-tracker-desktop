import tkinter as tk
from tkinter import ttk
from datetime import date


class MonthFilterFrame(ttk.Frame):
    """
    UI component that allows selecting a year and month.

    Responsibilities:
    - Let the user choose a month
    - Notify listeners when the selection changes
    - Expose navigation shortcuts (previous / next month)
    """

    def __init__(self, parent, on_month_changed):
        super().__init__(parent, padding=5)

        self.on_month_changed = on_month_changed
        today = date.today()

        self.year_var = tk.IntVar(value=today.year)
        self.month_var = tk.IntVar(value=today.month)

        self._build_ui()
        self._notify_change()

    def _build_ui(self):
        """Build filter controls and navigation buttons."""

        # ttk.Label(self, text="Select the time range:").pack(side=tk.LEFT, padx=0)
        ttk.Button(self, text="<", width=3, command=self._prev_month).pack(side=tk.LEFT)

        ttk.Label(self, text="Year:").pack(side=tk.LEFT, padx=5)

        ttk.Spinbox(
            self,
            from_=2000,
            to=2100,
            width=5,
            textvariable=self.year_var,
            command=self._notify_change,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(self, text="Month:").pack(side=tk.LEFT, padx=5)

        ttk.Combobox(
            self,
            values=list(range(1, 13)),
            width=3,
            textvariable=self.month_var,
            state="readonly",
        ).pack(side=tk.LEFT)

        self.month_var.trace_add("write", self._on_month_var_changed)

        ttk.Button(self, text=">", width=3, command=self._next_month).pack(
            side=tk.LEFT, padx=5
        )

        self.total_label = ttk.Label(
            self, text="Total: € 0.00", font=("Arial", 10, "bold")
        )
        self.total_label.pack(side=tk.RIGHT, padx=10)

    def _notify_change(self):
        """Notify listener with the currently selected year and month."""
        self.on_month_changed(self.year_var.get(), self.month_var.get())

    def _on_month_var_changed(self, *_):  # not interested in args (*_)
        """
        Callback triggered when the month variable changes.
        """
        self._notify_change()

    def update_total(self, total: float):
        """
        Update the displayed total amount.

        This method is intentionally simple and receives
        already computed values from the outside.
        """
        self.total_label.config(text=f"Total: € {total:.2f}")

    def _prev_month(self):
        """Move selection to the previous month."""
        year, month = self.year_var.get(), self.month_var.get()
        if month == 1:
            self.year_var.set(year - 1)
            self.month_var.set(12)
        else:
            self.month_var.set(month - 1)
        self._notify_change()

    def _next_month(self):
        """Move selection to the next month."""
        year, month = self.year_var.get(), self.month_var.get()
        if month == 12:
            self.year_var.set(year + 1)
            self.month_var.set(1)
        else:
            self.month_var.set(month + 1)
        self._notify_change()
