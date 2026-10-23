"""2D top-down floor plan renderer."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.figure import Figure

from home_planner.constants import APP_BACKGROUND, ROOM_COLORS
from home_planner.models import Furniture, Home, Room
from home_planner.units import Unit, format_length, from_cm


def _draw_room(
    ax: plt.Axes,
    room: Room,
    *,
    highlight: bool = False,
    display_unit: Unit = "m",
) -> None:
    x, y = room.position
    width, length = room.width, room.length

    color = "#2563eb" if highlight else "#334155"
    fill = ROOM_COLORS.get(room.room_type, ROOM_COLORS["Other"])

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
        room.label,
        ha="center",
        va="center",
        fontsize=11,
        color="#0f172a",
        fontweight="600",
    )


def _draw_furniture(
    ax: plt.Axes,
    room: Room,
    furniture: Furniture,
    display_unit: Unit,
) -> None:
    room_x, room_y = room.position
    x = room_x + furniture.x
    y = room_y + furniture.y
    rotated = furniture.rotation in (90, 270)
    width = furniture.depth if rotated else furniture.width
    depth = furniture.width if rotated else furniture.depth

    rect = plt.Rectangle(
        (x, y),
        width,
        depth,
        fill=True,
        facecolor="#ffffff",
        edgecolor="#111827",
        linewidth=2,
    )
    ax.add_patch(rect)

    ax.text(
        x + width / 2,
        y + depth / 2,
        f"{furniture.furniture_type}: {furniture.name}",
        ha="center",
        va="center",
        fontsize=9,
        color="#111827",
        fontweight="600",
    )
    ax.text(
        x + width / 2,
        y + depth / 2 + max(depth * 0.12, 8),
        f"{format_length(width, display_unit, precision=2)} × "
        f"{format_length(depth, display_unit, precision=2)}",
        ha="center",
        va="center",
        fontsize=8,
        color="#475569",
    )


def _draw_openings(ax: plt.Axes, room: Room) -> None:
    """Draw door and window marks over the room boundary."""
    x, y = room.position
    opening_counts = {"door": 0, "window": 0}
    for opening in room.openings:
        opening_counts[opening.type] += 1
        opening_name = opening.name or f"{opening.type.title()} {opening_counts[opening.type]}"
        color = "#b45309" if opening.type == "door" else "#0284c7"
        if opening.wall_id == "top":
            start, end = (x + opening.offset, y), (x + opening.offset + opening.width, y)
        elif opening.wall_id == "bottom":
            start, end = (x + opening.offset, y + room.length), (x + opening.offset + opening.width, y + room.length)
        elif opening.wall_id == "left":
            start, end = (x, y + opening.offset), (x, y + opening.offset + opening.width)
        else:
            start, end = (x + room.width, y + opening.offset), (x + room.width, y + opening.offset + opening.width)
        ax.plot([start[0], end[0]], [start[1], end[1]], color="white", linewidth=6, solid_capstyle="butt", zorder=4)
        ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=2, solid_capstyle="butt", zorder=5)
        midpoint_x = (start[0] + end[0]) / 2
        midpoint_y = (start[1] + end[1]) / 2
        ax.annotate(
            opening_name,
            (midpoint_x, midpoint_y),
            xytext=(0, -12),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=8,
            color=color,
            zorder=6,
        )


def render_floor_plan(
    home: Home,
    *,
    selected_room_id: str | None = None,
    furniture: list[Furniture] | None = None,
    display_unit: Unit = "m",
) -> Figure:
    """Render a top-down floor plan for all rooms in the home."""
    furniture = furniture or []
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    fig.set_facecolor(APP_BACKGROUND)
    ax.set_facecolor(APP_BACKGROUND)

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
    for room in home.rooms:
        _draw_openings(ax, room)
        room_items = [item for item in furniture if item.room_id == room.id]
        if not room_items and room is selected_room:
            room_items = [item for item in furniture if item.room_id is None]
        for item in room_items:
            _draw_furniture(ax, room, item, display_unit)

    xs, ys = [], []
    for room in home.rooms:
        x, y = room.position
        xs.extend([x, x + room.width])
        ys.extend([y, y + room.length])

    pad = max(max(xs) - min(xs), max(ys) - min(ys)) * 0.15 + 30
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.invert_yaxis()

    ax.xaxis.set_major_locator(MaxNLocator(nbins=30, steps=[1, 2, 5, 10]))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=30, steps=[1, 2, 5, 10]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{from_cm(value, display_unit):g}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{from_cm(value, display_unit):g}"))
    ax.grid(True, linestyle="--", linewidth=0.5, color="#e2e8f0", alpha=0.8)
    ax.set_xlabel(f"Distance ({display_unit})")
    ax.set_ylabel(f"Distance ({display_unit})")
    ax.set_title(f"{home.name} — Floor plan", fontsize=13, fontweight="600", color="#0f172a", pad=12)

    fig.tight_layout()
    return fig
