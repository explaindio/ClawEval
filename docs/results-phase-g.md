# Phase G — Discriminator Tests (Harder Tests That Separate Model Quality)

[← Back to main README](../README.md)

## Why Phase G?

Phase F tests showed identical scores (10/10) across all models for ~15 roles, meaning the tests were too easy to differentiate model quality. Phase G uses **harder, multi-constraint tests** designed to reveal real differences between 27B, 35B, and 120B+ models.

## Scoring Legend

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; ⏱️ = Think overflow (model never stops thinking)

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

| # | Test | 122B NoThink | GPT-OSS-120B Med |
|---|------|:----------:|:----------:|
| | | Qwen3.5-122B-A10B | GPT-OSS-120B |
| | | NVFP4 · SGLang | GGUF · llama.cpp |
| 36 | Code Gen (RateLimiter) | 🟢 8 | 🟡 7 |
| 2 | Input Validator (nested) | 🟢 **10** | 🟢 9 |
| 5 | Sentiment (hard, 20 items) | 🟢 **8** | 🟡 6 |
| 40 | Fact-Checking (plausible) | 🟢 **10** | 🟢 9 |
| 49 | Algorithm (LRU Cache + TTL) | 🟢 **10** | 🟢 **10** |
| 51 | Architect (trade-offs) | 🟢 **10** | 🟢 9 |
| 48 | STEM (multi-step calc) | 🟡 **5** | 🟡 **5** |
| 9 | Research (contradictions) | 🟢 8 | 🟢 **9** |
| 12 | Content Planner (15 constraints) | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟡 **7** | 🟡 **7** |
| 23 | Web Scraping (messy HTML) | 🟢 **10** | 🟢 **10** |
| | **TOTAL** | **87/110 (79%)** | **82/110 (75%)** |

---

## ☁️ Cloud Models

| # | Test | K2.5 Think | K2.5 NoThink | GLM-5 Think | GLM-5 NoThink |
|---|------|:---:|:---:|:---:|:---:|
| | | Kimi-K2.5 | Kimi-K2.5 | GLM-5 | GLM-5 |
| | | Alibaba | `thinking: False` | Alibaba | `enable_thinking: false` |
| 36 | Code Gen (RateLimiter) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 9 |
| 2 | Input Validator (nested) | 🟢 **10** | 🟢 **10** | 🔴 0 ⏱️ | 🟢 **10** |
| 5 | Sentiment (hard, 20 items) | 🟢 **8** | 🟢 **8** | 🟢 **8** | 🟢 **8** |
| 40 | Fact-Checking (plausible) | 🟢 10 | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 49 | Algorithm (LRU Cache + TTL) | 🟢 **9** | 🟢 **9** | 🟢 **10** | 🟢 9 |
| 51 | Architect (trade-offs) | 🟢 9 | 🟢 **10** | 🟢 **9** | 🟢 **9** |
| 48 | STEM (multi-step calc) | 🟢 **8** | 🟢 **8** | 🟡 6 | 🔴 4 |
| 9 | Research (contradictions) | 🟢 **8** | 🟢 **8** | 🟡 5 | 🔴 3 |
| 12 | Content Planner (15 constraints) | 🟡 **7** | 🔴 1 | 🔴 1 | 🔴 1 |
| 50 | Orchestrator (multi-agent) | 🟡 **7** | 🟡 **7** | 🟢 8 | 🟡 7 |
| 23 | Web Scraping (messy HTML) | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| | **TOTAL** | **96/110 (87%)** | **91/110 (83%)** | **76/110 (69%)** | **80/110 (73%)** |

> **GLM-5 Think timeout:** Input Validator scored 0/10 due to 300s timeout — heavy reasoning exceeded API time limit. NoThink completed it perfectly (10/10).

---

## Key Findings

### 🏆 Overall Ranking

| Rank | Model | Score | Notes |
|------|-------|-------|-------|
| 🥇 | **Kimi K2.5 Think** | 96/110 (87%) | Cloud · Champion · No test below 7 |
| 🥈 | **Kimi K2.5 NoThink** | 91/110 (83%) | Cloud · Faster · No thinking overhead |
| 🥉 | **122B NoThink** | 87/110 (79%) | Local 64-96GB · Best local model |
| 4 | **27B NoThink** | 83/110 (75%) | Local 24GB · Best budget model |
| 5 | **GPT-OSS-120B** | 82/110 (75%) | Local 64-96GB · Good all-rounder |
| 6 | **GLM-5 NoThink** | 80/110 (73%) | Cloud · Better than Think mode |
| 7 | **35B NoThink** | 77/110 (70%) | Local 24GB |
| 8 | **GLM-5 Think** | 76/110 (69%) | Cloud · Timeout hurt score |
| 9 | **35B Think** | 51/60 (85%)* | Local · 5/11 tests overflow |

\* Only 6/11 tests completed due to SGLang thinking budget bug

### Key Observations

1. **Kimi K2.5 is the clear champion** (96/110 Think, 91/110 NoThink) — first model to score 10/10 on Code Gen
2. **GLM-5 underperforms on Phase G** despite competitive Phase F scores (79%) — harder tests expose reasoning gaps
3. **Thinking helps most on Content Planner** — K2.5 Think 7/10 vs NoThink 1/10 across multiple models
4. **GLM-5 Think can timeout** — heavy reasoning on Alibaba API caused Input Validator 0/10
5. **STEM is the great differentiator** — K2.5 8/10 vs GLM-5 4-6/10 vs local 2-5/10
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
