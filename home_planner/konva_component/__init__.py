from pathlib import Path
import streamlit.components.v1 as components


_BUILD_DIR = Path(__file__).parent / "frontend" / "dist"

_konva_component = components.declare_component(
    "konva_floor_plan",
    path=str(_BUILD_DIR),
)


def konva_floor_plan(
    room_id,
    room_width,
    room_length,
    room_height,
    room_label,
    display_unit,
    connected,
    rooms,
    furniture,
):
    return _konva_component(
        room_id=room_id,
        room_width=room_width,
        room_length=room_length,
        room_height=room_height,
        room_label=room_label,
        display_unit=display_unit,
        connected=connected,
        rooms=rooms,
        furniture=furniture,
        default=None,
    )