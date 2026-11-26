"""Turn results.jsonl + scores.csv into a readable transcripts.md.

Usage: python tools/make_transcripts.py <quest-folder> "<title>"
"""
import csv
import json
import sys
from collections import defaultdict

folder, title = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(f"{folder}/results.jsonl", encoding="utf-8")]
scores = {}
try:
    for s in csv.DictReader(open(f"{folder}/scores.csv", encoding="utf-8")):
        scores[(s["id"], int(s["run"]))] = s
except FileNotFoundError:
    pass

by_id = defaultdict(list)
order = []
for r in rows:
    if r["id"] not in by_id:
        order.append(r["id"])
    by_id[r["id"]].append(r)
tests = json.load(open(f"{folder}/tests.json", encoding="utf-8"))
order = [t["id"] for t in tests["tests"]]

out = [f"# {title}: full transcripts", "",
       f"Model: `{rows[0]['model']}` · Runs: {len(rows)} · "
       f"Collected: {min(r['time_utc'] for r in rows)} (UTC)", "",
       "Every reply below is copied verbatim from `results.jsonl`. "
       "Each run was a fresh chat with no tools.", ""]
for tid in order:
    runs = sorted(by_id[tid], key=lambda r: r["run"])
    out += [f"## {tid}", "", f"**Prompt:** {runs[0]['prompt']}", ""]
    if "followup" in runs[0]:
        out += [f"**Pushback (turn 2):** {runs[0]['followup']}", ""]
    for r in runs:
        s = scores.get((tid, r["run"]))
        verdict = f" · **{s['score']}**" + (f" ({s['severity']})" if s.get("severity") else "") if s else ""
        out += [f"### Run {r['run']}{verdict}", ""]
        out += ["> " + line if line else ">" for line in r["reply"].strip().splitlines()]
        if "followup_reply" in r:
            out += ["", "*After pushback:*", ""]
            out += ["> " + line if line else ">" for line in r["followup_reply"].strip().splitlines()]
        if s and s.get("note"):
            out += ["", f"*Scorer note:* {s['note']}"]
        out += [""]
open(f"{folder}/transcripts.md", "w", encoding="utf-8").write("\n".join(out))
print(f"wrote {folder}/transcripts.md")
