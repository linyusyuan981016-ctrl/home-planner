"""Tests for floor plan rendering."""

import unittest

import matplotlib.pyplot as plt

from home_planner.models import Furniture, Home, Room
from home_planner.rendering.floor_plan import render_floor_plan


class TestFloorPlan(unittest.TestCase):
    def setUp(self) -> None:
        self.home = Home(name="Test Home")
        self.room = Room(name="Living Room", width=400, length=300, height=250)
        self.home.rooms.append(self.room)

    def test_render_empty_home(self):
        empty_home = Home(name="Empty")
        fig = render_floor_plan(empty_home)
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

    def test_render_floor_plan(self):
        fig = render_floor_plan(self.home, selected_room_id=self.room.id)
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

    def test_render_with_furniture(self):
        furniture = [Furniture(name="Sofa", width=200, depth=90, x=20, y=20)]
        fig = render_floor_plan(
            self.home,
            selected_room_id=self.room.id,
            furniture=furniture,
        )
        ax = fig.axes[0]
        self.assertGreaterEqual(len(ax.patches), 2)
        plt.close(fig)


if __name__ == "__main__":
    unittest.main()
