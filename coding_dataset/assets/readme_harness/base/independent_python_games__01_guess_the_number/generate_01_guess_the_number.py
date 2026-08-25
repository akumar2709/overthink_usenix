#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\ndef main():\n    print("=== Guess the Number ===")\n    secret = random.randint(1, 100)\n    attempts = 0\n\n    while True:\n        try:\n            guess = int(input("Guess a number from 1 to 100: "))\n        except ValueError:\n            print("Please enter a whole number.")\n            continue\n\n        attempts += 1\n        if guess < secret:\n            print("Too low!")\n        elif guess > secret:\n            print("Too high!")\n        else:\n            print(f"Correct! You won in {attempts} attempts.")\n            break\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "01_guess_the_number.py"


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
    print(f"Created {output_path} from 01_guess_the_number.py.")


if __name__ == "__main__":
    main()
