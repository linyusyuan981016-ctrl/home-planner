"""2D top-down floor plan renderer."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from home_planner.models import Furniture, Home, Room
from home_planner.units import Unit, format_length


def _draw_room(
    ax: plt.Axes,
    room: Room,
    *,
    highlight: bool = False,
    display_unit: Unit = "cm",
) -> None:
    x, y = room.position
    width, length = room.width, room.length

    color = "#2563eb" if highlight else "#334155"
    fill = "#dbeafe" if highlight else "#f8fafc"

    rect = plt.Rectangle(
        (x, y),
        width,
        length,
        fill=True,
        facecolor=fill,
        edgecolor=color,
        linewidth=2,
    )
    ax.add_patch(rect)

    label_kw = dict(ha="center", va="center", fontsize=9, color="#1e293b", fontweight="500")
    offset_x = max(width * 0.04, 8)
    offset_y = max(length * 0.04, 8)

    ax.text(x + width / 2, y - offset_y, format_length(width, display_unit, precision=2), **label_kw)
    ax.text(x + width / 2, y + length + offset_y, format_length(width, display_unit, precision=2), **label_kw)
    ax.text(
        x - offset_x,
        y + length / 2,
        format_length(length, display_unit, precision=2),
        ha="right",
        va="center",
        fontsize=9,
        color="#1e293b",
        fontweight="500",
    )
    ax.text(
        x + width + offset_x,
        y + length / 2,
        format_length(length, display_unit, precision=2),
        ha="left",
        va="center",
        fontsize=9,
        color="#1e293b",
        fontweight="500",
    )

    ax.text(
        x + width / 2,
        y + length / 2,
        room.name,
        ha="center",
        va="center",
        fontsize=11,
        color="#0f172a",
        fontweight="600",
    )


def _draw_furniture(ax: plt.Axes, room: Room, furniture: Furniture) -> None:
    room_x, room_y = room.position
    x = room_x + furniture.x
    y = room_y + furniture.y

    rect = plt.Rectangle(
        (x, y),
        furniture.width,
        furniture.depth,
        fill=True,
        facecolor="#ffffff",
        edgecolor="#111827",
        linewidth=2,
    )
    ax.add_patch(rect)

    ax.text(
        x + furniture.width / 2,
        y + furniture.depth / 2,
        furniture.name,
        ha="center",
        va="center",
        fontsize=9,
        color="#111827",
        fontweight="600",
    )


def render_floor_plan(
    home: Home,
    *,
    selected_room_id: str | None = None,
    furniture: list[Furniture] | None = None,
    display_unit: Unit = "cm",
) -> Figure:
    """Render a top-down floor plan for all rooms in the home."""
    furniture = furniture or []
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.set_facecolor("#ffffff")

    if not home.rooms:
        ax.text(
            0.5,
            0.5,
            "Add a room to see the floor plan",
            transform=ax.transAxes,
            ha="center",
            va="center",
            color="#94a3b8",
            fontsize=12,
        )
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 300)
        ax.axis("off")
        fig.tight_layout()
        return fig

    for room in home.rooms:
        _draw_room(ax, room, highlight=room.id == selected_room_id, display_unit=display_unit)

    selected_room = next((room for room in home.rooms if room.id == selected_room_id), None)
    if selected_room:
        for item in furniture:
            _draw_furniture(ax, selected_room, item)

    xs, ys = [], []
    for room in home.rooms:
        x, y = room.position
        xs.extend([x, x + room.width])
        ys.extend([y, y + room.length])

    pad = max(max(xs) - min(xs), max(ys) - min(ys)) * 0.15 + 30
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)

    ax.grid(True, linestyle="--", linewidth=0.5, color="#e2e8f0", alpha=0.8)
    ax.set_xlabel(display_unit)
    ax.set_ylabel(display_unit)
    ax.set_title(f"{home.name} — Floor plan", fontsize=13, fontweight="600", color="#0f172a", pad=12)

    fig.tight_layout()
    return fig
