from home_planner.konva_component import konva_floor_plan


def render_floor_plan(
    home,
    selected_room_id=None,
    furniture=None,
    display_unit="cm",
):
    furniture = furniture or []

    if not home.rooms:
        return None

    selected_room = None

    if selected_room_id is not None:
        selected_room = next(
            (
                room
                for room in home.rooms
                if room.id == selected_room_id
            ),
            None,
        )

    if selected_room is None:
        selected_room = home.rooms[0]

    updated_furniture = konva_floor_plan(
        room_width=float(selected_room.width),
        room_length=float(selected_room.length),
        room_height=float(selected_room.height),
        furniture=furniture,
    )


    return updated_furniture 