#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 800, 500\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Pong")\nfont = pygame.font.Font(None, 50)\nclock = pygame.time.Clock()\n\nleft = pygame.Rect(30, 190, 18, 120)\nright = pygame.Rect(WIDTH-48, 190, 18, 120)\nball = pygame.Rect(WIDTH//2-10, HEIGHT//2-10, 20, 20)\nvx, vy = 6, 5\nleft_score = right_score = 0\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n\n    keys = pygame.key.get_pressed()\n    if keys[pygame.K_w]: left.y -= 7\n    if keys[pygame.K_s]: left.y += 7\n    if keys[pygame.K_UP]: right.y -= 7\n    if keys[pygame.K_DOWN]: right.y += 7\n    left.clamp_ip(screen.get_rect())\n    right.clamp_ip(screen.get_rect())\n\n    ball.x += vx\n    ball.y += vy\n    if ball.top <= 0 or ball.bottom >= HEIGHT:\n        vy *= -1\n    if ball.colliderect(left) and vx < 0:\n        vx *= -1\n    if ball.colliderect(right) and vx > 0:\n        vx *= -1\n    if ball.right < 0:\n        right_score += 1\n        ball.center = (WIDTH//2, HEIGHT//2)\n        vx = 6\n    if ball.left > WIDTH:\n        left_score += 1\n        ball.center = (WIDTH//2, HEIGHT//2)\n        vx = -6\n\n    screen.fill((15,15,20))\n    pygame.draw.line(screen, (100,100,110), (WIDTH//2,0), (WIDTH//2,HEIGHT), 3)\n    pygame.draw.rect(screen, (255,255,255), left)\n    pygame.draw.rect(screen, (255,255,255), right)\n    pygame.draw.ellipse(screen, (255,255,255), ball)\n    score = font.render(f"{left_score}       {right_score}", True, (255,255,255))\n    screen.blit(score, score.get_rect(center=(WIDTH//2,50)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "07_pong_pygame.py"


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
    print(f"Created {output_path} from 07_pong_pygame.py.")


if __name__ == "__main__":
    main()
