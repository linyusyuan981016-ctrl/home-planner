"""Room create/edit panel."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import (
    DEFAULT_ROOM_HEIGHT_CM,
    DEFAULT_ROOM_LENGTH_CM,
    DEFAULT_ROOM_WIDTH_CM,
    MAX_ROOM_DIMENSION_CM,
    MAX_ROOM_HEIGHT_CM,
    MIN_ROOM_DIMENSION_CM,
    MIN_ROOM_HEIGHT_CM,
)
from home_planner.models import Home, Room
from home_planner.services.rooms import add_room, delete_room, find_room
from home_planner.units import Unit, format_length


def render_room_panel(home: Home, display_unit: Unit) -> Room | None:
    st.subheader("Room")
    st.caption("Enter measurements in centimeters. Labels on the floor plan use your display unit.")

    selected = find_room(home, st.session_state.selected_room_id)
    editing = selected is not None

    with st.form("room_form", clear_on_submit=not editing):
        name = st.text_input("Room name", value=selected.name if editing else "Living Room")
        col1, col2, col3 = st.columns(3)
        with col1:
            width = st.number_input(
                "Width (cm)",
                min_value=MIN_ROOM_DIMENSION_CM,
                max_value=MAX_ROOM_DIMENSION_CM,
                value=int(selected.width) if editing else DEFAULT_ROOM_WIDTH_CM,
                step=10,
            )
        with col2:
            length = st.number_input(
                "Length (cm)",
                min_value=MIN_ROOM_DIMENSION_CM,
                max_value=MAX_ROOM_DIMENSION_CM,
                value=int(selected.length) if editing else DEFAULT_ROOM_LENGTH_CM,
                step=10,
            )
        with col3:
            height = st.number_input(
                "Height (cm)",
                min_value=MIN_ROOM_HEIGHT_CM,
                max_value=MAX_ROOM_HEIGHT_CM,
                value=int(selected.height) if editing else DEFAULT_ROOM_HEIGHT_CM,
                step=10,
            )

        submitted = st.form_submit_button("Update room" if editing else "Add room", type="primary")

    if submitted:
        if editing and selected:
            selected.name = name.strip() or "Room"
            selected.width = float(width)
            selected.length = float(length)
            selected.height = float(height)
            st.success(f"Updated **{selected.name}**.")
        else:
            room = Room(
                name=name.strip() or "Room",
                width=float(width),
                length=float(length),
                height=float(height),
            )
            add_room(home, room)
            st.session_state.selected_room_id = room.id
            st.success(f"Added **{room.name}**.")
        st.rerun()

    if editing and selected and st.button("Delete room", type="secondary"):
        st.session_state.selected_room_id = delete_room(home, selected.id)
        st.session_state.furniture = []
        st.rerun()

    selected = find_room(home, st.session_state.selected_room_id)
    if selected:
        _render_room_metrics(selected, display_unit)

    return selected


def _render_room_metrics(room: Room, display_unit: Unit) -> None:
    st.subheader("Selected room")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Width", format_length(room.width, display_unit))
    c2.metric("Length", format_length(room.length, display_unit))
    c3.metric("Height", format_length(room.height, display_unit))
    c4.metric("Floor area", f"{room.floor_area_m2:.1f} m²")
