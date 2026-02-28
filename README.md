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

| 🟡 16GB VRAM | 🟢 24GB VRAM | 🔵 96GB VRAM |
|---|---|---|
| Qwen3-8B, Phi-4 14B | Qwen3.5-35B-A3B Q4_K_M | Qwen3.5-122B-A10B NVFP4 |
| Mistral Small 24B, GPT-OSS-20B | Qwen3.5-27B Q4_K_M | More models coming |
| Coming soon | llama.cpp · SGLang · vLLM | SGLang · vLLM |

> 📖 **VRAM Guides:** [16GB](docs/OpenClaw%2016GB%20VRAM%20Local%20LLM%20Subagents.md) · [24GB](docs/The%2024GB%20VRAM%20Tier_%20Where%20Local%20AI%20Agents%20Get%20Serious.md) · [32GB](docs/openclaw-model-selection-32gb-tier.md) · [48GB](docs/openclaw-48gb-tier.md) · [64GB](docs/openclaw-64gb-tier.md) · [96GB](docs/openclaw-96gb-tier.md) — Which models fit, context limits, speed estimates

### ☁️ CLOUD Models — Run via API

Don't have a GPU? We also test open-source models hosted on cloud providers so you can compare **local vs cloud performance at every agent role.** Same tests, same scoring — find out if paying for cloud is worth it, or if your local setup already matches.

| Provider | Models | Status |
|---|---|---|
| OpenRouter, Chutes, and other affordable providers | Open-source models via API | 🔜 Coming soon |


## 🏆 Per-Role Agent Scores (Phase F — 59 Roles)

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual (5) &nbsp; ⬛ = Thinking overflow

Best config per model. All scores out of 10. For think/nothink comparisons, see the VRAM tier tables below.

> 📊 **[Full detailed results with all configs →](RESULTS.md)**

| # | Agent Role | 122B (96GB) | 35B MoE (24GB) | 27B Dense (24GB) |
|---|---|---|---|---|
| | | Qwen3.5-122B-A10B | Qwen3.5-35B-A3B | Qwen3.5-27B |
| | | NVFP4 · Think 16K · SGLang | Q4_K_M · NoThink · llama.cpp | Q4_K_M · NoThink · llama.cpp |
| | **Tier 1 — Utility** | | | |
| 1 | Router / Triage | 🟢 10 | 🟢 10 | 🟢 9 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🔴 3 | 🔴 3 | 🔴 3 |
| 4 | Notification | 🟢 8 | 🟢 8 | 🟢 8 |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 5 | 🟡 6 | 🟡 6 |
| 7 | Translation | 🟢 10 | 🟢 9 | 🟢 10 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | |
| 9 | Research Agent | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟡 7 | 🟢 10 | 🟢 10 |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟢 8 | 🟢 10 | 🟢 10 |
| 14 | Doc Summary | 🟢 8 | 🟢 10 | 🟢 10 |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🔴 4 | 🔴 4 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 6 | 🔴 4 | 🟡 6 |
| 22 | Data Analysis | 🔴 2 | 🔴 3 | 🔴 3 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 9 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 10 |
| 27 | Sprint Summary | 🟢 10 | 🟡 5 | 🟡 7 |
| 28 | Transaction | 🟢 10 | 🟢 9 | 🟢 8 |
| 29 | Home Automation | 🟢 10 | 🟢 9 | 🟢 9 |
| 30 | Fitness Tracking | 🟢 9 | 🟡 7 | 🟢 9 |
| 31 | Recipe / Cooking | 🔴 2 | 🟢 9 | 🔴 2 |
| 32 | Personal Finance | 🟡 7 | 🔴 4 | 🔴 4 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 8 | 🟡 7 | 🟡 7 |
| | **Tier 3 — Advanced** | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 10 | 🟢 8 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 10 | 🟢 8 |
| 39 | Task Planning | 🟢 9 | 🟢 10 | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🔴 0 | 🟡 7 | 🟢 8 |
| 43 | Synthesizer | 🟡 7 | 🟢 9 | 🟡 7 |
| 44 | Curriculum Design | 🟡 6 | 🟡 6 | 🟡 5 |
| 45 | Prototype Gen | 🟡 6 | 🟡 6 | 🟡 6 |
| 46 | DevOps | 🟡 7 | 🟢 9 | 🟢 10 |
| | **Tier 4 — Expert** | | | |
| 47 | Math / Logic | 🟡 6 | 🔴 4 | 🔴 4 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 10 | 🟢 10 | 🟢 10 |
| 52 | Debugger | 🟢 10 | 🟢 10 | 🟢 8 |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 |
| 54 | Medical | 🟡 7 | 🟢 10 | 🟢 10 |
| 55 | Financial | 🟢 10 | 🟢 10 | 🟢 10 |
| 56 | Security | 🟡 6 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🟡 6 | 🔴 3 | 🟡 6 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟡 7 | 🟢 8 | 🟢 9 |

