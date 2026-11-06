import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "lab2"))
from dss import Request, ask_missing, explain, make_request, parse_fields, recommend


class DSSTests(unittest.TestCase):
    def request(self, text):
        return make_request(parse_fields(text))

    def test_fast_electric_furnace(self):
        request = self.request(
            "Product: iron_plate; Planet: nauvis; "
            "Priority: speed; Energy: electricity"
        )
        self.assertEqual(recommend(request)[0]["machine"], "electric_furnace")

    def test_lowest_electric_draw(self):
        request = self.request(
            "Product: iron_gear_wheel; Planet: nauvis; "
            "Priority: electricity; Energy: electricity"
        )
        self.assertEqual(recommend(request)[0]["machine"], "assembling_machine_1")

    def test_fuel_and_speed(self):
        request = self.request(
            "Product: iron_plate; Planet: nauvis; "
            "Priority: speed; Energy: fuel"
        )
        self.assertEqual(recommend(request)[0]["machine"], "steel_furnace")

    def test_assembler(self):
        request = self.request(
            "Product: electronic_circuit; Planet: nauvis; Priority: speed"
        )
        self.assertEqual(recommend(request)[0]["machine"], "assembling_machine_2")

    def test_foundry(self):
        request = self.request(
            "Product: molten_iron; Planet: vulcanus; Priority: speed"
        )
        self.assertEqual(recommend(request)[0]["machine"], "foundry")

    def test_no_candidate(self):
        request = self.request(
            "Product: molten_iron; Planet: nauvis; Priority: speed"
        )
        self.assertEqual(recommend(request), [])
        self.assertIn("No suitable machine", explain(request, []))

    def test_unknown_value(self):
        with self.assertRaisesRegex(ValueError, "Unknown value"):
            parse_fields("Product: unknown; Planet: nauvis")

    def test_conflicting_duplicate(self):
        with self.assertRaisesRegex(ValueError, "Duplicate field"):
            parse_fields("Planet: nauvis; Planet: vulcanus")

    def test_missing_slot_prompts(self):
        fields = parse_fields("Product: sulfur")
        with patch("builtins.input", side_effect=["nauvis", "speed"]):
            self.assertEqual(ask_missing(fields), Request("sulfur", "nauvis", "speed", "any"))


if __name__ == "__main__":
    unittest.main()
