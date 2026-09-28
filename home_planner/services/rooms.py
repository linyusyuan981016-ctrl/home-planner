"""Room management helpers."""

from __future__ import annotations

from home_planner.models import Home, Room
from home_planner.constants import ROOM_GAP_CM


def find_room(home: Home, room_id: str | None) -> Room | None:
    if not room_id:
        return None
    return next((room for room in home.rooms if room.id == room_id), None)


def room_name_exists(home: Home, name: str, *, exclude_id: str | None = None) -> bool:
    normalized_name = name.strip().casefold()
    return any(
        room.id != exclude_id and room.name.strip().casefold() == normalized_name
        for room in home.rooms
    )


def add_room(home: Home, room: Room) -> None:
    if home.rooms:
        last = home.rooms[-1]
        room.position = (last.position[0] + last.width + ROOM_GAP_CM, last.position[1])
    home.rooms.append(room)


def attach_room(home: Home, room_id: str, target_id: str, side: str) -> None:
    """Place a room flush against another room on the requested side."""
    room = find_room(home, room_id)
    target = find_room(home, target_id)
    if room is None or target is None or room.id == target.id:
        raise ValueError("Choose two different existing rooms to attach.")
    if side not in {"top", "right", "bottom", "left"}:
        raise ValueError("Side must be top, right, bottom, or left.")

    target_x, target_y = target.position
    if side == "right":
        room.position = (target_x + target.width, target_y)
    elif side == "left":
        room.position = (target_x - room.width, target_y)
    elif side == "bottom":
        room.position = (target_x, target_y + target.length)
    else:
        room.position = (target_x, target_y - room.length)
    home.connected = True


def delete_room(home: Home, room_id: str) -> str | None:
    home.rooms = [room for room in home.rooms if room.id != room_id]
    return home.rooms[0].id if home.rooms else None
