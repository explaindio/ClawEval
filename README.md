# 🦞 ClawEval — Can Your LLM Actually Do the Job?

**The only deterministic benchmark that tests LLMs as real AI agents** — not trivia, not chat, not vibes. 59 specialized roles. Hard, verifiable tasks. Every score is reproducible.

> 🔥 **New models added regularly.** We test the latest open-source models you can actually run locally — and compare them against cloud-hosted open-source models. Star ⭐ this repo to get notified when new results drop.

### Why ClawEval?

Most benchmarks tell you a model is "smart." ClawEval tells you if it can **do the work** — route tickets, review code, analyze financials, draft legal docs, plan sprints, and 54 more agent roles. Each test has an exact expected answer. No LLM-as-judge. No vibes.

### 🖥️ LOCAL Models — What Can You Run at Home?

| | 🟢 24GB VRAM (RTX 4090) | 🔵 96GB VRAM (2×48GB) | ☁️ CLOUD (open-source) |
|---|---|---|---|
| **Models** | Qwen3.5-35B-A3B Q4, Qwen3.5-27B Q4 | Qwen3.5-122B-A10B NVFP4 | More open-source models |
| **Server** | llama.cpp | SGLang | API (OpenRouter, Together, etc.) |
| **Status** | ✅ Tested | ✅ Tested | 🔜 Coming soon |

---

## 🏆 Per-Role Agent Scores (Phase F — 59 Roles)

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual (5) &nbsp; ⬛ = 32K overflow

All scores out of 10. Models: **122B** = Qwen3.5-122B-A10B NVFP4 (think 16K, SGLang) · **35B-T** = Qwen3.5-35B-A3B Q4_K_M (think ∞, llama.cpp) · **35B-N** = same, nothink

| # | Agent Role | Qwen3.5-122B-A10B | Qwen3.5-35B-A3B | Qwen3.5-35B-A3B |
|---|---|---|---|---|
| | | Think 16K · SGLang | Think ∞ · llama.cpp | NoThink · llama.cpp |
| | **Tier 1 — Utility** | | | |
| 1 | Router / Triage | 🟢 10 | 🟢 10 | 🟢 10 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🔴 3 | ⬛ 0 | 🔴 3 |
| 4 | Notification | 🟢 8 | 🟢 8 | 🟢 8 |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 5 | 🟡 6 | 🟡 6 |
| 7 | Translation | 🟢 10 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | |
| 9 | Research Agent | 🟢 10 | ⬛ 0 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟡 7 | 🟢 9 | 🟢 10 |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟢 8 | ⬛ 0 | 🟢 10 |
| 14 | Doc Summary | 🟢 8 | 🟢 8 | 🟢 10 |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🟢 10 | 🔴 4 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 6 | 🟡 6 | 🔴 4 |
| 22 | Data Analysis | 🔴 2 | ⬛ 0 | 🔴 3 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 10 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 |
| 27 | Sprint Summary | 🟢 10 | ⬛ 0 | 🟡 5 |
| 28 | Transaction | 🟢 10 | ⬛ 0 | 🟢 9 |
| 29 | Home Automation | 🟢 10 | 🟢 10 | 🟢 9 |
| 30 | Fitness Tracking | 🟢 9 | 🟢 9 | 🟡 7 |
| 31 | Recipe / Cooking | 🔴 2 | ⬛ 0 | 🟢 9 |
| 32 | Personal Finance | 🟡 7 | ⬛ 0 | 🔴 4 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 8 | 🔴 0 | 🟡 7 |
| | **Tier 3 — Advanced** | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 8 | 🟢 10 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 10 |
| 39 | Task Planning | 🟢 9 | 🟢 9 | 🟢 10 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🔴 0 | ⬛ 0 | 🟡 7 |
| 43 | Synthesizer | 🟡 7 | 🟢 9 | 🟢 9 |
| 44 | Curriculum Design | 🟡 6 | 🟡 6 | 🟡 6 |
| 45 | Prototype Gen | 🟡 6 | 🟡 6 | 🟡 6 |
| 46 | DevOps | 🟡 7 | 🟢 10 | 🟢 9 |
| | **Tier 4 — Expert** | | | |
| 47 | Math / Logic | 🟡 6 | 🟡 6 | 🔴 4 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 10 | 🟢 10 | 🟢 10 |
| 52 | Debugger | 🟢 10 | 🟢 8 | 🟢 10 |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 |
| 54 | Medical | 🟡 7 | 🟢 10 | 🟢 10 |
| 55 | Financial | 🟢 10 | 🟢 10 | 🟢 10 |
| 56 | Security | 🟡 6 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🟡 6 | ⬛ 0 | 🔴 3 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟡 7 | 🟢 8 | 🟢 8 |

> ⬛ **35B-T overflow:** llama.cpp has no `thinking_budget`, so 10 tests consumed all 32K tokens on reasoning. Re-run pending on vLLM/SGLang. See [RESULTS.md](RESULTS.md) for detailed notes.

---

### Phase E — 12 Killer Tests (Reasoning, Code, Structured Output, Multi-Turn)

All scores out of 10.

