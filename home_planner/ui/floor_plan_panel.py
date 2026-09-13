"""Floor plan preview panel."""

from __future__ import annotations

from dataclasses import asdict
from io import BytesIO

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages

from home_planner.floor_plan import render_floor_plan
from home_planner.models import Home
from home_planner.rendering.floor_plan import render_floor_plan as render_pdf_page
from home_planner.units import Unit


def _build_floor_plan_pdf(home: Home, display_unit: Unit, furniture: list) -> bytes:
    pdf_buffer = BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        for room in home.rooms:
            room_furniture = [item for item in furniture if item.room_id == room.id]
            page_home = Home(name=home.name, rooms=[room])
            figure = render_pdf_page(
                page_home,
                selected_room_id=room.id,
                furniture=room_furniture,
                display_unit=display_unit,
            )
            pdf.savefig(figure)
            plt.close(figure)
    return pdf_buffer.getvalue()


def render_floor_plan_panel(
    home: Home,
    *,
    selected_room_id: str | None,
    display_unit: Unit,
) -> None:
    st.subheader("2D floor plan")
    room_furniture = [
        item
        for item in st.session_state.furniture
        if item.room_id == selected_room_id
    ]
    updated_furniture = render_floor_plan(
        home,
        selected_room_id=selected_room_id,
        furniture=[asdict(item) for item in room_furniture],
        display_unit=display_unit,
    )
    if updated_furniture is not None:
        updated_by_id = {item["id"]: item for item in updated_furniture}
        for item in room_furniture:
            updated = updated_by_id.get(item.id)
            if updated:
                item.x = float(updated["x"])
                item.y = float(updated["y"])

    if home.rooms:
        pdf_bytes = _build_floor_plan_pdf(home, display_unit, st.session_state.furniture)
        st.download_button(
            "Download floor plan PDF",
            data=pdf_bytes,
            file_name="home-plan.pdf",
            mime="application/pdf",
            key="download_floor_plan_pdf",
            on_click="ignore",
        )
