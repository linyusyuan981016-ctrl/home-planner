"""Streamlit application entry."""

from __future__ import annotations

import streamlit as st

from home_planner.ui.floor_plan_panel import render_floor_plan_panel
from home_planner.ui.furniture_panel import render_furniture_panel
from home_planner.ui.ai_panel import render_ai_panel
from home_planner.ui.room_panel import render_room_panel
from home_planner.ui.sidebar import render_sidebar
from home_planner.ui.state import init_session_state
from home_planner.units import DISPLAY_UNITS, Unit


def run_app() -> None:
    st.set_page_config(page_title="Home Planner", page_icon="🏠", layout="wide")

    init_session_state()
    home = st.session_state.home

    st.title("Home Planner")
    st.markdown(
        "Turn room measurements into a clear layout in minutes.\n\n"
        "Plan smarter, place furniture with confidence, and design your space with ease."
    )

    display_unit: Unit = st.selectbox("Display unit", DISPLAY_UNITS, key="display_unit")

    render_sidebar(home)
    render_ai_panel(home, st.session_state.furniture)

    left, right = st.columns([1, 2], gap="large")

    with left:
        selected_room = render_room_panel(home, display_unit)
        render_furniture_panel(selected_room, display_unit)

    with right:
        render_floor_plan_panel(
            home,
            selected_room_id=st.session_state.selected_room_id,
            display_unit=display_unit,
        )
