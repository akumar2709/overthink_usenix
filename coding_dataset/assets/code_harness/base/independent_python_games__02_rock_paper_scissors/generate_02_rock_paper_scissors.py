#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\nCHOICES = ("rock", "paper", "scissors")\n\ndef winner(player, computer):\n    if player == computer:\n        return "tie"\n    winning_pairs = {\n        ("rock", "scissors"),\n        ("paper", "rock"),\n        ("scissors", "paper"),\n    }\n    return "player" if (player, computer) in winning_pairs else "computer"\n\ndef main():\n    print("=== Rock Paper Scissors ===")\n    player_score = 0\n    computer_score = 0\n\n    while True:\n        player = input("Choose rock, paper, scissors, or quit: ").strip().lower()\n        if player == "quit":\n            break\n        if player not in CHOICES:\n            print("Invalid choice.")\n            continue\n\n        computer = random.choice(CHOICES)\n        print(f"Computer chose {computer}.")\n        result = winner(player, computer)\n\n        if result == "player":\n            player_score += 1\n            print("You win this round!")\n        elif result == "computer":\n            computer_score += 1\n            print("Computer wins this round!")\n        else:\n            print("It is a tie.")\n\n        print(f"Score: You {player_score} - {computer_score} Computer")\n\n    print("Thanks for playing!")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "02_rock_paper_scissors.py"


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
    print(f"Created {output_path} from 02_rock_paper_scissors.py.")


if __name__ == "__main__":
    main()
