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
| 1 | Router / Triage | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 9 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🟡 5 | 🟠 5 | 🟠 5 | 🟠 5 |
| 4 | Notification | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 9 |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 5 | 🟠 5 | 🟠 5 | 🟠 5 |
| 7 | Translation | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | |
| 9 | Research Agent | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟢 9 | 🟡 7 | 🔴 0 | 🟢 9 |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🔴 0 | 🟢 10 |
| 13 | Email Drafting | 🟢 8 | 🟢 8 | 🟢 9 | 🟢 10 |
| 14 | Doc Summary | 🟢 10 | 🟢 10 | 🟢 8 | 🟡 7 |
| 15 | Meeting Notes | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 19 | 🟢 19 | 🟢 19 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟠 5 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🟢 8 | 🟢 8 | 🟢 10 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 6 | 🟡 6 | 🟠 4 | 🟡 6 |
| 22 | Data Analysis | 🔴 0 | 🔴 1 | 🔴 0 | 🔴 2 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 9 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 27 | Sprint Summary | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 8 |
| 28 | Transaction | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 9 |
| 29 | Home Automation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 30 | Fitness Tracking | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 31 | Recipe / Cooking | 🔴 2 | 🔴 2 | 🔴 2 | 🟢 9 |
| 32 | Personal Finance | 🟡 6 | 🟠 5 | 🟡 7 | 🟡 6 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 8 | 🟢 9 | 🔴 0 | 🟢 8 |
| | **Tier 3 — Advanced** | | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 8 | 🟢 10 | 🟢 8 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 8 |
| 39 | Task Planning | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 8 |
| 40 | Fact-Checking | 🟢 10 | 🟡 7 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🟢 8 | 🟡 6 | 🟡 6 | 🟡 6 |
| 43 | Synthesizer | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 44 | Curriculum Design | 🟡 6 | 🟡 6 | 🟡 6 | 🟡 6 |
| 45 | Prototype Gen | 🟡 5 | 🟡 7 | 🟠 5 | 🟠 5 |
| 46 | DevOps | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 10 |
| | **Tier 4 — Expert** | | | | |
| 47 | Math / Logic | 🟡 6 | 🟢 8 | 🔴 0 | 🟡 6 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 9 | 🟢 10 | 🟢 9 | 🟢 10 |
| 52 | Debugger | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 |
| 54 | Medical | 🟢 10 | 🟢 9 | 🟢 9 | 🟢 9 |
| 55 | Financial | 🟡 6 | 🟡 6 | 🟡 6 | 🟢 10 |
| 56 | Security | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🟡 7 | 🟡 6 | 🔴 3 | 🟡 6 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟡 7 | 🟢 8 | 🟢 9 | 🟡 7 |
| | **TOTAL (Phase F)** | **461 (78%)** | **468 (79%)** | **428 (73%)** | **478 (81%)** |

> 📝 Manual review tests default to 5/10 pending review.

---

### Phase G (Discriminator Tests)

| Model | Phase G Score | Notes |
|---|---|---|
| **Gemma-4-E2B** | **74/110 (67%)** | Perfect 10s on Input Validator and Web Scraping. Struggles hard on Content Planner (1/10) and Algorithm drops to 3/10. Phenomenal overall given 2B sizing. ~140-160 t/s locally on RTX 3090. |
| **Gemma-4-E4B** | **78/110 (71%)** | Huge jump in Algorithm / Data Structure tests (9/10 up from E2B's 3/10). Retains perfect 10/10 on Input Validator. Consistent ~100-115 t/s locally. |
| **Gemma-4-26B-A4B** | **23/110 (21%)** | ⚠️ Severely impacted by `llama.cpp` MoE reasoning loop bug — 8/11 tests hit 32K token ceiling with blank output. Tests that completed show high capability: Algorithm 10/10, Orchestrator 7/10, Research 6/10. ~54-65 t/s on RTX 3090. |
| **Gemma-4-31B** | **76/110 (69%)** | Perfect 10s on Input Validator, Fact-Checking, Algorithm, and Web Scraping! Extremely stable dense architecture, completely immune to the MoE looping bugs. Very reliable logic limits. Generates at ~15 t/s locally on RTX 3090. |

