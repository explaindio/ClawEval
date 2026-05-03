# 🖥️ RTX 3090 (24GB VRAM) — Best Local Models

All models tested on a single NVIDIA RTX 3090 24GB. No cloud, no API costs — fully offline inference.

---

## 🏅 Local Model Leaderboard

| Rank | Model | Quant | Params | Score | % | Context |
|------|-------|-------|--------|-------|---|---------|
| 🥇 | **Qwen3.6-35B-A3B** | UD-Q4_K_M | 35B MoE (3B active) | 1029/1220 | **84.3%** | 32K |
| 🥈 | **Gemma-4-E2B** | BF16 | 2B | 981/1220 | **80.4%** | 32K |
| 🥉 | **Nemotron-Nano-Omni** (IQ4) | IQ4_NL_XL | 30B MoE (3B active) | 948/1220 | **77.7%** | 262K |
| 4 | **Gemma-4-31B** (TurboQuant3) | Q4_K_M + turbo3 KV | 31B | 1014/1220 | **83.1%** | 262K |
| 5 | **Gemma-4-31B** | Q4_K_M | 31B | 927/1220 | **76.0%** | 53K |
| 6 | **Nemotron-Nano-Omni** (Q4) | Q4_K_S | 30B MoE (3B active) | 925/1220 | **75.8%** | 262K |
| 7 | **Ministral-3 8B** | Q4_K_M | 8B | 884/1220 | **72.5%** | 32K |
| 8 | **Gemma-4-E4B** | BF16 | 4B | 867/1220 | **71.1%** | 32K |
| 9 | **Ministral-3 3B** | Q4_K_M | 3B | 760/1220 | **62.3%** | 32K |
| 10 | **Ministral-3 8B Think** | Q4_K_M | 8B | 791/1220 | **64.8%** | 32K |
| 11 | **Ministral-3 3B Think** | Q4_K_M | 3B | 704/1220 | **57.7%** | 32K |
| 12 | **Gemma-4-A4B** | UD-Q4_K_M | 26B MoE (4B active) | 622/1220 | **51.0%** | 32K |
| 13 | **Qwen3.5-9B** | Q4_K_M | 9B | 543/1220 | **44.5%** | 32K |
| 14 | **Qwen3.5-4B** | Q4_K_M | 4B | 374/1220 | **30.7%** | 32K |
| 15 | **LFM2.5-350M** | Q4_K_M | 350M | 308/1220 | **25.2%** | 32K |
| 16 | **Qwen3.5-0.8B** | Q4_K_M | 0.8B | 58/1220 | **4.8%** | 32K |
| 17 | **Qwen3.5-2B** | Q4_K_M | 2B | 50/1220 | **4.1%** | 32K |

> Qwen3.6-35B-A3B at 84.3% **ties Kimi K2.6 cloud** — the best local model matches top-tier cloud APIs.

---

## ⚡ Throughput (Tokens/Second)

| Model | Quant | Avg t/s | Min t/s | Max t/s |
|-------|-------|---------|---------|---------|
| LFM2.5-350M | Q4_K_M | 628.3 | 178.9 | 712.2 |
| Qwen3.5-0.8B | Q4_K_M | 258.3 | 255.2 | 275.7 |
| Qwen3.5-2B | Q4_K_M | 212.8 | 208.2 | 232.3 |
| Nemotron-Nano-Omni (IQ4) | IQ4_NL_XL | 127.1 | — | 144.9 |
| Nemotron-Nano-Omni (Q4) | Q4_K_S | 123.4 | — | 148.3 |
| Qwen3.5-4B | Q4_K_M | 119.5 | 115.5 | 135.0 |
| Ministral-3 3B | Q4_K_M | 174.8 | 142.7 | 184.0 |
| Ministral-3 3B Think | Q4_K_M | 165.9 | 146.0 | 182.2 |
| Ministral-3 8B | Q4_K_M | 102.3 | 92.7 | 107.0 |
| Ministral-3 8B Think | Q4_K_M | 99.3 | 89.3 | 105.3 |
| Gemma-4-E2B | BF16 | 101.1 | 98.9 | 111.7 |
| Qwen3.6-35B-A3B | UD-Q4_K_M | 99.3 | 94.8 | 108.6 |
| Gemma-4-A4B | UD-Q4_K_M | 89.6 | 82.5 | 106.4 |
| Qwen3.5-9B | Q4_K_M | 90.3 | 87.3 | 101.1 |
| Gemma-4-E4B | BF16 | 61.8 | 59.7 | 66.0 |
| Gemma-4-31B | Q4_K_M | 28.1 | 25.9 | 33.7 |
| Gemma-4-31B (TQ3) | Q4_K_M + turbo3 | 27.1 | — | 32.8 |

