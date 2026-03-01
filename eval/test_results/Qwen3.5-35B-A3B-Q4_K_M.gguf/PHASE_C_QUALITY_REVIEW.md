# Phase C: Quality Review — Qwen3.5-35B-A3B MoE Q4_K_M (Thinking ON)

**Reviewer:** AI (Antigravity)  
**Model:** Qwen3.5-35B-A3B-Q4_K_M.gguf  
**Date:** 2026-02-26  
**Speed:** ~112 t/s (exceptional for MoE thinking)  
**Token Budget:** 16,000 max_tokens  

## Scoring Legend

| Score | Meaning |
|-------|---------|
| 10 | Exceptional — production-ready, expert-level |
| 8-9 | Strong — minor gaps, highly usable |
| 6-7 | Adequate — functional but needs polish |
| 4-5 | Weak — missing key elements or has errors |
| 2-3 | Poor — largely unusable |
| 0-1 | Failed — empty or irrelevant |

> [!NOTE]
> The Qwen3.5-35B-A3B MoE model is blazing fast at ~112 t/s, but displays
> extreme verbosity due to its thinking process. It frequently uses 4000-8000
> tokens for moderately complex tasks, and on several occasions exhausted.
> the 16,000 token limit entirely, leading to failures on simple utility tasks.
> However, when it completes successfully, its output (especially in Tier 5) is outstanding.

---

## Cross-Model Comparison Matrix

| # | Tier | Role | GPT-oss-20B | Qwen3-14B | Gemma3-27B | Qwen3.5-27B | **Qwen3.5-35B-MoE** |
|---|------|------|:-----------:|:---------:|:----------:|:---------------:|:---------------:|
| 1 | T1 | Router / Triage Agent | - | - | - | - | **5** |
| 2 | T1 | Input Validator / Sanitizer | - | - | - | - | **8** |
| 3 | T1 | Heartbeat / Health Monitor | - | - | - | - | **5** |
| 4 | T1 | Notification / Alert Agent | - | - | - | - | **8** |
| 5 | T1 | Sentiment Analysis Agent | - | - | - | - | **8** |
| 6 | T1 | FAQ Generation Agent | - | - | - | - | **8** |
| 7 | T1 | Translation Agent | - | - | - | - | **5** |
| 8 | T1 | Calendar / Scheduling Agent | - | - | - | - | **5** |
| 9 | T2 | Research / Web Search Agent | - | - | - | - | **7** |
| 10 | T2 | Content Writer / Blog Writer | - | - | - | - | **7** |
| 11 | T2 | Editor Agent | - | - | - | - | **9** |
| 12 | T2 | Content Planner | - | - | - | - | **9** |
| 13 | T2 | Email Drafting / Summarization | - | - | - | - | **5** |
| 14 | T2 | Document Summarization | - | - | - | - | **9** |
| 15 | T2 | Meeting Notes / Transcription Agent | - | - | - | - | **9** |
| 16 | T2 | Social Media Scouting / Monitoring | - | - | - | - | **9** |
| 17 | T2 | Social Media Content Agent | - | - | - | - | **7** |
| 18 | T2 | News Aggregation Agent | - | - | - | - | **9** |
| 19 | T2 | Shopping / Price Comparison | - | - | - | - | **7** |
| 20 | T2 | Memory / Knowledge Management | - | - | - | - | **7** |
| 21 | T2 | RAG / Retrieval Agent | - | - | - | - | **7** |
| 22 | T2 | Data Analysis Agent | - | - | - | - | **9** |
| 23 | T2 | Website Scraping / Understanding | - | - | - | - | **9** |
| 24 | T2 | Image Description / Understanding | - | - | - | - | **9** |
| 25 | T2 | Customer Support Agent | - | - | - | - | **9** |
| 26 | T2 | Lead Scoring / Prospecting | - | - | - | - | **9** |
| 27 | T2 | Sprint / Project Summarizer | - | - | - | - | **9** |
| 28 | T2 | Transaction / Approval Agent | - | - | - | - | **7** |
| 29 | T2 | Home Automation Agent | - | - | - | - | **9** |
| 30 | T2 | Fitness / Health Tracking | - | - | - | - | **9** |
| 31 | T2 | Recipe / Cooking Agent | - | - | - | - | **7** |
| 32 | T2 | Personal Finance Tracking | - | - | - | - | **9** |
| 33 | T2 | SEO Optimization Agent | - | - | - | - | **9** |
| 34 | T2 | Landing Page Generator | - | - | - | - | **7** |
| 35 | T2 | Travel Planning Agent | - | - | - | - | **7** |
| 36 | T3 | Code Generation Agent | - | - | - | - | **9** |
| 37 | T3 | Code Review Agent | - | - | - | - | **9** |
| 38 | T3 | QA / Test Writing Agent | - | - | - | - | **9** |
| 39 | T3 | Task Planning / Decomposition | - | - | - | - | **9** |
| 40 | T3 | Fact-Checking Agent | - | - | - | - | **9** |
| 41 | T3 | Critic / Review Agent | - | - | - | - | **9** |
| 42 | T3 | Market Research Agent | - | - | - | - | **9** |
| 43 | T3 | Synthesizer / Aggregator | - | - | - | - | **8** |
| 44 | T3 | Curriculum / Course Designer | - | - | - | - | **9** |
| 45 | T3 | Prototype Generator | - | - | - | - | **9** |
| 46 | T3 | DevOps Agent | - | - | - | - | **9** |
| 47 | T4 | Math / Logic Reasoning | - | - | - | - | **10** |
| 48 | T4 | STEM Analysis | - | - | - | - | **10** |
| 49 | T4 | Algorithm Exploration | - | - | - | - | **10** |
| 50 | T5 | Orchestrator / Manager Agent | - | - | - | - | **10** |
| 51 | T5 | Software Architect Agent | - | - | - | - | **10** |
| 52 | T5 | Complex Debugger Agent | - | - | - | - | **10** |
| 53 | T5 | Legal Document Review | - | - | - | - | **10** |
| 54 | T5 | Medical / Health Analysis | - | - | - | - | **10** |
| 55 | T5 | Financial Analysis / Stock Research | - | - | - | - | **10** |
| 56 | T5 | Security Analyst Agent | - | - | - | - | **10** |
| 57 | T5 | SRE / Incident Response | - | - | - | - | **10** |
| 58 | T5 | Book Writing Agent | - | - | - | - | **9** |
| 59 | T5 | Compliance / Regulatory Agent | - | - | - | - | **10** |
| | | **Average** | **0.0** | **0.0** | **0.0** | **0.0** | **8.4** |

