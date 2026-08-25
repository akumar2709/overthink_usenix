#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'def main():\n    print("=== The Lost Temple ===")\n    print("You stand before an ancient temple.")\n    choice = input("Enter the temple or walk around it? ").strip().lower()\n\n    if "enter" in choice:\n        print("Inside, you see two doors: one red and one blue.")\n        door = input("Choose red or blue: ").strip().lower()\n\n        if door == "red":\n            print("A sleeping dragon guards a golden key.")\n            action = input("Sneak past or run away? ").strip().lower()\n            if "sneak" in action:\n                print("You steal the key and escape. You win!")\n            else:\n                print("You escape safely, but without treasure.")\n        elif door == "blue":\n            print("You find a room full of treasure. You win!")\n        else:\n            print("The hallway collapses while you hesitate.")\n    else:\n        print("Behind the temple, you find a hidden tunnel.")\n        tunnel = input("Enter the tunnel? yes or no: ").strip().lower()\n        if tunnel == "yes":\n            print("The tunnel leads directly to the treasure room. You win!")\n        else:\n            print("You return home safely.")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "09_text_adventure.py"


def write_game(output_path: Path) -> None:
    output_path.write_text(SOURCE_CODE, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the standalone game source file."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / DEFAULT_OUTPUT,
        help="Path where the game file should be written. Defaults to the current working directory.",
    )
    args = parser.parse_args()

    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_game(output_path)
    print(f"Created {output_path} from 09_text_adventure.py.")


if __name__ == "__main__":
    main()
