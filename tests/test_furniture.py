"""Tests for furniture placement logic."""

import unittest

from home_planner.models import Furniture, Room
from home_planner.services.furniture import furniture_fits, validate_furniture_dimensions


def _living_room() -> Room:
    return Room(name="Living Room", width=400, length=300, height=250)


class TestFurniture(unittest.TestCase):
    def test_furniture_fits(self):
        room = _living_room()
        item = Furniture(name="Sofa", width=200, depth=90, x=20, y=20)
        self.assertTrue(furniture_fits(room, item))

    def test_furniture_too_wide(self):
        room = _living_room()
        item = Furniture(name="Sofa", width=500, depth=90, x=20, y=20)
        self.assertFalse(furniture_fits(room, item))

    def test_furniture_too_deep(self):
        room = _living_room()
        item = Furniture(name="Sofa", width=200, depth=400, x=20, y=20)
        self.assertFalse(furniture_fits(room, item))

    def test_exact_fit(self):
        room = _living_room()
        item = Furniture(name="Rug", width=400, depth=300, x=0, y=0)
        self.assertTrue(furniture_fits(room, item))

    def test_rotated_furniture_uses_swapped_dimensions(self):
        room = Room(name="Narrow Room", width=100, length=200, height=250)
        item = Furniture(
            name="Table",
            width=150,
            depth=100,
            x=0,
            y=0,
            rotation=90,
        )
        self.assertTrue(furniture_fits(room, item))

    def test_validate_furniture_dimensions_rejects_invalid_sizes(self):
        room = _living_room()
        self.assertIsNone(validate_furniture_dimensions(200, 90, room))
        self.assertIn("greater than zero", validate_furniture_dimensions(0, 90, room))
        self.assertIn("exceed the room size", validate_furniture_dimensions(500, 90, room))

if __name__ == "__main__":
    unittest.main()
