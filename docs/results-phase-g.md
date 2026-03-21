# Phase G — Discriminator Tests (Harder Tests That Separate Model Quality)

[← Back to main README](../README.md)

## Why Phase G?

Phase F tests showed identical scores (10/10) across all models for ~15 roles, meaning the tests were too easy to differentiate model quality. Phase G uses **harder, multi-constraint tests** designed to reveal real differences between 27B, 35B, and 120B+ models.

## Scoring Legend

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; ⏱️ = Think overflow (model never stops thinking)

---

## 🔴 8GB VRAM Results (Small Models)

| # | Test | 0.8B Think | 0.8B NT |
|---|------|:---:|:---:|
| | | Qwen3.5-0.8B | Qwen3.5-0.8B |
| | | Q4_K_M · llama.cpp | Q4_K_M · llama.cpp |
| 36 | Code Gen (RateLimiter) | 🔴 0 | 🔴 0 |
| 2 | Input Validator (nested) | 🟡 5 | 🟡 5 |
| 5 | Sentiment (hard, 20 items) | 🔴 2 | 🔴 2 |
| 40 | Fact-Checking (plausible) | 🔴 0 | 🔴 0 |
| 49 | Algorithm (LRU Cache + TTL) | 🔴 3 | 🔴 3 |
| 51 | Architect (trade-offs) | 🟡 7 | 🟡 7 |
| 48 | STEM (multi-step calc) | 🔴 0 | 🔴 0 |
| 9 | Research (contradictions) | 🟢 **8** | 🟢 **8** |
| 12 | Content Planner (15 constraints) | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟡 **7** | 🟡 **7** |
| 23 | Web Scraping (messy HTML) | 🔴 0 | 🔴 0 |
| | **TOTAL** | **33/110 (30%)** | **33/110 (30%)** |

> 0.8B model shows near-identical Think/NoThink scores — the model doesn't generate meaningful COT at this size. Research Agent (8/10) and Architect (7/10) are standout results for a sub-1B model.

---

## 24GB VRAM Results

| # | Test | 35B Think | 35B NoThink | 27B NoThink |
|---|------|:---------:|:-----------:|:-----------:|
| | | Qwen3.5-35B-A3B | Qwen3.5-35B-A3B | Qwen3.5-27B |
| | | NVFP4 · SGLang | Q4_K_M · llama.cpp | Q4_K_M · llama.cpp |
| 36 | Code Gen (RateLimiter) | ⏱️ | 🟢 9 | 🟢 **10** |
| 2 | Input Validator (nested) | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 5 | Sentiment (hard, 20 items) | 🟢 **8** | 🟢 **8** | 🟢 **8** |
| 40 | Fact-Checking (plausible) | ⏱️ | 🟢 9 | 🟢 **10** |
| 49 | Algorithm (LRU Cache + TTL) | ⏱️ | 🟡 5 | 🟢 **9** |
| 51 | Architect (trade-offs) | 🟢 8 | 🟢 **9** | 🟢 **9** |
| 48 | STEM (multi-step calc) | ⏱️ | 🔴 1 | 🔴 **2** |
| 9 | Research (contradictions) | 🟢 **10** | 🟢 9 | 🟢 9 |
| 12 | Content Planner (15 constraints) | 🟢 **8** | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟡 **7** | 🟡 **7** | 🟡 **7** |
| 23 | Web Scraping (messy HTML) | ⏱️ | 🟢 **10** | 🟢 8 |
| | **Completed tests** | **51/60 (85%)** | **77/110 (70%)** | **83/110 (75%)** |
| | | 6/11 completed | 11/11 completed | 11/11 completed |

## 64–96GB VRAM Results