---

### 🟢 24GB VRAM — Think vs NoThink (RTX 3090)

All tested with Q4_K_M quantization, KV cache q8_0, on llama.cpp.

| # | Agent Role | 35B-A3B Think | 35B-A3B NoThink | 27B Think | 27B NoThink |
|---|---|---|---|---|---|
| | **Tier 1 — Utility** | | | | |
| 1 | Router / Triage | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | ⬛ 0 | 🔴 3 | ⬛ 0 | 🔴 3 |
| 4 | Notification | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 8 |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 6 | 🟡 6 | 🟢 8 | 🟡 6 |
| 7 | Translation | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 |
| 8 | Calendar | 🔴 0 | 🔴 0 | ⬛ 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | |
| 9 | Research Agent | ⬛ 0 | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 10 |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | ⬛ 0 | 🟢 10 | 🟢 9 | 🟢 10 |
| 14 | Doc Summary | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 10 |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🔴 4 | 🟢 10 | 🔴 4 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 6 | 🔴 4 | 🟡 6 | 🟡 6 |
| 22 | Data Analysis | ⬛ 0 | 🔴 3 | ⬛ 0 | 🔴 3 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 10 |
| 27 | Sprint Summary | ⬛ 0 | 🟡 5 | ⬛ 0 | 🟡 7 |
| 28 | Transaction | ⬛ 0 | 🟢 9 | ⬛ 0 | 🟢 8 |
| 29 | Home Automation | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 9 |
| 30 | Fitness Tracking | 🟢 9 | 🟡 7 | 🟢 9 | 🟢 9 |
| 31 | Recipe / Cooking | ⬛ 0 | 🟢 9 | 🔴 2 | 🔴 2 |
| 32 | Personal Finance | ⬛ 0 | 🔴 4 | 🟡 7 | 🔴 4 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🔴 0 | 🟡 7 | ⬛ 0 | 🟡 7 |
| | **Tier 3 — Advanced** | | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 8 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 8 |
| 39 | Task Planning | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | ⬛ 0 | 🟡 7 | 🟡 6 | 🟢 8 |
| 43 | Synthesizer | 🟢 9 | 🟢 9 | 🟢 9 | 🟡 7 |
| 44 | Curriculum Design | 🟡 6 | 🟡 6 | 🟡 6 | 🟡 5 |
| 45 | Prototype Gen | 🟡 6 | 🟡 6 | 🟡 5 | 🟡 6 |
| 46 | DevOps | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 |
| | **Tier 4 — Expert** | | | | |
| 47 | Math / Logic | 🟡 6 | 🔴 4 | 🟡 6 | 🔴 4 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 52 | Debugger | 🟢 8 | 🟢 10 | ⬛ 0 | 🟢 8 |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 54 | Medical | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 55 | Financial | 🟢 10 | 🟢 10 | ⬛ 0 | 🟢 10 |
| 56 | Security | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | ⬛ 0 | 🔴 3 | 🔴 3 | 🟡 6 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 9 |

> ⬛ **Thinking overflow:** llama.cpp has no `thinking_budget`, so thinking models can consume all tokens on reasoning before outputting an answer. 35B-Think: 10 overflows, 27B-Think: 9 overflows. These scores would be higher on vLLM/SGLang with proper budget control.

---

### 🔵 96GB VRAM (RTX PRO 6000 Blackwell)

Only 1 model tested so far — more coming.

