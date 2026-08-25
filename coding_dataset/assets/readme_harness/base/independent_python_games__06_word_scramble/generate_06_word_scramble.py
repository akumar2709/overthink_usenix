#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\nWORDS = ["computer", "elephant", "mountain", "library", "diamond", "blanket"]\n\ndef scramble(word):\n    letters = list(word)\n    while True:\n        random.shuffle(letters)\n        result = "".join(letters)\n        if result != word:\n            return result\n\ndef main():\n    print("=== Word Scramble ===")\n    score = 0\n\n    for round_number in range(1, 6):\n        word = random.choice(WORDS)\n        mixed = scramble(word)\n        print(f"\\nRound {round_number}: Unscramble \'{mixed}\'")\n        answer = input("Your answer: ").strip().lower()\n\n        if answer == word:\n            score += 1\n            print("Correct!")\n        else:\n            print("Incorrect. The word was:", word)\n\n    print(f"\\nFinal score: {score}/5")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "06_word_scramble.py"


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
    print(f"Created {output_path} from 06_word_scramble.py.")


if __name__ == "__main__":
    main()
