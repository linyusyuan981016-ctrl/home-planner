"""Room create/edit panel."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import (
    DEFAULT_ROOM_LENGTH_CM,
    DEFAULT_ROOM_WIDTH_CM,
    MAX_ROOM_DIMENSION_CM,
    MIN_ROOM_DIMENSION_CM,
    DEFAULT_ROOM_HEIGHT_CM,
)
from home_planner.models import Home, Room
from home_planner.services.rooms import add_room, delete_room, find_room


def render_room_panel(home: Home) -> Room | None:
    st.subheader("Room")
    st.caption("Enter measurements in centimeters. Labels on the floor plan use your display unit.")

    selected = find_room(home, st.session_state.selected_room_id)
    editing = selected is not None

    with st.form("room_form", clear_on_submit=not editing):
        name = st.text_input("Room name", value=selected.name if editing else "Living Room")
        col1, col2 = st.columns(2)
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
        update_col, add_col = st.columns(2)
        with update_col:
            update_submitted = st.form_submit_button(
                "Update room",
                type="primary",
                disabled=not editing,
            )
        with add_col:
            add_submitted = st.form_submit_button("Add room")

    if update_submitted or add_submitted:
        if update_submitted and editing and selected:
            selected.name = name.strip() or "Room"
            selected.width = float(width)
            selected.length = float(length)
            st.success(f"Updated **{selected.name}**.")
        else:
            room = Room(
                name=name.strip() or "Room",
                width=float(width),
                length=float(length),
                height=DEFAULT_ROOM_HEIGHT_CM,
            )
            add_room(home, room)
            st.session_state.selected_room_id = room.id
            st.success(f"Added **{room.name}**.")
        st.rerun()

    if editing and selected and st.button("Delete room", type="secondary"):
        st.session_state.selected_room_id = delete_room(home, selected.id)
        st.session_state.furniture = []
        st.session_state.editing_furniture_id = None
        st.rerun()

    return find_room(home, st.session_state.selected_room_id)
