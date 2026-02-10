from ast import List
from datetime import date
import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from typing import Iterable
from services.analysis_service import AnalysisService, ExpenseAnalysisResult
from domain.models import CategoryAmount
from ui.analysis.category_pie_chart import CategoryPieChart


class AnalysisTab(ttk.Frame):
    def __init__(
        self,
        master,
        analysis_service: AnalysisService,
        category_name_map: dict[int, str],
    ):
        super().__init__(master)

        self.analysis_service = analysis_service
        self.category_name_map = category_name_map
        self.header_label = None
        self.overall_frame = None
        self.categories_frame = None

        self._build_ui()

    def _build_ui(self) -> None:

        # Empty screen
        self.empty_state_label = ttk.Label(
            self,
            text="Nessuna spesa nel periodo selezionato",
            foreground="#777777",
            font=("TkDefaultFont", 10, "italic"),
        )

        # Main grid container
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame.columnconfigure(0, weight=0, minsize=150)
        self.content_frame.columnconfigure(1, weight=1, minsize=300)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure(1, weight=1)

        # Overall summary (sinistra)
        self.overall_frame = ttk.Frame(self.content_frame)
        self.overall_frame.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10)
        )

        # Categories (destra)
        self.categories_frame = ttk.Frame(self.content_frame)
        self.categories_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 10))

        # Pie chart (sinistra)
        self.pie_chart_frame = ttk.Frame(self.content_frame)
        self.pie_chart_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10))

        self.category_pie_chart = CategoryPieChart(self.pie_chart_frame)
        self.category_pie_chart.pack(fill=tk.BOTH, expand=True)

        # Other charts (destra)
        # self.other_charts_frame = ttk.Frame(self.content_frame)
        # self.other_charts_frame.grid(row=1, column=1, sticky="nsew")

    def refresh(self, start_date: date, end_date: date):
        result = self.analysis_service.get_expense_summary(
            start_date, end_date, self.category_name_map
        )

        # rendering in step successivo
        if not result.overall:
            self._show_empty_state()
            return

        self._hide_empty_state()

        self._render_overall(result)

        data = [
            CategoryAmount(category_name=c.category_name, total_amount=c.total_amount)
            for c in result.by_category
        ]

        self.category_pie_chart.render(
            self.aggregate_categories_for_pie(data, max_slices=6),
            total_amount=result.overall.total_amount,
        )
        self._render_by_category(result)

    def _render_overall(self, result: ExpenseAnalysisResult) -> None:
        if self.overall_frame is None:
            return

        for widget in self.overall_frame.winfo_children():
            widget.destroy()

        overall = result.overall

        rows = [
            ("Totale", overall.total_amount, self._format_currency),
            ("Media giornaliera", overall.daily_average, self._format_currency),
            ("Spesa massima", overall.max_single_expense, self._format_currency),
            ("Δ periodo precedente", overall.delta_percent, self._format_percent),
        ]

        for i, (label, value, format_function) in enumerate(rows):
            ttk.Label(self.overall_frame, text=label).grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )

            ttk.Label(
                self.overall_frame,
                text=format_function(value),
            ).grid(row=i, column=1, sticky="e", padx=5)

    def _render_by_category(self, result: ExpenseAnalysisResult) -> None:
        for widget in self.categories_frame.winfo_children():
            widget.destroy()

        columns = ("category", "total", "delta")

        tree = ttk.Treeview(
            self.categories_frame,
            columns=columns,
            show="headings",
            height=6,
        )

        tree.heading("category", text="Categoria")
        tree.heading("total", text="Totale")
        tree.heading("delta", text="Δ %")

        tree.column("category", anchor="w")
        tree.column("total", anchor="e")
        tree.column("delta", anchor="e")

        items = sorted(
            result.by_category,
            key=lambda item: item.total_amount,
            reverse=True,
        )

        for item in items:
            tree.insert(
                "",
                "end",
                values=(
                    item.category_name or f"Category {item.category_id}",
                    self._format_currency(item.total_amount),
                    self._format_percent(item.delta_percent),
                ),
            )

        tree.pack(fill=tk.BOTH, expand=True)

    def _format_currency(self, value: Decimal | None) -> str:
        if value is None:
            return "—"
        return f"€ {value:.2f}"

    def _format_percent(self, value: Decimal | None) -> str:
        if value is None:
            return "—"
        sign = "+" if value > 0 else ""
        return f"{sign}{value:.1f} %"

    def _show_empty_state(self) -> None:
        self.empty_state_label.pack(expand=True)
        self.content_frame.pack_forget()

    def _hide_empty_state(self) -> None:
        self.empty_state_label.pack_forget()
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def aggregate_categories_for_pie(
        self,
        categories: Iterable[CategoryAmount],
        *,
        max_slices: int = 6,
    ) -> list[CategoryAmount]:
        """
        Aggregate categories for pie chart visualization.

        Keeps the top `max_slices - 1` categories by total_amount and groups
        the remaining ones into a single 'Altro' category.

        If the number of categories is less than or equal to max_slices,
        no aggregation is performed.
        """
        categories = list(categories)

        # Sort categories by amount descending
        sorted_categories = sorted(
            categories,
            key=lambda c: c.total_amount,
            reverse=True,
        )

        if len(categories) <= max_slices:
            return sorted_categories

        visible = sorted_categories[: max_slices - 1]
        hidden = sorted_categories[max_slices - 1 :]

        other_total = sum(
            (c.total_amount for c in hidden),
            start=Decimal("0"),
        )

        if other_total > Decimal("0"):
            visible.append(
                CategoryAmount(
                    category_name="Altro",
                    total_amount=other_total,
                )
            )

        return visible
