"""Streamlit chat panel for the home planning assistant."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Home
from home_planner.services.ai_agent import is_ollama_available, stream_assistant


def render_ai_panel(home: Home, furniture: list) -> None:
    """Render a fixed bottom-right assistant launcher and chat panel."""
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []
    if "ai_chat_open" not in st.session_state:
        st.session_state.ai_chat_open = False

    if not st.session_state.ai_chat_open:
        if st.button("✦", key="ai_chat_launcher", help="Open AI Space Assistant"):
            st.session_state.ai_chat_open = True
            st.rerun()
        return

    with st.container(key="ai_chat_panel"):
        ollama_available = is_ollama_available()
        header, minimize = st.columns([5, 1], vertical_alignment="center")
        with header:
            st.markdown("**AI Space Assistant**")
        with minimize:
            if st.button("−", key="ai_chat_minimize", help="Minimize assistant"):
                st.session_state.ai_chat_open = False
                st.rerun()

        if not ollama_available:
            st.caption("AI assistant unavailable: its Ollama server can't be reached.")

        with st.container(key="ai_chat_history", height=350, border=False):
            for message in st.session_state.ai_messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            response_slot = st.empty()

        with st.form("ai_chat_form", clear_on_submit=True):
            prompt = st.text_area(
                "Message",
                placeholder="Ask about your layout",
                height=100,
            )
            submitted = st.form_submit_button(
                "Send",
                type="primary",
                disabled=not ollama_available,
                use_container_width=True,
            )

    if not submitted or not prompt.strip():
        return

    st.session_state.ai_messages.append({"role": "user", "content": prompt.strip()})
    answer = ""
    with response_slot.container():
        with st.chat_message("user"):
            st.write(prompt.strip())
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            try:
                for chunk in stream_assistant(
                    st.session_state.ai_messages,
                    home=home,
                    furniture=furniture,
                ):
                    answer += chunk
                    response_placeholder.markdown(answer)
            except Exception:
                answer = "Ollama not working"
                response_placeholder.markdown(answer)

    st.session_state.ai_messages.append({"role": "assistant", "content": answer})
    st.rerun()