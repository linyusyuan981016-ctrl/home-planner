"""Furniture creation and editing controls."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import (
    BED_TYPES,
    FURNITURE_TYPES,
    MAX_FURNITURE_DIMENSION_CM,
    MIN_FURNITURE_DIMENSION_CM,
)
from home_planner.models import Furniture, Room
from home_planner.services.furniture import furniture_fits, validate_furniture_dimensions
from home_planner.units import Unit, from_cm, to_cm

ROTATIONS = (0.0, 90.0)


def _sync_furniture_name(type_key: str, name_key: str) -> None:
    st.session_state[name_key] = st.session_state[type_key]


def _furniture_form(
    item: Furniture | None,
    room: Room,
    form_key: str,
    display_unit: Unit,
) -> tuple[dict, bool]:
    editing = item is not None
    prefix = f"{form_key}_"
    furniture_type_options = list(FURNITURE_TYPES)
    context_key = f"{prefix}context"
    type_key = f"{prefix}type"
    name_key = f"{prefix}name"
    width_key = f"{prefix}width"
    depth_key = f"{prefix}depth"
    bed_variant_key = f"{prefix}bed_variant"
    unit_context_key = f"{prefix}unit_context"
    context = item.id if editing else "new"
    initial_type = item.furniture_type if editing and item.furniture_type in FURNITURE_TYPES else "Other"
    if st.session_state.get(context_key) != context:
        initial_width, initial_depth = FURNITURE_TYPES[initial_type]
        st.session_state[context_key] = context
        st.session_state[type_key] = initial_type
        st.session_state[name_key] = item.name if editing else initial_type
        st.session_state[f"{prefix}last_type"] = initial_type
        st.session_state[unit_context_key] = display_unit
        st.session_state[width_key] = from_cm(
            item.width if editing else initial_width,
            display_unit,
        )
        st.session_state[depth_key] = from_cm(
            item.depth if editing else initial_depth,
            display_unit,
        )

    furniture_type = st.selectbox(
        "Furniture type",
        furniture_type_options,
        index=(
            furniture_type_options.index(item.furniture_type)
            if editing and item.furniture_type in furniture_type_options
            else furniture_type_options.index("Other") if editing else 0
        ),
        key=type_key,
        on_change=_sync_furniture_name,
        args=(type_key, name_key),
    )

    if furniture_type == "Bed":
        bed_variant_options = list(BED_TYPES)
        initial_bed_variant = "Queen"
        if editing and item.furniture_type == "Bed":
            for variant_name, dimensions in BED_TYPES.items():
                if dimensions == (item.width, item.depth) or dimensions == (item.depth, item.width):
                    initial_bed_variant = variant_name
                    break
        bed_variant = st.selectbox(
            "Bed size",
            bed_variant_options,
            index=bed_variant_options.index(st.session_state.get(bed_variant_key, initial_bed_variant)),
            key=bed_variant_key,
        )
        st.caption("Standard bed sizes use fixed dimensions for a consistent fit.")
        default_width, default_depth = BED_TYPES[bed_variant]
    else:
        default_width, default_depth = FURNITURE_TYPES[furniture_type]
        bed_variant = None
    previous_unit = st.session_state.get(unit_context_key)
    if previous_unit and previous_unit != display_unit:
        if width_key in st.session_state:
            st.session_state[width_key] = from_cm(
                to_cm(float(st.session_state[width_key]), previous_unit),
                display_unit,
            )
        if depth_key in st.session_state:
            st.session_state[depth_key] = from_cm(
                to_cm(float(st.session_state[depth_key]), previous_unit),
                display_unit,
            )
        st.session_state[unit_context_key] = display_unit
    with st.form(form_key, clear_on_submit=not editing):
        name = st.text_input(
            "Furniture name",
            key=name_key,
        )
        rotation = st.selectbox(
            "Rotation",
            ROTATIONS,
            index=ROTATIONS.index(item.rotation) if editing and item.rotation in ROTATIONS else 0,
            key=f"{prefix}rotation",
        )
        col1, col2 = st.columns(2)
        room_max_length = max(room.width, room.length)
        width_is_fixed = furniture_type == "Bed"
        with col1:
            width = st.number_input(
                f"Length ({display_unit})",
                min_value=float(from_cm(MIN_FURNITURE_DIMENSION_CM, display_unit)),
                max_value=float(from_cm(min(room_max_length, MAX_FURNITURE_DIMENSION_CM), display_unit)),
                value=float(from_cm(item.width if editing else default_width, display_unit)),
                key=width_key,
                disabled=width_is_fixed,
            )
        with col2:
            depth = st.number_input(
                f"Breadth ({display_unit})",
                min_value=float(from_cm(MIN_FURNITURE_DIMENSION_CM, display_unit)),
                max_value=float(from_cm(min(room_max_length, MAX_FURNITURE_DIMENSION_CM), display_unit)),
                value=float(from_cm(item.depth if editing else default_depth, display_unit)),
                key=depth_key,
                disabled=width_is_fixed,
            )

        if bed_variant is not None:
            width_cm = BED_TYPES[bed_variant][0]
            depth_cm = BED_TYPES[bed_variant][1]
        else:
            width_cm = to_cm(float(width), display_unit)
            depth_cm = to_cm(float(depth), display_unit)
        validation_error = validate_furniture_dimensions(width_cm, depth_cm, room, float(rotation))
        if validation_error:
            st.warning(validation_error)
        x = item.x if editing else 0.0
        y = item.y if editing else 0.0

        submitted = st.form_submit_button("Update furniture" if editing else "Add furniture", type="primary")

    return {
        "name": name.strip() or furniture_type,
        "width": width_cm,
        "depth": depth_cm,
        "x": x,
        "y": y,
        "rotation": float(rotation),
        "furniture_type": furniture_type,
    }, submitted


def render_furniture_panel(selected_room: Room | None, display_unit: Unit) -> None:
    st.header("Furniture")
    if not selected_room:
        st.caption("Add a room first, then you can place furniture.")
        return

    editing_id = st.session_state.get("editing_furniture_id")
    room_furniture = [item for item in st.session_state.furniture if item.room_id == selected_room.id]
    editing_item = next((item for item in room_furniture if item.id == editing_id), None)
    values, submitted = _furniture_form(
        editing_item,
        selected_room,
        "edit_furniture" if editing_item else "add_furniture",
        display_unit,
    )

    if submitted:
        validation_error = validate_furniture_dimensions(
            values["width"],
            values["depth"],
            selected_room,
            float(values["rotation"]),
        )
        if validation_error:
            st.error(validation_error)
            return

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
