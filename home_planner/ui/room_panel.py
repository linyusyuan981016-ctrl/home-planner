"""Room create/edit panel."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import (
    DEFAULT_ROOM_LENGTH_CM,
    DEFAULT_ROOM_WIDTH_CM,
    MAX_ROOM_DIMENSION_CM,
    MIN_ROOM_DIMENSION_CM,
    DEFAULT_ROOM_HEIGHT_CM,
    ROOM_TYPES,
)
from home_planner.models import Home, Room
from home_planner.services.openings import create_opening
from home_planner.services.rooms import add_room, attach_room, delete_room, find_room, room_name_exists
from home_planner.units import Unit, from_cm, to_cm


def render_room_panel(home: Home, display_unit: Unit) -> Room | None:
    st.subheader("Room")
    st.caption("Enter room measurements in your selected display unit.")

    selected = find_room(home, st.session_state.selected_room_id)
    editing = selected is not None

    with st.form("room_form", clear_on_submit=not editing):
        room_type_options = list(ROOM_TYPES)
        room_type = st.selectbox(
            "Room type",
            room_type_options,
            index=(
                room_type_options.index(selected.room_type)
                if editing and selected.room_type in room_type_options
                else room_type_options.index("Other") if editing else 0
            ),
        )
        name = st.text_input(
            "Room name",
            value=selected.name if editing else ROOM_TYPES[room_type],
        )
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input(
                f"Breadth ({display_unit})",
                min_value=float(from_cm(MIN_ROOM_DIMENSION_CM, display_unit)),
                max_value=float(from_cm(MAX_ROOM_DIMENSION_CM, display_unit)),
                value=float(from_cm(selected.width if editing else DEFAULT_ROOM_WIDTH_CM, display_unit)),
                step=float(from_cm(10, display_unit)),
            )
        with col2:
            length = st.number_input(
                f"Length ({display_unit})",
                min_value=float(from_cm(MIN_ROOM_DIMENSION_CM, display_unit)),
                max_value=float(from_cm(MAX_ROOM_DIMENSION_CM, display_unit)),
                value=float(from_cm(selected.length if editing else DEFAULT_ROOM_LENGTH_CM, display_unit)),
                step=float(from_cm(10, display_unit)),
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
        normalized_name = name.strip() or "Room"
        duplicate_id = selected.id if update_submitted and selected else None
        if room_name_exists(home, normalized_name, exclude_id=duplicate_id):
            st.error(f'A room named "{normalized_name}" already exists.')
            return selected

        if update_submitted and editing and selected:
            selected.name = normalized_name
            selected.room_type = room_type
            selected.width = to_cm(float(width), display_unit)
            selected.length = to_cm(float(length), display_unit)
            st.success(f"Updated **{selected.name}**.")
        else:
            room = Room(
                name=name.strip() or "Room",
                width=to_cm(float(width), display_unit),
                length=to_cm(float(length), display_unit),
                height=DEFAULT_ROOM_HEIGHT_CM,
                room_type=room_type,
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

    if editing and selected:
        st.divider()
        st.markdown("**Doors and windows**")
        opening_col1, opening_col2 = st.columns(2)
        with opening_col1:
            if st.button("Add door", key=f"add_door_{selected.id}"):
                selected.openings.append(create_opening(selected, "door"))
                st.rerun()
        with opening_col2:
            if st.button("Add window", key=f"add_window_{selected.id}"):
                selected.openings.append(create_opening(selected, "window"))
                st.rerun()
        for opening in selected.openings:
            with st.expander(f"{opening.type.title()} · {opening.id}"):
                opening_width = st.number_input(
                    f"Length ({display_unit})",
                    min_value=float(from_cm(20, display_unit)),
                    max_value=float(from_cm(selected.width if opening.wall_id in {"top", "bottom"} else selected.length, display_unit)),
                    value=float(from_cm(opening.width, display_unit)),
                    key=f"opening_width_{opening.id}",
                )
                opening_height = st.number_input(
                    f"Height ({display_unit})",
                    min_value=float(from_cm(20, display_unit)),
                    value=float(from_cm(opening.height, display_unit)),
                    key=f"opening_height_{opening.id}",
                )
                if st.button("Save opening size", key=f"save_opening_{opening.id}"):
                    opening.width = to_cm(float(opening_width), display_unit)
                    opening.height = to_cm(float(opening_height), display_unit)
                    wall_length = selected.width if opening.wall_id in {"top", "bottom"} else selected.length
                    opening.offset = min(opening.offset, max(0, wall_length - opening.width))
                    st.rerun()
                if st.button("Delete opening", key=f"delete_opening_{opening.id}"):
                    selected.openings = [
                        existing for existing in selected.openings
                        if existing.id != opening.id
                    ]
                    st.rerun()

    if len(home.rooms) > 1:
        with st.expander("Attach this room to another"):
            other_rooms = [room for room in home.rooms if room.id != (selected.id if selected else None)]
            if other_rooms:
                with st.form(f"attach_room_{selected.id if selected else 'none'}"):
                    target_id = st.selectbox(
                        "Attach to",
                        options=[room.id for room in other_rooms],
                        format_func=lambda room_id: next(room.name for room in other_rooms if room.id == room_id),
                    )
                    side = st.selectbox("Place against", ("right", "left", "bottom", "top"))
                    attach_submitted = st.form_submit_button("Attach rooms")
                if attach_submitted and selected:
                    try:
                        attach_room(home, selected.id, target_id, side)
                    except ValueError as error:
                        st.error(str(error))
                    else:
                        st.success("Rooms attached. The floor plan now shows the house layout.")
                        st.rerun()

    return find_room(home, st.session_state.selected_room_id)
