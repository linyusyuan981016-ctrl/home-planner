"""Furniture placement logic."""

from __future__ import annotations

from home_planner.models import Furniture, Room


def furniture_fits(room: Room, furniture: Furniture) -> bool:
    """Return True when furniture fits entirely within the room bounds."""
    rotated = furniture.rotation in (90, 270)
    width = furniture.depth if rotated else furniture.width
    depth = furniture.width if rotated else furniture.depth
    return (
        furniture.x + width <= room.width
        and furniture.y + depth <= room.length
    )
