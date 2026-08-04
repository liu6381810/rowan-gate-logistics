"""Catering headcount planning for Rowan Gate events."""

import math

DEFAULT_BUFFER_RATIO = 0.10


def headcount_with_buffer(confirmed_rsvps, buffer_ratio=DEFAULT_BUFFER_RATIO):
    """Apply a safety buffer to the confirmed RSVP count."""
    buffered = confirmed_rsvps * (1 + buffer_ratio)
    return int(math.ceil(buffered))


def split_meal_counts(total_headcount, meal_options):
    """Split total headcount across meal options by requested share."""
    if not meal_options:
        raise ValueError("At least one meal option is required")
    shares = sum(option["share"] for option in meal_options)
    if abs(shares - 1.0) > 0.001:
        raise ValueError("Meal option shares must add up to 1.0")
    counts = {}
    for option in meal_options:
        counts[option["name"]] = int(round(total_headcount * option["share"]))
    return counts


def estimate_beverage_cases(total_headcount, drinks_per_person=2.5, per_case=24):
    """Estimate beverage cases needed for the event."""
    total_drinks = total_headcount * drinks_per_person
    return int(math.ceil(total_drinks / per_case))
