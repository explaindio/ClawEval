# 🔴 Small VRAM Models — Phase F (59-Role Evaluation)

[← Back to Main Results](../README.md) · [Phase G Discriminator Tests →](results-phase-g.md)

All tested with Q4_K_M quantization, KV cache q8_0, on llama.cpp (local server).

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual review (5)

| # | Agent Role | 0.8B Think | 0.8B NT | 2B Think | 2B NT | 4B Think | 4B NT | 9B Think | 9B NT | Mini3 3B | Mini3 8B | Mini3 14B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | Qwen3.5-0.8B | Qwen3.5-0.8B | Qwen3.5-2B | Qwen3.5-2B | Qwen3.5-4B | Qwen3.5-4B | Qwen3.5-9B | Qwen3.5-9B | Ministral | Ministral | Ministral |
| | **Tier 1 — Utility** | | | | | | | | | | | |
| 1 | Router / Triage | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🔴 2 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🟡 5 | 🟡 5 |
| 4 | Notification | 🟡 6 | 🟡 6 | 🟢 9 | 🟢 9 | 🟡 7 | 🟡 7 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 9 |
| 5 | Sentiment | 🟡 6 | 🔴 4 | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 8 | 🟢 9 |
| 6 | FAQ Generation | 🔴 1 | 🔴 3 | 🟡 5 | 🟡 5 | 🟡 6 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 6 | 🟡 7 | 🟡 6 |
| 7 | Translation | 🟡 7 | 🟢 9 | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | | | | | | | | |
| 9 | Research Agent | 🟡 6 | 🟡 6 | 🟢 9 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 10 | 🟡 7 | 🟢 8 | 🟢 9 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟡 6 | 🔴 4 | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 8 | 🟡 6 | 🟢 8 |
| 14 | Doc Summary | 🟡 6 | 🟢 8 | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 19 | 🟢 18 | 🟢 19 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🔴 4 | 🔴 2 | 🔴 0 | 🔴 2 | 🔴 2 | 🔴 0 | 🔴 4 | 🟢 8 | 🔴 0 | 🔴 0 | 🔴 4 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 8 |
| 21 | RAG / Retrieval | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | 🔴 2 |
| 22 | Data Analysis | 🔴 1 | 🔴 0 | 🔴 3 | 🔴 2 | 🔴 2 | 🔴 3 | 🔴 2 | 🔴 4 | 🔴 2 | 🔴 2 | 🔴 1 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟡 6 | 🟡 6 | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 9 |
| 26 | Lead Scoring | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | 🟡 6 | 🟡 6 | 🟢 8 | 🟢 8 | 🔴 4 | 🟢 8 | 🔴 4 |
| 27 | Sprint Summary | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | 🟡 6 | 🟡 6 | 🟡 7 | 🟡 7 | 🟡 5 | 🟡 6 | 🟡 5 |
| 28 | Transaction | 🔴 1 | 🔴 1 | 🟢 9 | 🟢 9 | 🟢 8 | 🟢 8 | 🔴 4 | 🟡 6 | 🔴 0 | 🟡 7 | 🟢 8 |
| 29 | Home Automation | 🟡 7 | 🟢 10 | 🟡 7 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 8 |
| 30 | Fitness Tracking | 🔴 3 | 🔴 3 | 🔴 4 | 🔴 3 | 🔴 4 | 🟡 5 | 🟡 6 | 🟡 6 | 🔴 0 | 🟡 5 | 🟡 5 |
| 31 | Recipe / Cooking | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 0 | 🔴 3 | 🔴 2 |
| 32 | Personal Finance | 🔴 3 | 🔴 3 | 🔴 4 | 🔴 4 | 🔴 4 | 🟡 5 | 🟡 5 | 🔴 4 | 🔴 4 | 🔴 3 | 🔴 4 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🔴 4 | 🔴 4 | 🟡 6 | 🟡 6 | 🟡 7 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 9 | 🟢 10 |
| | **Tier 3 — Advanced** | | | | | | | | | | | |
| 36 | Code Generation | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 | 🟢 10 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟡 7 | 🟡 7 | 🟢 8 | 🟢 8 | 🟢 10 | 🟡 7 | 🟡 7 |
| 39 | Task Planning | 🟢 9 | 🟡 7 | 🟢 10 | 🟢 8 | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 |
| 40 | Fact-Checking | 🟡 5 | 🔴 4 | 🟡 6 | 🟡 6 | 🟢 9 | 🟢 9 | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🔴 4 | 🔴 4 | 🔴 3 | 🔴 3 | 🟡 6 | 🟡 6 | 🟡 6 | 🟡 6 | 🔴 1 | 🔴 3 | 🟡 5 |
| 43 | Synthesizer | 🟢 9 | 🟢 9 | 🟡 7 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 10 |
| 44 | Curriculum Design | 🔴 4 | 🔴 4 | 🟡 7 | 🟡 7 | 🟡 6 | 🟡 7 | 🟡 6 | 🟡 7 | 🟡 7 | 🟢 8 | 🟢 9 |
| 45 | Prototype Gen | 🟡 7 | 🔴 2 | 🟡 6 | 🟡 7 | 🟡 5 | 🟡 5 | 🟡 6 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 |
| 46 | DevOps | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 |
| | **Tier 4 — Expert** | | | | | | | | | | | |
| 47 | Math / Logic | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | 🔴 4 | 🔴 4 | 🔴 4 | 🔴 4 | 🔴 2 | 🔴 4 | 🔴 4 |
| 48 | STEM Analysis | 🔴 0 | 🔴 0 | 🔴 2 | 🔴 2 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🔴 0 | 🔴 0 | 🔴 0 |
| 49 | Algorithm | 🟡 5 | 🔴 0 | 🔴 0 | 🔴 0 | 🟢 10 | 🟢 10 | 🔴 0 | 🔴 0 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | | | | | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 8 |
| 51 | Architect | 🟢 8 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 52 | Debugger | 🟡 6 | 🟢 10 | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 54 | Medical | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 |
| 55 | Financial | 🔴 2 | 🔴 1 | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟡 5 | 🟢 10 |
| 56 | Security | 🟡 6 | 🔴 3 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🔴 2 | 🔴 2 | 🔴 3 | 🔴 2 | 🔴 4 | 🔴 4 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟡 7 | 🟡 7 | 🟢 9 | 🟡 7 | 🟢 8 |
| | **TOTAL** | **339/585 (57.9%)** | **331/585 (56.6%)** | **392/590 (66.4%)** | **392/590 (66.4%)** | **440/590 (74.6%)** | **442/590 (74.9%)** | **433/590 (73.4%)** | **444/590 (75.3%)** | **69.0%** | **72.7%** | **74.1%** |

