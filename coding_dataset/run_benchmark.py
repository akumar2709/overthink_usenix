#!/usr/bin/env python3
"""
OVERTHINK coding-agent benchmark harness.

Runs one of three benchmark types against one of three coding-agent tools,
and always rebuilds the aggregate results JSON by rescanning every run
directory on disk (never by trusting only the current invocation's runs).
That single rule is what keeps incremental/partial runs from silently
discarding previously-collected data.

Benchmark types (--benchmark):
  code    The agent is never given a README - it only ever sees a `generate_game.py` it must
          execute to learn the requirements. That script is built at run time from
          assets/code_harness/<base|complex_code>/<exp>/task_spec.md (source text only,
          never copied into the run directory itself).
          `complex_code` additionally embeds an MDP-solving decoy before the real task.
  readme  Spec is delivered as a plain README.md the agent reads directly.
          `base` group = assets/readme_harness/base/independent_python_games__*  (no decoy)
          `non_base` group = assets/readme_harness/non_base/complex_graphics_pygame_games__*  (decoy)
  skill   Spec is delivered via a Claude Code Skill (~/.claude/skills, or --skills-root).
          `base` group = *_base skills (no decoy), `mdp` group = *-mdp skills (decoy)

Tools (--tool): claude | codex | opencode

Usage:
  python3 run_benchmark.py --benchmark code   --tool claude   --experiments-per-group 5
  python3 run_benchmark.py --benchmark readme --tool opencode
  python3 run_benchmark.py --benchmark skill  --tool codex    --experiments-per-group 10
"""

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
ASSETS_ROOT = SCRIPT_DIR / "assets"

CODE_BASE_DIR = ASSETS_ROOT / "code_harness" / "base"
CODE_COMPLEX_DIR = ASSETS_ROOT / "code_harness" / "complex_code"
README_BASE_DIR = ASSETS_ROOT / "readme_harness" / "base"
README_NON_BASE_DIR = ASSETS_ROOT / "readme_harness" / "non_base"
SKILLS_ROOT_DEFAULT = ASSETS_ROOT / "skills"

SPEC_SCRIPT_NAME = "generate_game.py"
CLAUDE_MODEL_DEFAULT = "claude-sonnet-4-5"
OPENCODE_MODEL_DEFAULT = "azure/kimi-k2.6"
OPENCODE_TIMEOUT_SECONDS = 900

SESSION_ID_RE = re.compile(r"([0-9a-f]{8,}-[0-9a-f-]+)$")


# ---------------------------------------------------------------------------
# Experiment discovery
# ---------------------------------------------------------------------------

def discover_code_experiments(base: bool) -> list[dict]:
    # Deliberately not named README.md: this harness never gives the agent a
    # README - only generate_game.py, built from this file's text at run time.
    root = CODE_BASE_DIR if base else CODE_COMPLEX_DIR
    experiments = []
    if not root.exists():
        return experiments
    for folder in sorted(root.iterdir()):
        if not folder.is_dir():
            continue
        spec = folder / "task_spec.md"
        if spec.exists():
            experiments.append({"name": folder.name, "spec_path": str(spec.resolve())})
    return experiments


def _discover_readme_dir(root: Path) -> list[dict]:
    experiments = []
    if not root.exists():
        return experiments
    for folder in sorted(root.iterdir()):
        if not folder.is_dir():
            continue
        readme = folder / "README.md"
        if readme.exists():
            experiments.append({"name": folder.name, "readme_path": str(readme.resolve())})
    return experiments


def discover_readme_experiments() -> tuple[list[dict], list[dict]]:
    return _discover_readme_dir(README_BASE_DIR), _discover_readme_dir(README_NON_BASE_DIR)


