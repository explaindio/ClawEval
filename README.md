# 🦞 ClawEval — Can Your Local or Cloud LLM Actually Do the Job?

**The only deterministic benchmark that tests LLMs as real AI agents** — not trivia, not chat, not vibes. 59 specialized roles. Hard, verifiable tasks. Every score is reproducible.

> 🔥 **New models added regularly.** Star ⭐ this repo to get notified when new results drop.
>
> 📬 **[Subscribe to AIgenteur Dispatch](https://aigenteurdispatch.substack.com/)** — benchmark results, local AI guides, and agent workflows in your inbox.
>
> 🎓 **[Join AIgenteur Academy (free)](https://www.skool.com/aigenteur-academy-9764)** — community for freelancers and entrepreneurs putting AI agents to work. Want a model tested? Post your request in the community.

> 💡 **You'd be surprised** how well some small, fast models handle sub-agent tasks — even on an RTX 3090 (we got ours for $799). Before you rent cloud GPUs, check the scores below.

### Why ClawEval?

Most benchmarks tell you a model is "smart." ClawEval tells you if it can **do the work** — route tickets, review code, analyze financials, draft legal docs, plan sprints, and 54 more agent roles. Each test has an exact expected answer. No LLM-as-judge. No vibes.

### 🖥️ LOCAL Models — Run on YOUR Hardware

We test quantized open-source models that fit on hardware you already own. Find out which model is best for each agent role **before you commit your VRAM.** We're also testing smaller models for max context and usability — even a 16GB GPU can run capable sub-agents.

| 🟡 16GB VRAM | 🟢 24GB VRAM | 🔵 64–96GB VRAM |
|---|---|---|
| Qwen3-8B, Phi-4 14B | Qwen3.5-35B-A3B Q4_K_M | Qwen3.5-122B-A10B NVFP4 |
| Mistral Small 24B, GPT-OSS-20B | Qwen3.5-27B Q4_K_M | GPT-OSS-120B GGUF (llama.cpp) |
| Coming soon | llama.cpp · SGLang · vLLM | SGLang · vLLM · llama.cpp |

> 📖 **VRAM Guides:** [16GB](docs/OpenClaw%2016GB%20VRAM%20Local%20LLM%20Subagents.md) · [24GB](docs/The%2024GB%20VRAM%20Tier_%20Where%20Local%20AI%20Agents%20Get%20Serious.md) · [32GB](docs/openclaw-model-selection-32gb-tier.md) · [48GB](docs/openclaw-48gb-tier.md) · [64GB](docs/openclaw-64gb-tier.md) · [96GB](docs/openclaw-96gb-tier.md) — Which models fit, context limits, speed estimates

### ☁️ CLOUD Models — Run via API

Don't have a GPU? We also test open-source models hosted on cloud providers so you can compare **local vs cloud performance at every agent role.** Same tests, same scoring — find out if paying for cloud is worth it, or if your local setup already matches.

| Provider | Models | Status |
|---|---|---|
| Alibaba Coding Plan | **Kimi K2.5** — 473/590 (80%) Phase F, 96/110 (87%) Phase G | ✅ Tested |
| Alibaba Coding Plan | **GLM-5** — 465/590 (79%) Phase F, 80/110 (73%) Phase G | ✅ Tested |
| OpenRouter, Alibaba, and other affordable providers | Open-source models via API | 🔜 Coming soon |


## 🏆 Best Model Per Role — Which One Should You Run?

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual review (5)

**The only table you need.** Best-scoring model for each role at each VRAM tier. Combines Phase F (role tests) + Phase G (discriminator tests). All scores out of 10.

| # | Agent Role | 🟢 Best 24GB | | 🔵 Best 64–96GB | |
|---|---|---|---|---|---|
| | | **Model** | **Score** | **Model** | **Score** |
| | **Tier 1 — Utility** | | | | |
| 1 | Router / Triage | 27B / 35B NoThink | 🟢 10 | 122B Think | 🟢 10 |
| 2 | Input Validator | 27B NoThink | 🟢 10 | 122B NoThink | 🟢 10 |
| 3 | Health Monitor | 27B / 35B NoThink | 🔴 3 | GPT-OSS-120B | 🟢 8 |
| 4 | Notification | 27B Think | 🟢 9 | GPT-OSS-120B | 🟢 9 |
| 5 | Sentiment | 27B / 35B NoThink | 🟢 8† | 122B NoThink | 🟢 8† |
| 6 | FAQ Generation | 27B Think | 🟢 8 | 122B / GPT-OSS | 🟡 5 |
| 7 | Translation | 27B NoThink | 🟢 10 | 122B Think | 🟢 10 |
| 8 | Calendar | — | 🔴 0 | — | 🔴 0 |
| | **Tier 2 — Moderate** | | | | |
| 9 | Research Agent | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B / 122B NT | 🟢 9† |
| 10 | Content Writer | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 11 | Editor | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B | 🟢 9 |
| 12 | Content Planner | 27B / 35B NoThink | 🟢 10 | 122B NoThink | 🟢 10 |
| 13 | Email Drafting | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B | 🟢 9 |
| 14 | Doc Summary | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B | 🟢 10 |
| 15 | Meeting Notes | 27B / 35B NoThink | 🟢 9 | 122B Think | 🟢 9 |
| 16 | Social Scouting | 27B / 35B NoThink | 🟢 10 | 122B NoThink | 🟢 10 |
| 17 | Social Content | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 18 | News Aggregation | 27B / 35B NoThink | 🟢 10 | 122B NoThink | 🟢 10 |
| 19 | Shopping | 27B / 35B Think | 🟢 10 | 122B Think | 🟢 10 |
| 20 | Memory Mgmt | 27B / 35B NoThink | 🟢 9 | 122B NoThink | 🟢 9 |
| 21 | RAG / Retrieval | 27B NoThink | 🟡 6 | 122B / GPT-OSS | 🟡 6 |
| 22 | Data Analysis | 27B / 35B NoThink | 🔴 3 | 122B / GPT-OSS | 🔴 2 |
| 23 | Web Scraping | 35B NoThink | 🟢 10 | 122B NoThink / GPT-OSS | 🟢 10 |
| 24 | Image Description | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 25 | Customer Support | 27B / 35B Think | 🟢 10 | 122B NoThink / GPT-OSS | 🟢 10 |
| 26 | Lead Scoring | 27B NoThink | 🟢 10 | 122B / GPT-OSS | 🟢 8 |
| 27 | Sprint Summary | 27B NoThink | 🟡 7 | 122B Think | 🟢 10 |
| 28 | Transaction | 35B NoThink | 🟢 9 | 122B NoThink / GPT-OSS | 🟢 10 |
| 29 | Home Automation | 27B / 35B Think | 🟢 10 | 122B Think | 🟢 10 |
| 30 | Fitness Tracking | 27B NoThink / Think | 🟢 9 | 122B NoThink / GPT-OSS | 🟢 9 |
| 31 | Recipe / Cooking | 35B NoThink | 🟢 9 | GPT-OSS-120B | 🟢 9 |
| 32 | Personal Finance | 27B Think | 🟡 7 | 122B Think | 🟡 7 |
| 33 | SEO Optimization | 27B / 35B NoThink | 🟢 9 | 122B NoThink | 🟢 9 |
| 34 | Landing Page | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 35 | Travel Planning | 27B / 35B NoThink | 🟡 7 | 122B Think | 🟢 8 |
| | **Tier 3 — Advanced** | | | | |
| 36 | Code Generation | 27B NoThink | 🟢 10† | 122B NoThink | 🟢 8† |
| 37 | Code Review | 35B NoThink / 27B Think | 🟢 10 | 122B Think | 🟢 10 |
| 38 | QA / Test Writing | 35B NoThink | 🟢 10 | 122B / GPT-OSS | 🟢 8 |
| 39 | Task Planning | 35B NoThink | 🟢 10 | 122B / GPT-OSS | 🟢 9 |
| 40 | Fact-Checking | 27B NoThink | 🟢 10† | 122B NoThink | 🟢 10† |
| 41 | Critic / Review | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 42 | Market Research | 27B NoThink | 🟢 8 | GPT-OSS-120B | 🔴 4 |
| 43 | Synthesizer | 27B / 35B Think | 🟢 9 | GPT-OSS-120B | 🟢 10 |
| 44 | Curriculum Design | 27B / 35B NoThink | 🟡 6 | GPT-OSS-120B | 🟡 7 |
| 45 | Prototype Gen | 27B / 35B Think/NoThink | 🟡 6 | 122B Think | 🟡 6 |
| 46 | DevOps | 27B NoThink / 35B Think | 🟢 10 | GPT-OSS-120B | 🟢 10 |
| | **Tier 4 — Expert** | | | | |
| 47 | Math / Logic | 27B / 35B Think | 🟡 6 | GPT-OSS-120B | 🟢 8 |
| 48 | STEM Analysis | 27B NoThink | 🔴 2† | 122B NoThink / GPT-OSS | 🟡 5† |
| 49 | Algorithm | 27B NoThink | 🟢 9† | 122B NoThink / GPT-OSS | 🟢 10† |
| | **Tier 5 — Senior** | | | | |
| 50 | Orchestrator | 27B / 35B NoThink | 🟡 7† | 122B NoThink / GPT-OSS | 🟡 7† |
| 51 | Architect | 27B / 35B NoThink | 🟢 9† | 122B NoThink | 🟢 10† |
| 52 | Debugger | 35B NoThink | 🟢 10 | 122B NoThink / GPT-OSS | 🟢 10 |
| 53 | Legal Review | 27B / 35B NoThink | 🟢 10 | 122B Think | 🟢 10 |
| 54 | Medical | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B | 🟢 9 |
| 55 | Financial | 27B / 35B NoThink | 🟢 10 | 122B NoThink | 🟢 10 |
| 56 | Security | 27B / 35B NoThink | 🟢 10 | GPT-OSS-120B | 🟢 10 |
| 57 | SRE / Incident | 27B NoThink | 🟡 6 | 122B / GPT-OSS | 🟡 6 |
| 58 | Book Writing | 📝 Manual | 📝 5 | 📝 Manual | 📝 5 |
| 59 | Compliance | 27B NoThink | 🟢 9 | GPT-OSS-120B | 🟢 8 |

> † Phase G discriminator score (harder test that differentiates models — [details](docs/results-phase-g.md))
>
> 📊 **Detailed local comparisons:**
> - [🟢 24GB VRAM — Think vs NoThink (4 models)](docs/results-24gb-vram.md)
> - [🔵 64–96GB VRAM — GPT-OSS-120B vs Qwen3.5-122B](docs/results-64-96gb-vram.md)
> - [🆕 Phase G — Discriminator Tests (harder tests)](docs/results-phase-g.md)
> - [Phase E — 12 Killer Tests (all models)](docs/results-phase-e.md)
> - [Full detailed results with all configs →](RESULTS.md)


## ☁️ Best Cloud Model Per Role

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual review (5)

> 🔜 **More cloud models coming soon.** Currently tested: Kimi K2.5, GLM-5. Next up: additional models via OpenRouter, Alibaba, and other providers.

| # | Agent Role | ☁️ Best Cloud | |
|---|---|---|---|
| | | **Model** | **Score** |
| | **Tier 1 — Utility** | | |
| 1 | Router / Triage | GLM-5 NoThink | 🟢 10 |
| 2 | Input Validator | K2.5 / GLM-5 | 🟢 10† |
| 3 | Health Monitor | K2.5 / GLM-5 | 🟡 5 |
| 4 | Notification | Kimi K2.5 | 🟢 9 |
| 5 | Sentiment | K2.5 / GLM-5 | 🟢 10† |
| 6 | FAQ Generation | K2.5 / GLM-5 | 🟡 7 |
| 7 | Translation | K2.5 / GLM-5 | 🟢 9 |
| 8 | Calendar | — | 🔴 0 |
| | **Tier 2 — Moderate** | | |
| 9 | Research Agent | K2.5 / GLM-5 | 🟢 10† |
| 10 | Content Writer | 📝 Manual | 📝 5 |
| 11 | Editor | Kimi K2.5 | 🟢 10 |
| 12 | Content Planner | K2.5 / GLM-5 | 🟢 10† |
| 13 | Email Drafting | Kimi K2.5 | 🟢 10 |
| 14 | Doc Summary | K2.5 / GLM-5 | 🟢 8 |
| 15 | Meeting Notes | Kimi K2.5 | 🟢 10 |
| 16 | Social Scouting | K2.5 / GLM-5 | 🟢 10 |
| 17 | Social Content | 📝 Manual | 📝 5 |
| 18 | News Aggregation | K2.5 / GLM-5 | 🟢 10 |
| 19 | Shopping | K2.5 / GLM-5 | 🟢 10 |
| 20 | Memory Mgmt | K2.5 / GLM-5 | 🟢 9 |
| 21 | RAG / Retrieval | K2.5 / GLM-5 | 🟡 6 |
| 22 | Data Analysis | GLM-5 NoThink | 🔴 3 |
| 23 | Web Scraping | K2.5 / GLM-5 | 🟢 10† |
| 24 | Image Description | 📝 Manual | 📝 5 |
| 25 | Customer Support | K2.5 / GLM-5 | 🟢 10 |
| 26 | Lead Scoring | GLM-5 NoThink | 🟢 10 |
| 27 | Sprint Summary | GLM-5 | 🟢 9 |
| 28 | Transaction | GLM-5 | 🟢 10 |
| 29 | Home Automation | K2.5 / GLM-5 | 🟢 10 |
| 30 | Fitness Tracking | GLM-5 | 🟢 9 |
| 31 | Recipe / Cooking | GLM-5 | 🔴 2 |
| 32 | Personal Finance | GLM-5 | 🟡 7 |
| 33 | SEO Optimization | K2.5 / GLM-5 | 🟢 9 |
| 34 | Landing Page | 📝 Manual | 📝 5 |
| 35 | Travel Planning | Kimi K2.5 | 🟢 10 |
| | **Tier 3 — Advanced** | | |
| 36 | Code Generation | K2.5 / GLM-5 | 🟢 10† |
| 37 | Code Review | K2.5 / GLM-5 | 🟢 10 |
| 38 | QA / Test Writing | K2.5 / GLM-5 | 🟢 8 |
| 39 | Task Planning | Kimi K2.5 | 🟢 10 |
| 40 | Fact-Checking | K2.5 / GLM-5 | 🟢 10† |
| 41 | Critic / Review | 📝 Manual | 📝 5 |
| 42 | Market Research | K2.5 / GLM-5 | 🟢 8 |
| 43 | Synthesizer | Kimi K2.5 | 🟢 10 |
| 44 | Curriculum Design | Kimi K2.5 | 🟡 7 |
| 45 | Prototype Gen | GLM-5 NoThink | 🟡 7 |
| 46 | DevOps | Kimi K2.5 | 🟢 10 |
| | **Tier 4 — Expert** | | |
| 47 | Math / Logic | Kimi K2.5 | 🟢 8 |
| 48 | STEM Analysis | K2.5 / GLM-5 | 🟢 10† |
| 49 | Algorithm | GLM-5 Think | 🟢 10† |
| | **Tier 5 — Senior** | | |
| 50 | Orchestrator | GLM-5 Think | 🟢 8† |
| 51 | Architect | K2.5 / GLM-5 | 🟢 10† |
| 52 | Debugger | Kimi K2.5 | 🟢 10 |
| 53 | Legal Review | K2.5 / GLM-5 | 🟢 10 |
| 54 | Medical | GLM-5 | 🟢 10 |
| 55 | Financial | Kimi K2.5 | 🟢 10 |
| 56 | Security | K2.5 / GLM-5 | 🟢 10 |
| 57 | SRE / Incident | GLM-5 NoThink | 🟡 6 |
| 58 | Book Writing | 📝 Manual | 📝 5 |
| 59 | Compliance | Kimi K2.5 | 🟢 9 |

> † Phase G discriminator score · [☁️ Full cloud model comparison + speed data →](docs/results-cloud.md)

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
├── docs/                       # VRAM tier guides & model selection
│   ├── 16GB, 24GB, 32GB, 48GB, 64GB, 96GB tier guides
│   └── Subagent type reference
├── RESULTS.md                  # Detailed per-role score comparison
└── README.md
```

## 🗺️ Model Testing Roadmap

This is a living benchmark. We're continuously adding new models as they release. Here's what's on the radar — and we take requests.

**16GB VRAM tier (coming soon)**
- Qwen3-8B, Qwen3.5-14B
- Phi-4 14B, Phi-4-mini 3.8B
- Mistral Small 3.1 24B (tight fit)
- GPT-OSS-20B MXFP4
- Gemma 3 12B
- Ministral 3B (ultra-fast routing/triage)

**24GB VRAM tier**
- ✅ Qwen3.5-35B-A3B Q4_K_M (tested)
- ✅ Qwen3.5-27B Q4_K_M (tested)
- Gemma 3 27B QAT
- More MoE models as they release

**64–96GB VRAM tier**
- ✅ Qwen3.5-122B-A10B NVFP4 (tested)
- ✅ GPT-OSS-120B GGUF · llama.cpp (tested — 3 reasoning levels)
- More large models coming

**Cloud (open-source via API)**
- Open-source models via OpenRouter, Alibaba, and other affordable providers

> 💬 **Want us to test a specific model?** [Open an issue](https://github.com/explaindio/ClawEval/issues) or drop a comment — we prioritize community requests. New models are added as they release.

## 📄 License

MIT

## 🔗 Links

- **Newsletter**: [AIgenteur Dispatch](https://aigenteurdispatch.substack.com/) — subscribe for new benchmark results and AI agent guides
- **Community**: [AIgenteur Academy (free)](https://www.skool.com/aigenteur-academy-9764) — discuss results, get help, share what's working
- **GitHub**: [github.com/explaindio/ClawEval](https://github.com/explaindio/ClawEval)
