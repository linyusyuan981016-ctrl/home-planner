"""Tests for room management logic."""

import unittest

from home_planner.models import Home, Room
from home_planner.services.rooms import add_room


class TestRooms(unittest.TestCase):
    def test_add_room_inserts_once_and_positions_after_existing_room(self):
        home = Home()
        first = Room(name="Living Room", width=400, length=300, height=250)
        second = Room(name="Office", width=300, length=250, height=250)

        add_room(home, first)
        add_room(home, second)

        self.assertEqual(home.rooms, [first, second])
        self.assertEqual(second.position, (first.width + 50, 0.0))


if __name__ == "__main__":
    unittest.main()
