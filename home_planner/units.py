"""Measurement unit conversions. Internal storage is always centimeters."""

from __future__ import annotations

from typing import Literal

Unit = Literal["cm", "m", "inch", "feet"]

CM_PER_UNIT: dict[Unit, float] = {
    "cm": 1.0,
    "m": 100.0,
    "inch": 2.54,
    "feet": 30.48,
}

UNITS: tuple[Unit, ...] = ("cm", "m", "inch", "feet")


def to_cm(value: float, unit: Unit) -> float:
    """Convert a value in the given unit to centimeters."""
    return value * CM_PER_UNIT[unit]


def from_cm(value_cm: float, unit: Unit) -> float:
    """Convert centimeters to the given unit."""
    return value_cm / CM_PER_UNIT[unit]


def format_length(value_cm: float, unit: Unit, *, precision: int = 0) -> str:
    """Format a centimeter value for display in the chosen unit."""
    return f"{from_cm(value_cm, unit):.{precision}f} {unit}"
