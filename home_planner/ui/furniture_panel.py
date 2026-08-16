"""Furniture placement panel."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import DEFAULT_FURNITURE_DEPTH_CM, DEFAULT_FURNITURE_WIDTH_CM
from home_planner.models import Furniture, Room
from home_planner.services.furniture import furniture_fits
from home_planner.units import UNITS, Unit, from_cm, to_cm


def render_furniture_panel(selected_room: Room | None) -> None:
    st.header("Furniture")

    if not selected_room:
        st.caption("Add a room first, then you can place furniture.")
        return

    with st.form("furniture_form"):
        furniture_name = st.text_input("Furniture name", value="Sofa")
        furniture_unit: Unit = st.selectbox("Furniture unit", UNITS)

        col1, col2 = st.columns(2)
        with col1:
            furniture_width = st.number_input(
                f"Width ({furniture_unit})",
                min_value=1.0,
                value=float(from_cm(DEFAULT_FURNITURE_WIDTH_CM, furniture_unit)),
            )
        with col2:
            furniture_depth = st.number_input(
                f"Depth ({furniture_unit})",
                min_value=1.0,
                value=float(from_cm(DEFAULT_FURNITURE_DEPTH_CM, furniture_unit)),
            )

        width_cm = to_cm(furniture_width, furniture_unit)
        depth_cm = to_cm(furniture_depth, furniture_unit)

        col3, col4 = st.columns(2)
        with col3:
            furniture_x = st.slider(
                "Move left / right",
                min_value=0,
                max_value=max(0, int(selected_room.width - width_cm)),
                value=0,
            )
        with col4:
            furniture_y = st.slider(
                "Move up / down",
                min_value=0,
                max_value=max(0, int(selected_room.length - depth_cm)),
                value=0,
            )

        add_furniture = st.form_submit_button("Add furniture")

    if add_furniture:
        item = Furniture(
            name=furniture_name.strip() or "Furniture",
            width=width_cm,
            depth=depth_cm,
            x=float(furniture_x),
            y=float(furniture_y),
        )

        if furniture_fits(selected_room, item):
            st.session_state.furniture.append(item)
            st.success("Furniture fits in the room!")
        else:
            st.error("Furniture does not fit in the room!")
