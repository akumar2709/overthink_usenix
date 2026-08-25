#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\nimport os\n\nWIDTH = 10\nHEIGHT = 10\n\ndef clear_screen():\n    os.system("cls" if os.name == "nt" else "clear")\n\ndef draw(snake, food):\n    clear_screen()\n    for y in range(HEIGHT):\n        row = []\n        for x in range(WIDTH):\n            pos = (x, y)\n            if pos == snake[0]:\n                row.append("@")\n            elif pos in snake:\n                row.append("o")\n            elif pos == food:\n                row.append("*")\n            else:\n                row.append(".")\n        print(" ".join(row))\n\ndef new_food(snake):\n    spaces = [\n        (x, y)\n        for y in range(HEIGHT)\n        for x in range(WIDTH)\n        if (x, y) not in snake\n    ]\n    return random.choice(spaces) if spaces else None\n\ndef main():\n    print("=== Snake Lite ===")\n    print("Use W A S D, then press Enter after each move.")\n    snake = [(4, 4), (3, 4), (2, 4)]\n    direction = (1, 0)\n    food = new_food(snake)\n\n    while food is not None:\n        draw(snake, food)\n        print(f"Score: {len(snake) - 3}")\n        move = input("Move: ").strip().lower()\n\n        directions = {\n            "w": (0, -1),\n            "s": (0, 1),\n            "a": (-1, 0),\n            "d": (1, 0),\n        }\n\n        if move in directions:\n            candidate = directions[move]\n            if candidate != (-direction[0], -direction[1]):\n                direction = candidate\n\n        head_x, head_y = snake[0]\n        new_head = (head_x + direction[0], head_y + direction[1])\n\n        if (\n            new_head[0] < 0 or new_head[0] >= WIDTH or\n            new_head[1] < 0 or new_head[1] >= HEIGHT or\n            new_head in snake[:-1]\n        ):\n            draw(snake, food)\n            print("Game over!")\n            return\n\n        snake.insert(0, new_head)\n\n        if new_head == food:\n            food = new_food(snake)\n        else:\n            snake.pop()\n\n    print("You filled the board. You win!")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "10_snake_lite.py"


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
    print(f"Created {output_path} from 10_snake_lite.py.")


if __name__ == "__main__":
    main()
