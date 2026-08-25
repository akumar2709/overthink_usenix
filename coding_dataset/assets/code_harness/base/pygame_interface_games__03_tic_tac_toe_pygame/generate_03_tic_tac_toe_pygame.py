#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nSIZE = 600\nscreen = pygame.display.set_mode((SIZE, SIZE + 80))\npygame.display.set_caption("Tic-Tac-Toe")\nfont = pygame.font.Font(None, 90)\nsmall = pygame.font.Font(None, 34)\nclock = pygame.time.Clock()\n\nboard = [""] * 9\nplayer = "X"\nmessage = "Player X\'s turn"\ngame_over = False\n\ndef winner(mark):\n    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]\n    return any(all(board[i] == mark for i in line) for line in lines)\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:\n            board = [""] * 9\n            player = "X"\n            message = "Player X\'s turn"\n            game_over = False\n        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:\n            x, y = event.pos\n            if y < SIZE:\n                col, row = x // 200, y // 200\n                idx = row * 3 + col\n                if board[idx] == "":\n                    board[idx] = player\n                    if winner(player):\n                        message = f"Player {player} wins! Press R."\n                        game_over = True\n                    elif all(board):\n                        message = "Draw! Press R."\n                        game_over = True\n                    else:\n                        player = "O" if player == "X" else "X"\n                        message = f"Player {player}\'s turn"\n\n    screen.fill((25, 28, 40))\n    for i in range(1, 3):\n        pygame.draw.line(screen, (220,220,220), (i*200,0), (i*200,SIZE), 5)\n        pygame.draw.line(screen, (220,220,220), (0,i*200), (SIZE,i*200), 5)\n    for i, mark in enumerate(board):\n        if mark:\n            row, col = divmod(i, 3)\n            text = font.render(mark, True, (90,220,170) if mark == "X" else (240,120,120))\n            screen.blit(text, text.get_rect(center=(col*200+100,row*200+100)))\n    status = small.render(message, True, (255,255,255))\n    screen.blit(status, status.get_rect(center=(SIZE//2, SIZE+40)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "03_tic_tac_toe_pygame.py"


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
    print(f"Created {output_path} from 03_tic_tac_toe_pygame.py.")


if __name__ == "__main__":
    main()
