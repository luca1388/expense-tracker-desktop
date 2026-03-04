from datetime import date
import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from typing import Iterable
from services.analysis_service import AnalysisService, ExpenseAnalysisResult
from domain.models import CategoryAmount
from ui.analysis.category_pie_chart import CategoryPieChart
from ui.analysis.daily_bar_chart import DailyBarChart


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
        self.current_start_date = None
        self.current_end_date = None
        self._selected_category_id = None
        self._last_selected_item_id = None
        self.tree = None
        self.filter_label = None

        self._build_ui()

    def _build_ui(self) -> None:

        # Empty screen
        self.empty_state_label = ttk.Label(
            self,
            text="Nessuna spesa nel periodo selezionato",
            foreground="#777777",
            font=("TkDefaultFont", 10, "italic"),
        )

        self.chart_type = tk.StringVar(value="pie")

        # Main grid container
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame.columnconfigure(0, weight=0, minsize=150)
        self.content_frame.columnconfigure(1, weight=1, minsize=300)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure(1, weight=0)
        self.content_frame.rowconfigure(2, weight=1)

        # Overall summary
        self.overall_frame = ttk.Frame(self.content_frame)
        self.overall_frame.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10)
        )

        # Categories
        self.categories_frame = ttk.Frame(self.content_frame)
        self.categories_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 10))

        # Toolbar (below categories)
        toolbar = ttk.Frame(self.content_frame)
        toolbar.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(5, 10))

        ttk.Radiobutton(
            toolbar,
            text="Per categoria",
            variable=self.chart_type,
            value="pie",
            command=self._on_chart_type_changed,
        ).pack(side=tk.LEFT)

        ttk.Radiobutton(
            toolbar,
            text="Andamento giornaliero",
            variable=self.chart_type,
            value="daily",
            command=self._on_chart_type_changed,
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.filter_label = ttk.Label(toolbar, text="", foreground="#666666")
        self.filter_label.pack(side=tk.LEFT, padx=(20, 0))

        # Pie chart
        self.chart_container = ttk.Frame(self.content_frame)
        self.chart_container.grid(row=2, column=1, sticky="nsew", padx=(0, 10))

        self.category_pie_chart = CategoryPieChart(self.chart_container)
        self.category_pie_chart.pack(fill=tk.BOTH, expand=True)

        # Bar charts
        self.bar_chart = DailyBarChart(self.chart_container)
        self.bar_chart.pack(fill=tk.BOTH, expand=True)

    def _on_chart_type_changed(self) -> None:
        for child in self.chart_container.winfo_children():
            child.pack_forget()

        if self.chart_type.get() == "pie":
            self.category_pie_chart.pack(fill=tk.BOTH, expand=True)
        else:
            self.bar_chart.pack(fill=tk.BOTH, expand=True)

        # Clear selection when switching chart types
        if self.tree:
            self.tree.selection_remove(self.tree.selection())
        self._selected_category_id = None
        self._last_selected_item_id = None

        self._update_filter_label()

        if self.current_start_date and self.current_end_date:
            self.refresh(self.current_start_date, self.current_end_date)

    def refresh_charts(self, daily_totals, result):
        if not result.overall:
            return

        data = [
            CategoryAmount(
                category_name=c.category_name,
                total_amount=c.total_amount,
                category_id=c.category_id,
            )
            for c in result.by_category
        ]

        if self.chart_type.get() == "pie":
            self.category_pie_chart.render(
                self.aggregate_categories_for_pie(data, max_slices=6),
                total_amount=result.overall.total_amount,
                selected_category_id=self._selected_category_id,
            )
        else:
            self.bar_chart.update_chart(daily_totals)

    def get_analysis_data(self, start_date: date, end_date: date):
        result = self.analysis_service.get_expense_summary(
            start_date, end_date, self.category_name_map
        )
        daily_totals = self.analysis_service.get_daily_totals_for_period(
            start_date=start_date, end_date=end_date
        )
        return result, daily_totals

    def refresh(self, start_date: date, end_date: date):
        self.current_start_date = start_date
        self.current_end_date = end_date
        result, daily_totals = self.get_analysis_data(
            start_date=start_date, end_date=end_date
        )

        if not result.overall:
            self._show_empty_state()
            return

        self._hide_empty_state()

        self._render_overall(result)
        self._render_by_category(result)
        self.refresh_charts(daily_totals, result)

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

        columns = ("id", "category", "total", "delta")

        self.tree = ttk.Treeview(
            self.categories_frame,
            columns=columns,
            show="headings",
            height=6,
        )
        self.tree.column("id", width=0, stretch=False)
        self.tree.bind("<<TreeviewSelect>>", self._on_category_selected)

        self.tree.heading("category", text="Categoria")
        self.tree.heading("total", text="Totale")
        self.tree.heading("delta", text="Δ %")

        self.tree.column("category", anchor="w")
        self.tree.column("total", anchor="e")
        self.tree.column("delta", anchor="e")

        items = sorted(
            result.by_category,
            key=lambda item: item.total_amount,
            reverse=True,
        )

        for item in items:
            self.tree.insert(
                "",
                "end",
                values=(
                    item.category_id,
                    item.category_name or f"Category {item.category_id}",
                    self._format_currency(item.total_amount),
                    self._format_percent(item.delta_percent),
                ),
            )

        self.tree.pack(fill=tk.BOTH, expand=True)

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
                    category_name="Altro", total_amount=other_total, category_id="other"
                )
            )

        return visible

    def _update_filter_label(self) -> None:
        """Update the filter label to show category name when filtering daily totals."""
        if self.chart_type.get() == "daily" and self._selected_category_id:
            category_name = self.category_name_map.get(
                self._selected_category_id, f"Category {self._selected_category_id}"
            )
            self.filter_label.config(text=f"Filtro: {category_name}")
        else:
            self.filter_label.config(text="")

    def _on_category_selected(self, event):
        selected = self.tree.selection()

        if not selected:
            self._selected_category_id = None
            self._last_selected_item_id = None
        else:
            item_id = selected[0]

            # Toggle: if clicking the same item, deselect it
            if item_id == self._last_selected_item_id:
                self.tree.selection_remove(item_id)
                self._selected_category_id = None
                self._last_selected_item_id = None
                self._update_filter_label()
                return

            self._last_selected_item_id = item_id
            values = self.tree.item(item_id)["values"]
            self._selected_category_id = int(values[0])  # assumo prima colonna = id

        if self.current_start_date and self.current_end_date:
            result, daily_totals = self.get_analysis_data(
                start_date=self.current_start_date, end_date=self.current_end_date
            )

            # If showing daily chart and category is selected, get category-specific daily totals
            if self.chart_type.get() == "daily" and self._selected_category_id:
                daily_totals = (
                    self.analysis_service.get_daily_totals_for_period_and_category(
                        start_date=self.current_start_date,
                        end_date=self.current_end_date,
                        category_id=self._selected_category_id,
                    )
                )

            self.refresh_charts(result=result, daily_totals=daily_totals)
            self._update_filter_label()
