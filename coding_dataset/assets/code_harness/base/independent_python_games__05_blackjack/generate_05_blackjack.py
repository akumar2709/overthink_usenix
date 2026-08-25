#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import random\n\ndef draw_card():\n    return random.randint(1, 13)\n\ndef card_name(card):\n    names = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}\n    return names.get(card, str(card))\n\ndef hand_value(hand):\n    value = sum(min(card, 10) for card in hand)\n    aces = hand.count(1)\n    while aces and value + 10 <= 21:\n        value += 10\n        aces -= 1\n    return value\n\ndef main():\n    print("=== Simple Blackjack ===")\n    player = [draw_card(), draw_card()]\n    dealer = [draw_card(), draw_card()]\n\n    while True:\n        print("\\nYour hand:", ", ".join(card_name(c) for c in player))\n        print("Your total:", hand_value(player))\n        print("Dealer shows:", card_name(dealer[0]))\n\n        if hand_value(player) > 21:\n            print("Bust! Dealer wins.")\n            return\n\n        action = input("Hit or stand? ").strip().lower()\n        if action == "hit":\n            player.append(draw_card())\n        elif action == "stand":\n            break\n        else:\n            print("Type hit or stand.")\n\n    while hand_value(dealer) < 17:\n        dealer.append(draw_card())\n\n    pv = hand_value(player)\n    dv = hand_value(dealer)\n    print("\\nDealer hand:", ", ".join(card_name(c) for c in dealer))\n    print("Dealer total:", dv)\n\n    if dv > 21 or pv > dv:\n        print("You win!")\n    elif pv < dv:\n        print("Dealer wins.")\n    else:\n        print("Push: it is a tie.")\n\nif __name__ == "__main__":\n    main()\n'
DEFAULT_OUTPUT = "05_blackjack.py"


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
    print(f"Created {output_path} from 05_blackjack.py.")


if __name__ == "__main__":
    main()
