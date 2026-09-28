"""Sidebar: home name and room selection."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Home


def render_sidebar(home: Home) -> None:
    st.sidebar.header("Home")
    home.name = st.sidebar.text_input("Home name", value=home.name)

    st.sidebar.divider()
    st.sidebar.header("Rooms")

    if not home.rooms:
        st.sidebar.caption("No rooms yet — add one in the room panel.")
        return

    room_options = {room.id: room.label for room in home.rooms}
    ids = list(room_options)
    current_id = st.session_state.selected_room_id
    if current_id not in ids:
        current_id = ids[0]

    selected_id = st.sidebar.radio(
        "Select room",
        options=ids,
        index=ids.index(current_id),
        format_func=room_options.get,
    )
    st.session_state.selected_room_id = selected_id