| # | Test | Nemotron-3-Super-120B-A12B Think | Nemotron-3-Super-120B-A12B NoThink | 122B NoThink | GPT-OSS-120B Med | Mistral-Small-4-119B Med |
|---|------|:----------:|:----------:|:----------:|:----------:|:----------:|
| | | Nemotron-3-Super-120B | Nemotron-3-Super-120B | Qwen3.5-122B-A10B | GPT-OSS-120B | Mistral-Small-4-119B |
| | | NVFP4 · SGLang | NVFP4 · SGLang | NVFP4 · SGLang | GGUF · llama.cpp | NVFP4 · vLLM |
| 36 | Code Gen (RateLimiter) | 🟢 **10** | 🔴 0 | 🟢 8 | 🟡 7 | 🟡 7 |
| 2 | Input Validator (nested) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 5 | Sentiment (hard, 20 items) | 🟢 8 | 🟢 8 | 🟢 8 | 🟡 6 | 🟢 8 |
| 40 | Fact-Checking (plausible) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 |
| 49 | Algorithm (LRU Cache + TTL) | 🟢 **10** | 🟡 4 | 🟢 **10** | 🟢 **10** | 🟢 9 |
| 51 | Architect (trade-offs) | 🟢 9 | 🟢 8 | 🟢 **10** | 🟢 9 | 🟢 9 |
| 48 | STEM (multi-step calc) | 🟡 5 | 🔴 0 | 🟡 5 | 🟡 5 | 🔴 2 |
| 9 | Research (contradictions) | 🟢 9 | 🟢 **10** | 🟢 8 | 🟢 9 | 🟢 **10** |
| 12 | Content Planner (15 constraints) | 🟢 9 | 🟢 9 | 🔴 1 | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟢 9 | 🟢 9 | 🟡 7 | 🟡 7 | 🟡 7 |
| 23 | Web Scraping (messy HTML) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| | **TOTAL** | **99/110 (90%)** 🥇 | **78/110 (71%)** | **87 (79%)** | **82 (75%)** | **82 (75%)** |

---

## ☁️ Cloud Models

| # | Test | K2.5 T | K2.5 NT | GLM T | GLM NT | M2.5 T | Q3.5+ T | Q3.5+ NT | M2.7 T |
|---|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| | | Kimi-K2.5 | Kimi-K2.5 | GLM-5 | GLM-5 | MiniMax-M2.5 | Qwen3.5+ | Qwen3.5+ | MiniMax-M2.7 |
| | | Alibaba | `no think` | Alibaba | `no think` | Alibaba | Alibaba | `no think` | Ollama Cloud |
| 36 | Code Gen (RateLimiter) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 8 | 🟢 **10** | 🟢 **10** | 🔴 0 ⚡ |
| 2 | Input Validator (nested) | 🟢 **10** | 🟢 **10** | 🔴 0 ⏱️ | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🔴 0 ⚡ |
| 5 | Sentiment (hard, 20 items) | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** | 🟢 8 |
| 40 | Fact-Checking (plausible) | 🟢 10 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| 49 | Algorithm (LRU Cache + TTL) | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 51 | Architect (trade-offs) | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 8 | 🟢 **10** | 🟢 **10** |
| 48 | STEM (multi-step calc) | 🟢 **8** | 🟢 **8** | 🟡 6 | 🔴 4 | 🟡 5 | 🟡 6 | 🔴 4 | 🔴 0 ⚡ |
| 9 | Research (contradictions) | 🟢 **8** | 🟢 **8** | 🟡 5 | 🔴 3 | 🟡 6 | 🟡 6 | 🟡 5 | 🟢 **9** |
| 12 | Content Planner (15 constraints) | 🟡 **7** | 🔴 1 | 🔴 1 | 🔴 1 | 🔴 0 ⏱️ | 🔴 1 | 🔴 1 | 🔴 0 ⚡ |
| 50 | Orchestrator (multi-agent) | 🟡 **7** | 🟡 **7** | 🟢 **8** | 🟡 7 | 🔴 3 | 🟡 7 | 🟡 7 | 🟡 7 |
| 23 | Web Scraping (messy HTML) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| | **TOTAL** | **96 (87%)** | **91 (83%)** | **76 (69%)** | **80 (73%)** | **78 (71%)** | **86 (78%)** | **86 (78%)** | **64 (58%)** |

> **Timeouts:** GLM-5 Think Input Validator 0/10 (300s), MiniMax-M2.5 Content Planner 0/10 (504 Gateway Timeout).
> **Qwen3.5+ NoThink Sentiment 10/10** (19/20) — best NoThink sentiment score of any cloud model.
> ⚡ M2.7 reasoning overflow — model consumes entire 8000 token budget on thinking, no answer produced.

