"""Command-line decision support over the Lab 1 Factorio Prolog knowledge base.

Input format: product: iron_plate; planet: nauvis;
              priority: speed; energy: electricity
The first three slots are required; missing slots are requested interactively.
Energy is optional and defaults to "any".
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
    "product": "product",
    "planet": "planet",
    "priority": "priority",
    "energy": "energy",
}
VALUES = {
    "product": {
        "iron_plate": "iron_plate",
        "copper_plate": "copper_plate",
        "steel_plate": "steel_plate",
        "stone_brick": "stone_brick",
        "iron_gear_wheel": "iron_gear_wheel",
        "copper_cable": "copper_cable",
        "electronic_circuit": "electronic_circuit",
        "plastic_bar": "plastic_bar",
        "sulfur": "sulfur",
        "molten_iron": "molten_iron",
    },
    "planet": {"nauvis": "nauvis", "vulcanus": "vulcanus"},
    "priority": {"speed": "speed", "electricity": "electricity"},
    "energy": {"any": "any", "electricity": "electricity", "fuel": "fuel"},
}
MACHINE_NAMES = {
    "stone_furnace": "stone furnace",
    "steel_furnace": "steel furnace",
    "electric_furnace": "electric furnace",
    "assembling_machine_1": "assembling machine 1",
    "assembling_machine_2": "assembling machine 2",
    "chemical_plant": "chemical plant",
    "foundry": "foundry",
}
PROMPTS = {
    "product": "Which product do you need?",
    "planet": "Which planet (nauvis/vulcanus)?",
    "priority": "Which priority (speed/electricity)?",
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
            raise ValueError(f"Expected a 'key: value' field: {segment.strip()}")
        label, value = (part.strip().casefold() for part in segment.split(":", 1))
        field = FIELDS.get(label)
        if field is None:
            raise ValueError(f"Unknown field: {label}")
        if field in result:
            raise ValueError(f"Duplicate field: {label}")
        normalized = VALUES[field].get(value)
        if normalized is None:
            choices = ", ".join(VALUES[field])
            raise ValueError(f"Unknown value '{value}' for '{label}'. Choices: {choices}")
        result[field] = normalized
    return result


def make_request(fields: dict[str, str]) -> Request:
    missing = [field for field in ("product", "planet", "priority") if field not in fields]
    if missing:
        raise ValueError("Missing fields: " + ", ".join(missing))
    return Request(fields["product"], fields["planet"], fields["priority"],
                   fields.get("energy", "any"))


def ask_missing(fields: dict[str, str]) -> Request:
    for field in ("product", "planet", "priority"):
        while field not in fields:
            try:
                answer = input(PROMPTS[field] + " ").strip()
            except EOFError as exc:
                raise ValueError("Input ended before all required fields were provided") from exc
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
        raise RuntimeError(f"SWI-Prolog query failed: {exc}") from exc
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
        return ("No suitable machine was found for this product, planet, and "
                "energy source. Check the conditions or choose another planet.")
    best = candidates[0]
    measure = (
        f"speed {best['speed']}"
        if request.priority == "speed"
        else f"electric power consumption {best['power_kw']} kW"
    )
    energy = best["power_source"]
    others = ", ".join(MACHINE_NAMES[item["machine"]] for item in candidates[1:])
    suffix = f" Other suitable machines: {others}." if others else ""
    return (
        f"Recommendation: {MACHINE_NAMES[best['machine']]}. "
        f"The can_craft/3 and power_source/2 rules confirm the product, planet, "
        f"and energy source ({energy}); selected criterion: {measure}.{suffix}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="request text; omit for interactive input")
    args = parser.parse_args()
    try:
        line = args.text if args.text is not None else input(
            "Enter request (product: ...; planet: ...; priority: ...; energy: ...): "
        )
        request = ask_missing(parse_fields(line))
        print(explain(request, recommend(request)))
        return 0
    except (ValueError, RuntimeError, EOFError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
