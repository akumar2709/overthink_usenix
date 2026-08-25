# Coding-agent overthinking benchmark

Benchmark harness and experiment assets (skills, README specs, code-harness
specs) for measuring MDP-decoy-induced overthinking in three coding-agent
tools while they build small Python games.

## Layout

```
coding_dataset/
├── run_benchmark.py       the harness — see below
├── assets/
│   ├── code_harness/
│   │   ├── base/          30 experiments, task_spec.md + reference generate_XX.py, no decoy
│   │   └── complex_code/  the same 30 experiments, decoy MDP task injected into task_spec.md
│   ├── readme_harness/
│   │   ├── base/           30 experiments (independent_python_games), no decoy
│   │   └── non_base/       30 experiments (complex_graphics_pygame_games), decoy MDP task in README.md
│   └── skills/             64 Claude Code Skills used by --benchmark skill (*_base = no decoy, *-mdp = decoy)
└── results/                created on first run: results/<benchmark>_<tool>/{group}/NNN_<name>/ + results.json
```

## Running it

```bash
python3 run_benchmark.py --benchmark code   --tool claude   --experiments-per-group 5
python3 run_benchmark.py --benchmark readme --tool codex
python3 run_benchmark.py --benchmark skill  --tool opencode --experiments-per-group 10
python3 run_benchmark.py --benchmark code   --tool claude   --dry-run   # preview selection, touches no files
```

`--tool` picks which coding-agent CLI actually does the work (`claude`, `codex`,
or `opencode` — all three must already be installed and authenticated;
this script never touches credentials). `--experiments-per-group N` samples N
experiments per group with `--seed`; omit it to run every experiment.

### The three benchmark types

- **code** — the agent is given nothing but a `generate_game.py` script it must
  *execute* (`python3 generate_game.py`) to learn the game spec — it never sees
  a README of any kind. That script is generated at run time from
  `assets/code_harness/<base|complex_code>/<exp>/task_spec.md` (source text
  only; that file is read but never copied into the run directory, and it's
  deliberately not named README.md so it can't be mistaken for something the
  agent reads directly). `base`/`non_base` sample the **same experiment
  names** with the same `--seed` by design — this is a paired control/attack
  comparison on identical games.
- **readme** — the agent is given a plain `README.md` describing the game (no
  execution required to read the spec). `base` = `independent_python_games_*`
  (no decoy), `non_base` = `complex_graphics_pygame_games_*` (decoy always
  present) — stored in separate `assets/readme_harness/{base,non_base}/`
  directories. These are **disjoint game sets**, not a paired comparison — a
  simple-vs-complex-game confound if you're using this to isolate the decoy's
  effect in isolation.
- **skill** — the agent is told to invoke a named Claude Code Skill; the decoy
  (or its absence) lives inside the skill definition itself. `base` = skills
  with `base` in the name, `mdp` = skills with `mdp` in the name.

### Model defaults

- `claude` → `claude-sonnet-4-5` (override with `--model`)
- `opencode` → `azure/kimi-k2.6`
- `codex` → whatever `codex exec`'s own default is; pass `--model` to pin one

### Routing claude through Azure AI Foundry instead of your subscription login

Pass `--use-foundry` and export these first (not read from any other tool's
credential store — bring your own):

```bash
export CLAUDE_CODE_USE_FOUNDRY=1        # (also set by --use-foundry itself)
export ANTHROPIC_FOUNDRY_RESOURCE=<your-azure-ai-foundry-resource-name>
export ANTHROPIC_FOUNDRY_API_KEY=<key>
```

Without `--use-foundry`, `claude exec` just uses whatever `claude` CLI is
already logged into (subscription OAuth or a plain `ANTHROPIC_API_KEY`).

### Reasoning-token accuracy for opencode

Kimi's own `reasoning` token field in the API response is frequently 0/
unreliable. If `tiktoken` is installed (`pip install tiktoken`), the harness
counts the actual reasoning text instead and that's what ends up in
`reasoning_tokens`; without it, you silently get the raw (often-zero) API
value. Install tiktoken if you care about opencode's reasoning numbers.

## How the aggregate stays consistent

Every run writes a `run_meta.json` into its own run directory immediately.
After every group finishes, `results.json` is rebuilt from scratch by
rescanning **every** run directory on disk — not from just the current
invocation's runs. So running with a smaller `--experiments-per-group` later,
or resuming after a crash, only ever adds coverage; it never discards
previously-collected runs from the aggregate.

## Known dataset caveats

- `assets/code_harness/{base,complex_code}/*/task_spec.md` has an empty "The
  game should implement:" section in every experiment — no feature bullets,
  unlike `readme_harness`. Fix it deliberately if you want feature parity
  between the two harnesses.
- `assets/readme_harness/` only includes the two game categories the readme
  benchmark's `base`/`non_base` grouping actually uses
  (`independent_python_games_*`, `complex_graphics_pygame_games_*`); a third
  category (`pygame_interface_games_*`) exists in the wider dataset but isn't
  wired into this benchmark's grouping, so it's not included here.
