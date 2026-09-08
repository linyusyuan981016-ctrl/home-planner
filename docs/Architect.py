"""Home Planner — Feature 1.1: Dimensions → Map (Streamlit prototype)."""

from __future__ import annotations

import streamlit as st

from home_planner.floor_plan import render_floor_plan
from home_planner.models import Home, Room

st.set_page_config(page_title="Home Planner", page_icon="🏠", layout="wide")

DEFAULT_WIDTH = 400
DEFAULT_LENGTH = 300
DEFAULT_HEIGHT = 250


def _init_state() -> None:
    if "home" not in st.session_state:
        st.session_state.home = Home(name="My Home")
    if "selected_room_id" not in st.session_state:
        st.session_state.selected_room_id = None


def _find_room(home: Home, room_id: str | None) -> Room | None:
    if not room_id:
        return None
    return next((r for r in home.rooms if r.id == room_id), None)


def _render_sidebar(home: Home) -> None:
    st.sidebar.header("Home")
    home.name = st.sidebar.text_input("Home name", value=home.name)

    st.sidebar.divider()
    st.sidebar.header("Rooms")

    if home.rooms:
        room_names = {r.name: r.id for r in home.rooms}
        ids = list(room_names.values())
        current_id = st.session_state.selected_room_id
        if current_id not in ids:
            current_id = ids[0]
        selected_name = st.sidebar.radio(
            "Select room",
            options=list(room_names.keys()),
            index=ids.index(current_id),
        )
        st.session_state.selected_room_id = room_names[selected_name]
    else:
        st.sidebar.caption("No rooms yet — add one below.")


def _render_room_form(home: Home) -> None:
    st.subheader("Room form")
    st.caption("Enter basic measurements. All dimensions are in centimeters.")

    selected = _find_room(home, st.session_state.selected_room_id)
    editing = selected is not None

    with st.form("room_form", clear_on_submit=not editing):
        name = st.text_input("Room name", value=selected.name if editing else "Living Room")
        col1, col2, col3 = st.columns(3)
        with col1:
            width = st.number_input("Width (cm)", min_value=50, max_value=2000, value=int(selected.width) if editing else DEFAULT_WIDTH, step=10)
        with col2:
            length = st.number_input("Length (cm)", min_value=50, max_value=2000, value=int(selected.length) if editing else DEFAULT_LENGTH, step=10)
        with col3:
            height = st.number_input("Height (cm)", min_value=200, max_value=500, value=int(selected.height) if editing else DEFAULT_HEIGHT, step=10)

        submitted = st.form_submit_button("Update room" if editing else "Add room", type="primary")

    if submitted:
        if editing and selected:
            selected.name = name.strip() or "Room"
            selected.width = float(width)
            selected.length = float(length)
            selected.height = float(height)
            st.success(f"Updated **{selected.name}**.")
        else:
            room = Room(
                name=name.strip() or "Room",
                width=float(width),
                length=float(length),
                height=float(height),
            )
            if home.rooms:
                last = home.rooms[-1]
                room.position = (last.position[0] + last.width + 50, last.position[1])
            home.rooms.append(room)
            st.session_state.selected_room_id = room.id
            st.success(f"Added **{room.name}**.")
        st.rerun()

    if editing and selected:
        if st.button("Delete room", type="secondary"):
            home.rooms = [r for r in home.rooms if r.id != selected.id]
            st.session_state.selected_room_id = home.rooms[0].id if home.rooms else None
            st.rerun()


def _render_room_details(room: Room | None) -> None:
    if not room:
        return
    st.subheader("Selected room")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Width", f"{room.width:.0f} cm")
    c2.metric("Length", f"{room.length:.0f} cm")
    c3.metric("Height", f"{room.height:.0f} cm")
    c4.metric("Floor area", f"{room.width * room.length / 10_000:.1f} m²")


def main() -> None:
    _init_state()
    home: Home = st.session_state.home

    st.title("Home Planner")
    st.markdown("Turn room measurements into a simple, dimension-accurate floor plan.")

    _render_sidebar(home)

    left, right = st.columns([1, 2], gap="large")

    with left:
        _render_room_form(home)
        _render_room_details(_find_room(home, st.session_state.selected_room_id))

    with right:
        st.subheader("2D floor plan")
        fig = render_floor_plan(home, selected_room_id=st.session_state.selected_room_id)
        st.pyplot(fig, use_container_width=True)


if __name__ == "__main__":
    main()