---

## 🎯 Best Model Per Agent Role

Which local model to pick for each of the 59 agent roles. Qwen3.6-35B-A3B dominates with **36/59 wins**.

| Wins | Model | Best For |
|------|-------|----------|
| **36** | Qwen3.6-35B-A3B | Most roles — general champion |
| **6** | Gemma-4-31B | Research, scheduling, notifications, social media, finance |
| **6** | Nemotron-Nano-Omni (IQ4) | Content writing, editing, debugging, security, RAG |
| **4** | Nemotron-Nano-Omni (Q4) | Router/triage, DevOps, legal, SRE |
| **3** | Gemma-4-E2B | Customer support, transactions, compliance |
| **2** | Gemma-4-A4B | Email drafting, social media monitoring |
| **2** | Gemma-4-E4B | Task planning, SEO |

### Full Role Breakdown

| Test | Agent Role | Best Local Model | Score | % |
|------|-----------|-----------------|-------|---|
| H-01 | Router / Triage Agent | Nemotron-Nano-Omni (Q4) | 29/30 | 97% |
| H-02 | Input Validator / Sanitizer | Qwen3.6-35B-A3B | 29/30 | 97% |
| H-03 | Heartbeat / Health Monitor | Gemma-4-31B | 15/15 | 100% |
| H-04 | Notification / Alert Agent | Gemma-4-31B | 25/30 | 83% |
| H-05 | Sentiment Analysis Agent | Qwen3.6-35B-A3B | 27/30 | 90% |
| H-06 | FAQ Generation Agent | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-07 | Translation Agent | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-08 | Calendar / Scheduling Agent | Gemma-4-31B | 12/20 | 60% |
| H-09 | Research / Web Search Agent | Gemma-4-31B | 30/30 | 100% |
| H-10 | Content Writer / Blog Writer | Nemotron-Nano-Omni (IQ4) | 20/20 | 100% |
| H-11 | Editor Agent | Nemotron-Nano-Omni (IQ4) | 29/30 | 97% |
| H-12 | Content Planner / Strategist | Qwen3.6-35B-A3B | 26/30 | 87% |
| H-13 | Email Drafting / Summarization | Gemma-4-A4B | 44/45 | 98% |
| H-14 | Document Summarization Agent | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-15 | Meeting Notes / Transcription | Qwen3.6-35B-A3B | 34/35 | 97% |
| H-16 | Social Media Scouting | Gemma-4-A4B | 57/60 | 95% |
| H-17 | Social Media Content Agent | Gemma-4-31B | 20/20 | 100% |
| H-18 | News Aggregation Agent | Qwen3.6-35B-A3B | 7/7 | 100% |
| H-19 | Shopping / Price Comparison | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-20 | Memory / Knowledge Management | Qwen3.6-35B-A3B | 20/20 | 100% |
| H-21 | RAG / Retrieval Agent | Nemotron-Nano-Omni (IQ4) | 13/15 | 87% |
| H-22 | Data Analysis Agent | Qwen3.6-35B-A3B | 14/15 | 93% |
| H-23 | Website Scraping / Understanding | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-24 | Image Description / Understanding | Qwen3.6-35B-A3B | 20/20 | 100% |
| H-25 | Customer Support Agent | Gemma-4-E2B | 53/60 | 88% |
| H-26 | Lead Scoring / Prospecting | Qwen3.6-35B-A3B | 13/15 | 87% |
| H-27 | Sprint / Project Summarizer | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-28 | Transaction / Approval Agent | Gemma-4-E2B | 19/20 | 95% |
| H-29 | Home Automation Agent | Qwen3.6-35B-A3B | 7/20 | 35% |
| H-30 | Fitness / Health Tracking | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-31 | Recipe / Cooking Agent | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-32 | Personal Finance Tracking | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-33 | SEO Optimization Agent | Gemma-4-E4B | 9/15 | 60% |
| H-34 | Landing Page Generator | Qwen3.6-35B-A3B | 20/20 | 100% |
| H-35 | Travel Planning Agent | Nemotron-Nano-Omni (IQ4) | 7/15 | 47% |
| H-36 | Code Generation Agent | Qwen3.6-35B-A3B | 30/30 | 100% |
| H-37 | Code Review Agent | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-38 | QA / Test Writing Agent | Qwen3.6-35B-A3B | 13/15 | 87% |
| H-39 | Task Planning / Decomposition | Gemma-4-E4B | 8/18 | 44% |
| H-40 | Fact-Checking Agent | Qwen3.6-35B-A3B | 29/30 | 97% |
| H-41 | Critic / Review Agent | Qwen3.6-35B-A3B | 20/20 | 100% |
| H-42 | Market Research Agent | Qwen3.6-35B-A3B | 14/15 | 93% |
| H-43 | Synthesizer / Aggregator | Qwen3.6-35B-A3B | 13/15 | 87% |
| H-44 | Curriculum / Course Designer | Qwen3.6-35B-A3B | 7/15 | 47% |
| H-45 | Prototype Generator | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-46 | DevOps Agent | Nemotron-Nano-Omni (Q4) | 8/15 | 53% |
| H-47 | Math / Logic Reasoning | Qwen3.6-35B-A3B | 14/15 | 93% |
| H-48 | STEM Research Analyst | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-49 | Algorithm / Data Structure | Qwen3.6-35B-A3B | 30/30 | 100% |
| H-50 | Orchestrator / Manager Agent | Qwen3.6-35B-A3B | 13/15 | 87% |
| H-51 | Software Architect Agent | Qwen3.6-35B-A3B | 6/15 | 40% |
| H-52 | Complex Debugger Agent | Nemotron-Nano-Omni (IQ4) | 15/15 | 100% |
| H-53 | Legal Document Review | Nemotron-Nano-Omni (Q4) | 8/15 | 53% |
| H-54 | Medical / Health Analysis | Qwen3.6-35B-A3B | 15/15 | 100% |
| H-55 | Financial Analysis / Stock Research | Gemma-4-31B | 15/15 | 100% |
| H-56 | Security Analyst Agent | Nemotron-Nano-Omni (IQ4) | 15/15 | 100% |
| H-57 | SRE / Incident Response | Nemotron-Nano-Omni (Q4) | 13/15 | 87% |
| H-58 | Book / Long-Form Writing | Qwen3.6-35B-A3B | 20/20 | 100% |
| H-59 | Compliance / Regulatory Agent | Gemma-4-E2B | 6/15 | 40% |

