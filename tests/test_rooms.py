"""Tests for room management logic."""

import unittest

from home_planner.models import Home, Room
from home_planner.services.openings import create_opening, update_opening_position
from home_planner.services.rooms import add_room, attach_room, room_name_exists


class TestRooms(unittest.TestCase):
    def test_add_room_inserts_once_and_positions_after_existing_room(self):
        home = Home()
        first = Room(name="Living Room", width=400, length=300, height=250)
        second = Room(name="Office", width=300, length=250, height=250)

        add_room(home, first)
        add_room(home, second)

        self.assertEqual(home.rooms, [first, second])
        self.assertEqual(second.position, (first.width + 50, 0.0))

    def test_room_name_exists_is_case_insensitive_and_can_exclude_room(self):
        home = Home(rooms=[Room(name="Living Room", width=400, length=300, height=250)])

        self.assertTrue(room_name_exists(home, " living room "))
        self.assertFalse(room_name_exists(home, "Living Room", exclude_id=home.rooms[0].id))

    def test_attach_room_positions_it_flush_to_target(self):
        first = Room(name="Living Room", width=400, length=300, height=250)
        second = Room(name="Kitchen", width=250, length=200, height=250)
        home = Home(rooms=[first, second])

        attach_room(home, second.id, first.id, "right")

        self.assertEqual(second.position, (400, 0))
        self.assertTrue(home.connected)

    def test_opening_defaults_to_center_of_top_wall_and_clamps_to_wall(self):
        room = Room(name="Living Room", width=400, length=300, height=250)

        opening = create_opening(room, "door")
        update_opening_position(opening, "left", 280, room)

        self.assertEqual(opening.wall_id, "left")
        self.assertEqual(opening.offset, 210)
        self.assertEqual(opening.width, 90)
        self.assertEqual(opening.name, "Door 1")


if __name__ == "__main__":
    unittest.main()