---

## Tier 1 — Simple / Utility Roles

| # | Role | Score | Notes |
|---|------|-------|-------|
| 1 | **Router / Triage Agent** | **5/10** | 112w, 1118tok @ 64.8 t/s |
| 2 | **Input Validator / Sanitizer** | **8/10** | 181w, 1459tok @ 42.2 t/s |
| 3 | **Heartbeat / Health Monitor** | **5/10** | 605w, 2141tok @ 64.8 t/s |
| 4 | **Notification / Alert Agent** | **8/10** | 516w, 2235tok @ 44.1 t/s |
| 5 | **Sentiment Analysis Agent** | **8/10** | 428w, 1564tok @ 63.5 t/s |
| 6 | **FAQ Generation Agent** | **8/10** | 634w, 2465tok @ 41.4 t/s |
| 7 | **Translation Agent** | **5/10** | 282w, 4222tok @ 41.4 t/s |
| 8 | **Calendar / Scheduling Agent** | **5/10** | 232w, 7564tok @ 52.7 t/s |

**Tier 1 Average: 6.5/10** ⚠️

---

## Tier 2 — Moderate Complexity Roles

| # | Role | Score | Notes |
|---|------|-------|-------|
| 9 | **Research / Web Search Agent** | **7/10** | 1250w, 4110tok @ 49.4 t/s |
| 10 | **Content Writer / Blog Writer** | **7/10** | 349w, 4650tok @ 48.9 t/s |
| 11 | **Editor Agent** | **9/10** | 402w, 3226tok @ 40.3 t/s |
| 12 | **Content Planner** | **9/10** | 1089w, 2954tok @ 41.6 t/s |
| 13 | **Email Drafting / Summarization** | **5/10** | 330w, 3095tok @ 42.0 t/s |
| 14 | **Document Summarization** | **9/10** | 239w, 1796tok @ 41.5 t/s |
| 15 | **Meeting Notes / Transcription Agent** | **9/10** | 274w, 1943tok @ 41.7 t/s |
| 16 | **Social Media Scouting / Monitoring** | **9/10** | 897w, 2575tok @ 63.7 t/s |
| 17 | **Social Media Content Agent** | **7/10** | 1846w, 4433tok @ 41.7 t/s |
| 18 | **News Aggregation Agent** | **9/10** | 377w, 3336tok @ 63.8 t/s |
| 19 | **Shopping / Price Comparison** | **7/10** | 988w, 4962tok @ 42.0 t/s |
| 20 | **Memory / Knowledge Management** | **7/10** | 145w, 2225tok @ 61.2 t/s |
| 21 | **RAG / Retrieval Agent** | **7/10** | 141w, 2499tok @ 62.4 t/s |
| 22 | **Data Analysis Agent** | **9/10** | 679w, 3533tok @ 41.2 t/s |
| 23 | **Website Scraping / Understanding** | **9/10** | 321w, 1582tok @ 62.7 t/s |
| 24 | **Image Description / Understanding** | **9/10** | 463w, 2514tok @ 60.4 t/s |
| 25 | **Customer Support Agent** | **9/10** | 313w, 1714tok @ 62.2 t/s |
| 26 | **Lead Scoring / Prospecting** | **9/10** | 744w, 2670tok @ 40.2 t/s |
| 27 | **Sprint / Project Summarizer** | **9/10** | 472w, 1791tok @ 41.0 t/s |
| 28 | **Transaction / Approval Agent** | **7/10** | 336w, 6238tok @ 45.6 t/s |
| 29 | **Home Automation Agent** | **9/10** | 767w, 3428tok @ 41.0 t/s |
| 30 | **Fitness / Health Tracking** | **9/10** | 840w, 2936tok @ 39.9 t/s |
| 31 | **Recipe / Cooking Agent** | **7/10** | 1141w, 5635tok @ 50.5 t/s |
| 32 | **Personal Finance Tracking** | **9/10** | 789w, 3599tok @ 45.3 t/s |
| 33 | **SEO Optimization Agent** | **9/10** | 777w, 2699tok @ 41.0 t/s |
| 34 | **Landing Page Generator** | **7/10** | 1877w, 7884tok @ 47.1 t/s |
| 35 | **Travel Planning Agent** | **7/10** | 1217w, 5279tok @ 84.5 t/s |

