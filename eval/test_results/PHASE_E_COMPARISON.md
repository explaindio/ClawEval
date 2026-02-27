# Phase E: Killer Evaluation Comparison — All Models

**Date:** 2026-02-26  
**Test Suite:** 12 tests (10 single-shot + 2 multi-turn agentic)  
**Scoring:** 100% automated, binary sub-checks  

---

## Head-to-Head Comparison

| # | Test | Category | 27B-nothink | 35B-nothink | 35B-think |
|---|------|----------|:-----------:|:-----------:|:---------:|
| 1 | Precise Counting | reasoning | 4 | 4 | 4 |
| 2 | Constrained JSON | structured | **10** | 9 | **10** |
| 3 | Logic Grid Puzzle | reasoning | 5 | 6 | **10** |
| 4 | Multi-Step Math | reasoning | **10** | **10** | **10** |
| 5 | Code Output | code | **10** | **10** | **10** |
| 6 | Contradictions | reasoning | 5 | 5 | 5 |
| 7 | Complex Sorting | reasoning | **8** | 3 | **8** |
| 8 | Regex Construction | code | **10** | 7 | **10** |
| 9 | Data Transform | structured | 0 | 2 | **10** |
| 10 | Instruction Chain | instruction | 4 | 4 | **8** |
| 11 | Multi-Turn Code | multi_turn | **10** | 9 | 8 |
| 12 | Multi-Turn State | multi_turn | 7 | 7 | **9** |
| | **TOTAL** | | **83 (69%)** | **76 (63%)** | **102 (85%)** |

---

## Category Breakdown

| Category | 27B-nothink | 35B-nothink | 35B-think |
|----------|:-----------:|:-----------:|:---------:|
| Code | **100%** | 85% | **100%** |
| Multi-Turn | **85%** | 80% | **85%** |
| Reasoning | **64%** | 56% | **74%** |
| Structured Output | 50% | 55% | **100%** |
| Instruction | 40% | 40% | **80%** |

---

## Resource Usage

| Metric | 27B-nothink | 35B-nothink | 35B-think |
|--------|:-----------:|:-----------:|:---------:|
| Total tokens | ~2K | ~3K | ~92K |
| Total time | ~2 min | ~30s | ~15 min |
| Avg speed | ~30 t/s | ~85 t/s | ~95 t/s |
| Token budget | 4,000 | 4,000 | 32,000 |

---

## Key Findings

> [!IMPORTANT]
> 27B nothink (69.2%) **outperforms** 35B MoE nothink (63.3%) on Phase E despite being a smaller dense model.
> 35B-think (85.0%) dominates both on hard reasoning, but at 30x token cost.

**27B nothink strengths vs 35B nothink:**
- Sorting: 8 vs 3 (+5)
- Regex: 10 vs 7 (+3)
- Constrained JSON: 10 vs 9 (+1)
- Multi-Turn Code: 10 vs 9 (+1) — best multi-turn score of all models

**27B nothink weaknesses:**
- Data Transform: 0 vs 2 (both bad, but 27B worse)
- Logic Puzzle: 5 vs 6 (-1)

**Thinking is the only path to 85%+ on Phase E** — the reasoning chain is essential for data transforms, logic puzzles, and instruction chains.