| # | Agent Role | 122B Think 16K |
|---|---|---|
| | | Qwen3.5-122B-A10B · NVFP4 · SGLang |
| | **Tier 1 — Utility** | |
| 1 | Router / Triage | 🟢 10 |
| 2 | Input Validator | 🟢 10 |
| 3 | Health Monitor | 🔴 3 |
| 4 | Notification | 🟢 8 |
| 5 | Sentiment | 🟢 10 |
| 6 | FAQ Generation | 🟡 5 |
| 7 | Translation | 🟢 10 |
| 8 | Calendar | 🔴 0 |
| | **Tier 2 — Moderate** | |
| 9 | Research Agent | 🟢 10 |
| 10 | Content Writer | 📝 5 |
| 11 | Editor | 🟡 7 |
| 12 | Content Planner | 🟢 10 |
| 13 | Email Drafting | 🟢 8 |
| 14 | Doc Summary | 🟢 8 |
| 15 | Meeting Notes | 🟢 9 |
| 16 | Social Scouting | 🟢 10 |
| 17 | Social Content | 📝 5 |
| 18 | News Aggregation | 🟢 10 |
| 19 | Shopping | 🟢 10 |
| 20 | Memory Mgmt | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 6 |
| 22 | Data Analysis | 🔴 2 |
| 23 | Web Scraping | 🟢 10 |
| 24 | Image Description | 📝 5 |
| 25 | Customer Support | 🟢 10 |
| 26 | Lead Scoring | 🟢 8 |
| 27 | Sprint Summary | 🟢 10 |
| 28 | Transaction | 🟢 10 |
| 29 | Home Automation | 🟢 10 |
| 30 | Fitness Tracking | 🟢 9 |
| 31 | Recipe / Cooking | 🔴 2 |
| 32 | Personal Finance | 🟡 7 |
| 33 | SEO Optimization | 🟢 9 |
| 34 | Landing Page | 📝 5 |
| 35 | Travel Planning | 🟢 8 |
| | **Tier 3 — Advanced** | |
| 36 | Code Generation | 🟢 10 |
| 37 | Code Review | 🟢 10 |
| 38 | QA / Test Writing | 🟢 8 |
| 39 | Task Planning | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 |
| 41 | Critic / Review | 📝 5 |
| 42 | Market Research | 🔴 0 |
| 43 | Synthesizer | 🟡 7 |
| 44 | Curriculum Design | 🟡 6 |
| 45 | Prototype Gen | 🟡 6 |
| 46 | DevOps | 🟡 7 |
| | **Tier 4 — Expert** | |
| 47 | Math / Logic | 🟡 6 |
| 48 | STEM Analysis | 🟢 10 |
| 49 | Algorithm | 🟢 10 |
| | **Tier 5 — Senior** | |
| 50 | Orchestrator | 🟢 8 |
| 51 | Architect | 🟢 10 |
| 52 | Debugger | 🟢 10 |
| 53 | Legal Review | 🟢 10 |
| 54 | Medical | 🟡 7 |
| 55 | Financial | 🟢 10 |
| 56 | Security | 🟡 6 |
| 57 | SRE / Incident | 🟡 6 |
| 58 | Book Writing | 📝 5 |
| 59 | Compliance | 🟡 7 |

> ⭐ Star this repo to get notified when new 96GB models are added.

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

**96GB VRAM tier**
- ✅ Qwen3.5-122B-A10B NVFP4 (tested)
- More large models coming

**Cloud (open-source via API)**
- Open-source models via OpenRouter, Chutes, and other affordable providers

> 💬 **Want us to test a specific model?** [Open an issue](https://github.com/explaindio/ClawEval/issues) or drop a comment — we prioritize community requests. New models are added as they release.

## 📄 License

MIT

## 🔗 Links

- **Newsletter**: [AIgenteur Dispatch](https://aigenteurdispatch.substack.com/) — subscribe for new benchmark results and AI agent guides
- **Community**: [AIgenteur Academy (free)](https://www.skool.com/aigenteur-academy-9764) — discuss results, get help, share what's working
- **GitHub**: [github.com/explaindio/ClawEval](https://github.com/explaindio/ClawEval)
