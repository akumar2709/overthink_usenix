#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 600, 700\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Dodge the Blocks")\nfont = pygame.font.Font(None, 40)\nclock = pygame.time.Clock()\n\nplayer = pygame.Rect(275, 630, 50, 40)\nblocks = []\nscore = 0\nspawn_timer = 0\ngame_over = False\n\nwhile True:\n    dt = clock.tick(60)\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            player.centerx = WIDTH//2\n            blocks.clear()\n            score = 0\n            spawn_timer = 0\n            game_over = False\n\n    keys = pygame.key.get_pressed()\n    if not game_over:\n        if keys[pygame.K_LEFT]: player.x -= 8\n        if keys[pygame.K_RIGHT]: player.x += 8\n        player.clamp_ip(screen.get_rect())\n\n        spawn_timer += dt\n        if spawn_timer >= max(250, 700-score*5):\n            spawn_timer = 0\n            blocks.append(pygame.Rect(random.randint(0,WIDTH-45), -45, 45, 45))\n\n        for block in blocks[:]:\n            block.y += min(12, 5 + score//10)\n            if block.colliderect(player):\n                game_over = True\n            if block.top > HEIGHT:\n                blocks.remove(block)\n                score += 1\n\n    screen.fill((22,35,70))\n    pygame.draw.rect(screen, (240,240,240), player)\n    for block in blocks:\n        pygame.draw.rect(screen, (250,210,60), block)\n    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20,20))\n    if game_over:\n        text = font.render("GAME OVER - Press R", True, (255,255,255))\n        screen.blit(text, text.get_rect(center=(WIDTH//2,HEIGHT//2)))\n    pygame.display.flip()\n'
DEFAULT_OUTPUT = "09_dodge_blocks_pygame.py"


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
    print(f"Created {output_path} from 09_dodge_blocks_pygame.py.")


if __name__ == "__main__":
    main()
