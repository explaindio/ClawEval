# 🟢 Gemma-4 Local Benchmarks on RTX 3090 (24GB VRAM)

[← Back to Main Results](../README.md) · [Full Detailed Results →](../RESULTS.md)

Using `Q4_K_M` variations of the new Gemma-4 (or Griffin/Gemma 3) models from Unsloth.
KV Cache Configuration: `q8_0` (8-bit KV caching for optimized VRAM geometry).
System Specs: Single NVIDIA RTX 3090 (24 GB VRAM).

| Model Size / Architecture | Hugging Face GGUF File | Max Safe Context (Tokens) |
|---|---|---|
| **E2B** (~2B) | `gemma-4-E2B-it-Q4_K_M.gguf` | **131,072** (Trained Native Max) |
| **E4B** (~4B) | `gemma-4-E4B-it-Q4_K_M.gguf` | **131,072** (Trained Native Max) |
| **26B-A4B** (Active 4B MoE) | `gemma-4-26B-A4B-it-UD-Q4_K_M.gguf` | **262,144** (Trained Native Max) |
| **31B** (~31B dense) | `gemma-4-31B-it-Q4_K_M.gguf` | **53,248** (GPU VRAM Ceiling) |

### Context Observations
1. **Unsloth 'Gemma-4' architecture requirement**: The models utilize an architecture `gemma4` which is so new it required a freshly built `llama.cpp` pulled today.
2. **Dense 31B on 24GB VRAM**: The `31B` dense model squeezed an impressive precision boundary of `53,248` tokens total context on a 24GB RTX 3090 using `q8_0` KV cache before issuing a hard OOM error.
3. **Massive MoE Efficiency**: The 26B-A4B architecture allows an effectively "infinite" context for local setups. Because it only caches its small active subsets computationally via Sliding Window Attention (SWA) or MoE routing, it successfully loaded over `260,000` context—smashing right into extreme `llama.cpp` sequence bounds without memory errors.

---

## Benchmark Results

All tests run locally via `llama.cpp` server perfectly controlling reasoning budget using the new OpenAI compliant `reasoning_budget_tokens` and global `max_tokens` settings. E.g. `max_tokens: 16000`, `reasoning_budget_tokens: 8192`.

> 💡 **Standout Gemma-4-E2B Capabilities**: Despite its microscopic 2B size, it scored a perfect 10/10 on the complex **Input Validator** and **Web Scraping** tests across both Phase F and the discriminator Phase G.

| # | Agent Role | Gemma-4-E2B | Gemma-4-E4B | Gemma-4-A4B | Gemma-4-31B |
|---|---|---|---|---|---|
| | **Tier 1 — Utility** | | | | |
| 1 | Router / Triage | 🟢 9 | | | |
| 2 | Input Validator | 🟢 10 | | | |
| 3 | Health Monitor | 🟡 5 | | | |
| 4 | Notification | 🟢 8 | | | |
| 5 | Sentiment | 🟢 10 | | | |
| 6 | FAQ Generation | 🟡 5 | | | |
| 7 | Translation | 🟢 9 | | | |
| 8 | Calendar | 🔴 0 | | | |
| | **Tier 2 — Moderate** | | | | |
| 9 | Research Agent | 🟢 10 | | | |
| 10 | Content Writer | 📝 5 | | | |
| 11 | Editor | 🟢 9 | | | |
| 12 | Content Planner | 🟢 10 | | | |
| 13 | Email Drafting | 🟢 8 | | | |
| 14 | Doc Summary | 🟢 10 | | | |
| 15 | Meeting Notes | 🟢 9 | | | |
| 16 | Social Scouting | 🟢 10 | | | |
| 17 | Social Content | 📝 5 | | | |
| 18 | News Aggregation | 🟢 10 | | | |
| 19 | Shopping | 🟢 10 | | | |
| 20 | Memory Mgmt | 🟢 9 | | | |
| 21 | RAG / Retrieval | 🟡 6 | | | |
| 22 | Data Analysis | 🔴 0 | | | |
| 23 | Web Scraping | 🟢 10 | | | |
| 24 | Image Description | 📝 5 | | | |
| 25 | Customer Support | 🟢 10 | | | |
| 26 | Lead Scoring | 🟢 8 | | | |
| 27 | Sprint Summary | 🟢 10 | | | |
| 28 | Transaction | 🟢 10 | | | |
| 29 | Home Automation | 🟢 10 | | | |
| 30 | Fitness Tracking | 🟢 9 | | | |
| 31 | Recipe / Cooking | 🔴 2 | | | |
| 32 | Personal Finance | 🟡 6 | | | |
| 33 | SEO Optimization | 🟢 9 | | | |
| 34 | Landing Page | 📝 5 | | | |
| 35 | Travel Planning | 🟢 8 | | | |
| | **Tier 3 — Advanced** | | | | |
| 36 | Code Generation | 🟢 10 | | | |
| 37 | Code Review | 🟢 10 | | | |
| 38 | QA / Test Writing | 🟢 8 | | | |
| 39 | Task Planning | 🟢 9 | | | |
| 40 | Fact-Checking | 🟢 10 | | | |
| 41 | Critic / Review | 📝 5 | | | |
| 42 | Market Research | 🟢 8 | | | |
| 43 | Synthesizer | 🟢 9 | | | |
| 44 | Curriculum Design | 🟡 6 | | | |
| 45 | Prototype Gen | 🟡 5 | | | |
| 46 | DevOps | 🟢 9 | | | |
| | **Tier 4 — Expert** | | | | |
| 47 | Math / Logic | 🟡 6 | | | |
| 48 | STEM Analysis | 🟢 10 | | | |
| 49 | Algorithm | 🟢 10 | | | |
| | **Tier 5 — Senior** | | | | |
| 50 | Orchestrator | 🟢 8 | | | |
| 51 | Architect | 🟢 9 | | | |
| 52 | Debugger | 🟢 10 | | | |
| 53 | Legal Review | 🟢 10 | | | |
| 54 | Medical | 🟢 10 | | | |
| 55 | Financial | 🟡 6 | | | |
| 56 | Security | 🟢 10 | | | |
| 57 | SRE / Incident | 🟡 7 | | | |
| 58 | Book Writing | 📝 5 | | | |
| 59 | Compliance | 🟡 7 | | | |
| | **TOTAL (Phase F)** | **461 (78%)** | | | |

> 📝 Manual review tests default to 5/10 pending review.

---

### Phase G (Discriminator Tests)

| Model | Phase G Score | Notes |
|---|---|---|
| **Gemma-4-E2B** | **74/110 (67%)** | Perfect 10s on Input Validator and Web Scraping. Struggles hard on Content Planner (1/10) and Algorithm drops to 3/10. Phenomenal overall given 2B sizing. ~140-160 t/s locally on RTX 3090. |
| **Gemma-4-E4B** | TBD | |
| **Gemma-4-26B-A4B** | TBD | |
| **Gemma-4-31B** | TBD | |

