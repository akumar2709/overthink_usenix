#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\ndef roll():\n    return random.randint(1, 6)\n\ndef main():\n    print("=== Dice Battle ===")\n    player_hp = 20\n    enemy_hp = 20\n\n    while player_hp > 0 and enemy_hp > 0:\n        input("\\nPress Enter to roll the dice...")\n        player_roll = roll()\n        enemy_roll = roll()\n\n        print(f"You rolled {player_roll}. Enemy rolled {enemy_roll}.")\n\n        if player_roll > enemy_roll:\n            damage = player_roll - enemy_roll\n            enemy_hp -= damage\n            print(f"You deal {damage} damage!")\n        elif enemy_roll > player_roll:\n            damage = enemy_roll - player_roll\n            player_hp -= damage\n            print(f"Enemy deals {damage} damage!")\n        else:\n            print("No damage this round.")\n\n        print(f"Your HP: {max(player_hp, 0)} | Enemy HP: {max(enemy_hp, 0)}")\n\n    print("\\nYou won!" if player_hp > 0 else "\\nThe enemy won.")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "08_dice_battle.py"


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
    print(f"Created {output_path} from 08_dice_battle.py.")


if __name__ == "__main__":
    main()
