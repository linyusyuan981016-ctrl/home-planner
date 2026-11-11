"""Furniture creation and editing controls."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from home_planner.constants import FURNITURE_TYPES
from home_planner.models import Furniture, Room
from home_planner.services.furniture import furniture_fits
from home_planner.units import Unit, from_cm, to_cm

ROTATIONS = (0.0, 90.0)
ICON_DIRECTORY = Path(__file__).resolve().parents[1] / "icons"
FURNITURE_ICON_FILES = {
    "Sofa": "sofa.png",
    "Bed": "bed.png",
    "Dining table": "dining_table.png",
    "Round dining table": "dinigtable_round.png",
    "Chair": "dining_chair.png",
    "Armchair": "armchair.png",
    "Office chair": "office_chair.png",
    "Desk": "desk.png",
    "Cabinet": "cabinet.png",
    "Fridge": "fridge.png",
    "TV console": "tvconsole.png",
    "Rug": "rug.png",
    "Other": "armchair.png",
}


def _sync_furniture_type(
    type_key: str,
    name_key: str,
    width_key: str,
    depth_key: str,
    display_unit: Unit,
) -> None:
    st.session_state[name_key] = st.session_state[type_key]
    default_width, default_depth = FURNITURE_TYPES[st.session_state[type_key]]
    st.session_state[width_key] = from_cm(default_width, display_unit)
    st.session_state[depth_key] = from_cm(default_depth, display_unit)


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
    rotation_key = f"{prefix}rotation"
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
        st.session_state[rotation_key] = (
            item.rotation if editing and item.rotation in ROTATIONS else ROTATIONS[0]
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
        on_change=_sync_furniture_type,
        args=(type_key, name_key, width_key, depth_key, display_unit),
    )
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
    name = st.text_input("Furniture name", key=name_key)
    rotation = st.selectbox("Rotation", ROTATIONS, key=rotation_key)
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input(
            f"Length ({display_unit})",
            min_value=float(from_cm(1, display_unit)),
            key=width_key,
        )
    with col2:
        depth = st.number_input(
            f"Breadth ({display_unit})",
            min_value=float(from_cm(1, display_unit)),
            key=depth_key,
        )

    width_cm = to_cm(float(width), display_unit)
    depth_cm = to_cm(float(depth), display_unit)
    icon_file = FURNITURE_ICON_FILES[furniture_type]
    icon_path = ICON_DIRECTORY / icon_file
    icon_data = base64.b64encode(icon_path.read_bytes()).decode("ascii")
    icon_mime_type = "image/svg+xml" if icon_path.suffix == ".svg" else "image/png"
    rotated = rotation in (90, 270)
    preview_length = depth_cm if rotated else width_cm
    preview_breadth = width_cm if rotated else depth_cm
    preview_scale = min(220 / max(preview_length, 1), 180 / max(preview_breadth, 1))
    preview_width = preview_length * preview_scale
    preview_height = preview_breadth * preview_scale
    st.markdown(
        "<div style='height:188px;display:flex;align-items:center;justify-content:center'>"
        f"<img src='data:{icon_mime_type};base64,{icon_data}' alt='{furniture_type} preview' "
        f"style='width:{preview_width:.1f}px;height:{preview_height:.1f}px;object-fit:fill'>"
        "</div>",
        unsafe_allow_html=True,
    )

    x = item.x if editing else 0.0
    y = item.y if editing else 0.0
    submitted = st.button(
        "Update furniture" if editing else "Add furniture",
        type="primary",
        key=f"{form_key}_submit",
    )

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
                st.session_state[f"add_furniture_context"] = None
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
