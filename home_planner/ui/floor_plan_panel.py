"""Floor plan preview panel."""

from __future__ import annotations

from dataclasses import asdict

import streamlit as st

from home_planner.floor_plan import render_floor_plan
from home_planner.models import Home
from home_planner.units import Unit


def render_floor_plan_panel(
    home: Home,
    *,
    selected_room_id: str | None,
    display_unit: Unit,
) -> None:
    st.subheader("2D floor plan")
    room_furniture = [
        item
        for item in st.session_state.furniture
        if item.room_id == selected_room_id
    ]
    updated_furniture = render_floor_plan(
        home,
        selected_room_id=selected_room_id,
        furniture=[asdict(item) for item in room_furniture],
        display_unit=display_unit,
    )
    if updated_furniture is not None:
        updated_by_id = {item["id"]: item for item in updated_furniture}
        for item in room_furniture:
            updated = updated_by_id.get(item.id)
            if updated:
                item.x = float(updated["x"])
                item.y = float(updated["y"])
