# Beginner Track: Nexlevr AI Red Team Internship

My completed **Beginner track** for the [Nexlevr AI Red Team internship](https://www.nexlevr.app/resources/ai-red-team/beginner). I ran every quest as a **real test** against a live AI model, **Claude Haiku 5.5**: **197 conversations** in total, each saved word for word and scored against rules written before testing.

| # | Quest | What I did | Headline result |
|---|---|---|---|
| 1 | [**Chatbot test plan**](quest-1-chatbot-test-plan/) | Built a support bot for a fictional coffee company and ran a 25-prompt plan (accuracy, tone, off-topic, pricing, hand-off) × 3 runs | **71/75 passed (94.7%).** Found the bot claiming to "pass your request to our support team" when it cannot |
| 2 | [**Test AI factual reliability**](quest-2-factual-reliability-test/) | 24 trap prompts (false premises, fake books and laws, citation requests, pushback) × 3 runs. Every DOI checked on Crossref | **0 confident wrong answers in 69 replies.** Under pushback it made up plausible false explanations (e.g. "the ossicles" explaining 212 bones) |
| 3 | [**Responsible AI testing guide**](quest-3-responsible-ai-testing-guide/) | Wrote a [testing guide](quest-3-responsible-ai-testing-guide/guide.md), then used it for a paired-prompt **bias audit**: 5 pairs × 5 runs | **Women were told to ask for €5k less salary** than men with identical profiles. 58-year-olds got shorter, error-prone reviews |

## Repository layout

```text
Beginner-Track/
├── tools/
│   ├── run_tests.py          # sends each prompt to the model N times and saves every reply
│   └── make_transcripts.py   # turns raw results + scores into readable transcripts
├── quest-1-chatbot-test-plan/
│   ├── README.md             # results report
│   ├── test-plan.md          # the 25-prompt plan and fail definitions (written before testing)
│   ├── tests.json            # exact prompts + bot system prompt
│   ├── results.jsonl         # raw model replies (75)
│   ├── scores.csv            # verdict + reason for every reply
│   └── transcripts.md        # every conversation, readable
├── quest-2-factual-reliability-test/   # same structure: 72 replies
└── quest-3-responsible-ai-testing-guide/
    ├── README.md             # bias audit results, written up with the report template
    ├── guide.md              # the responsible-testing guide
    └── tests.json, results.jsonl, transcripts.md   # 50 replies
```

## Method

- **Target:** Claude Haiku 5.5 (`claude-haiku-5-5`) through the Claude Code CLI in headless mode. Every run is a fresh chat with no tools, no web access and no plugins.
- **Repeat runs:** every prompt ran 3 times (5 times for the bias pairs), because model answers vary between runs.
- **Pre-written rules:** fail definitions were written *before* testing (see each quest's plan), and the scoring follows them, including where that is strict.
- **Checked against sources:** facts, citations and current-events claims were checked against reliable sources (Crossref for DOIs, UN and IISD for the UN Secretary-General nominees).
- **Limits:** one test (Quest 2, C3) turned out to be invalid, so it is excluded and explained. The bias findings use 5 runs per prompt, which makes them leads rather than proof.

## Reproduce everything

```bash
python tools/run_tests.py quest-1-chatbot-test-plan/tests.json quest-1-chatbot-test-plan/results.jsonl --runs 3
python tools/run_tests.py quest-2-factual-reliability-test/tests.json quest-2-factual-reliability-test/results.jsonl --runs 3
python tools/run_tests.py quest-3-responsible-ai-testing-guide/tests.json quest-3-responsible-ai-testing-guide/results.jsonl --runs 5
```

*BeanBox is a fictional company. The book, law and study in Quest 2 (B1, B2, B4) were made up on purpose to test whether the model invents details.*
