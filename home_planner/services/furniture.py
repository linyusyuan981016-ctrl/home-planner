"""Furniture placement logic."""

from __future__ import annotations

from home_planner.models import Furniture, Room


def furniture_fits(room: Room, furniture: Furniture) -> bool:
    """Return True when furniture fits entirely within the room bounds."""
    return (
        furniture.x + furniture.width <= room.width
        and furniture.y + furniture.depth <= room.length
    )
