"""Streamlit application entry."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import APP_BACKGROUND
from home_planner.ui.floor_plan_panel import _build_floor_plan_pdf, render_floor_plan_panel
from home_planner.ui.furniture_panel import render_furniture_panel
from home_planner.ui.ai_panel import render_ai_panel
from home_planner.ui.room_panel import render_room_panel
from home_planner.ui.sidebar import render_sidebar
from home_planner.ui.state import init_session_state
from home_planner.units import DISPLAY_UNITS, Unit


def run_app() -> None:
    st.set_page_config(page_title="Home Planner", page_icon="🏠", layout="wide")
    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stSidebar"] {{
            background-color: {APP_BACKGROUND};
        }}
        :root {{
            --home-toolbar-height: 60px;
            --home-header-height: 15rem;
            --home-header-offset: calc(var(--home-toolbar-height) + var(--home-header-height));
        }}
        .st-key-home_page_header {{
            position: fixed;
            top: var(--home-toolbar-height);
            left: 0;
            right: 0;
            z-index: 10000;
            width: 100vw;
            min-height: var(--home-header-height);
            margin: 0;
            padding: 0.75rem 1cm;
            box-sizing: border-box;
            background-color: {APP_BACKGROUND};
            border-bottom: 1px solid rgba(55, 50, 45, 0.16);
        }}
        .st-key-home_page_header [data-testid="stHorizontalBlock"] {{
            align-items: center;
            width: 100%;
            margin: 0;
            gap: 1rem;
        }}
        .st-key-home_page_header [data-testid="column"]:first-child {{
            padding-left: 0;
        }}
        .st-key-home_page_header [data-testid="column"]:last-child {{
            padding-right: 0;
        }}
        [data-testid="stMainBlockContainer"] {{
            padding-top: calc(var(--home-header-offset) + 1rem);
        }}
        [data-testid="stSidebar"] {{
            align-self: flex-start;
            height: calc(100vh - var(--home-header-offset)) !important;
            max-height: calc(100vh - var(--home-header-offset)) !important;
            margin-top: var(--home-header-offset);
            min-height: 0;
            overflow: hidden;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            height: 100%;
            max-height: 100%;
            padding-top: 1rem;
            box-sizing: border-box;
            overflow-y: auto;
        }}
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stSidebarCollapsedControl"] {{
            position: fixed;
            top: calc(var(--home-header-offset) + 0.5rem);
            z-index: 10001;
        }}
        [data-testid="stExpandSidebarButton"] {{
            position: fixed;
            top: calc(var(--home-header-offset) + 0.5rem);
            left: 1cm;
            z-index: 10001;
        }}
        @media (max-width: 640px) {{
            :root {{
                --home-header-height: 19rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_session_state()
    home = st.session_state.home

    display_unit: Unit = st.session_state.get("display_unit", DISPLAY_UNITS[0])
    pdf_bytes = _build_floor_plan_pdf(home, display_unit, st.session_state.furniture)
    with st.container(key="home_page_header"):
        header_left, header_right = st.columns([5, 1], vertical_alignment="center")
        with header_left:
            st.title("Home Planer")
            st.markdown(
                "Home Planar helps you to turn room measurements into a simple, "
                "dimension-accurate floor plan by just simply inputing the dimensions "
                "of the rooms and how you want your rooms look like. This will also "
                "provides you the recommended furnitures for your rooms. You can also "
                "use the AI feature to generate a floor plan for you based on your requirements."
            )
        with header_right:
            st.download_button(
                "Download floorplan pdf",
                data=pdf_bytes,
                file_name="home-plan.pdf",
                mime="application/pdf",
                key="download_floor_plan_pdf",
                on_click="ignore",
                disabled=not home.rooms,
                use_container_width=True,
            )

    display_unit = st.selectbox("Display unit", DISPLAY_UNITS, key="display_unit")

    render_sidebar(home)
    render_ai_panel(home, st.session_state.furniture)

    left, right = st.columns([1, 2], gap="large")

    with left:
        selected_room = render_room_panel(home, display_unit)
        render_furniture_panel(selected_room, display_unit)

    with right:
        render_floor_plan_panel(
            home,
            selected_room_id=st.session_state.selected_room_id,
            display_unit=display_unit,
        )
