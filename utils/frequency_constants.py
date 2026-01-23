"""
Shared frequency mapping constants for the expense tracker application.
"""

from domain.models import RecurrenceFrequency

# Mapping of RecurrenceFrequency enum values to Italian display names
FREQUENCY_LABELS = {
    RecurrenceFrequency.MONTHLY: "Mensile",
    RecurrenceFrequency.EVERY_2_MONTHS: "Bimestrale",
    RecurrenceFrequency.EVERY_3_MONTHS: "Trimestrale",
    RecurrenceFrequency.EVERY_4_MONTHS: "Quadrimestrale",
    RecurrenceFrequency.EVERY_6_MONTHS: "Semestrale",
    RecurrenceFrequency.YEARLY: "Annuale",
}

# Mapping for the expense form including single expense option
FREQUENCY_FORM_OPTIONS = {
    "single": "Spesa singola",
    **FREQUENCY_LABELS,
}
