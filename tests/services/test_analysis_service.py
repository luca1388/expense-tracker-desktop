from datetime import date
from decimal import Decimal

from domain.models import (
    CategorySummary,
    Expense,
    ExpenseAnalysisResult,
    OverallSummary,
    PeriodComparison,
)
from services.analysis_service import AnalysisService

expense1 = Expense(
    id=1,
    date=date(year=2024, month=1, day=10),
    amount=Decimal("10.00"),
    category_id=1,
    description=None,
    is_recurring=False,
    attachment_path=None,
    attachment_type=None,
    analysis_data=None,
    analysis_summary=None,
    created_at=date.today(),
    recurring_expense_id=None,
)
expense2 = Expense(
    id=2,
    date=date(year=2024, month=1, day=15),
    amount=Decimal("20.00"),
    category_id=1,
    description=None,
    is_recurring=False,
    attachment_path=None,
    attachment_type=None,
    analysis_data=None,
    analysis_summary=None,
    created_at=date.today(),
    recurring_expense_id=None,
)
expense3 = Expense(
    id=3,
    date=date(year=2024, month=1, day=20),
    amount=Decimal("5.00"),
    category_id=2,
    description=None,
    is_recurring=False,
    attachment_path=None,
    attachment_type=None,
    analysis_data=None,
    analysis_summary=None,
    created_at=date.today(),
    recurring_expense_id=None,
)
expense4 = Expense(
    id=4,
    date=date(year=2024, month=2, day=9),
    amount=Decimal("5.00"),
    category_id=2,
    description=None,
    is_recurring=False,
    attachment_path=None,
    attachment_type=None,
    analysis_data=None,
    analysis_summary=None,
    created_at=date.today(),
    recurring_expense_id=None,
)
expense5 = Expense(
    id=5,
    date=date(year=2024, month=2, day=21),
    amount=Decimal("5.00"),
    category_id=2,
    description=None,
    is_recurring=False,
    attachment_path=None,
    attachment_type=None,
    analysis_data=None,
    analysis_summary=None,
    created_at=date.today(),
    recurring_expense_id=None,
)


class FakeExpenseService:
    def __init__(self, expenses: list[Expense]):
        self._expenses = expenses

    def get_expenses_for_period(self, start_date: date, end_date: date):
        return [e for e in self._expenses if start_date <= e.date <= end_date]


def test_get_expense_summary_returns_valid_structure() -> None:
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_expense_summary(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        compare_previous_period=True,
    )

    # Top-level object
    assert isinstance(result, ExpenseAnalysisResult)

    # Overall summary
    overall = result.overall
    assert isinstance(overall, OverallSummary)
    assert isinstance(overall.total_amount, Decimal)
    assert isinstance(overall.daily_average, Decimal)
    assert isinstance(overall.max_single_expense, Decimal)

    assert isinstance(overall.previous_total_amount, Decimal | None)
    assert isinstance(overall.previous_daily_average, Decimal | None)
    assert isinstance(overall.delta_percent, Decimal | None)

    # Category summaries
    assert isinstance(result.by_category, list)
    assert len(result.by_category) > 0

    first_category = result.by_category[0]
    assert isinstance(first_category, CategorySummary)
    assert first_category.category_name is None
    assert isinstance(first_category.category_id, int)
    assert isinstance(first_category.total_amount, Decimal)
    assert isinstance(first_category.previous_total_amount, Decimal | None)
    assert isinstance(first_category.delta_percent, Decimal | None)


def test_get_total_by_category():
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_total_by_category(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )

    assert result == {
        1: Decimal("30.00"),
        2: Decimal("5.00"),
    }


def test_get_total_for_period():
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_total_for_period(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )

    assert result == Decimal("35.00")


def test_get_daily_average_for_period():
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_daily_average_for_period(
        start_date=date(2024, 1, 10),
        end_date=date(2024, 1, 20),
    )

    assert result == Decimal(
        "3.181818181818181818181818182"
    )  # 35.00 / 11 days = 3.181818...


def test_get_max_expense_for_period():
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_max_expense_for_period(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )

    assert result == expense2


def test_compare_total_for_periods():
    service = AnalysisService(
        expense_service=FakeExpenseService(
            expenses=[expense1, expense2, expense3, expense4, expense5]
        )
    )

    result = service.compare_total_for_periods(
        current_start_date=date(year=2024, day=1, month=2),
        current_end_date=date(year=2024, day=28, month=2),
        previous_start_date=date(year=2024, day=1, month=1),
        previous_end_date=date(year=2024, month=1, day=31),
    )

    assert result.current == Decimal("10.00")
    assert result.previous == Decimal("35.00")
    assert result.delta_absolute == Decimal("-25.00")
    assert result.delta_percentage == Decimal(
        "-71.42857142857142857142857143"
    )  # -25.00 / 35.00 * 100 = -71.43%


def test_compare_daily_average_for_periods():
    service = AnalysisService(
        expense_service=FakeExpenseService(
            expenses=[expense1, expense2, expense3, expense4, expense5]
        )
    )

    result = service.compare_daily_average_for_periods(
        current_start_date=date(year=2024, day=1, month=2),
        current_end_date=date(year=2024, day=28, month=2),
        previous_start_date=date(year=2024, day=1, month=1),
        previous_end_date=date(year=2024, month=1, day=31),
    )

    assert result.current == Decimal(
        "0.3571428571428571428571428571"
    )  # 10.00 / 28 days
    assert result.previous == Decimal(
        "1.129032258064516129032258065"
    )  # 35.00 / 31 days
    assert result.delta_absolute == Decimal("-0.7718894009216589861751152079")
    assert result.delta_percentage == Decimal(
        "-68.36734693877551020408163267"
    )  # -0.7718894009216589861751152079 / 1.129032258064516129032258065 * 100


def test_compare_totals_by_category_for_periods():
    service = AnalysisService(
        expense_service=FakeExpenseService(
            expenses=[expense1, expense2, expense3, expense4, expense5]
        )
    )

    result = service.compare_totals_by_category_for_periods(
        current_start_date=date(year=2024, day=1, month=2),
        current_end_date=date(year=2024, day=28, month=2),
        previous_start_date=date(year=2024, day=1, month=1),
        previous_end_date=date(year=2024, month=1, day=31),
    )

    assert result == {
        1: PeriodComparison(
            current=Decimal("0"),
            previous=Decimal("30.00"),
            delta_absolute=Decimal("-30.00"),
            delta_percentage=Decimal("-100.00"),
        ),
        2: PeriodComparison(
            current=Decimal("10.00"),
            previous=Decimal("5.00"),
            delta_absolute=Decimal("5.00"),
            delta_percentage=Decimal("100.00"),
        ),
    }


def test_get_expense_summary_without_previous_period() -> None:
    service = AnalysisService(
        expense_service=FakeExpenseService(expenses=[expense1, expense2, expense3])
    )

    result = service.get_expense_summary(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        compare_previous_period=False,
    )

    overall = result.overall

    # Current values are always present
    assert isinstance(overall.total_amount, Decimal)
    assert isinstance(overall.daily_average, Decimal)
    assert isinstance(overall.max_single_expense, Decimal)

    # Previous-period values must be None
    assert overall.previous_total_amount is None
    assert overall.previous_daily_average is None
    assert overall.delta_percent is None

    # Category summaries
    for category in result.by_category:
        assert isinstance(category.total_amount, Decimal)
        assert category.previous_total_amount is None
        assert category.delta_percent is None
