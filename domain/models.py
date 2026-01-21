"""Domain models for the expense tracker application."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from enum import Enum


@dataclass
class Category:
    """Represents an expense category."""

    id: int | None
    name: str
    is_custom: bool


@dataclass
class Expense:
    """
    Rappresenta una singola spesa registrata nel sistema.
    """

    id: Optional[int]
    date: date
    amount: float
    category_id: int
    description: Optional[str]

    is_recurring: bool

    attachment_path: Optional[str]
    attachment_type: Optional[str]

    analysis_data: Optional[str]
    analysis_summary: Optional[str]

    created_at: datetime


class RecurrenceFrequency(Enum):
    """
    Defines how often a recurring expense occurs.
    """

    MONTHLY = "monthly"
    EVERY_2_MONTHS = "every_2_months"
    EVERY_3_MONTHS = "every_3_months"
    EVERY_4_MONTHS = "every_4_months"
    EVERY_6_MONTHS = "every_6_months"
    YEARLY = "yearly"


@dataclass
class RecurringExpense:
    """
    Represents a recurring expense template.

    This entity is used to generate actual Expense instances.
    """

    id: Optional[int]

    name: str
    amount: float
    category_id: int

    frequency: RecurrenceFrequency

    start_date: date
    end_date: Optional[date]

    description: Optional[str]

    attachment_path: Optional[str]
    attachment_type: Optional[str]

    last_generated_date: Optional[date]

    created_at: datetime = field(default_factory=datetime.now)
