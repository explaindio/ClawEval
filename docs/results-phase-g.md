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

## Key Findings

1. **122B NoThink is the best complete-run model** (87/110, 79%) — best at algorithm, architecture, and reasoning
2. **27B NoThink is the best 24GB model** (83/110, 75%) — aces Code Gen (10/10) and Fact-Checking (10/10)
3. **35B Think scores highest per-test** (51/60, 85% on completed tests) — Content Planner 8/10 is unique; but 5/11 tests overflow
4. **GPT-OSS-120B is a strong all-rounder** (82/110, 75%) — ties 122B on Algorithm and STEM
5. **Content Planner** — 35B Think scored **8/10** while all NoThink configs score 1/10, proving thinking genuinely helps for complex constraint satisfaction

## ⚠️ SGLang Thinking Budget Bug

The `thinking_budget` parameter in `chat_template_kwargs` is **not enforced** for QWen3.5-35B-A3B on SGLang. Setting `thinking_budget: 4096` or `8192` has no effect — the model generates 32K–65K tokens of chain-of-thought reasoning without ever producing the actual answer.

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
