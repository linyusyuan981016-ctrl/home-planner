"""Tests for floor plan rendering."""

import unittest

import matplotlib.pyplot as plt

from home_planner.models import Furniture, Home, Opening, Room
from home_planner.rendering.floor_plan import render_floor_plan
from home_planner.ui.floor_plan_panel import _build_floor_plan_pdf


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

    def test_render_labels_doors_and_windows(self):
        self.room.openings.extend([
            Opening(
                id="door-1",
                room_id=self.room.id,
                wall_id="top",
                type="door",
                offset=20,
                width=90,
                height=210,
                name="Door 1",
            ),
            Opening(
                id="window-1",
                room_id=self.room.id,
                wall_id="right",
                type="window",
                offset=30,
                width=120,
                height=120,
                name="Window 1",
            ),
        ])

        fig = render_floor_plan(self.home, selected_room_id=self.room.id)

        labels = [text.get_text() for text in fig.axes[0].texts]
        self.assertIn("Door 1", labels)
        self.assertIn("Window 1", labels)
        plt.close(fig)

    def test_connected_home_download_is_a_finalized_pdf(self):
        second_room = Room(
            name="Kitchen",
            width=300,
            length=250,
            height=250,
            position=(self.room.width, 0),
        )
        home = Home(name="Test Home", rooms=[self.room, second_room], connected=True)

        pdf = _build_floor_plan_pdf(home, "m", [])

        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertTrue(pdf.rstrip().endswith(b"%%EOF"))


if __name__ == "__main__":
    unittest.main()
