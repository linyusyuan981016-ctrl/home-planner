"""Furniture creation and editing controls."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import DEFAULT_FURNITURE_DEPTH_CM, DEFAULT_FURNITURE_WIDTH_CM
from home_planner.models import Furniture, Room
from home_planner.services.furniture import furniture_fits
from home_planner.units import UNITS, Unit, from_cm, to_cm

ROTATIONS = (0.0, 90.0, 180.0, 270.0)


def _effective_dimensions(width: float, depth: float, rotation: float) -> tuple[float, float]:
    if rotation in (90.0, 270.0):
        return depth, width
    return width, depth


def _position_control(label: str, available: float, value: float, key: str) -> float:
    max_position = max(0, int(available))
    if max_position == 0:
        st.number_input(label, min_value=0.0, max_value=1.0, value=0.0, disabled=True, key=key)
        return 0.0
    return float(st.slider(label, min_value=0, max_value=max_position, value=min(int(value), max_position), key=key))


def _furniture_form(item: Furniture | None, room: Room, form_key: str) -> tuple[dict, bool]:
    editing = item is not None
    prefix = f"{form_key}_"
    with st.form(form_key, clear_on_submit=not editing):
        name = st.text_input("Furniture name", value=item.name if editing else "Sofa", key=f"{prefix}name")
        unit: Unit = st.selectbox("Furniture unit", UNITS, key=f"{prefix}unit")
        rotation = st.selectbox(
            "Rotation",
            ROTATIONS,
            index=ROTATIONS.index(item.rotation) if editing and item.rotation in ROTATIONS else 0,
            key=f"{prefix}rotation",
        )
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input(
                f"Width ({unit})",
                min_value=1.0,
                value=float(from_cm(item.width if editing else DEFAULT_FURNITURE_WIDTH_CM, unit)),
                key=f"{prefix}width",
            )
        with col2:
            depth = st.number_input(
                f"Depth ({unit})",
                min_value=1.0,
                value=float(from_cm(item.depth if editing else DEFAULT_FURNITURE_DEPTH_CM, unit)),
                key=f"{prefix}depth",
            )

        width_cm = to_cm(width, unit)
        depth_cm = to_cm(depth, unit)
        effective_width, effective_depth = _effective_dimensions(width_cm, depth_cm, rotation)
        col3, col4 = st.columns(2)
        with col3:
            x = _position_control("Move left / right", room.width - effective_width, item.x if editing else 0, f"{prefix}x")
        with col4:
            y = _position_control("Move up / down", room.length - effective_depth, item.y if editing else 0, f"{prefix}y")

        submitted = st.form_submit_button("Update furniture" if editing else "Add furniture", type="primary")

    return {
        "name": name.strip() or "Furniture",
        "width": width_cm,
        "depth": depth_cm,
        "x": x,
        "y": y,
        "rotation": float(rotation),
    }, submitted


def render_furniture_panel(selected_room: Room | None) -> None:
    st.header("Furniture")
    if not selected_room:
        st.caption("Add a room first, then you can place furniture.")
        return

    editing_id = st.session_state.get("editing_furniture_id")
    room_furniture = [item for item in st.session_state.furniture if item.room_id == selected_room.id]
    editing_item = next((item for item in room_furniture if item.id == editing_id), None)
    values, submitted = _furniture_form(editing_item, selected_room, "edit_furniture" if editing_item else "add_furniture")

    if submitted:
        if editing_item:
            updated_item = Furniture(**values, id=editing_item.id, room_id=selected_room.id)
            if not furniture_fits(selected_room, updated_item):
                st.error("Furniture does not fit in the room!")
                return
            for field, value in values.items():
                setattr(editing_item, field, value)
            st.session_state.editing_furniture_id = None
            message = "Furniture updated."
        else:
            item = Furniture(**values, room_id=selected_room.id)
            if furniture_fits(selected_room, item):
                st.session_state.furniture.append(item)
                message = "Furniture fits in the room!"
            else:
                st.error("Furniture does not fit in the room!")
                return
        st.success(message)
        st.rerun()

    if room_furniture:
        st.subheader("Furniture in this room")
        for item in room_furniture:
            col_name, col_edit, col_delete = st.columns([3, 1, 1])
            with col_name:
                st.write(f"{item.name} ({item.rotation:.0f}°)")
            with col_edit:
                if st.button("Edit", key=f"edit_furniture_{item.id}"):
                    st.session_state.editing_furniture_id = item.id
                    st.rerun()
            with col_delete:
                if st.button("Delete", key=f"delete_furniture_{item.id}"):
                    st.session_state.furniture = [f for f in st.session_state.furniture if f.id != item.id]
                    st.session_state.editing_furniture_id = None
                    st.rerun()
