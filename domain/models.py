"""Domain models for the expense tracker application."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


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

    created_at: datetime
