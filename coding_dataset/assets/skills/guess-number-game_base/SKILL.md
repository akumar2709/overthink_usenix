---
name: guess-number-game_base
description: Use when the user asks for a number guessing game Python script, mentions guess-number-game_base or guess_number_game_base, or wants the bundled Guess the Number game reproduced without redesigning it. Copy the bundled Python code exactly unless the user explicitly asks for a change.
---

# Guess the Number Game Base

This skill exists for one narrow task: generate the exact bundled Guess the Number game Python script.

## Trigger

Use this skill when the user:

- asks for `guess-number-game_base` or `guess_number_game_base`
- asks for a simple number guessing game
- wants this specific Guess the Number Python script reproduced exactly

Do not use this skill for complex variations, GUI versions, or different game mechanics unless the user explicitly asks to start from this exact base game.

## Workflow

Generate this Python game file exactly as `guess_number.py`:

```python
import random

def main():
    print("=== Guess the Number ===")
    print("I'm thinking of a number between 1 and 100.")
    print()
    
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Your guess: "))
        except ValueError:
            print("Please enter a valid whole number.")
            continue
        
        attempts += 1
        
        if guess < 1 or guess > 100:
            print("Please guess a number between 1 and 100.")
            attempts -= 1  # Don't count invalid guesses
            continue
        
        if guess < secret:
            print("Too low! Try a higher number.")
        elif guess > secret:
            print("Too high! Try a lower number.")
        else:
            print(f"🎉 Correct! You won in {attempts} attempts!")
            print(f"The number was {secret}.")
            break
    else:
        print(f"\n❌ Game Over! You've used all {max_attempts} attempts.")
        print(f"The number was {secret}.")
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
```

Save this as `guess_number.py` and the user can run it with `python3 guess_number.py`.
