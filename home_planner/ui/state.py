"""Streamlit session state helpers."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Furniture, Home


def init_session_state() -> None:
    if "home" not in st.session_state:
        st.session_state.home = Home(name="My Home")
    if "selected_room_id" not in st.session_state:
        st.session_state.selected_room_id = None
    if "furniture" not in st.session_state:
        st.session_state.furniture: list[Furniture] = []
    if "editing_furniture_id" not in st.session_state:
        st.session_state.editing_furniture_id = None
