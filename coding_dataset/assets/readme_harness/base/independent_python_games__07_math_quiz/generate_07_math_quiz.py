#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\nimport operator\n\nOPERATIONS = {\n    "+": operator.add,\n    "-": operator.sub,\n    "*": operator.mul,\n}\n\ndef main():\n    print("=== Math Quiz ===")\n    score = 0\n    rounds = 10\n\n    for number in range(1, rounds + 1):\n        symbol = random.choice(list(OPERATIONS))\n        a = random.randint(1, 12)\n        b = random.randint(1, 12)\n\n        if symbol == "-" and b > a:\n            a, b = b, a\n\n        correct = OPERATIONS[symbol](a, b)\n\n        try:\n            answer = int(input(f"{number}. What is {a} {symbol} {b}? "))\n        except ValueError:\n            print(f"Invalid input. The answer was {correct}.")\n            continue\n\n        if answer == correct:\n            score += 1\n            print("Correct!")\n        else:\n            print(f"Wrong. The answer was {correct}.")\n\n    print(f"\\nYou scored {score}/{rounds}.")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "07_math_quiz.py"


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
    print(f"Created {output_path} from 07_math_quiz.py.")


if __name__ == "__main__":
    main()
