import tkinter as tk
from tkinter import ttk
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DailyBarChart(ttk.Frame):
    def __init__(self, parent, *, height=3):
        super().__init__(parent)

        self.figure = plt.Figure(figsize=(5, height), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Configure once
        self.ax.set_title("Andamento giornaliero", fontsize=10)
        self.ax.set_xlabel("Giorno")
        self.ax.set_ylabel("€")
        self.ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

        self.figure.tight_layout()

    def update_chart(self, daily_totals: dict[date, float]) -> None:

        self.ax.cla()  # clears only data

        if not daily_totals:
            self._draw_empty_state()
            self.canvas.draw_idle()
            return

        dates = sorted(daily_totals.keys())
        totals = [daily_totals[d] for d in dates]
        labels = [d.day for d in dates]

        x = range(len(totals))

        bars = self.ax.bar(x, totals)

        avg = sum(totals) / len(totals)

        for bar, value in zip(bars, totals):
            bar.set_alpha(0.9 if value > avg else 0.6)

        self.ax.axhline(avg, linestyle=":", linewidth=1, alpha=0.7)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels, fontsize=8)

        self.canvas.draw_idle()

    def _draw_empty_state(self) -> None:
        self.ax.text(
            0.5,
            0.5,
            "Nessuna spesa nel periodo selezionato",
            ha="center",
            va="center",
            transform=self.ax.transAxes,
            fontsize=9,
            color="#777777",
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
