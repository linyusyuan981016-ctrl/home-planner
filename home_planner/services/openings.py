"""Room opening creation and geometry helpers."""

from __future__ import annotations

import uuid

from home_planner.models import Opening, Room


def create_opening(room: Room, opening_type: str) -> Opening:
    """Create a centered door or window on the room's top wall."""
    if opening_type not in {"door", "window"}:
        raise ValueError("Opening type must be door or window.")
    opening_width = min(90.0 if opening_type == "door" else 120.0, room.width)
    opening_number = sum(item.type == opening_type for item in room.openings) + 1
    return Opening(
        id=uuid.uuid4().hex[:8],
        room_id=room.id,
        wall_id="top",
        type=opening_type,
        name=f"{opening_type.title()} {opening_number}",
        offset=(room.width - opening_width) / 2,
        width=opening_width,
        height=210.0 if opening_type == "door" else 120.0,
        sill_height=None if opening_type == "door" else 90.0,
    )


def update_opening_position(opening: Opening, wall_id: str, offset: float, room: Room) -> None:
    """Clamp an opening to its selected room wall."""
    wall_length = room.width if wall_id in {"top", "bottom"} else room.length
    opening.wall_id = wall_id
    opening.offset = min(max(0.0, offset), max(0.0, wall_length - opening.width))
