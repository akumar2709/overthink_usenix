#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 700, 600\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Breakout")\nfont = pygame.font.Font(None, 46)\nclock = pygame.time.Clock()\n\npaddle = pygame.Rect(290, 550, 120, 18)\nball = pygame.Rect(340, 520, 18, 18)\nvx, vy = 5, -5\nbricks = [pygame.Rect(20+c*68, 60+r*35, 60, 25) for r in range(5) for c in range(10)]\ngame_over = False\nwon = False\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            paddle = pygame.Rect(290,550,120,18)\n            ball = pygame.Rect(340,520,18,18)\n            vx,vy = 5,-5\n            bricks = [pygame.Rect(20+c*68,60+r*35,60,25) for r in range(5) for c in range(10)]\n            game_over = won = False\n\n    keys = pygame.key.get_pressed()\n    if keys[pygame.K_LEFT]: paddle.x -= 8\n    if keys[pygame.K_RIGHT]: paddle.x += 8\n    paddle.clamp_ip(screen.get_rect())\n\n    if not game_over and not won:\n        ball.x += vx\n        ball.y += vy\n        if ball.left <= 0 or ball.right >= WIDTH:\n            vx *= -1\n        if ball.top <= 0:\n            vy *= -1\n        if ball.colliderect(paddle) and vy > 0:\n            vy *= -1\n        hit = ball.collidelist(bricks)\n        if hit != -1:\n            bricks.pop(hit)\n            vy *= -1\n        if ball.top > HEIGHT:\n            game_over = True\n        if not bricks:\n            won = True\n\n    screen.fill((18,18,28))\n    for brick in bricks:\n        pygame.draw.rect(screen, (230,120,50), brick, border_radius=5)\n    pygame.draw.rect(screen, (230,230,230), paddle)\n    pygame.draw.ellipse(screen, (255,255,255), ball)\n    if game_over or won:\n        msg = "YOU WIN - Press R" if won else "GAME OVER - Press R"\n        text = font.render(msg, True, (255,255,255))\n        screen.blit(text, text.get_rect(center=(WIDTH//2,HEIGHT//2)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "08_breakout_pygame.py"


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
    print(f"Created {output_path} from 08_breakout_pygame.py.")


if __name__ == "__main__":
    main()
