#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\nWORDS = [\n    "python", "castle", "planet", "puzzle", "window",\n    "garden", "rocket", "bridge", "forest", "dragon"\n]\n\ndef display_word(word, guesses):\n    return " ".join(letter if letter in guesses else "_" for letter in word)\n\ndef main():\n    print("=== Hangman ===")\n    word = random.choice(WORDS)\n    guessed = set()\n    wrong = 0\n    max_wrong = 6\n\n    while wrong < max_wrong:\n        print("\\nWord:", display_word(word, guessed))\n        print(f"Wrong guesses remaining: {max_wrong - wrong}")\n        guess = input("Guess a letter: ").strip().lower()\n\n        if len(guess) != 1 or not guess.isalpha():\n            print("Enter exactly one letter.")\n            continue\n        if guess in guessed:\n            print("You already guessed that letter.")\n            continue\n\n        guessed.add(guess)\n        if guess not in word:\n            wrong += 1\n            print("Wrong guess!")\n\n        if all(letter in guessed for letter in word):\n            print("\\nYou won! The word was:", word)\n            return\n\n    print("\\nYou lost. The word was:", word)\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "03_hangman.py"


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
    print(f"Created {output_path} from 03_hangman.py.")


if __name__ == "__main__":
    main()
