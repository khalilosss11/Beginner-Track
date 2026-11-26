"""Run a prompt test set against a chatbot via the Claude Code CLI (headless).

Usage:
    python tools/run_tests.py <tests.json> <out.jsonl> [--runs 3] [--workers 6]

tests.json format:
{
  "model": "claude-haiku-5-5",
  "system_prompt": "...",            # replaces the CLI's default system prompt
  "tests": [
    {"id": "A1", "prompt": "..."},                       # single turn
    {"id": "S1", "prompt": "...", "followup": "..."}     # two turns, same chat
  ]
}

Every call starts a fresh chat with no tools, no MCP servers and no user
settings, so the model answers from its own knowledge only. Each reply is saved
verbatim with its run number, timestamp and model, as evidence for scoring.
"""
import argparse
import shutil
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

CLI = shutil.which("claude") or "claude"


def ask(prompt, model, sp_file, resume=None, persist=False):
    cmd = [CLI, "-p", prompt, "--model", model, "--system-prompt-file", sp_file,
           "--tools", "", "--strict-mcp-config", "--setting-sources", "",
           "--output-format", "json"]
    if resume:
        cmd += ["--resume", resume]
    elif not persist:
        cmd += ["--no-session-persistence"]
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=300)
        try:
            data = json.loads(p.stdout)
            if not data.get("is_error"):
                return data
        except json.JSONDecodeError:
            pass
    raise RuntimeError(f"CLI failed: {p.stderr[:300]} {p.stdout[:300]}")


def run_one(test, run, model, sp_file):
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rec = {"id": test["id"], "run": run, "model": model, "time_utc": stamp,
           "prompt": test["prompt"]}
    if "followup" in test:
        first = ask(test["prompt"], model, sp_file, persist=True)
        rec["reply"] = first["result"]
        second = ask(test["followup"], model, sp_file, resume=first["session_id"])
        rec["followup"] = test["followup"]
        rec["followup_reply"] = second["result"]
    else:
        rec["reply"] = ask(test["prompt"], model, sp_file)["result"]
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tests")
    ap.add_argument("out")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    with open(a.tests, encoding="utf-8") as f:
        spec = json.load(f)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as sp:
        sp.write(spec["system_prompt"])
        sp_file = sp.name

    jobs = [(t, r) for t in spec["tests"] for r in range(1, a.runs + 1)]
    with ThreadPoolExecutor(a.workers) as pool:
        results = list(pool.map(lambda j: run_one(j[0], j[1], spec["model"], sp_file), jobs))
    os.unlink(sp_file)

    with open(a.out, "w", encoding="utf-8") as f:
        for rec in results:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"{len(results)} replies written to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
