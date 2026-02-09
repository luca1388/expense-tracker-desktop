"""
Docstring for services.analysis_service
"""

# from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from domain.models import (
    CategorySummary,
    Expense,
    ExpenseAnalysisResult,
    OverallSummary,
    PeriodComparison,
    DateRange,
)
from services.expense_service import ExpenseService


class AnalysisService:
    """
    Docstring for AnalysisService

    :var start_date: Description
    :vartype start_date: date
    :var end_date: Description
    :vartype end_date: date
    :var compare_previous_period: Description
    :vartype compare_previous_period: bool
    """

    def __init__(self, expense_service: ExpenseService):
        self._expense_service = expense_service

    def get_total_by_category(
        self, start_date: date, end_date: date
    ) -> dict[int, Decimal]:
        """
        Docstring for get_total_by_category

        :param self: Description
        :param start_date: Description
        :type start_date: date
        :param end_date: Description
        :type end_date: date
        :return: Description
        :rtype: dict[int, Decimal]
        """
        expenses = self._expense_service.get_expenses_for_period(
            start_date=start_date, end_date=end_date
        )

        # totals: dict[int, Decimal] = defaultdict(Decimal)

        # for expense in expenses:
        #     totals[expense.category_id] += expense.amount

        # return dict(totals)

        totals: dict[int, Decimal] = {}

        for expense in expenses:
            category_id = expense.category_id

            if category_id not in totals:
                totals[category_id] = Decimal("0")

            totals[category_id] += Decimal(expense.amount)

        return totals

    def get_daily_average_for_period(self, start_date: date, end_date: date) -> Decimal:
        """
        Docstring for get_daily_average_for_period
        """
        total = self.get_total_for_period(start_date, end_date)

        days = (end_date - start_date).days + 1  # inclusive

        if days == 0:
            return Decimal("0")

        daily_average = total / Decimal(days)

        return daily_average

    def get_max_expense_for_period(self, start_date: date, end_date: date) -> Expense:
        """
        Docstring for get_max_expense_for_period

        :param start_date: Description
        :type start_date: date
        :param end_date: Description
        :type end_date: date
        :return: Description
        :rtype: Expense
        """
        expenses = self._expense_service.get_expenses_for_period(
            start_date=start_date, end_date=end_date
        )

        if not expenses:
            return None

        max_expense: Expense = None

        max_expense = max(expenses, key=lambda e: e.amount)

        return max_expense

    def get_total_for_period(self, start_date: date, end_date: date) -> Decimal:
        """
        Docstring for get_total_for_period

        :param start_date: Description
        :type start_date: date
        :param end_date: Description
        :type end_date: date
        :return: Description
        :rtype: Decimal
        """
        expenses = self._expense_service.get_expenses_for_period(
            start_date=start_date, end_date=end_date
        )

        total = Decimal("0")

        for expense in expenses:
            total += Decimal(expense.amount)

        return total

    def compare_total_for_periods(
        self,
        current_start_date: date,
        current_end_date: date,
        previous_start_date: date,
        previous_end_date: date,
    ) -> PeriodComparison:
        """
        Docstring for compare_total_for_periods

        """
        current_total = self.get_total_for_period(
            start_date=current_start_date, end_date=current_end_date
        )
        previous_total = self.get_total_for_period(
            start_date=previous_start_date, end_date=previous_end_date
        )

        delta_absolute = current_total - previous_total

        return PeriodComparison(
            current=current_total,
            previous=previous_total,
            delta_absolute=delta_absolute,
            delta_percentage=(
                (
                    (delta_absolute / previous_total * 100)
                    if previous_total != Decimal("0")
                    else None
                )
            ),
        )

    def compare_totals_by_category_for_periods(
        self,
        current_start_date: date,
        current_end_date: date,
        previous_start_date: date,
        previous_end_date: date,
    ) -> dict[int, PeriodComparison]:
        """
        Docstring for compare_totals_by_category_for_periods
        """
        current_totals = self.get_total_by_category(
            current_start_date, current_end_date
        )
        previous_totals = self.get_total_by_category(
            previous_start_date, previous_end_date
        )

        all_category_ids = set(current_totals.keys()).union(previous_totals.keys())

        comparisons: dict[int, PeriodComparison] = {}

        for category_id in all_category_ids:
            current_total = current_totals.get(category_id, Decimal("0"))
            previous_total = previous_totals.get(category_id, Decimal("0"))
            delta_absolute = current_total - previous_total

            comparisons[category_id] = PeriodComparison(
                current=current_total,
                previous=previous_total,
                delta_absolute=delta_absolute,
                delta_percentage=(
                    (
                        (delta_absolute / previous_total * 100)
                        if previous_total != Decimal("0")
                        else None
                    )
                ),
            )

        return comparisons

    def compare_daily_average_for_periods(
        self,
        current_start_date: date,
        current_end_date: date,
        previous_start_date: date,
        previous_end_date: date,
    ) -> PeriodComparison:
        """
        Docstring for compare_daily_average_for_periods
        """
        current_average = self.get_daily_average_for_period(
            start_date=current_start_date, end_date=current_end_date
        )
        previous_average = self.get_daily_average_for_period(
            start_date=previous_start_date, end_date=previous_end_date
        )

        delta_absolute = current_average - previous_average

        return PeriodComparison(
            current=current_average,
            previous=previous_average,
            delta_absolute=delta_absolute,
            delta_percentage=(
                (
                    (delta_absolute / previous_average * 100)
                    if previous_average != Decimal("0")
                    else None
                )
            ),
        )

    def _get_previous_period(
        self, start_date: date, end_date: date
    ) -> tuple[date, date]:
        """
        Docstring for _get_previous_period

        :param self: Description
        :param start_date: Description
        :type start_date: date
        :param end_date: Description
        :type end_date: date
        :return: Description
        :rtype: tuple[date, date]
        """
        period_length = (end_date - start_date).days + 1  # inclusive

        previous_end_date = start_date - timedelta(days=1)
        previous_start_date = previous_end_date - timedelta(days=period_length - 1)

        return previous_start_date, previous_end_date

    def get_expense_summary(
        self,
        start_date: date,
        end_date: date,
        category_map: dict[int, str],
        compare_previous_period: bool = True,
    ) -> ExpenseAnalysisResult:
        """
        Return a summary of expenses for the given period.

        This is a stub implementation.

        """
        current_period_start_date = start_date
        current_period_end_date = end_date

        previous_period_start_date, previous_period_end_date = (
            self._get_previous_period(
                start_date=current_period_start_date, end_date=current_period_end_date
            )
        )

        overall_comparison = self.compare_total_for_periods(
            current_start_date=current_period_start_date,
            current_end_date=current_period_end_date,
            previous_start_date=previous_period_start_date,
            previous_end_date=previous_period_end_date,
        )

        average_comparison = self.compare_daily_average_for_periods(
            current_start_date=current_period_start_date,
            current_end_date=current_period_end_date,
            previous_start_date=previous_period_start_date,
            previous_end_date=previous_period_end_date,
        )

        max_single_expense = self.get_max_expense_for_period(
            start_date=current_period_start_date, end_date=current_period_end_date
        )

        if max_single_expense:
            max_single_expense_amount = max_single_expense.amount
        else:
            max_single_expense_amount = 0

        overall = OverallSummary(
            total_amount=overall_comparison.current,
            previous_total_amount=(
                overall_comparison.previous if compare_previous_period else None
            ),
            delta_percent=(
                (
                    overall_comparison.delta_percentage
                    if compare_previous_period
                    else None
                )
            ),
            daily_average=average_comparison.current,
            previous_daily_average=(
                average_comparison.previous if compare_previous_period else None
            ),
            max_single_expense=max_single_expense_amount,
        )

        totals = self.compare_totals_by_category_for_periods(
            current_start_date=current_period_start_date,
            current_end_date=current_period_end_date,
            previous_start_date=previous_period_start_date,
            previous_end_date=previous_period_end_date,
        )

        by_category: list[CategorySummary] = [
            CategorySummary(
                category_id=category_id,
                category_name=category_map.get(category_id),
                total_amount=comparison.current,
                previous_total_amount=(
                    comparison.previous if compare_previous_period else None
                ),
                delta_percent=(
                    comparison.delta_percentage if compare_previous_period else None
                ),
            )
            for category_id, comparison in totals.items()
        ]

        return ExpenseAnalysisResult(
            period=DateRange(
                start_date=current_period_start_date,
                end_date=current_period_end_date,
            ),
            overall=overall if overall.total_amount > 0 else None,
            by_category=tuple(by_category),
        )
