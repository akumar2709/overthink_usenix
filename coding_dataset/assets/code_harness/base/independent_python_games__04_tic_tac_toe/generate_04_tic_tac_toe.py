#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'def show(board):\n    print()\n    for row in range(3):\n        print(" | ".join(board[row * 3:(row + 1) * 3]))\n        if row < 2:\n            print("--+---+--")\n    print()\n\ndef has_won(board, player):\n    lines = [\n        (0,1,2), (3,4,5), (6,7,8),\n        (0,3,6), (1,4,7), (2,5,8),\n        (0,4,8), (2,4,6)\n    ]\n    return any(all(board[i] == player for i in line) for line in lines)\n\ndef main():\n    print("=== Tic-Tac-Toe ===")\n    board = [str(i) for i in range(1, 10)]\n    player = "X"\n\n    for _ in range(9):\n        show(board)\n        try:\n            choice = int(input(f"Player {player}, choose a square (1-9): ")) - 1\n        except ValueError:\n            print("Enter a number from 1 to 9.")\n            continue\n\n        if choice not in range(9) or board[choice] in ("X", "O"):\n            print("That square is unavailable.")\n            continue\n\n        board[choice] = player\n        if has_won(board, player):\n            show(board)\n            print(f"Player {player} wins!")\n            return\n\n        player = "O" if player == "X" else "X"\n\n    show(board)\n    print("It is a draw!")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "04_tic_tac_toe.py"


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
    print(f"Created {output_path} from 04_tic_tac_toe.py.")


if __name__ == "__main__":
    main()
