"""Domain models for the expense tracker application."""

from dataclasses import dataclass


@dataclass
class Category:
    """Represents an expense category."""

    id: int | None
    name: str
    is_custom: bool
