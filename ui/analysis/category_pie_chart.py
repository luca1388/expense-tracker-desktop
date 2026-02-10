from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from decimal import Decimal

from domain.models import CategoryAmount


class CategoryPieChart(ttk.Frame):
    """
    Pie chart showing expense distribution by category.
    """

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def render(self, data: list[CategoryAmount], total_amount: Decimal) -> None:
        """
        Render the pie chart using category totals.

        :param data: list of CategoryAmount objects
        """
        self.ax.clear()

        if not data:
            self._render_empty_state()
            return

        labels = [c.category_name for c in data]
        values = [c.total_amount for c in data]
        wedges, texts = self.ax.pie(
            values,
            labels=None,
            startangle=90,
            pctdistance=1.3,
        )

        legend_labels = [
            f"{name} – {amount / total_amount * 100:.1f}%"
            for name, amount in zip(labels, values)
        ]
        self.ax.axis("equal")  # keep circle shape

        self.ax.legend(
            wedges,
            legend_labels,
            title="Categorie",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _render_empty_state(self) -> None:
        self.ax.text(
            0.5,
            0.5,
            "Nessuna spesa nel periodo",
            ha="center",
            va="center",
            fontsize=10,
            transform=self.ax.transAxes,
        )
        self.ax.set_axis_off()
        self.canvas.draw_idle()
