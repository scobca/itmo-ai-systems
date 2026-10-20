"""Command-line decision support over the Lab 1 Factorio Prolog knowledge base.

Input format: Продукт: железная плита; Планета: Наувис;
              Приоритет: скорость; Энергия: электричество
The first three slots are required; missing slots are requested interactively.
Energy is optional and defaults to "любая".
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

KB = Path(__file__).resolve().parents[1] / "lab1" / "factorio.pl"

FIELDS = {
    "продукт": "product",
    "планета": "planet",
    "приоритет": "priority",
    "энергия": "energy",
}
VALUES = {
    "product": {
        "железная плита": "iron_plate",
        "медная плита": "copper_plate",
        "стальная плита": "steel_plate",
        "каменный кирпич": "stone_brick",
        "железная шестерня": "iron_gear_wheel",
        "медный кабель": "copper_cable",
        "электронная схема": "electronic_circuit",
        "пластмасса": "plastic_bar",
        "сера": "sulfur",
        "расплавленное железо": "molten_iron",
    },
    "planet": {"наувис": "nauvis", "вулканус": "vulcanus"},
    "priority": {"скорость": "speed", "электроэнергия": "electricity"},
    "energy": {"любая": "any", "электричество": "electricity", "топливо": "fuel"},
}
MACHINE_NAMES = {
    "stone_furnace": "каменная печь",
    "steel_furnace": "стальная печь",
    "electric_furnace": "электрическая печь",
    "assembling_machine_1": "сборочный автомат 1",
    "assembling_machine_2": "сборочный автомат 2",
    "chemical_plant": "химический завод",
    "foundry": "литейная",
}
PROMPTS = {
    "product": "Какой продукт нужен?",
    "planet": "На какой планете (Наувис/Вулканус)?",
    "priority": "Что важнее (скорость/электроэнергия)?",
}


@dataclass(frozen=True)
class Request:
    product: str
    planet: str
    priority: str
    energy: str


def parse_fields(line: str) -> dict[str, str]:
    """Parse exact semicolon-separated key/value slots; reject unknown values."""
    result: dict[str, str] = {}
    for segment in line.split(";"):
        if not segment.strip():
            continue
        if segment.count(":") != 1:
            raise ValueError(f"Ожидается поле «Ключ: значение»: {segment.strip()}")
        label, value = (part.strip().casefold() for part in segment.split(":", 1))
        field = FIELDS.get(label)
        if field is None:
            raise ValueError(f"Неизвестное поле: {label}")
        if field in result:
            raise ValueError(f"Поле «{label}» указано дважды")
        normalized = VALUES[field].get(value)
        if normalized is None:
            choices = ", ".join(VALUES[field])
            raise ValueError(f"Неизвестное значение «{value}» для «{label}». Варианты: {choices}")
        result[field] = normalized
    return result


def make_request(fields: dict[str, str]) -> Request:
    missing = [field for field in ("product", "planet", "priority") if field not in fields]
    if missing:
        raise ValueError("Не заполнены поля: " + ", ".join(missing))
    return Request(fields["product"], fields["planet"], fields["priority"],
                   fields.get("energy", "any"))


def ask_missing(fields: dict[str, str]) -> Request:
    for field in ("product", "planet", "priority"):
        while field not in fields:
            try:
                answer = input(PROMPTS[field] + " ").strip()
            except EOFError as exc:
                raise ValueError("Ввод завершился до заполнения обязательных полей") from exc
            label = next(label for label, key in FIELDS.items() if key == field)
            try:
                fields.update(parse_fields(f"{label}: {answer}"))
            except ValueError as exc:
                print(exc, file=sys.stderr)
    return make_request(fields)


def query_prolog(request: Request) -> list[dict]:
    """The only atoms inserted into the goal come from the fixed allowlists above."""
    power_filter = (
        "true" if request.energy == "any"
        else f"power_source(M,{request.energy})"
    )
    goal = (
        "use_module(library(http/json)),"
        "findall(_{machine:M,speed:S,power_kw:W,power_source:E},"
        f"(can_craft(M,{request.product},{request.planet}),"
        f"{power_filter},machine_speed(M,S),machine_power(M,W),power_source(M,E)),R),"
        "json_write_dict(current_output,R),halt"
    )
    try:
        completed = subprocess.run(
            ["swipl", "-q", "-s", str(KB), "-g", goal],
            check=True, capture_output=True, text=True, timeout=10,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Не удалось выполнить запрос к SWI-Prolog: {exc}") from exc
    return json.loads(completed.stdout)


def recommend(request: Request) -> list[dict]:
    candidates = query_prolog(request)
    if request.priority == "speed":
        candidates.sort(key=lambda item: (-item["speed"], item["power_kw"], item["machine"]))
    else:
        candidates.sort(key=lambda item: (item["power_kw"], -item["speed"], item["machine"]))
    return candidates


def explain(request: Request, candidates: list[dict]) -> str:
    if not candidates:
        return ("Для выбранных продукта, планеты и источника энергии в базе нет "
                "подходящей машины. Проверьте условия или выберите другую планету.")
    best = candidates[0]
    measure = (
        f"скорость {best['speed']}"
        if request.priority == "speed"
        else f"потребление электричества {best['power_kw']} кВт"
    )
    energy = "электричество" if best["power_source"] == "electricity" else "топливо"
    others = ", ".join(MACHINE_NAMES[item["machine"]] for item in candidates[1:])
    suffix = f" Другие подходящие: {others}." if others else ""
    return (
        f"Рекомендация: {MACHINE_NAMES[best['machine']]}. "
        f"Правила can_craft/3 и power_source/2 подтверждают продукт, планету "
        f"и источник энергии ({energy}); выбранный критерий: {measure}.{suffix}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="фиксированная строка запроса; без нее ввод интерактивный")
    args = parser.parse_args()
    try:
        line = args.text if args.text is not None else input(
            "Введите запрос (Продукт: ...; Планета: ...; Приоритет: ...; Энергия: ...): "
        )
        request = ask_missing(parse_fields(line))
        print(explain(request, recommend(request)))
        return 0
    except (ValueError, RuntimeError, EOFError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
