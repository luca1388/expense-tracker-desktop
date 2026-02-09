from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CategoryPieChart(ttk.Frame):
    """
    Pie chart showing expense distribution by category.
    """

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def render(self, data: dict[str, float]) -> None:
        """
        Render the pie chart using category totals.

        :param data: mapping {category_name: total_amount}
        """
        self.ax.clear()

        if not data:
            self._render_empty_state()
            return

        labels = list(data.keys())
        values = list(data.values())

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
        )
        self.ax.axis("equal")  # keep circle shape

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
