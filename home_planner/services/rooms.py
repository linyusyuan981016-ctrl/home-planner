"""Room management helpers."""

from __future__ import annotations

from home_planner.constants import ROOM_GAP_CM
from home_planner.models import Home, Room


def find_room(home: Home, room_id: str | None) -> Room | None:
    if not room_id:
        return None
    return next((room for room in home.rooms if room.id == room_id), None)


def add_room(home: Home, room: Room) -> None:
    if home.rooms:
        last = home.rooms[-1]
        room.position = (last.position[0] + last.width + ROOM_GAP_CM, last.position[1])
    home.rooms.append(room)


def delete_room(home: Home, room_id: str) -> str | None:
    home.rooms = [room for room in home.rooms if room.id != room_id]
    return home.rooms[0].id if home.rooms else None
