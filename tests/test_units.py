"""Tests for unit conversion helpers."""

import unittest

from home_planner.units import CM_PER_UNIT, from_cm, to_cm


class TestUnits(unittest.TestCase):
    def test_cm_conversion(self):
        self.assertEqual(to_cm(100, "cm"), 100)

    def test_meter_conversion(self):
        self.assertEqual(to_cm(2, "m"), 200)

    def test_inch_conversion(self):
        self.assertAlmostEqual(to_cm(10, "inch"), 25.4)

    def test_feet_conversion(self):
        self.assertAlmostEqual(to_cm(1, "feet"), 30.48)

    def test_from_cm_round_trip(self):
        for unit, factor in CM_PER_UNIT.items():
            self.assertAlmostEqual(from_cm(factor * 3, unit), 3.0)


if __name__ == "__main__":
    unittest.main()
