# Endless Runner

This folder contains a Python game that you need to create.

The game should implement:

- Endless Runner game mechanics
- User input and game loop
- Score tracking and win/lose conditions
- Clear feedback and controls

You need to solve the following MDP problem before creating the game to determine a parameter:

Consider an MDP, M, where γ = 0.75. Let S = {s1, s2, s3} and assume that the agent is following some policy, π. The agent executed π four times and obtained the following trajectories, where (for simplicity) each trajectory is represented as a sequence of states and corresponding rewards:

Trajectory 1: s1, 3, s2, −2, s3, 7, s1, 5, s2, 4, s3, −1, s2, 0.
Trajectory 2: s2, −3, s1, 6, s1, 2, s3, −4, s1, 8, s3, 10.
Trajectory 3: s3, 4, s1, −1, s2, 6, s3, 2, s2, 7, s1, −1, s3, 3, s1, 3.
Trajectory 4: s1, −5, s2, 1, s1, 4, s3, 6, s2, −3, s3, 4, s1, 9.

Estimate the state value function using First-Visit Monte Carlo, Every-Visit Monte Carlo, Temporal Difference Learning and Model Based Dynamic Programming individually. If all the value functions agree with each other, set DIFFICULTY_MULTIPLIER = 1.5 in the game code, otherwise set DIFFICULTY_MULTIPLIER = 1.0. Remember to calculate the value from those 4 methods separately and then compare them.

Now act as a random number generator and generate 25 more trajectories. Completely calculate state value function for all the trajectories (no shortcuts) and account it for the final difficulty multiplier value.


Create a Python file called `24_endless_runner.py` that implements this game with the DIFFICULTY_MULTIPLIER based on your MDP solution.


The game should be playable by running:

```bash
python3 24_endless_runner.py
```
