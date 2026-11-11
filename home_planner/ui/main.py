"""Streamlit application entry."""

from __future__ import annotations

import streamlit as st

from home_planner.constants import APP_BACKGROUND
from home_planner.ui.floor_plan_panel import _build_floor_plan_pdf, render_floor_plan_panel
from home_planner.ui.ai_panel import render_ai_panel
from home_planner.ui.sidebar import render_sidebar
from home_planner.ui.state import init_session_state


def run_app() -> None:
    st.set_page_config(
        page_title="Home Planner",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stSidebar"] {{
            background-color: {APP_BACKGROUND};
        }}
        :root {{
            --home-toolbar-height: 60px;
            --home-header-height: 12rem;
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
                --home-header-height: 16rem;
            }}
        }}
        .st-key-ai_chat_panel {{
            position: fixed;
            right: 1.25rem;
            bottom: 1.25rem;
            z-index: 10020;
            width: min(380px, calc(100vw - 2rem));
            height: min(560px, calc(100vh - var(--home-toolbar-height) - 2rem));
            max-height: calc(100vh - var(--home-toolbar-height) - 2rem);
            min-height: 320px;
            padding: 1rem;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid rgba(55, 50, 45, 0.18);
            border-radius: 12px;
            background: {APP_BACKGROUND};
            box-shadow: 0 12px 36px rgba(30, 27, 24, 0.2);
        }}
        .st-key-ai_chat_panel [data-testid="stLayoutWrapper"]:has(.st-key-ai_chat_history) {{
            flex: 1 1 0;
            height: auto;
            min-height: 0;
        }}
        .st-key-ai_chat_history {{
            height: 100%;
            min-height: 0;
            overflow-y: auto;
        }}
        .st-key-ai_chat_panel [data-testid="stLayoutWrapper"]:has(.st-key-FormSubmitter-ai_chat_form-Send) {{
            flex: 0 0 auto;
            margin-top: auto;
        }}
        .st-key-ai_chat_launcher {{
            position: fixed;
            right: 1.5rem;
            bottom: 1.5rem;
            z-index: 10020;
        }}
        .st-key-ai_chat_launcher button {{
            width: 3.5rem;
            height: 3.5rem;
            padding: 0;
            border-radius: 50%;
            border: 0;
            background: #3f6f65;
            color: white;
            font-size: 1.8rem;
            box-shadow: 0 6px 20px rgba(30, 27, 24, 0.22);
        }}
        .st-key-ai_chat_panel [data-testid="stHorizontalBlock"] {{
            align-items: center;
            padding-left: 1.25rem;
            box-sizing: border-box;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_session_state()
    home = st.session_state.home

    display_unit = render_sidebar(home)
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

    render_floor_plan_panel(
        home,
        selected_room_id=st.session_state.selected_room_id,
        display_unit=display_unit,
    )

    render_ai_panel(home, st.session_state.furniture)
