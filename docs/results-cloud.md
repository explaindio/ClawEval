# ☁️ Cloud Models — Phase F (59-Role Evaluation)

[← Back to Main Results](../README.md) · [Phase G Discriminator Tests →](results-phase-g.md)

## ⚡ Speed & Efficiency (Alibaba Coding Plan API)

| Model | Score | Total Tokens | Avg Tokens/Test | Speed |
|-------|-------|:---:|:---:|:---:|
| **K2.5 Think** | 473/590 (80%) | 43K | 734 | ~30 t/s |
| **K2.5 NoThink** | 469/590 (80%) | 46K | 774 | ~35 t/s |
| **GLM-5 Think** | 465/590 (79%) | **185K** | **3,137** | ~45 t/s |
| **GLM-5 NoThink** | 461/590 (78%) | 34K | 578 | ~30 t/s |
| **M2.5 Think** | 465/590 (79%) | 125K | 2,112 | **~85 t/s** |

> 💡 **MiniMax-M2.5 is the fastest** at ~85 t/s — 2-3x faster than other models. GLM-5 Think uses the most tokens (185K). Kimi K2.5 is the most token-efficient (734 tok/test).

---

## Phase F — All Cloud Models Compared

| # | Agent Role | K2.5 Think | K2.5 NT | GLM-5 Think | GLM-5 NT | M2.5 Think |
|---|---|---|---|---|---|---|
| | | Kimi-K2.5 | Kimi-K2.5 | GLM-5 | GLM-5 | MiniMax-M2.5 |
| | **Tier 1 — Utility** | | | | | |
| 1 | Router / Triage | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 |
| 4 | Notification | 🟢 **9** | 🟢 **9** | 🟢 8 | 🟡 7 | 🟢 **9** |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 **7** | 🟡 6 | 🟡 **7** | 🔴 2 | 🟡 6 |
| 7 | Translation | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | | |
| 9 | Research Agent | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟢 **10** | 🟢 9 | 🔴 0 | 🟢 **10** | 🟢 **10** |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟢 **10** | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 8 |
| 14 | Doc Summary | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** |
| 15 | Meeting Notes | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 8 | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 **6** | 🟡 **6** | 🟡 **6** | 🔴 2 | 🟡 **6** |
| 22 | Data Analysis | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 **3** | 🔴 2 |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** | 🟢 8 |
| 27 | Sprint Summary | 🟡 7 | 🟡 5 | 🟢 **9** | 🟡 7 | 🟢 **9** |
| 28 | Transaction | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| 29 | Home Automation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🔴 0 |
| 30 | Fitness Tracking | 🟢 8 | 🟢 8 | 🟢 **9** | 🟢 **9** | 🟢 8 |
| 31 | Recipe / Cooking | 🔴 1 | 🔴 1 | 🔴 2 | 🔴 1 | 🔴 2 |
| 32 | Personal Finance | 🟡 5 | 🟡 5 | 🟡 **7** | 🟡 **7** | 🟡 **7** |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 | 🔴 3 |
| | **Tier 3 — Advanced** | | | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 39 | Task Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🟢 8 | 🟢 8 | 🟢 8 | 🟡 6 | 🟢 **9** |
| 43 | Synthesizer | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** |
| 44 | Curriculum Design | 🟡 6 | 🟡 **7** | 🟡 6 | 🟡 6 | 🟡 6 |
| 45 | Prototype Gen | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 **7** | 🔴 2 |
| 46 | DevOps | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 |
| | **Tier 4 — Expert** | | | | | |
| 47 | Math / Logic | 🟢 **8** | 🟢 **8** | 🟡 6 | 🔴 4 | 🔴 4 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 52 | Debugger | 🟢 **10** | 🟢 **10** | 🟢 8 | 🟢 **10** | 🟢 **10** |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 |
| 54 | Medical | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 55 | Financial | 🟢 **10** | 🟢 **10** | 🟡 6 | 🟡 7 | 🟢 **10** |
| 56 | Security | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🔴 3 | 🔴 2 | 🔴 4 | 🟡 **6** | 🔴 3 |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟢 8 | 🟢 **9** | 🟡 7 | 🟢 8 | 🟢 **9** |
| | **TOTAL** | **473 (80%)** | **469 (80%)** | **465 (79%)** | **461 (78%)** | **465 (79%)** |

### Tier Breakdown

| Tier | K2.5 Think | K2.5 NT | GLM-5 Think | GLM-5 NT | M2.5 Think |
|------|-----------|---------|-------------|----------|------------|
| 1 — Utility | 59/80 (74%) | 58/80 (73%) | 58/80 (73%) | 53/80 (66%) | 58/80 (73%) |
| 2 — Moderate | 222/270 (82%) | 218/270 (81%) | 214/270 (79%) | 218/270 (81%) | 209/270 (77%) |
| 3 — Advanced | 91/110 (83%) | 93/110 (85%) | 89/110 (81%) | 88/110 (80%) | 89/110 (81%) |
| 4 — Expert | 28/30 (**93%**) | 28/30 (**93%**) | 26/30 (87%) | 24/30 (80%) | 24/30 (80%) |
| 5 — Senior | 83/100 (83%) | 82/100 (82%) | 78/100 (78%) | 78/100 (78%) | **85/100 (85%)** |

### Key Observations

- **Kimi K2.5 leads overall** (473 Think / 469 NoThink) — most consistent cloud model
- **MiniMax-M2.5 dominates Senior tier (85%)** — Architect 10, Debugger 10, Financial 10, Medical 10
- **MiniMax-M2.5 is 2-3x faster** (~85 t/s) than other models — best for latency-sensitive use
- **MiniMax-M2.5 weaknesses**: Home Automation 0, Travel 3, Prototype 2, Math 4
- **GLM-5 Think vs NoThink is volatile** — 23 tests differ (vs only 9 for Kimi K2.5)

### Notes

- All models tested via Alibaba Coding Plan API (cloud)
- 📝 Manual review tests default to 5/10 pending human review
- Calendar (0/10) and Recipe (1-2/10) are hard for all models
- **M2.5 NoThink + Phase G results pending**

---

## Phase G — Discriminator Scores (Harder Tests)

See [Phase G Results](results-phase-g.md#%EF%B8%8F-cloud-models) for the 11 harder tests:

**Kimi K2.5:**
- Think: 96/110 (87%) — No test below 7/10
- NoThink: 91/110 (83%)

**GLM-5:**
- Think: 76/110 (69%) — Input Validator timed out (0/10)
- NoThink: 80/110 (73%) — Better than Think due to no timeout issues

**MiniMax-M2.5:**
- Think: 78/110 (71%) — Content Planner timed out (0/10), Architect 10/10, NoThink not supported

---

[← Back to Main Results](../README.md)
