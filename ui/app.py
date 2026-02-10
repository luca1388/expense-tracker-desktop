"""
Docstring for ui.app
Defines the main application window for the Expense Tracker desktop app.
"""

from datetime import date
import tkinter as tk
from tkinter import ttk


from persistence.expense_repository import ExpenseRepository
from persistence.category_repository import CategoryRepository
from persistence.db import get_connection
from persistence.recurring_expense_repository import RecurringExpenseRepository
from services.category_service import CategoryService
from services.expense_service import ExpenseService, SortDirection, ExpenseSortField
from services.recurring_expense_service import RecurringExpenseService
from services.analysis_service import AnalysisService
from ui.expense_list import ExpenseListFrame
from ui.period_selector import PeriodSelector
from ui.analysis_tab import AnalysisTab

from utils.dates import month_date_range


class ExpenseTrackerApp(tk.Tk):
    """
    Docstring for ExpenseTrackerApp
    """

    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("900x500")

        db_connection = get_connection()

        expense_repository = ExpenseRepository(connection=db_connection)

        # Repositories
        self.expense_service = ExpenseService(expense_repository)
        self.category_service = CategoryService(
            CategoryRepository(connection=db_connection)
        )
        self.recurring_expense_repo = RecurringExpenseRepository(
            connection=db_connection
        )
        self.recurring_expense_service = RecurringExpenseService(
            self.recurring_expense_repo, expense_repository
        )
        self.analysis_service = AnalysisService(expense_service=self.expense_service)

        self.recurring_expense_service.generate_missing_expenses(date.today())

        self._sort_field = ExpenseSortField.DATE
        self._sort_direction = SortDirection.ASC
        self._init_styles()

        self._build_ui()

    def _init_styles(self) -> None:
        style = ttk.Style()

        style.configure(
            "Treeview.Heading",
            font=("TkDefaultFont", 10),
        )

        style.configure(
            "Sorted.Treeview.Heading",
            font=("TkDefaultFont", 10, "bold"),
        )

        # Notebook tab styles
        style.configure(
            "TNotebook.Tab",
            padding=(8, 2),  # Increase padding (horizontal, vertical)
        )

    def _build_ui(self):
        # --- TOP
        main_frame = ttk.Frame(self, padding=(10, 0))
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbar = PeriodSelector(
            main_frame,
            on_month_changed=self._on_month_changed,
        )
        self.toolbar.pack(fill=tk.X)

        # --- BOTTOM: content frame (Expense list + Add form)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Left: Expense list
        self.expense_list = ExpenseListFrame(
            self.notebook,
            expense_service=self.expense_service,
            on_selection_changed=self._on_expense_selection_changed,
            recurring_expense_service=self.recurring_expense_service,
            category_service=self.category_service,
            on_refresh_requested=self.refresh_expense_list,
            on_sort_requested=self.on_sort_requested,
        )
        self.expense_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        categories = self.category_service.get_all_categories()

        category_name_map = {category.id: category.name for category in categories}

        self.expenses_tab = self.expense_list
        self.analysis_tab = AnalysisTab(
            self.notebook,
            analysis_service=self.analysis_service,
            category_name_map=category_name_map,
        )

        self.notebook.add(self.expenses_tab, text="Spese")
        self.notebook.add(self.analysis_tab, text="Analisi")

        # Bind notebook tab change event to refresh analysis tab
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self._on_month_changed(
            self.toolbar.year_var.get(), self.toolbar.get_selected_month_number()
        )

    def _on_expense_added(self, modal):
        """Refresh the expense list with the currently selected month after adding an expense."""

        self.refresh_expense_list()
        self.expense_list.disable_actions()

        modal.destroy()

    def on_sort_requested(self, sort_field: ExpenseSortField) -> None:
        """
        Docstring for on_sort_requested

        :param self: Description
        :param sort_field: Description
        :type sort_field: ExpenseSortField
        """
        if self._sort_field == sort_field:
            # toggle direction
            self._sort_direction = (
                SortDirection.DESC
                if self._sort_direction == SortDirection.ASC
                else SortDirection.ASC
            )
        else:
            self._sort_field = sort_field
            self._sort_direction = SortDirection.ASC

        self.refresh_expense_list()

    def _on_month_changed(self, year: int, month: int):
        """Callback triggered when the month selection changes."""
        if not hasattr(self, "toolbar") or not hasattr(self, "expense_list"):
            return
        start_date, end_date = month_date_range(year, month)

        self.expense_list.refresh(
            start_date=start_date,
            end_date=end_date,
            sort_field=self._sort_field,
            sort_direction=self._sort_direction,
        )
        self.expense_list.disable_actions()

        self.analysis_tab.refresh(start_date=start_date, end_date=end_date)

    def _on_tab_changed(self, event):
        """Callback triggered when a notebook tab is changed."""
        selected_tab_index = self.notebook.index(self.notebook.select())
        # If analysis tab is selected, refresh it
        if selected_tab_index == 1:  # Analysis tab is at index 1
            start_date, end_date = month_date_range(
                self.toolbar.year_var.get(), self.toolbar.get_selected_month_number()
            )
            self.analysis_tab.refresh(start_date=start_date, end_date=end_date)

    def _on_expense_selection_changed(self, selected_id: int | None):
        """Callback triggered when expense selection changes."""
        if selected_id is None:
            self.expense_list.disable_actions()
            return

        selected_expense = self.expense_service.get_by_id(selected_id)

        if bool(selected_id):
            if selected_expense and selected_expense.is_recurring:
                self.expense_list.disable_actions()
            else:
                self.expense_list.enable_actions()

    def _on_stop_recurring_expense_requested(self):
        print("Stop recurring expense requested")

    def _handle_update_expense(self, expense_id: int, data: dict):
        self.expense_service.update_expense(
            expense_id,
            **data,
        )
        # self.refresh_expense_list()

        self.refresh_expense_list()
        self.expense_list.disable_actions()

    def refresh_expense_list(self):
        """Refresh the expense list with the currently selected month."""
        start_date, end_date = month_date_range(
            self.toolbar.year_var.get(), self.toolbar.get_selected_month_number()
        )
        self.expense_list.refresh(
            start_date=start_date,
            end_date=end_date,
            sort_field=self._sort_field,
            sort_direction=self._sort_direction,
        )
        self.expense_list.set_sorted_column(self._sort_field)