### Notes

- Social Scouting (#16) scored 16/10 due to scoring bug — capped to 10 in totals above
- STEM (#48) scored 0/5 (not 0/10) — model generated degenerate repetitive output filling the token limit
- Algorithm (#49): 9B scored 0/10 because it named the class `LRUCache` (PascalCase) instead of the prompt's `lru_cache`. The code is functionally correct — Phase G confirms 9/10 on the harder version of this test
- Think and NoThink perform nearly identically for all small models — they don't produce meaningful chain-of-thought at this size

---

## Phase G — Discriminator Tests (Small Models)

| # | Test | 0.8B Think | 0.8B NT | 2B Think | 2B NT | 4B Think | 4B NT | 9B Think | 9B NT | Mini3 3B | Mini3 8B | Mini3 14B |
|---|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 36 | Code Gen (RateLimiter) | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 4 | 🔴 4 | 🟢 10 | 🟢 10 |
| 2 | Input Validator (nested) | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 5 | Sentiment (hard, 20 items) | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 |
| 40 | Fact-Checking (plausible) | 🔴 0 | 🔴 0 | 🟡 7 | 🟡 7 | 🟡 6 | 🟡 6 | 🟢 8 | 🟢 8 |
| 49 | Algorithm (LRU+TTL) | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 51 | Architect (trade-offs) | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 |
| 48 | STEM (multi-step calc) | 🔴 0 | 🔴 0 | 🔴 1 | 🔴 1 | 🔴 2 | 🔴 2 | 🔴 1 | 🔴 1 |
| 9 | Research (contradictions) | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 | 🟢 10 |
| 12 | Content Planner (15 constraints) | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 | 🟢 8 | 🟢 8 | 🟡 7 | 🟡 7 |
| 23 | Web Scraping (messy HTML) | 🔴 0 | 🔴 0 | 🟡 6 | 🟡 6 | 🟢 8 | 🟡 6 | 🟢 8 | 🟢 8 |
| | **TOTAL** | **33/110 (30.0%)** | **33/110 (30.0%)** | **52/110 (47.3%)** | **52/110 (47.3%)** | **73/110 (66.4%)** | **71/110 (64.5%)** | **81/110 (73.6%)** | **81/110 (73.6%)** |

---

## Summary — Best Score Per VRAM Tier

| VRAM | Best Model | Phase F | Phase G |
|------|-----------|:---:|:---:|
| **8GB** | Qwen3.5-4B NT | 442/590 (75%) | 71/110 (65%) |
| **12GB** | Qwen3.5-4B Think | 440/590 (75%) | 73/110 (66%) |
| **16GB** | Qwen3.5-9B NT | 444/590 (75%) | 81/110 (74%) |
| **24GB** | Qwen3.5-35B-A3B NT | 433/590 (73%) | 77/110 (70%) |

---

## 📐 Max Context Per VRAM Tier

**GPU**: RTX 3090 (24 GB) | **FA**: On | **Quant**: Q4_K_M | **Native max**: 262,144 tokens

Context capped at native max. If native max fits at a lower VRAM tier, higher tiers show ✅ (skipped).

### Quick Summary — q8_0 KV (recommended)

| Model | File | Base VRAM | 8 GB | 12 GB | 16 GB | 24 GB |
|-------|------|-----------|------|-------|-------|-------|
| **Qwen3.5-0.8B** | 0.5 GB | 1,343 MiB | **262K ⭐** | ✅ | ✅ | ✅ |
| **Qwen3.5-2B** | 1.3 GB | 2,061 MiB | **262K ⭐** | ✅ | ✅ | ✅ |
| **Ministral-3-3B** | 2.1 GB | 2,665 MiB | 100K | 172K | 245K | 256K |
| **Qwen3.5-4B** | 2.7 GB | 3,501 MiB | **262K ⭐** | ✅ | ✅ | ✅ |
| **Ministral-3-8B** | 5.2 GB | 5,307 MiB | 40K | 97K | 152K | 256K |
| **Qwen3.5-9B** | 5.7 GB | 5,765 MiB | 145K | **262K ⭐** | ✅ | ✅ |
| **Ministral-3-14B** | 8.2 GB | 8,149 MiB | ❌ | 50K | 97K | 256K |

⭐ = native max reached | ✅ = same (skipped)

### Quick Summary — f16 KV

| Model | File | Base VRAM | 8 GB | 12 GB | 16 GB | 24 GB |
|-------|------|-----------|------|-------|-------|-------|
| **Qwen3.5-0.8B** | 0.5 GB | 1,343 MiB | **262K ⭐** | ✅ | ✅ | ✅ |
| **Qwen3.5-2B** | 1.3 GB | 2,061 MiB | **262K ⭐** | ✅ | ✅ | ✅ |
| **Ministral-3-3B** | 2.1 GB | 2,665 MiB | 52K | 92K | 132K | 207K |
| **Qwen3.5-4B** | 2.7 GB | 3,501 MiB | 150K | **262K ⭐** | ✅ | ✅ |
| **Ministral-3-8B** | 5.2 GB | 5,307 MiB | 20K | 50K | 82K | 140K |
| **Qwen3.5-9B** | 5.7 GB | 5,765 MiB | 77K | 202K | **262K ⭐** | ✅ |
| **Ministral-3-14B** | 8.2 GB | 8,149 MiB | ❌ | 25K | 52K | 100K |

### Architecture Impact on Context Length

Qwen3.5 uses a **hybrid DeltaNet + Attention** architecture (only 1 in 4 layers uses full attention), resulting in dramatically lower KV cache cost per token compared to Ministral's standard Transformer attention:

| Model | KV Cost (q8_0) per 1K tokens | Architecture |
|-------|------------------------------|-------------|
| Qwen3.5-0.8B | ~7 MiB | Hybrid DeltaNet |
| Qwen3.5-2B | ~8 MiB | Hybrid DeltaNet |
| Qwen3.5-4B | ~18 MiB | Hybrid DeltaNet |
| Qwen3.5-9B | ~33 MiB | Hybrid DeltaNet |
| Ministral-3-3B | ~55 MiB | Standard Attention |
| Ministral-3-8B | ~73 MiB | Standard Attention |
| Ministral-3-14B | ~113 MiB | Standard Attention |

> Qwen3.5 models achieve **3-6× more context** than equivalently-sized Ministral models at the same VRAM budget, purely due to the hybrid architecture.

---

### Detailed Results — Qwen3.5

#### Qwen3.5-0.8B

**File**: 0.5 GB | **Base VRAM**: 1,343 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 262,144 ⭐ | 262,144 ⭐ |
| 12GB | ✅ | ✅ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

#### Qwen3.5-2B

**File**: 1.3 GB | **Base VRAM**: 2,061 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 262,144 ⭐ | 262,144 ⭐ |
| 12GB | ✅ | ✅ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

#### Qwen3.5-4B

**File**: 2.7 GB | **Base VRAM**: 3,501 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 150,000 | 250,000 |
| 12GB | 262,144 ⭐ | 262,144 ⭐ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

#### Qwen3.5-9B

**File**: 5.7 GB | **Base VRAM**: 5,765 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 77,500 | 145,000 |
| 12GB | 202,500 | 262,144 ⭐ |
| 16GB | 262,144 ⭐ | ✅ |
| 24GB | ✅ | ✅ |

---

### Detailed Results — Ministral 3

#### Ministral-3-3B

**File**: 2.1 GB | **Base VRAM**: 2,665 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 52,500 | 100,000 |
| 12GB | 92,500 | 172,500 |
| 16GB | 132,500 | 245,000 |
| 24GB | 207,500 | 256,000 |

#### Ministral-3-8B

**File**: 5.2 GB | **Base VRAM**: 5,307 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 20,000 | 40,000 |
| 12GB | 50,000 | 97,500 |
| 16GB | 82,500 | 152,500 |
| 24GB | 140,000 | 256,000 |

#### Ministral-3-14B

**File**: 8.2 GB | **Base VRAM**: 8,149 MiB

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | ❌ | ❌ |
| 12GB | 25,000 | 50,000 |
| 16GB | 52,500 | 97,500 |
| 24GB | 100,000 | 256,000 |

---

[← Back to Main Results](../README.md)