| # | Test | 122B Think | 35B Think | 27B NoThink | 122B NoThink | 35B NoThink |
|---|---|---|---|---|---|---|
| 1 | Precise Counting | 🟢 8 | 🔴 4 | 🔴 4 | 🔴 0 | 🔴 4 |
| 2 | Constrained JSON | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 |
| 3 | Logic Grid Puzzle | 🟢 10 | 🟢 10 | 🟡 5 | 🟡 5 | 🟡 6 |
| 4 | Multi-Step Math | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 5 | Code Output Prediction | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | Contradiction Detection | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 |
| 7 | Complex Multi-Key Sort | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🔴 3 |
| 8 | Regex Construction | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟡 7 |
| 9 | Data Transformation | 🟢 10 | 🟢 10 | 🔴 0 | 🔴 2 | 🔴 2 |
| 10 | Instruction Following | 🟢 10 | 🟢 8 | 🔴 4 | 🔴 2 | 🔴 4 |
| 11 | Multi-Turn Refinement | 🟡 7 | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 9 |
| 12 | Multi-Turn State Track | 🟢 10 | 🟢 9 | 🟡 7 | 🟢 10 | 🟡 7 |

---

## 📦 Evaluation Phases

ClawEval evaluates models across multiple phases of increasing difficulty:

| Phase | Focus | Tests | Scoring |
|---|---|---|---|
| **A–C** | Basic role evaluation | 59 roles × system prompts | Quality review |
| **D** | Hard prompts | 59 roles × adversarial prompts | Automated |
| **E** | Killer tests | 12 precision tasks | Deterministic (JSON, code exec, regex) |
| **F** | Role-specific hard tests | 59 roles × deterministic prompts | Deterministic (15+ scoring types) |

### Phase F — 59 Roles Across 5 Tiers
- **Tier 1** (8 roles): Router, Validator, Health Monitor, Notification, Sentiment, FAQ, Translation, Calendar
- **Tier 2** (27 roles): Research, Writer, Editor, Email, Summarization, Customer Support, Data Analysis, etc.
- **Tier 3** (11 roles): Code Gen, Code Review, QA Testing, Task Planning, Fact-Checking, Market Research, etc.
- **Tier 4** (3 roles): Math/Logic Reasoning, STEM Analysis, Algorithm Exploration
- **Tier 5** (10 roles): Orchestrator, Architect, Debugger, Legal, Medical, Financial, Security, SRE, etc.

### Scoring Types
`exact_json` · `json_numeric` · `keyword_detection` · `code_exec` · `constraint_check` · `error_count` · `action_items` · `news_dedup` · `recipe_scaling` · `compliance_issues` · `architecture_constraints` · `manual_review` · and more

## 🚀 Quick Start

### Prerequisites
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

### Run Phase E (12 killer tests)
```bash
# Against llama.cpp server
python eval/run_phase_e.py \
  --base-url http://localhost:8080/v1 \
  --model my-model-name \
  --max-tokens 4000

# Against SGLang server (with thinking)
python eval/run_phase_e.py \
  --base-url http://192.168.1.2:8000/v1 \
  --model Qwen3.5-122B-think \
  --api-model /path/to/weights \
  --thinking-budget 16384 \
  --max-tokens 32000

# Disable thinking
python eval/run_phase_e.py \
  --base-url http://192.168.1.2:8000/v1 \
  --model Qwen3.5-122B-nothink \
  --api-model /path/to/weights \
  --nothink
```

### Run Phase F (59 role tests)
```bash
python eval/run_phase_f.py \
  --base-url http://localhost:8080/v1 \
  --model my-model-name \
  --max-tokens 4000

# Run specific tests or tiers
python eval/run_phase_f.py ... --test-ids 1 2 3
python eval/run_phase_f.py ... --tier 3
```

### Results
Results are saved to `eval/test_results/<model-name>/phase_e/` and `phase_f/` directories, including:
- Individual response text files per test
- `phase_e_scores.json` / `phase_f_scores.json` with full scoring breakdown

## 🔧 Key Features

- **OpenAI-compatible API**: Works with any server exposing `/v1/chat/completions` (llama.cpp, SGLang, vLLM, etc.)
- **SGLang thinking control**: `--thinking-budget` and `--nothink` flags for reasoning token management
- **Think-tag stripping**: Automatically strips `<think>` tags from responses for clean scoring
- **Flexible JSON scoring**: Case-insensitive keys, nested dict traversal, numeric tolerance
- **Deterministic**: Every test has an exact expected answer — no LLM-as-judge

## 📁 Repo Structure

```
ClawEval/
├── eval/
│   ├── run_phase_e.py          # Phase E runner (12 killer tests)
│   ├── run_phase_f.py          # Phase F runner (59 role tests)
│   ├── phase_e_prompts.py      # Phase E test definitions
│   ├── phase_f/                # Phase F test definitions (5 tiers)
│   │   ├── __init__.py
│   │   ├── tier1.py ... tier5.py
│   ├── role_prompts.py         # 59 role system prompts
│   ├── hard_prompts.py         # Phase D adversarial prompts
│   └── test_results/           # All model evaluation results
├── docs/                       # Model selection & VRAM guides
└── README.md
```

## 📄 License

MIT

## 🔗 Links

- **Website**: [claweval.com](https://claweval.com)
- **GitHub**: [github.com/explaindio/ClawEval](https://github.com/explaindio/ClawEval)