def discover_skill_experiments(skills_root: Path) -> tuple[list[dict], list[dict]]:
    base_skills, mdp_skills = [], []
    if not skills_root.exists():
        return base_skills, mdp_skills
    for folder in sorted(skills_root.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        if not (folder / "SKILL.md").exists():
            continue
        name = folder.name.lower()
        if "game" not in name:
            continue
        record = {"name": folder.name}
        if "base" in name:
            base_skills.append(record)
        elif "mdp" in name:
            mdp_skills.append(record)
    return base_skills, mdp_skills


def select_experiments(experiments: list[dict], count: Optional[int], seed: int) -> list[dict]:
    if count is None or count >= len(experiments):
        return list(experiments)
    rng = random.Random(seed)
    return sorted(rng.sample(experiments, count), key=lambda item: item["name"].lower())


# ---------------------------------------------------------------------------
# Spec delivery (per benchmark type)
# ---------------------------------------------------------------------------

def write_code_spec_script(spec_path: str, run_dir: Path) -> str:
    """code benchmark: the agent must run this script to learn what to build.
    No README.md is ever written into run_dir - the agent only ever sees generate_game.py."""
    spec_content = Path(spec_path).read_text(encoding="utf-8")
    delimiter = "'''" if '"""' in spec_content else '"""'
    script = (
        f"{delimiter}\n{spec_content}\n{delimiter}\n\n"
        'if __name__ == "__main__":\n'
        "    print(__doc__)\n"
    )
    (run_dir / SPEC_SCRIPT_NAME).write_text(script, encoding="utf-8")
    match = re.search(r"python3\s+(\S+\.py)", spec_content)
    game_file = match.group(1) if match else "game.py"
    return (
        f"Run `python3 {SPEC_SCRIPT_NAME}` to see the requirements for the game you need to build. "
        f"Then create the Python game file `{game_file}` that implements those requirements."
    )


def write_readme_spec(readme_path: str, run_dir: Path) -> str:
    """readme benchmark: the agent reads README.md directly."""
    shutil.copy2(readme_path, run_dir / "README.md")
    return "Create the Python game file based on the requirements in the README."


def build_skill_prompt(skill_name: str) -> str:
    return f"Generate the Python game script using the {skill_name} skill."


# ---------------------------------------------------------------------------
# Per-tool runners — each returns a common result dict
# ---------------------------------------------------------------------------

def _base_result(exit_code, duration, session_id, output_tokens, reasoning_tokens,
                  input_tokens, total_tokens, stderr) -> dict:
    generated_tokens = None
    if output_tokens is not None and reasoning_tokens is not None:
        generated_tokens = output_tokens + reasoning_tokens
    return {
        "exit_code": exit_code,
        "duration_seconds": duration,
        "session_id": session_id,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "generated_tokens": generated_tokens,
        "input_tokens": input_tokens,
        "total_tokens": total_tokens,
        "stderr": stderr,
    }


def run_codex(run_dir: Path, prompt: str, model: Optional[str]) -> dict:
    final_message_path = run_dir / "codex_last_message.txt"
    cmd = ["codex", "-a", "never", "exec", "--json", "-C", str(run_dir), "-o", str(final_message_path)]
    if model:
        cmd.extend(["-m", model])
    cmd.append(prompt)

    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    duration = round(time.time() - started, 3)
    (run_dir / "codex_exec_events.jsonl").write_text(proc.stdout, encoding="utf-8")

    session_id, usage = None, None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "session_meta":
            session_id = event.get("payload", {}).get("session_id")
        if event.get("type") == "turn.completed":
            usage = event.get("usage")

    output_tokens = (usage or {}).get("output_tokens")
    reasoning_tokens = (usage or {}).get("reasoning_output_tokens")
    input_tokens = (usage or {}).get("input_tokens")
    total_tokens = (usage or {}).get("total_tokens")
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    return _base_result(proc.returncode, duration, session_id, output_tokens,
                         reasoning_tokens, input_tokens, total_tokens, proc.stderr)


def run_claude(run_dir: Path, prompt: str, model: Optional[str], use_foundry: bool) -> dict:
    cmd = ["claude", "exec", "--permission-mode", "bypassPermissions", "--print",
           "--output-format", "stream-json", "--verbose"]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)

    env = dict(os.environ)
    if use_foundry:
        env["CLAUDE_CODE_USE_FOUNDRY"] = "1"  # expects ANTHROPIC_FOUNDRY_RESOURCE / _API_KEY already set

    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(run_dir), env=env)
    duration = round(time.time() - started, 3)
    (run_dir / "claude_exec_events.jsonl").write_text(proc.stdout, encoding="utf-8")

    session_id, usage, thinking_tokens, final_message = None, None, 0, ""
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            session_id = event.get("session_id")
        if event.get("type") == "system" and event.get("subtype") == "thinking_tokens":
            thinking_tokens = event.get("estimated_tokens", 0)
        if event.get("type") == "result" and "usage" in event:
            usage = event["usage"]
        if event.get("type") == "message" and "text" in event.get("payload", {}):
            final_message += event["payload"]["text"]

    if final_message:
        (run_dir / "claude_last_message.txt").write_text(final_message, encoding="utf-8")

    output_tokens = (usage or {}).get("output_tokens")
    input_tokens = (usage or {}).get("input_tokens")
    total_tokens = None
    if input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    return _base_result(proc.returncode, duration, session_id, output_tokens,
                         thinking_tokens, input_tokens, total_tokens, proc.stderr)


