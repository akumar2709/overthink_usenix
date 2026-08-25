# overthink_usenix

Harnesses and experiment assets for the OVERTHINK MDP-decoy overthinking
experiments.

- **`coding_dataset/`** — code/readme/skill benchmarks against claude, codex,
  and opencode. See `coding_dataset/README.md`.
- **`image_dataset/`** — the GPT-5 → Claude Sonnet 5 / Kimi-K2.6 image
  overthinking pipeline. See `image_dataset/README.md`.

Each subfolder is self-contained: its own harness script, its own `assets/`,
its own `results/` on first run. Nothing outside a subfolder is required to
run what's inside it.
