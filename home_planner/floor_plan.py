from dataclasses import asdict

from home_planner.konva_component import konva_floor_plan


def render_floor_plan(
    home,
    selected_room_id=None,
    furniture=None,
    display_unit="m",
):
    furniture = furniture or []

    if not home.rooms:
        return None

    selected_room = next(
        (room for room in home.rooms if room.id == selected_room_id),
        home.rooms[0],
    )
    visible_rooms = home.rooms if home.connected else [selected_room]
    room_payloads = [
        {
            "id": room.id,
            "label": room.label,
            "width": float(room.width),
            "length": float(room.length),
            "height": float(room.height),
            "x": float(room.position[0]),
            "y": float(room.position[1]),
            "openings": [asdict(opening) for opening in room.openings],
        }
        for room in visible_rooms
    ]

    updated_furniture = konva_floor_plan(
        room_id=selected_room.id,
        room_width=float(selected_room.width),
        room_length=float(selected_room.length),
        room_height=float(selected_room.height),
        room_label=selected_room.label,
        display_unit=display_unit,
        connected=home.connected,
        rooms=room_payloads,
        furniture=furniture,
    )


    return updated_furniture 