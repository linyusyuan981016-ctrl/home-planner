import unittest
import matplotlib.pyplot as plt

from home_planner.models import Home, Room
from home_planner.floor_plan import render_floor_plan




conversion = {
    "cm": 1,
    "m": 100,
    "inch": 2.54,
    "feet": 30.48,
}


def furniture_fits(room, x, y, width, depth):
    return (
        x + width <= room.width
        and y + depth <= room.length
    )


class TestHomePlanner(unittest.TestCase):

    def test_cm_conversion(self):
        self.assertEqual(100 * conversion["cm"], 100)

    def test_meter_conversion(self):
        self.assertEqual(2 * conversion["m"], 200)

    def test_inch_conversion(self):
        self.assertEqual(10 * conversion["inch"], 25.4)

    def test_feet_conversion(self):
        self.assertEqual(1 * conversion["feet"], 30.48)

    def test_furniture_fits(self):
        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        result = furniture_fits(
            room,
            x=20,
            y=20,
            width=200,
            depth=90
        )

        self.assertTrue(result)

    def test_furniture_too_wide(self):
        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        result = furniture_fits(
            room,
            x=20,
            y=20,
            width=500,
            depth=90
        )

        self.assertFalse(result)

    def test_furniture_too_deep(self):
        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        result = furniture_fits(
            room,
            x=20,
            y=20,
            width=200,
            depth=400
        )

        self.assertFalse(result)

    def test_exact_fit(self):
        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        result = furniture_fits(
            room,
            x=0,
            y=0,
            width=400,
            depth=300
        )

        self.assertTrue(result)

    def test_render_floor_plan(self):
        home = Home(name="Test Home")

        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        home.rooms.append(room)

        fig = render_floor_plan(
            home,
            selected_room_id=room.id,
            furniture=[]
        )

        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, plt.Figure)

        plt.close(fig)

    def test_render_with_furniture(self):
        home = Home(name="Test Home")

        room = Room(
            name="Living Room",
            width=400,
            length=300,
            height=250
        )

        home.rooms.append(room)

        furniture = [
            {
                "name": "Sofa",
                "width": 200,
                "depth": 90,
                "x": 20,
                "y": 20
            }
        ]

        fig = render_floor_plan(
            home,
            selected_room_id=room.id,
            furniture=furniture
        )

        ax = fig.axes[0]

        # Room rectangle + furniture rectangle
        self.assertGreaterEqual(len(ax.patches), 2)

        plt.close(fig)


if __name__ == "__main__":
    unittest.main()