---

## Key Findings

### 🏆 Overall Ranking

| Rank | Model | Score | Notes |
|------|-------|-------|-------|
| 🥇 | **Nemotron-3-Super-120B-A12B Think** | 99/110 (90%) | Local 64-96GB · Champion · Content Planner 9/10 |
| 🥈 | **Kimi K2.5 Think** | 96/110 (87%) | Cloud · No test below 7 |
| 🥉 | **Kimi K2.5 NoThink** | 91/110 (83%) | Cloud · Faster · No thinking overhead |
| 4 | **122B NoThink** | 87/110 (79%) | Local 64-96GB |
| 5 | **Qwen3.5-Plus Think** | 86/110 (78%) | Cloud · Fact-Check 10/10, Algorithm 10/10 |
| 6 | **MiniMax-M2.7** | 83/110 (75%) | Cloud · With 16-24k tokens. Input Validator 9/10 |
| 6 | **27B NoThink** | 83/110 (75%) | Local 24GB · Best budget model |
| 8 | **GPT-OSS-120B** | 82/110 (75%) | Local 64-96GB · Good all-rounder |
| 8 | **Mistral-Small-4-119B** | 82/110 (75%) | Local 64-96GB · Research 10/10 |
| 10 | **GLM-5 NoThink** | 80/110 (73%) | Cloud · Better than Think mode |
| 11 | **Nemotron-3-Super-120B-A12B NoThink** | 78/110 (71%) | Local 64-96GB · Code Gen 0 hurts |
| 11 | **MiniMax-M2.5** | 78/110 (71%) | Cloud · Think only |
| 13 | **35B NoThink** | 77/110 (70%) | Local 24GB |
| 14 | **GLM-5 Think** | 76/110 (69%) | Cloud · Timeout hurt score |
| 15 | **35B Think** | 51/60 (85%)* | Local · 5/11 tests overflow |
| 16 | **0.8B Think / NT** | 33/110 (30%) | Local 8GB · Research 8/10 is impressive |

\* Only 6/11 tests completed due to SGLang thinking budget bug

### Key Observations

1. **Kimi K2.5 is the clear Phase G champion** (96/110 Think, 91/110 NoThink) — no test below 7
2. **Qwen3.5-Plus Think at #4** (86/110) — perfect on Fact-Check (20/20) and Algorithm (15/15)
3. **Thinking helps most on Content Planner** — K2.5 Think 7/10 vs all others 0-1/10
4. **GLM-5 and M2.5 can timeout** — heavy reasoning on Alibaba API caused 0/10 on some tests
5. **STEM is the great differentiator** — K2.5 8/10 vs Q3.5+ 6/10 vs GLM-5 4-6/10
6. **27B NoThink is remarkable value** — 83/110 on 24GB hardware vs 96/110 cloud

## ⚠️ SGLang Thinking Budget Bug

The `thinking_budget` parameter in `chat_template_kwargs` is **not enforced** for Qwen3.5-35B-A3B on SGLang. Setting `thinking_budget: 4096` or `8192` has no effect — the model generates 32K–65K tokens of chain-of-thought reasoning without ever producing the actual answer.

- **Affected:** 5/11 Phase G tests (Fact-Checking, STEM, Code Gen, Algorithm, Web Scraping)
- **Root cause:** Model fills entire `max_tokens` with thinking, leaves nothing for the answer
- **Workaround:** Use NoThink mode for structured-output tasks, Think mode for open-ended tasks

## What Makes Phase G Different from Phase F?

| Aspect | Phase F | Phase G |
|--------|---------|---------|
| Code Gen test | `merge_intervals()` — simple | `RateLimiter` class — 8 requirements, 10 test cases |
| Input Validator | 10 flat errors | 15 nested errors + cross-field dependencies |
| Sentiment | 10 statements | 20 with nested sarcasm + ambiguity |
| Fact-Checking | 10 well-known facts | 20 plausible falsehoods |
| Algorithm | Single function | LRU Cache with TTL — 15 test cases |
| Scoring | Binary pass/fail | Graduated (partial credit) |

> ⭐ Star this repo to get notified when new models are added.

---

[← Back to main README](../README.md)
