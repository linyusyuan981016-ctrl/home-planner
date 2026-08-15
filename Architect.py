
"""Home Planner — Feature 1.1: Dimensions → Map (Streamlit prototype)."""

from __future__ import annotations

import streamlit as st

from home_planner.floor_plan import render_floor_plan
from home_planner.models import Home, Room

st.set_page_config(page_title="Home Planner", page_icon="🏠", layout="wide")

DEFAULT_WIDTH = 400
DEFAULT_LENGTH = 300
DEFAULT_HEIGHT = 250

conversion = {
    "cm": 1,
    "m": 100,
    "inch": 2.54,
    "feet": 30.48
}

display_unit = st.selectbox(
    "Display unit",
    ["inch","cm","m","feet"]
)
def _init_state() -> None:
    if "home" not in st.session_state:
        st.session_state.home = Home(name="My Home")
    if "selected_room_id" not in st.session_state:
        st.session_state.selected_room_id = None
    if "furniture" not in st.session_state:
        st.session_state.furniture = []


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

    unit = st.selectbox(
        "Unit",
        ["cm","m","inch","feet"]
    )
    if unit == "cm":
        width_cm = width
    elif unit == "m":
        width_cm = width * 100
    elif unit == "inch":
        width_cm = width * 2.54
    elif unit == "feet":
        width_cm = width * 30.48


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
        furniture_name = st.text_input("Furniture name", value="Sofa")
        furniture_unit = st.selectbox(
                        "Furniture unit",
                        ["cm","m","inch","feet"]
        )

        col1, col2 = st.columns(2)

        _render_room_form(home)
        selected_room = _find_room(home, st.session_state.selected_room_id)
        _render_room_details(selected_room)

        st.header("Furniture")

        with st.form("furniture_form"):
            furniture_name = st.text_input(
                "Furniture name",
                value = "Sofa"
            )
            col1, col2 = st.columns(2)

            

            with col1:
                furniture_width = st.number_input(
                    "Furniture width (cm)",
                    min_value=1,
                    value=200
                )

            with col2:
                furniture_depth = st.number_input(
                    "Furniture depth (cm)",
                    min_value=1,
                    value=90
                )

            col3, col4 = st.columns(2)

            with col3:
                furniture_x = st.number_input(
                    "X position (cm)",
                    min_value=0,
                    value=20
                )

            with col4:
                furniture_y = st.number_input(
                    "Y position (cm)",
                    min_value=0,
                    value=20
                )

            add_furniture = st.form_submit_button("Add furniture")

        if add_furniture:
            factor = conversion[furniture_unit]

            furniture_width_cm = furniture_width * factor
            furniture_depth_cm = furniture_depth * factor
            furniture_x_cm = furniture_x * factor
            furniture_y_cm = furniture_y * factor

            if (
                furniture_x_cm + furniture_width_cm <= selected_room.width
                and furniture_y_cm + furniture_depth_cm <= selected_room.length
            ):
                st.success("Furniture fits in the room!")

                st.session_state.furniture.append({
                    "name": furniture_name,
                    "width": furniture_width_cm,
                    "depth": furniture_depth_cm,
                    "x": furniture_x_cm,
                    "y": furniture_y_cm,
                })

            else:
                st.error("Furniture does not fit in the room!")

            

    with right:
        st.subheader("2D floor plan")
        fig = render_floor_plan(
            home, 
            selected_room_id=st.session_state.selected_room_id, 
            furniture = st.session_state.furniture,
            display_unit = display_unit)
        st.pyplot(fig, use_container_width=True)



if __name__ == "__main__":
    main()


# Task 2 - furniture 

# st.header("Furniture")
# import streamlit as st


# if "furniture" not in st.session_state:
#     st.session_state.furniture = []

# 
#     furniture_name = st.text_input(
#         "Furniture name",
#         value="Sofa"
#     )

#     col1, col2 = st.columns(2)

#     with col1:
#         furniture_width = st.number_input(
#             "Width (cm)",
#             min_value=1,
#             value=200
#         )

#     with col2:
#         furniture_depth = st.number_input(
#             "Depth (cm)",
#             min_value=1,
#             value=90
#         )

#     col3, col4 = st.columns(2)

#     with col3:
#         furniture_x = st.number_input(
#             "X position (cm)",
#             min_value=0,
#             value=20
#         )

