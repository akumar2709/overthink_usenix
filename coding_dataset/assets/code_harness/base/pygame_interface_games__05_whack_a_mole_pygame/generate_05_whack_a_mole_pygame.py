#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 650, 650\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Whack-a-Mole")\nfont = pygame.font.Font(None, 38)\nclock = pygame.time.Clock()\n\nholes = [pygame.Rect(70+(i%3)*190, 120+(i//3)*160, 130, 100) for i in range(9)]\nactive = random.randrange(9)\nscore = 0\nstart = pygame.time.get_ticks()\nnext_move = start + 600\nduration = 20000\nfinished = False\n\nwhile True:\n    now = pygame.time.get_ticks()\n    if not finished and now >= next_move:\n        active = random.randrange(9)\n        next_move = now + 600\n    if not finished and now - start >= duration:\n        finished = True\n\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            score = 0\n            start = pygame.time.get_ticks()\n            next_move = start + 600\n            active = random.randrange(9)\n            finished = False\n        if event.type == pygame.MOUSEBUTTONDOWN and not finished:\n            if holes[active].collidepoint(event.pos):\n                score += 1\n                active = random.randrange(9)\n                next_move = now + 600\n\n    screen.fill((35, 110, 60))\n    remaining = max(0, (duration - (now-start)) // 1000)\n    title = f"Score: {score}   Time: {remaining}"\n    if finished:\n        title = f"Game over! Score: {score}. Press R."\n    screen.blit(font.render(title, True, (255,255,255)), (120, 35))\n    for i, hole in enumerate(holes):\n        pygame.draw.ellipse(screen, (45,30,20), hole)\n        if i == active and not finished:\n            mole = hole.inflate(-35, -10)\n            pygame.draw.ellipse(screen, (150,90,50), mole)\n            pygame.draw.circle(screen, (0,0,0), (mole.centerx-18,mole.centery-10), 5)\n            pygame.draw.circle(screen, (0,0,0), (mole.centerx+18,mole.centery-10), 5)\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "05_whack_a_mole_pygame.py"


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
    print(f"Created {output_path} from 05_whack_a_mole_pygame.py.")


if __name__ == "__main__":
    main()
