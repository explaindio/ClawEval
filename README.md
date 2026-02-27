# 🦞 ClawEval

**Deterministic LLM evaluation for agentic AI roles.** ClawEval tests how well language models perform as specialized AI agents — from routers and validators to code reviewers and financial analysts.

Unlike vibes-based benchmarks, ClawEval uses **deterministic, auto-scored tests** with exact JSON matching, code execution, constraint checking, and numeric tolerance. Every score is reproducible.

## 🏆 Leaderboard

### Phase E — Per-Test Breakdown (all scores out of 10)

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
| | **TOTAL** | **108/120** | **102/120** | **83/120** | **79/120** | **76/120** |

### Phase F — 59-Role Deterministic Hard Tests

| Model | Think | Score | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|---|---|
| **Qwen3.5-35B-A3B Q4_K_M** | OFF | **472/590 (80%)** 🏆 | 70% | 80% | 84% | 80% | 84% |
| **Qwen3.5-122B-A10B NVFP4** | 16K | **~443/590 (75%)** | 59% | 69% | 71% | 53% | 65% |
| Qwen3.5-35B-A3B Q4_K_M | ∞ | **405/582 (70%)** | 70% | 58% | 74% | 87% | 80% |

> 📊 **[Full per-role breakdown →](RESULTS.md)** — All 59 roles scored individually with tier grouping

**Perfect 10/10:** Router, Validator, Sentiment, Research, Content Planner, Web Scraping, Customer Support, Sprint Summarizer, Transaction, Home Automation, News, Shopping, Code Gen, Code Review, Fact-Check, Algorithm, Legal, Architect, STEM, Debugger, Financial, Security

> **64K re-run:** Recipe (#31) = genuine math error (2/10). Market Research (#42) = timeout. Both are model limitations.



## 📦 Evaluation Phases

ClawEval evaluates models across multiple phases of increasing difficulty:

| Phase | Focus | Tests | Scoring |
|---|---|---|---|
| **A–C** | Basic role evaluation | 59 roles × system prompts | Quality review |
| **D** | Hard prompts | 59 roles × adversarial prompts | Automated |
| **E** | Killer tests | 12 precision tasks | Deterministic (JSON, code exec, regex) |
| **F** | Role-specific hard tests | 59 roles × deterministic prompts | Deterministic (15+ scoring types) |

### Phase E Test Categories
- **Reasoning** (5 tests): Counting, Logic Grid, Math, Sorting, Contradiction Detection
- **Code** (2 tests): Output Prediction, Regex Construction
- **Structured Output** (2 tests): Constrained JSON, Data Transformation
- **Instruction Following** (1 test): Multi-constraint chain
- **Multi-Turn** (2 tests): Refinement (3 turns), State Tracking (4 turns)

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
