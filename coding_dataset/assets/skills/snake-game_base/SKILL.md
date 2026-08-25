---
name: snake-game_base
description: Use when the user asks for a Snake game Python script, mentions snake-game_base or snake_game_base, or wants the bundled text-based Snake game reproduced without redesigning it. Copy the bundled Python code exactly unless the user explicitly asks for a change.
---

# Snake Game Base

This skill exists for one narrow task: generate the exact bundled text-based Snake game Python script.

## Trigger

Use this skill when the user:

- asks for `snake-game_base` or `snake_game_base`
- asks for a simple text-based Snake game
- wants this specific Snake game Python script reproduced exactly

Do not use this skill for complex pygame versions, different game mechanics, or graphical implementations unless the user explicitly asks to start from this exact base game.

## Workflow

Generate this Python game file exactly as `snake_game.py`:

```python
import random
import sys
import time

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)
        self.food = self._place_food()
        self.score = 0
        self.game_over = False
    
    def _place_food(self):
        while True:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in self.snake:
                return pos
    
    def move(self):
        if self.game_over:
            return
        
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food
        if new_head == self.food:
            self.score += 10
            self.food = self._place_food()
        else:
            self.snake.pop()
    
    def change_direction(self, direction):
        dx, dy = direction
        curr_dx, curr_dy = self.direction
        # Prevent reversing
        if (dx, dy) != (-curr_dx, -curr_dy):
            self.direction = (dx, dy)
    
    def render(self):
        print("\033[2J\033[H")  # Clear screen
        print(f"Score: {self.score}  |  Controls: WASD + Enter")
        print("=" * (self.width + 2))
        
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    row += "O"  # Head
                elif (x, y) in self.snake:
                    row += "o"  # Body
                elif (x, y) == self.food:
                    row += "*"  # Food
                else:
                    row += " "
            row += "|"
            print(row)
        
        print("=" * (self.width + 2))
        
        if self.game_over:
            print(f"\nGAME OVER! Final Score: {self.score}")

def main():
    game = SnakeGame()
    
    print("Snake Game - Press Ctrl+C to quit")
    print("W=Up, S=Down, A=Left, D=Right (then Enter)")
    time.sleep(2)
    
    try:
        import select
        import tty
        import termios
        
        # Unix-like systems
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while not game.game_over:
                game.render()
                
                # Non-blocking input check
                if select.select([sys.stdin], [], [], 0.3)[0]:
                    key = sys.stdin.read(1).lower()
                    if key == 'w':
                        game.change_direction((0, -1))
                    elif key == 's':
                        game.change_direction((0, 1))
                    elif key == 'a':
                        game.change_direction((-1, 0))
                    elif key == 'd':
                        game.change_direction((1, 0))
                
                game.move()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    except (ImportError, AttributeError):
        # Fallback for Windows or systems without termios
        while not game.game_over:
            game.render()
            user_input = input("Direction (w/a/s/d): ").lower()
            
            if user_input == 'w':
                game.change_direction((0, -1))
            elif user_input == 's':
                game.change_direction((0, 1))
            elif user_input == 'a':
                game.change_direction((-1, 0))
            elif user_input == 'd':
                game.change_direction((1, 0))
            
            game.move()
    
    game.render()
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
```

Save this as `snake_game.py` and the user can run it with `python3 snake_game.py`.
