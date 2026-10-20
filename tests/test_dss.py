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
            "Продукт: железная плита; Планета: Наувис; "
            "Приоритет: скорость; Энергия: электричество"
        )
        self.assertEqual(recommend(request)[0]["machine"], "electric_furnace")

    def test_lowest_electric_draw(self):
        request = self.request(
            "Продукт: железная шестерня; Планета: Наувис; "
            "Приоритет: электроэнергия; Энергия: электричество"
        )
        self.assertEqual(recommend(request)[0]["machine"], "assembling_machine_1")

    def test_fuel_and_speed(self):
        request = self.request(
            "Продукт: железная плита; Планета: Наувис; "
            "Приоритет: скорость; Энергия: топливо"
        )
        self.assertEqual(recommend(request)[0]["machine"], "steel_furnace")

    def test_assembler(self):
        request = self.request(
            "Продукт: электронная схема; Планета: Наувис; Приоритет: скорость"
        )
        self.assertEqual(recommend(request)[0]["machine"], "assembling_machine_2")

    def test_foundry(self):
        request = self.request(
            "Продукт: расплавленное железо; Планета: Вулканус; Приоритет: скорость"
        )
        self.assertEqual(recommend(request)[0]["machine"], "foundry")

    def test_no_candidate(self):
        request = self.request(
            "Продукт: расплавленное железо; Планета: Наувис; Приоритет: скорость"
        )
        self.assertEqual(recommend(request), [])
        self.assertIn("нет подходящей машины", explain(request, []))

    def test_unknown_value(self):
        with self.assertRaisesRegex(ValueError, "Неизвестное значение"):
            parse_fields("Продукт: неизвестный; Планета: Наувис")

    def test_conflicting_duplicate(self):
        with self.assertRaisesRegex(ValueError, "дважды"):
            parse_fields("Планета: Наувис; Планета: Вулканус")

    def test_missing_slot_prompts(self):
        fields = parse_fields("Продукт: сера")
        with patch("builtins.input", side_effect=["Наувис", "скорость"]):
            self.assertEqual(ask_missing(fields), Request("sulfur", "nauvis", "speed", "any"))


if __name__ == "__main__":
    unittest.main()
