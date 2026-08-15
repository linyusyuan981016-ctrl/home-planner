"""2D top-down floor plan renderer."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


from home_planner.models import Home, Room


def _draw_room(ax, room: Room, *, highlight: bool = False, display_unit = "cm") -> None:
    x, y = room.position
    w, l = room.width, room.length
    conversion = {
    "cm": 1,
    "m": 100,
    "inch": 2.54,
    "feet": 30.48
    }

    factor = conversion[display_unit]

    display_w = w / factor
    display_l = l / factor

    color = "#2563eb" if highlight else "#334155"
    fill = "#dbeafe" if highlight else "#f8fafc"

    rect = plt.Rectangle((x, y), w, l, fill=True, facecolor=fill, edgecolor=color, linewidth=2)
    ax.add_patch(rect)

    # Dimension labels on each wall (cm)
    label_kw = dict(ha="center", va="center", fontsize=9, color="#1e293b", fontweight="500")
    ax.text(x + w / 2, y - max(l * 0.04, 8), f"{display_w:.2f} {display_unit}", **label_kw)
    ax.text(x + w / 2, y + l + max(l * 0.04, 8), f"{display_w:.2f} {display_unit}", **label_kw)
    ax.text(x - max(w * 0.04, 8), y + l / 2, f"{display_l:.2f} {display_unit}", ha="right", va="center", fontsize=9, color="#1e293b", fontweight="500")
    ax.text(x + w + max(w * 0.04, 8), y + l / 2, f"{display_l:.2f} {display_unit}", ha="left", va="center", fontsize=9, color="#1e293b", fontweight="500")

    # Room name inside
    ax.text(x + w / 2, y + l / 2, room.name, ha="center", va="center", fontsize=11, color="#0f172a", fontweight="600")


def render_floor_plan(
    home: Home,
    *, 
    selected_room_id: str | None = None, 
    furniture=None,
    display_unit = "cm"
) -> Figure:
    """Render a top-down floor plan for all rooms in the home."""
    conversion = {
            "cm" : 1,
            "m" : 100,
            "inch" :2.54,
            "feet" : 30.48
        }
    factor = conversion[display_unit]
    furniture = furniture or []
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.set_facecolor("#ffffff")

    if not home.rooms:
        ax.text(0.5, 0.5, "Add a room to see the floor plan", transform=ax.transAxes, ha="center", va="center", color="#94a3b8", fontsize=12)
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 300)
        ax.axis("off")
        fig.tight_layout()
        return fig

    for room in home.rooms:
        _draw_room(ax, room, highlight=room.id == selected_room_id, display_unit= display_unit)
    selected_room = next(
        (room for room in home.rooms if room.id == selected_room_id),
        None
    )
    if selected_room:
        room_x, room_y = selected_room.position
        for item in furniture:
            furniture_rect = plt.Rectangle(
                (
                    room_x + item["x"],
                    room_y + item["y"]
                ),
                item["width"],
                item["depth"],
                fill = True,
                facecolor = "#ffffff",
                edgecolor = "#111827",
                linewidth = 2
            )

            ax.add_patch(furniture_rect)

            ax.text(
                room_x + item["x"] + item["width"] /2, 
                room_y + item["y"] + item["depth"] / 2,

                item["name"],

                ha="center",

                va="center",

                fontsize=9,

                color="#111827",

                fontweight="600"
            )

    # Fit view with padding
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


