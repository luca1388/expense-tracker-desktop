from datetime import date
import calendar


def month_date_range(year: int, month: int) -> tuple[date, date]:
    """
    Return the start and end date for a given year and month.
    """
    start = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end = date(year, month, last_day)
    return start, end
