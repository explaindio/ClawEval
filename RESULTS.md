# ClawEval — Detailed Results

## Industry Benchmarks — Context

How the models we test compare on standard benchmarks (higher is better unless noted):

| Benchmark | 35B-A3B | 27B | 122B-A10B | 397B-A17B | Kimi K2.5 | GLM-5 | GPT-OSS-120B |
|---|---|---|---|---|---|---|---|
| **AA Intelligence Index** | 37.0 | 42.0 | 41.5 | 45.0 | **46.8** | 40.6 | 33.3 |
| **AA Coding Index** | 30.3 | 34.9 | 34.7 | **41.3** | 39.5 | 39.0 | 28.6 |
| **AA Agentic Index** | 44.1 | 54.6 | 53.0 | 55.8 | 58.9 | **60.3** | 37.9 |
| GPQA Diamond | 84.5% | 85.8% | 85.7% | **89.3%** | 87.9% | 66.6% | 78.2% |
| HLE (Humanity's Last Exam) | 19.7% | 22.2% | 23.4% | 27.3% | **29.4%** | 7.2% | 18.5% |
| IFBench | 72.5% | 75.6% | 75.7% | **78.8%** | 70.2% | 55.2% | 69.0% |
| AA-LCR | 62.7% | **67.3%** | 66.7% | 65.7% | 65.3% | 37.0% | 50.7% |
| GDPval-AA | 21.3% | 35.0% | 32.3% | 35.4% | 39.1% | **41.9%** | 23.4% |
| CritPt | 0.9% | 0.9% | 0.6% | 1.7% | **3.1%** | 0.0% | 1.1% |
| SciCode | 37.7% | 39.5% | 42.0% | 42.0% | **49.0%** | 38.3% | 38.9% |
| Terminal-Bench Hard | 26.5% | 32.6% | 31.1% | **40.9%** | 34.8% | 39.4% | 23.5% |
| AA-Omniscience Accuracy | 18.8% | 19.4% | 22.5% | 31.4% | **34.3%** | 22.7% | 21.5% |
| Hallucination Rate ↓ | 15.9% | 20.0% | 14.7% | 10.9% | 35.4% | 56.1% | **8.8%** |

> **Key insight:** The 122B-A10B model we test on ClawEval scores close to the full 397B model on most benchmarks, while being ~3× smaller. The 35B-A3B is the most efficient option for 24GB VRAM setups.

---

## Phase E — Per-Test Scores (12 Killer Tests)

All scores out of 10. Sorted by best overall model.

| # | Test | Category | 122B Think | 35B Think | 27B NoThink | 122B NoThink | 35B NoThink |
|---|---|---|---|---|---|---|---|
| 1 | Precise Counting | Reasoning | 🟢 8 | 🔴 4 | 🔴 4 | 🔴 0 | 🔴 4 |
| 2 | Constrained JSON | Structured | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 9 |
| 3 | Logic Grid Puzzle | Reasoning | 🟢 10 | 🟢 10 | 🟡 5 | 🟡 5 | 🟡 6 |
| 4 | Multi-Step Math | Reasoning | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 5 | Code Output Prediction | Code | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | Contradiction Detection | Reasoning | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 |
| 7 | Complex Multi-Key Sort | Reasoning | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🔴 3 |
| 8 | Regex Construction | Code | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟡 7 |
| 9 | Data Transformation | Structured | 🟢 10 | 🟢 10 | 🔴 0 | 🔴 2 | 🔴 2 |
| 10 | Instruction Following | Instruction | 🟢 10 | 🟢 8 | 🔴 4 | 🔴 2 | 🔴 4 |
| 11 | Multi-Turn Refinement | Multi-Turn | 🟡 7 | 🟢 8 | 🟢 10 | 🟢 8 | 🟢 9 |
| 12 | Multi-Turn State Track | Multi-Turn | 🟢 10 | 🟢 9 | 🟡 7 | 🟢 10 | 🟡 7 |
| | **TOTAL** | | **108/120** | **102/120** | **83/120** | **79/120** | **76/120** |
| | **Percentage** | | **90.0%** | **85.0%** | **69.2%** | **65.8%** | **63.3%** |

### Key Takeaways — Phase E
- **Thinking provides massive gains** on reasoning tasks: Logic 5→10, Data Transform 2→10, Instruction 2→10
- **Code tasks** are universally strong — all models score 10/10 on Code Output Prediction
- **Contradiction Detection** is hard for all models (ceiling of 5/10)
- **Multi-Turn** performance is generally strong across the board

---

## Phase F — Per-Role Scores (59 Deterministic Hard Tests)

🟢 = 8-10 &nbsp; 🟡 = 5-7 &nbsp; 🔴 = 0-4 &nbsp; 📝 = Manual (5) &nbsp; ⬛ = 32K overflow

### Tier 1 — Utility Agents

| # | Role | 122B Think 16K | 35B Think ∞ |
|---|---|---|---|
| 1 | Router / Triage Agent | 🟢 **10** | 🟢 **10** |
| 2 | Input Validator / Sanitizer | 🟢 **10** | 🟢 **10** |
| 3 | Heartbeat / Health Monitor | 🔴 3 | ⬛ 0 |
| 4 | Notification / Alert Agent | 🟢 **8** | 🟢 **8** |
| 5 | Sentiment Analysis Agent | 🟢 **10** | 🟢 **10** |
| 6 | FAQ Generation Agent | 🟡 5 | 🟡 6 |
| 7 | Translation Agent | 🟢 **10** | 🟢 **9** |
| 8 | Calendar / Scheduling Agent | 🔴 0 | 🔴 0 |

### Tier 2 — Moderate Complexity Agents

| # | Role | 122B Think 16K | 35B Think ∞ |
|---|---|---|---|
| 9 | Research / Web Search Agent | 🟢 **10** | ⬛ 0 |
| 10 | Content Writer / Blog Writer | 📝 5 | 📝 5 |
| 11 | Editor Agent | 🟡 7 | 🟢 **9** |
| 12 | Content Planner | 🟢 **10** | 🟢 **10** |
| 13 | Email Drafting / Summarization | 🟢 **8** | ⬛ 0 |
| 14 | Document Summarization | 🟢 **8** | 🟢 **8** |
| 15 | Meeting Notes / Transcription | 🟢 **9** | 🟢 **9** |
| 16 | Social Media Scouting | 🟢 **10** | 🟢 **10** |
| 17 | Social Media Content Agent | 📝 5 | 📝 5 |
| 18 | News Aggregation Agent | 🟢 **10** | 🟢 **10** |
| 19 | Shopping / Price Comparison | 🟢 **10** | 🟢 **10** |
| 20 | Memory / Knowledge Management | 🟢 **9** | 🟢 **9** |
| 21 | RAG / Retrieval Agent | 🟡 6 | 🟡 6 |
| 22 | Data Analysis Agent | 🔴 2 | ⬛ 0 |
| 23 | Website Scraping / Understanding | 🟢 **10** | 🟢 **10** |
| 24 | Image Description / Understanding | 📝 5 | 📝 5 |
| 25 | Customer Support Agent | 🟢 **10** | 🟢 **10** |
| 26 | Lead Scoring / Prospecting | 🟢 **8** | 🟢 **8** |
| 27 | Sprint / Project Summarizer | 🟢 **10** | ⬛ 0 |
| 28 | Transaction / Approval Agent | 🟢 **10** | ⬛ 0 |
| 29 | Home Automation Agent | 🟢 **10** | 🟢 **10** |
| 30 | Fitness / Health Tracking | 🟢 **9** | 🟢 **9** |
| 31 | Recipe / Cooking Agent | 🔴 2 | ⬛ 0 |
| 32 | Personal Finance Tracking | 🟡 7 | ⬛ 0 |
| 33 | SEO Optimization Agent | 🟢 **9** | 🟢 **9** |
| 34 | Landing Page Generator | 📝 5 | 📝 5 |
| 35 | Travel Planning Agent | 🟢 **8** | 🔴 0 |

### Tier 3 — Advanced Agents

| # | Role | 122B Think 16K | 35B Think ∞ |
|---|---|---|---|
| 36 | Code Generation Agent | 🟢 **10** | 🟢 **10** |
| 37 | Code Review Agent | 🟢 **10** | 🟢 **8** |
| 38 | QA / Test Writing Agent | 🟢 **8** | 🟢 **8** |
| 39 | Task Planning / Decomposition | 🟢 **9** | 🟢 **9** |
| 40 | Fact-Checking Agent | 🟢 **10** | 🟢 **10** |
| 41 | Critic / Review Agent | 📝 5 | 📝 5 |
| 42 | Market Research Agent | 🔴 0 | ⬛ 0 |
| 43 | Synthesizer / Aggregator | 🟡 7 | 🟢 **9** |
| 44 | Curriculum / Course Designer | 🟡 6 | 🟡 6 |
| 45 | Prototype Generator | 🟡 6 | 🟡 6 |
| 46 | DevOps Agent | 🟡 7 | 🟢 **10** |

### Tier 4 — Expert Agents

| # | Role | 122B Think 16K | 35B Think ∞ |
|---|---|---|---|
| 47 | Math / Logic Reasoning | 🟡 6 | 🟡 6 |
| 48 | STEM Analysis | 🟢 **10** | 🟢 **10** |
| 49 | Algorithm Exploration | 🟢 **10** | 🟢 **10** |

### Tier 5 — Complex / Senior Agents

| # | Role | 122B Think 16K | 35B Think ∞ |
|---|---|---|---|
| 50 | Orchestrator / Manager Agent | 🟢 **8** | 🟢 **8** |
| 51 | Software Architect Agent | 🟢 **10** | 🟢 **10** |
| 52 | Complex Debugger Agent | 🟢 **10** | 🟢 **8** |
| 53 | Legal Document Review | 🟢 **10** | 🟢 **10** |
| 54 | Medical / Health Analysis | 🟡 7 | 🟢 **10** |
| 55 | Financial Analysis / Stock Research | 🟢 **10** | 🟢 **10** |
| 56 | Security Analyst Agent | 🟡 6 | 🟢 **10** |
| 57 | SRE / Incident Response | 🟡 6 | ⬛ 0 |
| 58 | Book / Long-Form Writing | 📝 5 | 📝 5 |
| 59 | Compliance / Regulatory Agent | 🟡 7 | 🟢 **8** |

### Summary

| Metric | 122B Think 16K | 35B Think ∞ |
|---|---|---|
| **Total** | **~443/590 (75%)** | **405/582 (70%)** |
| 🟢 High (8-10) | 33 roles | 29 roles |
| 🟡 Medium (5-7) | 16 roles | 12 roles |
| 🔴 Low (0-4) | 4 roles | 2 roles |
| ⬛ 32K overflow | 0 | 10 roles |
| 📝 Manual review | 6 roles | 6 roles |

### Notes
- ⬛ **32K overflow:** The 35B model with unlimited thinking (llama.cpp, no thinking cap) fills the 32K max_tokens with reasoning tokens, leaving no room for the actual answer. The 122B model on SGLang has a 16K thinking budget that prevents this.
- 📝 Manual review tests default to 5/10 pending human review
- 🔴 Market Research (#42) fails on both models — overthinks and times out or overflows
- 🔴 Calendar (#8) fails on both models — timezone conversion errors
- The 35B model **outperforms 122B** on several tests (Editor, Synthesizer, DevOps, Medical, Security, Compliance) despite being ~3× smaller

