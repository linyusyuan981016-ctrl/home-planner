"""Domain models for Feature 1: Dimensions → Map."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Literal

OpeningType = Literal["door", "window"]
Swing = Literal["left-in", "left-out", "right-in", "right-out"]


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Opening:
    id: str
    room_id: str
    wall_id: str
    type: OpeningType
    offset: float  # cm from wall start
    width: float
    height: float
    sill_height: float | None = None
    swing: Swing | None = None


@dataclass
class Wall:
    id: str
    room_id: str
    start: tuple[float, float]
    end: tuple[float, float]

    @property
    def length(self) -> float:
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        return (dx**2 + dy**2) ** 0.5


@dataclass
class Furniture:
    """A rectangular furniture block stored in centimeters."""

    name: str
    width: float
    depth: float
    x: float
    y: float
    rotation: float = 0.0
    id: str = field(default_factory=_new_id)
    room_id: str | None = None


@dataclass
class Room:
    name: str
    width: float   # cm, X axis
    length: float  # cm, Y axis
    height: float  # cm, Z axis
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    position: tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0
    openings: list[Opening] = field(default_factory=list)

    @property
    def walls(self) -> list[Wall]:
        """Four walls derived from room dimensions."""
        x, y = self.position
        w, length = self.width, self.length
        corners = [(x, y), (x + w, y), (x + w, y + length), (x, y + length)]
        return [
            Wall(_new_id(), self.id, corners[i], corners[(i + 1) % 4])
            for i in range(4)
        ]

    @property
    def floor_area_m2(self) -> float:
        return self.width * self.length / 10_000


@dataclass
class Home:
    name: str = "My Home"
    units: Literal["cm", "in"] = "cm"
    rooms: list[Room] = field(default_factory=list)
    id: str = field(default_factory=_new_id)
