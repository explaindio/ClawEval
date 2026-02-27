# 🦞 ClawEval

**Deterministic LLM evaluation for agentic AI roles.** ClawEval tests how well language models perform as specialized AI agents — from routers and validators to code reviewers and financial analysts.

Unlike vibes-based benchmarks, ClawEval uses **deterministic, auto-scored tests** with exact JSON matching, code execution, constraint checking, and numeric tolerance. Every score is reproducible.

## 🏆 Leaderboard

### Phase E — 12 Killer Tests (Reasoning, Code, Structured Output, Multi-Turn)

| Model | VRAM | Think | Score | Code | Reasoning | Structured | Instruction | Multi-Turn |
|---|---|---|---|---|---|---|---|---|
| **Qwen3.5-122B-A10B NVFP4** | 96GB | 16K | **108/120 (90%)** | 100% | 82% | 100% | 100% | 85% |
| Qwen3.5-35B-A3B Q4_K_M | 24GB | 32K | 102/120 (85%) | 100% | 70% | 95% | 100% | 90% |
| Qwen3.5-27B Q4_K_M | 24GB | OFF | 83/120 (69%) | 100% | 46% | 70% | 20% | 100% |
| Qwen3.5-122B-A10B NVFP4 | 96GB | OFF | 79/120 (66%) | 100% | 56% | 55% | 20% | 90% |
| Qwen3.5-35B-A3B Q4_K_M | 24GB | OFF | 76/120 (63%) | 100% | 42% | 80% | 20% | 90% |

### Phase F — 59-Role Deterministic Hard Tests

| Model | Think | Score | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|---|---|
| **Qwen3.5-122B-A10B NVFP4** | 16K | **~443/590 (75.1%)** | 59% | 69% | 71% | 53% | 65% |

**Perfect 10/10 scores:** Router, Validator, Sentiment, Research, Content Planner, Web Scraping, Customer Support, Sprint Summarizer, Transaction, Home Automation, News Aggregation, Shopping, Code Gen, Code Review, Fact-Check, Algorithm, Legal, Software Architect, STEM Analysis

> **Scorer fixes applied:** 6 tests originally scored 0/10 due to scorer bugs (case-sensitive keys, strict keyword matching, flat JSON assumptions). After fixing, they scored 8–10/10. See commit `362ee3a` for details.

> **64K re-run finding:** Tests #31 (Recipe) and #42 (Market Research) were re-tested with 64K max_tokens to rule out thinking overflow. Recipe scored 2/10 (model answered but miscalculated scaling math). Market Research timed out at 1200s with 0 tokens returned. Both are **genuine model limitations**, not scorer or truncation issues.


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
