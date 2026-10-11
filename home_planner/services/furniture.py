"""Furniture placement logic."""

from __future__ import annotations

from home_planner.constants import (
    MAX_FURNITURE_DIMENSION_CM,
    MIN_FURNITURE_DIMENSION_CM,
)
from home_planner.models import Furniture, Room


def validate_furniture_dimensions(
    width_cm: float,
    depth_cm: float,
    room: Room | None = None,
    rotation: float = 0.0,
) -> str | None:
    """Return a validation error message or None when furniture dimensions are valid."""
    if width_cm <= 0 or depth_cm <= 0:
        return "Furniture dimensions must be greater than zero."

    if width_cm < MIN_FURNITURE_DIMENSION_CM or depth_cm < MIN_FURNITURE_DIMENSION_CM:
        return (
            "Furniture dimensions are below the minimum allowed size for a valid floor plan."
        )

    if width_cm > MAX_FURNITURE_DIMENSION_CM or depth_cm > MAX_FURNITURE_DIMENSION_CM:
        return "Furniture dimensions exceed the allowed maximum size."

    if room is not None:
        rotated = rotation in (90.0, 270.0)
        span_x = depth_cm if rotated else width_cm
        span_y = width_cm if rotated else depth_cm
        if span_x > room.width or span_y > room.length:
            return "Furniture dimensions exceed the room size."

    return None


def furniture_fits(room: Room, furniture: Furniture) -> bool:
    """Return True when furniture fits entirely within the room bounds."""
    rotated = furniture.rotation in (90, 270)
    width = furniture.depth if rotated else furniture.width
    depth = furniture.width if rotated else furniture.depth
    return (
        furniture.x + width <= room.width
        and furniture.y + depth <= room.length
    )
