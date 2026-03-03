# 🔴 Small VRAM Models — Phase F (59-Role Evaluation)

[← Back to Main Results](../README.md) · [Phase G Discriminator Tests →](results-phase-g.md)

All tested with Q4_K_M quantization, KV cache q8_0, on llama.cpp (local server).

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual review (5)

| # | Agent Role | 0.8B Think | 0.8B NT | 2B Think | 2B NT | 4B Think | 4B NT | 9B Think | 9B NT |
|---|---|---|---|---|---|---|---|---|---|
| | | Qwen3.5-0.8B | Qwen3.5-0.8B | Qwen3.5-2B | Qwen3.5-2B | Qwen3.5-4B | Qwen3.5-4B | Qwen3.5-9B | Qwen3.5-9B |
| | **Tier 1 — Utility** | | | | | | | | |
| 1 | Router / Triage | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 9 | — | — | — | — |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 3 | Health Monitor | 🔴 2 | 🔴 3 | 🔴 3 | 🔴 3 | — | — | — | — |
| 4 | Notification | 🟡 6 | 🟡 6 | 🟢 9 | 🟢 9 | — | — | — | — |
| 5 | Sentiment | 🟡 6 | 🔴 4 | 🟢 8 | 🟢 8 | — | — | — | — |
| 6 | FAQ Generation | 🔴 1 | 🔴 3 | 🟡 5 | 🟡 5 | — | — | — | — |
| 7 | Translation | 🟡 7 | 🟢 9 | 🟡 7 | 🟡 7 | — | — | — | — |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | — | — | — | — |
| | **Tier 2 — Moderate** | | | | | | | | |
| 9 | Research Agent | 🟡 6 | 🟡 6 | 🟢 9 | 🟢 8 | — | — | — | — |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 11 | Editor | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 | — | — | — | — |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 13 | Email Drafting | 🟡 6 | 🔴 4 | 🟢 8 | 🟢 8 | — | — | — | — |
| 14 | Doc Summary | 🟡 6 | 🟢 8 | 🟢 9 | 🟢 8 | — | — | — | — |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | — | — | — | — |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 19 | Shopping | 🔴 4 | 🔴 2 | 🔴 0 | 🔴 2 | — | — | — | — |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | — | — | — | — |
| 21 | RAG / Retrieval | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | — | — | — | — |
| 22 | Data Analysis | 🔴 1 | 🔴 0 | 🔴 3 | 🔴 2 | — | — | — | — |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 | — | — | — | — |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 25 | Customer Support | 🟡 6 | 🟡 6 | 🟡 7 | 🟡 7 | — | — | — | — |
| 26 | Lead Scoring | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | — | — | — | — |
| 27 | Sprint Summary | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | — | — | — | — |
| 28 | Transaction | 🔴 1 | 🔴 1 | 🟢 9 | 🟢 9 | — | — | — | — |
| 29 | Home Automation | 🟡 7 | 🟢 10 | 🟡 7 | 🟢 9 | — | — | — | — |
| 30 | Fitness Tracking | 🔴 3 | 🔴 3 | 🔴 4 | 🔴 3 | — | — | — | — |
| 31 | Recipe / Cooking | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | — | — | — | — |
| 32 | Personal Finance | 🔴 3 | 🔴 3 | 🔴 4 | 🔴 4 | — | — | — | — |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | — | — | — | — |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 35 | Travel Planning | 🔴 4 | 🔴 4 | 🟡 6 | 🟡 6 | — | — | — | — |
| | **Tier 3 — Advanced** | | | | | | | | |
| 36 | Code Generation | 🟢 8 | 🟢 8 | 🟢 10 | 🟢 10 | — | — | — | — |
| 37 | Code Review | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | — | — | — | — |
| 39 | Task Planning | 🟢 9 | 🟡 7 | 🟢 10 | 🟢 8 | — | — | — | — |
| 40 | Fact-Checking | 🟡 5 | 🔴 4 | 🟡 6 | 🟡 6 | — | — | — | — |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 42 | Market Research | 🔴 4 | 🔴 4 | 🔴 3 | 🔴 3 | — | — | — | — |
| 43 | Synthesizer | 🟢 9 | 🟢 9 | 🟡 7 | 🟢 9 | — | — | — | — |
| 44 | Curriculum Design | 🔴 4 | 🔴 4 | 🟡 7 | 🟡 7 | — | — | — | — |
| 45 | Prototype Gen | 🟡 7 | 🔴 2 | 🟡 6 | 🟡 7 | — | — | — | — |
| 46 | DevOps | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 9 | — | — | — | — |
| | **Tier 4 — Expert** | | | | | | | | |
| 47 | Math / Logic | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | — | — | — | — |
| 48 | STEM Analysis | 🔴 0 | 🔴 0 | 🔴 2 | 🔴 2 | — | — | — | — |
| 49 | Algorithm | 🟡 5 | 🔴 0 | 🔴 0 | 🔴 0 | — | — | — | — |
| | **Tier 5 — Senior** | | | | | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | — | — | — | — |
| 51 | Architect | 🟢 8 | 🟢 9 | 🟢 10 | 🟢 10 | — | — | — | — |
| 52 | Debugger | 🟡 6 | 🟢 10 | 🟢 8 | 🟢 8 | — | — | — | — |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | — | — | — | — |
| 54 | Medical | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | — | — | — | — |
| 55 | Financial | 🔴 2 | 🔴 1 | 🟢 8 | 🟢 8 | — | — | — | — |
| 56 | Security | 🟡 6 | 🔴 3 | 🟢 10 | 🟢 9 | — | — | — | — |
| 57 | SRE / Incident | 🔴 2 | 🔴 2 | 🔴 3 | 🔴 2 | — | — | — | — |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 | — | — | — | — |
| 59 | Compliance | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | — | — | — | — |
| | **TOTAL** | **339/585 (58%)** | **331/585 (57%)** | **392/590 (66%)** | **392/590 (66%)** | — | — | — | — |

