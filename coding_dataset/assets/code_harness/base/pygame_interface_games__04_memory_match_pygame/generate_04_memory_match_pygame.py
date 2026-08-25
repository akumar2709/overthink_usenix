#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 640, 720\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Memory Match")\nfont = pygame.font.Font(None, 54)\nsmall = pygame.font.Font(None, 30)\nclock = pygame.time.Clock()\n\nvalues = list("AABBCCDDEEFFGGHH")\nrandom.shuffle(values)\ncards = [pygame.Rect(35 + (i%4)*150, 60 + (i//4)*150, 120, 120) for i in range(16)]\nrevealed = set()\nmatched = set()\nfirst = None\nhide_at = 0\n\nwhile True:\n    now = pygame.time.get_ticks()\n    if hide_at and now >= hide_at:\n        revealed.clear()\n        first = None\n        hide_at = 0\n\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            values = list("AABBCCDDEEFFGGHH")\n            random.shuffle(values)\n            revealed.clear()\n            matched.clear()\n            first = None\n            hide_at = 0\n        if event.type == pygame.MOUSEBUTTONDOWN and not hide_at:\n            for i, card in enumerate(cards):\n                if card.collidepoint(event.pos) and i not in matched and i not in revealed:\n                    revealed.add(i)\n                    if first is None:\n                        first = i\n                    else:\n                        if values[first] == values[i]:\n                            matched.update((first, i))\n                            revealed.clear()\n                            first = None\n                        else:\n                            hide_at = now + 700\n                    break\n\n    screen.fill((28, 32, 46))\n    for i, card in enumerate(cards):\n        open_card = i in revealed or i in matched\n        pygame.draw.rect(screen, (70,150,210) if open_card else (70,75,100), card, border_radius=12)\n        pygame.draw.rect(screen, (230,230,230), card, 3, border_radius=12)\n        label = values[i] if open_card else "?"\n        text = font.render(label, True, (255,255,255))\n        screen.blit(text, text.get_rect(center=card.center))\n    msg = "You won! Press R." if len(matched) == 16 else f"Pairs: {len(matched)//2}/8"\n    screen.blit(small.render(msg, True, (255,255,255)), (20, 675))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "04_memory_match_pygame.py"


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
    print(f"Created {output_path} from 04_memory_match_pygame.py.")


if __name__ == "__main__":
    main()
