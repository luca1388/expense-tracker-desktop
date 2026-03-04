"""
Daily line chart for expense analysis.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date
from decimal import Decimal
from typing import Dict, Iterable

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DailyLineChart(ttk.Frame):
    """
    Line chart showing daily expense totals for a period.
    """

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self) -> None:
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Andamento giornaliero")
        self.ax.set_xlabel("Giorno")
        self.ax.set_ylabel("Spesa")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_data(self, daily_totals: Dict[date, Decimal]) -> None:
        """
        Update the chart with new daily totals.

        :param daily_totals: Mapping date -> total amount spent
        """
        self.ax.clear()

        if not daily_totals:
            self.canvas.draw()
            return

        dates = [date for date in daily_totals]
        amounts = [float(amount) for amount in daily_totals.values()]

        self.ax.plot(
            dates,
            amounts,
            marker="o",
            linewidth=2,
        )

        self.ax.set_title("Andamento giornaliero")
        self.ax.set_xlabel("Giorno")
        self.ax.set_ylabel("Spesa")

        self.ax.grid(True, linestyle="--", alpha=0.5)

        # Improve date label readability
        self.figure.autofmt_xdate()

        self.canvas.draw()
