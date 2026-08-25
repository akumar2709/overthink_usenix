#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_CODE = 'import pygame\nimport random\nimport sys\n\npygame.init()\n\nWIDTH, HEIGHT = 600, 400\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption("Guess the Number")\nfont = pygame.font.Font(None, 42)\nsmall = pygame.font.Font(None, 30)\nclock = pygame.time.Clock()\n\nsecret = random.randint(1, 100)\ntext = ""\nmessage = "Type a number from 1 to 100"\nattempts = 0\n\nwhile True:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            pygame.quit()\n            sys.exit()\n        if event.type == pygame.KEYDOWN:\n            if event.key == pygame.K_BACKSPACE:\n                text = text[:-1]\n            elif event.key == pygame.K_RETURN:\n                try:\n                    guess = int(text)\n                    attempts += 1\n                    if guess < secret:\n                        message = "Too low!"\n                    elif guess > secret:\n                        message = "Too high!"\n                    else:\n                        message = f"Correct in {attempts} tries! New number created."\n                        secret = random.randint(1, 100)\n                        attempts = 0\n                    text = ""\n                except ValueError:\n                    message = "Enter a valid number."\n                    text = ""\n            elif event.unicode.isdigit() and len(text) < 3:\n                text += event.unicode\n\n    screen.fill((25, 30, 45))\n    title = font.render("Guess the Number", True, (255, 255, 255))\n    prompt = small.render(message, True, (220, 220, 220))\n    entry = font.render(text or "_", True, (80, 220, 160))\n    screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))\n    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 180)))\n    screen.blit(entry, entry.get_rect(center=(WIDTH // 2, 250)))\n    pygame.display.flip()\n    clock.tick(60)\n'
DEFAULT_OUTPUT = "01_guess_number_pygame.py"


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
    print(f"Created {output_path} from 01_guess_number_pygame.py.")


if __name__ == "__main__":
    main()