#     with col4:
#         furniture_y = st.number_input(
#             "Y position (cm)",
#             min_value=0,
#             value=20
#         )

#     submitted = st.form_submit_button("Add furniture")

#     if submitted:
#         st.session_state.furniture.append(
#             {
#                 "name": furniture_name,
#                 "width": furniture_width,
#                 "depth": furniture_depth,
#                 "x": furniture_x,
#                 "y": furniture_y,
#             }
#         )
#         st.rerun()


# def render_floor_plan(room, furniture=None):
#     furniture = furniture or []

#     MAX_WIDTH = 750
#     MAX_HEIGHT = 520

#     # -------------------------
#     # 1. Calculate scale
#     # -------------------------

#     scale_x = MAX_WIDTH / room.width
#     scale_y = MAX_HEIGHT / room.length

#     scale = min(scale_x, scale_y)

#     # -------------------------
#     # 2. Convert room to pixels
#     # -------------------------

#     room_width_px = room.width * scale
#     room_length_px = room.length * scale

#     # -------------------------
#     # 3. Start SVG
#     # -------------------------

#     svg = f"""
#     <svg
#         width="{room_width_px + 80}"
#         height="{room_length_px + 80}"
#         viewBox="0 0 {room_width_px + 80} {room_length_px + 80}"
#         xmlns="http://www.w3.org/2000/svg"
#     >

#         <!-- Room -->
#         <rect
#             x="40"
#             y="40"
#             width="{room_width_px}"
#             height="{room_length_px}"
#             fill="#f7f7f7"
#             stroke="#222"
#             stroke-width="4"
#         />
#     """

#     # -------------------------
#     # 4. Draw furniture
#     # -------------------------

#     for item in furniture:

#         x_px = 40 + item["x"] * scale
#         y_px = 40 + item["y"] * scale

#         width_px = item["width"] * scale
#         depth_px = item["depth"] * scale

#         svg +=f"""
#         <rect
#             x="{x_px}"
#             y="{y_px}"
#             width="{width_px}"
#             height="{depth_px}"
#             rx="8"
#             fill="#d9d9d9"
#             stroke="#555"
#             stroke-width="2"
  
#             x="{x_px + width_px / 2}"
#             y="{y_px + depth_px / 2}"
#             text-anchor="middle"
#             dominant-baseline="middle"
#             font-size="14"

#             {item["name"]}

#         """

#     svg += "</svg>"

#     st.markdown(
#         svg,
#         unsafe_allow_html=True
#     )


# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
# import streamlit as st


# """
# def render_floor_plan(room, furniture=None):
#     furniture = furniture or []

#     fig, ax = plt.subplots(figsize=(8, 6))

#     # -------------------------
#     # Draw room
#     # -------------------------
#     room_rect = Rectangle(
#         (0, 0),
#         room.width,
#         room.length,
#         linewidth=2,
#         edgecolor="black",
#         facecolor="lightgray",
#         alpha=0.4,
#     )

#     ax.add_patch(room_rect)

#     # Room name
#     ax.text(
#         room.width / 2,
#         room.length / 2,
#         room.name,
#         ha="center",
#         va="center",
#         fontsize=12,
#         fontweight="bold",
#     )

#     # -------------------------
#     # Draw furniture
#     # -------------------------
#     for item in furniture:

#         x = item["x"]
#         y = item["y"]
#         width = item["width"]
#         depth = item["depth"]

#         furniture_rect = Rectangle(
#             (x, y),
#             width,
#             depth,
#             linewidth=2,
#             edgecolor="black",
#             facecolor="white",
#         )

#         ax.add_patch(furniture_rect)

#         ax.text(
#             x + width / 2,
#             y + depth / 2,
#             item["name"],
#             ha="center",
#             va="center",
#             fontsize=9,
#         )

#     # -------------------------
#     # Correct scale
#     # -------------------------
#     ax.set_xlim(-20, room.width + 20)
#     ax.set_ylim(-20, room.length + 20)

#     # THIS IS IMPORTANT
#     ax.set_aspect("equal")

#     ax.set_xlabel("cm")
#     ax.set_ylabel("cm")

#     ax.set_title(f"{room.name} — Floor Plan")

#     st.pyplot(fig)
#     """