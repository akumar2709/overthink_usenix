#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nCELL = 25\nCOLS, ROWS = 24, 20\nWIDTH, HEIGHT = COLS*CELL, ROWS*CELL\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Snake")\nfont = pygame.font.Font(None, 40)\nclock = pygame.time.Clock()\n\nsnake = [(10,10),(9,10),(8,10)]\ndirection = (1,0)\nnext_direction = direction\nfood = (15,10)\ngame_over = False\nmove_event = pygame.USEREVENT + 1\npygame.time.set_timer(move_event, 110)\n\ndef new_food():\n    spaces = [(x,y) for y in range(ROWS) for x in range(COLS) if (x,y) not in snake]\n    return random.choice(spaces)\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN:\n            keys = {\n                pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1),\n                pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)\n            }\n            if event.key in keys:\n                candidate = keys[event.key]\n                if candidate != (-direction[0], -direction[1]):\n                    next_direction = candidate\n            if event.key == pygame.K_r:\n                snake = [(10,10),(9,10),(8,10)]\n                direction = (1,0)\n                next_direction = direction\n                food = new_food()\n                game_over = False\n        if event.type == move_event and not game_over:\n            direction = next_direction\n            hx, hy = snake[0]\n            dx, dy = direction\n            head = (hx+dx, hy+dy)\n            body = snake if head == food else snake[:-1]\n            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in body:\n                game_over = True\n            else:\n                snake.insert(0, head)\n                if head == food:\n                    food = new_food()\n                else:\n                    snake.pop()\n\n    screen.fill((20,20,25))\n    pygame.draw.rect(screen, (220,60,60), (food[0]*CELL+3, food[1]*CELL+3, CELL-6, CELL-6), border_radius=8)\n    for i,(x,y) in enumerate(snake):\n        color = (70,230,100) if i == 0 else (35,150,70)\n        pygame.draw.rect(screen, color, (x*CELL+2,y*CELL+2,CELL-4,CELL-4), border_radius=5)\n    if game_over:\n        text = font.render("GAME OVER - Press R", True, (255,255,255))\n        screen.blit(text, text.get_rect(center=(WIDTH//2,HEIGHT//2)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "06_snake_pygame.py"


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
    print(f"Created {output_path} from 06_snake_pygame.py.")


if __name__ == "__main__":
    main()
