#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 700, 420\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Rock Paper Scissors")\nfont = pygame.font.Font(None, 44)\nsmall = pygame.font.Font(None, 30)\nclock = pygame.time.Clock()\n\nchoices = ["Rock", "Paper", "Scissors"]\nbuttons = [pygame.Rect(80 + i * 200, 250, 160, 70) for i in range(3)]\nmessage = "Choose your move"\nplayer_score = 0\ncomputer_score = 0\n\nwhile True:\n    mouse = pygame.mouse.get_pos()\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:\n            for i, button in enumerate(buttons):\n                if button.collidepoint(event.pos):\n                    player = choices[i]\n                    computer = random.choice(choices)\n                    wins = {("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Paper")}\n                    if player == computer:\n                        result = "Tie"\n                    elif (player, computer) in wins:\n                        player_score += 1\n                        result = "You win"\n                    else:\n                        computer_score += 1\n                        result = "Computer wins"\n                    message = f"You: {player} | Computer: {computer} | {result}"\n\n    screen.fill((32, 35, 48))\n    screen.blit(font.render("Rock Paper Scissors", True, (255,255,255)), (165, 55))\n    screen.blit(small.render(message, True, (230,230,230)), (50, 150))\n    score = small.render(f"Score: You {player_score} - {computer_score} Computer", True, (120,220,180))\n    screen.blit(score, (200, 195))\n    for i, button in enumerate(buttons):\n        color = (90, 130, 220) if button.collidepoint(mouse) else (65, 90, 160)\n        pygame.draw.rect(screen, color, button, border_radius=12)\n        label = small.render(choices[i], True, (255,255,255))\n        screen.blit(label, label.get_rect(center=button.center))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "02_rock_paper_scissors_pygame.py"


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
    print(f"Created {output_path} from 02_rock_paper_scissors_pygame.py.")


if __name__ == "__main__":
    main()