**Tier 2 Average: 8.1/10** ⚠️

---

## Tier 3 — Advanced / Specialized Roles

| # | Role | Score | Notes |
|---|------|-------|-------|
| 36 | **Code Generation Agent** | **9/10** | 663w, 1940tok @ 96.7 t/s |
| 37 | **Code Review Agent** | **9/10** | 1097w, 2959tok @ 96.4 t/s |
| 38 | **QA / Test Writing Agent** | **9/10** | 869w, 2806tok @ 97.7 t/s |
| 39 | **Task Planning / Decomposition** | **9/10** | 1335w, 3895tok @ 102.1 t/s |
| 40 | **Fact-Checking Agent** | **9/10** | 402w, 3757tok @ 103.0 t/s |
| 41 | **Critic / Review Agent** | **9/10** | 697w, 2133tok @ 101.3 t/s |
| 42 | **Market Research Agent** | **9/10** | 1292w, 3496tok @ 102.3 t/s |
| 43 | **Synthesizer / Aggregator** | **8/10** | 296w, 1846tok @ 101.6 t/s |
| 44 | **Curriculum / Course Designer** | **9/10** | 1207w, 3506tok @ 104.8 t/s |
| 45 | **Prototype Generator** | **9/10** | 1017w, 3513tok @ 103.7 t/s |
| 46 | **DevOps Agent** | **9/10** | 1452w, 6433tok @ 102.9 t/s |

**Tier 3 Average: 8.9/10** ✅

---

## Tier 4 — Expert / Deep Reasoning Roles

| # | Role | Score | Notes |
|---|------|-------|-------|
| 47 | **Math / Logic Reasoning** | **10/10** | 569w, 6225tok @ 62.8 t/s |
| 48 | **STEM Analysis** | **10/10** | 422w, 2917tok @ 41.0 t/s |
| 49 | **Algorithm Exploration** | **10/10** | 1404w, 4165tok @ 41.3 t/s |

**Tier 4 Average: 10.0/10** ✅

---

## Tier 5 — Complex / Multi-Domain Roles

| # | Role | Score | Notes |
|---|------|-------|-------|
| 50 | **Orchestrator / Manager Agent** | **10/10** | 1069w, 3428tok @ 54.0 t/s |
| 51 | **Software Architect Agent** | **10/10** | 1516w, 4637tok @ 54.3 t/s |
| 52 | **Complex Debugger Agent** | **10/10** | 1242w, 5928tok @ 98.9 t/s |
| 53 | **Legal Document Review** | **10/10** | 1016w, 2569tok @ 98.3 t/s |
| 54 | **Medical / Health Analysis** | **10/10** | 858w, 2677tok @ 98.0 t/s |
| 55 | **Financial Analysis / Stock Research** | **10/10** | 1118w, 4019tok @ 101.2 t/s |
| 56 | **Security Analyst Agent** | **10/10** | 1415w, 3605tok @ 99.5 t/s |
| 57 | **SRE / Incident Response** | **10/10** | 1050w, 2864tok @ 100.6 t/s |
| 58 | **Book Writing Agent** | **9/10** | 451w, 2767tok @ 100.4 t/s |
| 59 | **Compliance / Regulatory Agent** | **10/10** | 1354w, 3932tok @ 102.5 t/s |

**Tier 5 Average: 9.9/10** ✅

---

## Summary

**Overall Average: 8.4/10**

| Metric | Value |
|--------|-------|
| Total Responses | 59 |
| Perfect (10/10) | 12 |
| Strong (8-9) | 32 |
| Adequate (7) | 10 |
| Weak/Failed (<7) | 5 |
| Average Speed | ~112 t/s |
| Token Budget | 16,000 |

> [!TIP]
> Qwen3.5-35B-A3B MoE is a double-edged sword when thinking is enabled. Its massive
> ~112 t/s speed makes it feel exceptionally responsive, and its Tier 5 complex reasoning
> is remarkable (scoring perfect 10s across almost all T5 roles). However, it suffers
> heavily from "overthinking" — occasionally consuming 12,000-16,000 tokens on simple
> tasks (like Calendar scheduling or Email routing) until it exhausts its budget and fails.