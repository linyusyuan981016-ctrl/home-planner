"""Floor plan preview panel."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Home
from home_planner.rendering.floor_plan import render_floor_plan
from home_planner.units import Unit


def render_floor_plan_panel(
    home: Home,
    *,
    selected_room_id: str | None,
    display_unit: Unit,
) -> None:
    st.subheader("2D floor plan")
    fig = render_floor_plan(
        home,
        selected_room_id=selected_room_id,
        furniture=st.session_state.furniture,
        display_unit=display_unit,
    )
    st.pyplot(fig, use_container_width=True)