---

## 🧠 Key Insights

### Pick Your Priority

| Priority | Recommended Model | Why |
|----------|------------------|-----|
| **Best accuracy** | Qwen3.6-35B-A3B | 84.3% — ties cloud-tier models |
| **Best speed + quality** | Gemma-4-E2B | 101 t/s at 80.4% — tiny 2B model |
| **Fastest 70%+** | Nemotron-Nano-Omni (IQ4) | 127 t/s at 77.7% |
| **Longest context** | Gemma-4-31B (TQ3) or Nemotron-Omni | 262K tokens |
| **Maximum throughput** | LFM2.5-350M | 628 t/s (but only 25.2% accuracy) |

### Quant Sensitivity Finding

Nemotron-Nano-Omni IQ4_NL_XL (lower-quality quant) **outperformed** Q4_K_S (higher-quality) by +3.4%. The smaller quant leaves more VRAM headroom, which may reduce KV-cache pressure and improve generation quality.

### Thinking Model Warning ⚠️

Small thinking models are **dramatically worse** than non-thinking models of the same size for agent tasks:

| Model | Type | Params | Score | Failure Mode |
|-------|------|--------|-------|-------------|
| Gemma-4-E4B | Non-thinking | 4B | **71.1%** | — |
| Qwen3.5-4B | Thinking | 4B | **30.7%** | 38/59 tests scored 0 — 20 unparseable JSON, 6 empty responses |
| Gemma-4-E2B | Non-thinking | 2B | **80.4%** | — |
| Qwen3.5-2B | Thinking | 2B | **4.1%** | Nearly all tests failed |
| Qwen3.5-0.8B | Thinking | 0.8B | **4.8%** | Nearly all tests failed |

**Why?** Thinking models spend tokens on chain-of-thought reasoning *before* producing the answer. At small sizes (≤4B), the CoT consumes most of the token budget, leaving the model unable to produce structured output. Even with `reasoning_budget_tokens` caps, the model's capacity is too limited to both reason *and* format answers correctly.

**Takeaway:** For local agent deployment, prefer non-thinking models at ≤4B. Thinking architectures only become viable at ≥30B MoE (e.g. Qwen3.6-35B-A3B at 84.3%).
