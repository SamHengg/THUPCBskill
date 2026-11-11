"""Validate a point-to-point inter-board wiring table using Python's standard library."""

import argparse
import json
import math
import sys
from pathlib import Path


MATES = {
    "power_out": "power_in",
    "power_in": "power_out",
    "signal_out": "signal_in",
    "signal_in": "signal_out",
    "gnd": "gnd",
}
POWER_ROLES = {"power_in", "power_out"}


def unique_keys(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def is_finite_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    pins = data.get("pins")
    wires = data.get("wires")
    if not isinstance(pins, dict) or not pins:
        raise ValueError("pins must be a non-empty object")
    if not isinstance(wires, list):
        raise ValueError("wires must be an array")

    for key, pin in pins.items():
        parts = key.split(".")
        if len(parts) != 3 or not all(is_text(part) for part in parts):
            raise ValueError(f"{key!r} must be in board.connector.pin form")
        if not isinstance(pin, dict):
            raise ValueError(f"{key}: pin must be an object")
        role = pin.get("role")
        if not isinstance(role, str) or (role not in MATES and role != "nc"):
            raise ValueError(f"{key}: unknown role {role!r}")
        if role != "nc" and not all(is_text(pin.get(field)) for field in ("net", "function")):
            raise ValueError(f"{key}: connected pins require net and function")
        if role in POWER_ROLES:
            limits = pin.get("voltage_v")
            if (
                not isinstance(limits, list)
                or len(limits) != 2
                or not all(is_finite_number(value) for value in limits)
                or limits[0] > limits[1]
            ):
                raise ValueError(f"{key}: voltage_v must be an ordered finite range in volts")

    for index, wire in enumerate(wires, 1):
        if not isinstance(wire, list) or len(wire) != 2 or not all(is_text(end) for end in wire):
            raise ValueError(f"wire {index} must contain exactly two pin identifiers")
    return pins, wires


def check_pair(left, right):
    if MATES.get(left["role"]) != right["role"]:
        yield f"incompatible roles {left['role']} and {right['role']}"
        return
    if left["function"] != right["function"]:
        yield f"function mismatch {left['function']!r} and {right['function']!r}"
    if left["role"] in POWER_ROLES:
        source, load = (left, right) if left["role"] == "power_out" else (right, left)
        source_min, source_max = source["voltage_v"]
        load_min, load_max = load["voltage_v"]
        if source_min < load_min or source_max > load_max:
            yield (
                f"source range [{source_min}, {source_max}] V exceeds "
                f"load range [{load_min}, {load_max}] V"
            )


def check_wires(pins, wires):
    seen = set()
    for left, right in wires:
        pair = f"{left} <-> {right}"
        unknown = [end for end in (left, right) if end not in pins]
        if unknown:
            yield f"{pair}: unknown endpoint(s) {', '.join(unknown)}"
            continue
        if left.split(".")[0] == right.split(".")[0]:
            yield f"{pair}: both endpoints are on the same board"
        for end in (left, right):
            if end in seen:
                yield f"{end}: endpoint is used more than once"
            seen.add(end)
        for problem in check_pair(pins[left], pins[right]):
            yield f"{pair}: {problem}"

    for endpoint, pin in pins.items():
        if endpoint not in seen and pin["role"] != "nc":
            yield f"{endpoint}: expected endpoint has no wire"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", type=Path, help="JSON wiring table")
    args = parser.parse_args()

    try:
        data = json.loads(args.table.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_keys)
        pins, wires = validate_input(data)
    except (OSError, ValueError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        return 2

    issues = list(check_wires(pins, wires))
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    print(f"Interface table consistent: {len(wires)} wire(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
