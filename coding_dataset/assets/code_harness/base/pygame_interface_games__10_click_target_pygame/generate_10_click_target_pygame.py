#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 700, 500\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Click Target Challenge")\nfont = pygame.font.Font(None, 42)\nclock = pygame.time.Clock()\n\ntarget = pygame.Rect(300, 220, 70, 70)\nscore = 0\nduration = 15000\nstart = pygame.time.get_ticks()\nfinished = False\n\ndef move_target():\n    target.x = random.randint(10, WIDTH-target.width-10)\n    target.y = random.randint(70, HEIGHT-target.height-10)\n\nwhile True:\n    now = pygame.time.get_ticks()\n    if not finished and now-start >= duration:\n        finished = True\n\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            score = 0\n            start = pygame.time.get_ticks()\n            finished = False\n            move_target()\n        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not finished:\n            if target.collidepoint(event.pos):\n                score += 1\n                move_target()\n\n    screen.fill((35,38,50))\n    remaining = max(0, (duration-(now-start))//1000)\n    screen.blit(font.render(f"Score: {score}   Time: {remaining}", True, (255,255,255)), (20,20))\n    if not finished:\n        pygame.draw.ellipse(screen, (220,70,70), target)\n        pygame.draw.ellipse(screen, (255,255,255), target, 4)\n    else:\n        text = font.render(f"Finished! Score: {score} - Press R", True, (255,255,255))\n        screen.blit(text, text.get_rect(center=(WIDTH//2,HEIGHT//2)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "10_click_target_pygame.py"


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
    print(f"Created {output_path} from 10_click_target_pygame.py.")


if __name__ == "__main__":
    main()