### Notes

- Social Scouting (#16) scored 16/10 due to scoring bug — capped to 10 in totals above
- STEM (#48) scored 0/5 (not 0/10) — model generated degenerate repetitive output filling the token limit
- Think and NoThink perform nearly identically for 0.8B and 2B — the models don't produce meaningful chain-of-thought at this size

---

## Phase G — Discriminator Tests (Small Models)

| # | Test | 0.8B Think | 0.8B NT | 2B Think | 2B NT | 4B Think | 4B NT | 9B Think | 9B NT |
|---|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 36 | Code Gen (RateLimiter) | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | — | — | — | — |
| 2 | Input Validator (nested) | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | — | — | — | — |
| 5 | Sentiment (hard, 20 items) | 🔴 2 | 🔴 2 | 🔴 4 | 🔴 4 | — | — | — | — |
| 40 | Fact-Checking (plausible) | 🔴 0 | 🔴 0 | 🟡 7 | 🟡 7 | — | — | — | — |
| 49 | Algorithm (LRU+TTL) | 🔴 3 | 🔴 3 | 🔴 3 | 🔴 3 | — | — | — | — |
| 51 | Architect (trade-offs) | 🟡 7 | 🟡 7 | 🟢 9 | 🟢 9 | — | — | — | — |
| 48 | STEM (multi-step calc) | 🔴 0 | 🔴 0 | 🔴 1 | 🔴 1 | — | — | — | — |
| 9 | Research (contradictions) | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 9 | — | — | — | — |
| 12 | Content Planner (15 constraints) | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 1 | — | — | — | — |
| 50 | Orchestrator (multi-agent) | 🟡 7 | 🟡 7 | 🟡 7 | 🟡 7 | — | — | — | — |
| 23 | Web Scraping (messy HTML) | 🔴 0 | 🔴 0 | 🟡 6 | 🟡 6 | — | — | — | — |
| | **TOTAL** | **33/110 (30%)** | **33/110 (30%)** | **52/110 (47%)** | **52/110 (47%)** | — | — | — | — |

---

## Summary — Best Score Per VRAM Tier

| VRAM | Best Model | Phase F | Phase G |
|------|-----------|:---:|:---:|
| **8GB** | Qwen3.5-0.8B Think | 339/585 (58%) | 33/110 (30%) |
| **12GB** | Qwen3.5-2B Think | 392/590 (66%) | 52/110 (47%) |
| **16GB** | Qwen3.5-9B | *testing* | *testing* |
| **24GB** | Qwen3.5-35B-A3B NT | 433/590 (73%) | 77/110 (70%) |

---

## 📐 Max Context Per VRAM Tier

All models Q4_K_M, Flash Attention on, native max 262,144 tokens (256K).

Context is capped at native max. If native max fits at a lower VRAM tier, higher tiers are marked ✅ (same).

### f16 KV Cache

| Model | File Size | Base VRAM | 8 GB | 12 GB | 16 GB | 24 GB |
|-------|----------|-----------|------|-------|-------|-------|
| Qwen3.5-0.8B | 0.5 GB | 1,343 MiB | **262,144** ⭐ | ✅ | ✅ | ✅ |
| Qwen3.5-2B | 1.3 GB | 2,061 MiB | **262,144** ⭐ | ✅ | ✅ | ✅ |
| Qwen3.5-4B | 2.7 GB | 3,501 MiB | 150,000 | **262,144** ⭐ | ✅ | ✅ |
| Qwen3.5-9B | 5.7 GB | 5,765 MiB | 77,500 | 202,500 | **262,144** ⭐ | ✅ |

### q8_0 KV Cache

| Model | File Size | Base VRAM | 8 GB | 12 GB | 16 GB | 24 GB |
|-------|----------|-----------|------|-------|-------|-------|
| Qwen3.5-0.8B | 0.5 GB | 1,343 MiB | **262,144** ⭐ | ✅ | ✅ | ✅ |
| Qwen3.5-2B | 1.3 GB | 2,061 MiB | **262,144** ⭐ | ✅ | ✅ | ✅ |
| Qwen3.5-4B | 2.7 GB | 3,501 MiB | 250,000 | **262,144** ⭐ | ✅ | ✅ |
| Qwen3.5-9B | 5.7 GB | 5,765 MiB | 145,000 | **262,144** ⭐ | ✅ | ✅ |

⭐ = native max (262K) reached &nbsp; ✅ = same (fits at lower tier)

### Per-Model Details

<details>
<summary><b>Qwen3.5-0.8B</b> — File: 0.5 GB · Base VRAM: 1,343 MiB</summary>

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 262,144 ⭐ | 262,144 ⭐ |
| 12GB | ✅ | ✅ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

</details>

<details>
<summary><b>Qwen3.5-2B</b> — File: 1.3 GB · Base VRAM: 2,061 MiB</summary>

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 262,144 ⭐ | 262,144 ⭐ |
| 12GB | ✅ | ✅ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

</details>

<details>
<summary><b>Qwen3.5-4B</b> — File: 2.7 GB · Base VRAM: 3,501 MiB</summary>

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 150,000 | 250,000 |
| 12GB | 262,144 ⭐ | **262,144** ⭐ |
| 16GB | ✅ | ✅ |
| 24GB | ✅ | ✅ |

</details>

<details>
<summary><b>Qwen3.5-9B</b> — File: 5.7 GB · Base VRAM: 5,765 MiB</summary>

| VRAM Budget | f16 KV | q8_0 KV |
|------------|--------|--------|
| 8GB | 77,500 | 145,000 |
| 12GB | 202,500 | 262,144 ⭐ |
| 16GB | 262,144 ⭐ | ✅ |
| 24GB | ✅ | ✅ |

</details>

---

[← Back to Main Results](../README.md)

