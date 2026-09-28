"""Streamlit chat panel for the home planning assistant."""

from __future__ import annotations

import streamlit as st

from home_planner.models import Home
from home_planner.services.ai_agent import ask_assistant, is_ollama_available


def render_ai_panel(home: Home, furniture: list) -> None:
    """Render an optional AI assistant without exposing the API key."""
    st.sidebar.divider()
    st.sidebar.header("AI Space Assistant")

    if not is_ollama_available():
        st.sidebar.caption("Start Ollama locally to enable the assistant.")
        return

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for message in st.session_state.ai_messages:
        with st.sidebar.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.sidebar.chat_input("Ask about your layout")
    if not prompt:
        return

    st.session_state.ai_messages.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.write(prompt)

    try:
        answer = ask_assistant(
            st.session_state.ai_messages,
            home=home,
            furniture=furniture,
        )
    except Exception as exc:
        st.sidebar.error(f"The assistant could not respond: {exc}")
        return

    st.session_state.ai_messages.append({"role": "assistant", "content": answer})
    with st.sidebar.chat_message("assistant"):
        st.write(answer)