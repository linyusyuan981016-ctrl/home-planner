"""Sidebar: home name and room selection."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Home
from home_planner.ui.furniture_panel import render_furniture_panel
from home_planner.ui.room_panel import render_room_panel
from home_planner.units import DISPLAY_UNITS, Unit


def render_sidebar(home: Home) -> Unit:
    st.sidebar.header("Home")
    home.name = st.sidebar.text_input("Home name", value=home.name)

    st.sidebar.divider()
    st.sidebar.header("Rooms")
    if home.rooms:
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
    else:
        st.sidebar.caption("Add your first room below.")

    display_unit = st.sidebar.selectbox(
        "Display unit",
        DISPLAY_UNITS,
        key="display_unit",
    )

    with st.sidebar:
        selected_room = render_room_panel(home, display_unit)
        render_furniture_panel(selected_room, display_unit)

    return display_unit
