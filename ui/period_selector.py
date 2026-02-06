"""
Docstring for ui.toolbar
Defines the ToolbarFrame that consolidates filter controls, navigation,
action buttons, and total display.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date

MONTH_NAMES = [
    "Gennaio",
    "Febbraio",
    "Marzo",
    "Aprile",
    "Maggio",
    "Giugno",
    "Luglio",
    "Agosto",
    "Settembre",
    "Ottobre",
    "Novembre",
    "Dicembre",
]


class PeriodSelector(ttk.Frame):
    """
    Unified toolbar containing:
    - Month/year filter selector with prev/next navigation
    - Edit/delete action buttons for expenses
    """

    def __init__(
        self,
        parent,
        on_month_changed,
    ):
        super().__init__(parent)

        self.on_month_changed = on_month_changed

        today = date.today()
        self.year_var = tk.IntVar(value=today.year)
        self.month_var = tk.StringVar(value=MONTH_NAMES[today.month - 1])

        self._build_ui()

    def _build_ui(self):
        """Build the toolbar with all controls."""

        # --- LEFT: Filter and navigation
        filter_frame = ttk.Frame(self)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=False, pady=5)

        filter_container = ttk.Frame(
            filter_frame,
            borderwidth=2,
            relief="solid",  # flat, raised, sunken, groove, ridge, solid
            padding=(0, 5),
        )
        filter_container.pack(side=tk.LEFT, padx=0)

        ttk.Label(filter_container, text="Anno:").pack(side=tk.LEFT)

        ttk.Spinbox(
            filter_container,
            from_=2000,
            to=2100,
            width=5,
            textvariable=self.year_var,
            command=self._notify_change,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_container, text="Mese:").pack(side=tk.LEFT, padx=5)

        ttk.Combobox(
            filter_container,
            values=MONTH_NAMES,
            width=10,
            textvariable=self.month_var,
            state="readonly",
        ).pack(side=tk.LEFT, padx=5)

        self.month_var.trace_add("write", self._on_month_var_changed)

        ttk.Button(filter_container, text="<", width=3, command=self._prev_month).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(
            filter_container, text="Mese corrente", command=self._current_month
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(filter_container, text=">", width=3, command=self._next_month).pack(
            side=tk.LEFT, padx=5
        )

    def get_selected_month_number(self) -> int:
        """Returns the currently selected month number."""
        return MONTH_NAMES.index(self.month_var.get()) + 1

    def _notify_change(self):
        """Notify listener with the currently selected year and month."""
        self.on_month_changed(self.year_var.get(), self.get_selected_month_number())

    def _on_month_var_changed(self, *_):
        """Callback triggered when the month variable changes."""
        self._notify_change()

    def _prev_month(self):
        """Move selection to the previous month."""
        year, month = self.year_var.get(), self.get_selected_month_number()
        if month == 1:
            self.year_var.set(year - 1)
            self.month_var.set(MONTH_NAMES[11])
        else:
            self.month_var.set(MONTH_NAMES[month - 2])
        self._notify_change()

    def _next_month(self):
        """Move selection to the next month."""
        year, month = self.year_var.get(), self.get_selected_month_number()
        if month == 12:
            self.year_var.set(year + 1)
            self.month_var.set(MONTH_NAMES[0])
        else:
            self.month_var.set(MONTH_NAMES[month])
        self._notify_change()

    def _current_month(self):
        """Set selection to the current month."""
        today = date.today()
        self.year_var.set(today.year)
        self.month_var.set(MONTH_NAMES[today.month - 1])
        self._notify_change()