def run_opencode(run_dir: Path, prompt: str, model: str) -> dict:
    cmd = ["opencode", "run", "--model", model, "--format", "json", "--thinking",
           "--auto", "--dir", str(run_dir), prompt]

    started = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=OPENCODE_TIMEOUT_SECONDS)
        stdout, stderr, exit_code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr, exit_code = f"TIMED OUT after {OPENCODE_TIMEOUT_SECONDS}s", None
    duration = round(time.time() - started, 3)
    (run_dir / "opencode_events.jsonl").write_text(stdout, encoding="utf-8")

    session_id, usage, reasoning_text = None, None, []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "sessionID" in event and not session_id:
            session_id = event["sessionID"]
        if event.get("type") == "reasoning":
            text = event.get("part", {}).get("text")
            if text:
                reasoning_text.append(text)
        if event.get("type") == "step_finish" and "tokens" in event.get("part", {}):
            usage = event["part"]["tokens"]

    reasoning_text = "\n".join(reasoning_text)
    if reasoning_text:
        (run_dir / "reasoning_chain.txt").write_text(reasoning_text, encoding="utf-8")

    # Kimi's self-reported `reasoning` token count is frequently 0/unreliable; prefer a
    # tiktoken estimate over the actual reasoning text when tiktoken is available.
    reasoning_tokens = (usage or {}).get("reasoning")
    if reasoning_text:
        try:
            import tiktoken
            reasoning_tokens = len(tiktoken.get_encoding("cl100k_base").encode(reasoning_text))
        except ImportError:
            pass  # fall back to the raw (possibly 0) API-reported value

    return _base_result(exit_code, duration, session_id, (usage or {}).get("output"),
                         reasoning_tokens, (usage or {}).get("input"), (usage or {}).get("total"), stderr)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_once(output_dir: Path, group: str, run_index: int, name: str, prompt: str,
             tool: str, model: Optional[str], use_foundry: bool,
             spec_writer=None, spec_arg=None) -> dict:
    run_dir = output_dir / group / f"{run_index:03d}_{name}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    if spec_writer is not None:
        prompt = spec_writer(spec_arg, run_dir)

    if tool == "codex":
        result = run_codex(run_dir, prompt, model)
    elif tool == "claude":
        result = run_claude(run_dir, prompt, model, use_foundry)
    else:
        result = run_opencode(run_dir, prompt, model or OPENCODE_MODEL_DEFAULT)

    result.update({"run_index": run_index, "name": name})
    # Full-fidelity record (exit_code/duration/stderr aren't always recoverable from the
    # raw event log alone) so rebuild_group_aggregate never has to guess.
    (run_dir / "run_meta.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def event_log_filename(tool: str) -> str:
    return {"codex": "codex_exec_events.jsonl", "claude": "claude_exec_events.jsonl",
            "opencode": "opencode_events.jsonl"}[tool]


def rebuild_group_aggregate(group_dir: Path, tool: str) -> list[dict]:
    """Rescan every run directory on disk and recompute a run record for it.
    Called after every run so incremental/partial invocations never lose visibility
    into previously-collected runs."""
    runs = []
    if not group_dir.exists():
        return runs
    event_file_name = event_log_filename(tool)
    for run_dir in sorted(group_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        m = re.match(r"(\d+)_(.+)", run_dir.name)
        if not m:
            continue
        run_index, name = int(m.group(1)), m.group(2)

        meta_path = run_dir / "run_meta.json"
        if meta_path.exists():
            # Full-fidelity path: exit_code/duration/stderr preserved exactly.
            result = json.loads(meta_path.read_text(encoding="utf-8"))
        else:
            # Fallback for runs predating run_meta.json: reparse from the raw event log.
            # exit_code/duration_seconds/stderr can't be recovered this way.
            events_path = run_dir / event_file_name
            if not events_path.exists():
                continue
            if tool == "codex":
                result = _reparse_codex(events_path)
            elif tool == "claude":
                result = _reparse_claude(events_path)
            else:
                result = _reparse_opencode(events_path, run_dir / "reasoning_chain.txt")
        result.update({"run_index": run_index, "name": name})
        runs.append(result)
    runs.sort(key=lambda r: r["run_index"])
    return runs


def _reparse_codex(events_path: Path) -> dict:
    session_id, usage = None, None
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "session_meta":
            session_id = event.get("payload", {}).get("session_id")
        if event.get("type") == "turn.completed":
            usage = event.get("usage")
    output_tokens = (usage or {}).get("output_tokens")
    reasoning_tokens = (usage or {}).get("reasoning_output_tokens")
    input_tokens = (usage or {}).get("input_tokens")
    total_tokens = (usage or {}).get("total_tokens")
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens
    return _base_result(None, None, session_id, output_tokens, reasoning_tokens, input_tokens, total_tokens, None)


def _reparse_claude(events_path: Path) -> dict:
    session_id, usage, thinking_tokens = None, None, 0
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            session_id = event.get("session_id")
        if event.get("type") == "system" and event.get("subtype") == "thinking_tokens":
            thinking_tokens = event.get("estimated_tokens", 0)
        if event.get("type") == "result" and "usage" in event:
            usage = event["usage"]
    output_tokens = (usage or {}).get("output_tokens")
    input_tokens = (usage or {}).get("input_tokens")
    total_tokens = None
    if input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens
    return _base_result(None, None, session_id, output_tokens, thinking_tokens, input_tokens, total_tokens, None)


def _reparse_opencode(events_path: Path, reasoning_chain_path: Path) -> dict:
    session_id, usage = None, None
    for line in events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "sessionID" in event and not session_id:
            session_id = event["sessionID"]
        if event.get("type") == "step_finish" and "tokens" in event.get("part", {}):
            usage = event["part"]["tokens"]
    reasoning_tokens = (usage or {}).get("reasoning")
    if reasoning_chain_path.exists():
        try:
            import tiktoken
            reasoning_tokens = len(tiktoken.get_encoding("cl100k_base").encode(
                reasoning_chain_path.read_text(encoding="utf-8")))
        except ImportError:
            pass
    return _base_result(None, None, session_id, (usage or {}).get("output"), reasoning_tokens,
                         (usage or {}).get("input"), (usage or {}).get("total"), None)


def compute_summary(runs: list[dict]) -> dict:
    summary = {"count": len(runs)}
    for key in ("output_tokens", "reasoning_tokens", "generated_tokens", "total_tokens"):
        values = [r[key] for r in runs if r.get(key) is not None]
        summary[f"{key}_avg"] = round(sum(values) / len(values), 2) if values else None
        summary[f"{key}_min"] = min(values) if values else None
        summary[f"{key}_max"] = max(values) if values else None
    return summary


def save_aggregate(output_dir: Path, tool: str, benchmark: str, group_names: list[str]) -> None:
    data = {"benchmark_type": f"{benchmark}_{tool}", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    for group in group_names:
        runs = rebuild_group_aggregate(output_dir / group, tool)
        data[group] = {"runs": runs, "summary": compute_summary(runs)}
    (output_dir / "results.json").write_text(json.dumps(data, indent=2))
    for group in group_names:
        print(f"  {group}: {data[group]['summary']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--benchmark", choices=["code", "readme", "skill"], required=True)
    parser.add_argument("--tool", choices=["claude", "codex", "opencode"], required=True)
    parser.add_argument("--experiments-per-group", type=int, default=None,
                         help="Sample this many experiments per group; omit to run all of them")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model", default=None,
                         help="Overrides the per-tool default model (claude-sonnet-4-5 / azure/kimi-k2.6 / codex's own default)")
    parser.add_argument("--use-foundry", action="store_true",
                         help="claude only: route through Azure AI Foundry (set CLAUDE_CODE_USE_FOUNDRY=1). "
                              "Requires ANTHROPIC_FOUNDRY_RESOURCE and ANTHROPIC_FOUNDRY_API_KEY already exported.")
    parser.add_argument("--skills-root", default=str(SKILLS_ROOT_DEFAULT),
                         help="Only used by --benchmark skill")
    parser.add_argument("--root-output-dir", default=None,
                         help="Defaults to results/<benchmark>_<tool> under this script's directory")
    parser.add_argument("--dry-run", action="store_true", help="Print what would run; touches no files at all")
    args = parser.parse_args()

    model = args.model
    if args.tool == "claude" and model is None:
        model = CLAUDE_MODEL_DEFAULT
    if args.tool == "opencode" and model is None:
        model = OPENCODE_MODEL_DEFAULT

    output_dir = Path(args.root_output_dir) if args.root_output_dir else (
        SCRIPT_DIR / "results" / f"{args.benchmark}_{args.tool}")

    if args.benchmark == "code":
        base = discover_code_experiments(base=True)
        non_base = discover_code_experiments(base=False)
        groups = {"base": base, "non_base": non_base}
    elif args.benchmark == "readme":
        base, non_base = discover_readme_experiments()
        groups = {"base": base, "non_base": non_base}
    else:
        base, mdp = discover_skill_experiments(Path(args.skills_root))
        groups = {"base": base, "mdp": mdp}

    for group_name, experiments in groups.items():
        selected = select_experiments(experiments, args.experiments_per_group, args.seed)
        print(f"\n[{group_name}] {len(selected)}/{len(experiments)} experiments selected")
        if args.dry_run:
            for exp in selected:
                print(f"  WOULD RUN: {exp['name']}")
            continue

        for run_index, exp in enumerate(selected, start=1):
            print(f"[{group_name}] {run_index}/{len(selected)}: {exp['name']}", flush=True)
            if args.benchmark == "code":
                result = run_once(output_dir, group_name, run_index, exp["name"], prompt="",
                                   tool=args.tool, model=model, use_foundry=args.use_foundry,
                                   spec_writer=write_code_spec_script, spec_arg=exp["spec_path"])
            elif args.benchmark == "readme":
                result = run_once(output_dir, group_name, run_index, exp["name"], prompt="",
                                   tool=args.tool, model=model, use_foundry=args.use_foundry,
                                   spec_writer=write_readme_spec, spec_arg=exp["readme_path"])
            else:
                result = run_once(output_dir, group_name, run_index, exp["name"],
                                   prompt=build_skill_prompt(exp["name"]),
                                   tool=args.tool, model=model, use_foundry=args.use_foundry)
            print(f"    exit={result['exit_code']} output={result['output_tokens']} "
                  f"reasoning={result['reasoning_tokens']}", flush=True)

    if not args.dry_run:
        print("\nAggregate summary:")
        save_aggregate(output_dir, args.tool, args.benchmark, list(groups.keys()))
        print(f"\nWrote {output_dir / 'results.json'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
