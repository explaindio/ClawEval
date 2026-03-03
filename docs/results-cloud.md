# ☁️ Cloud Models — Phase F (59-Role Evaluation)

[← Back to Main Results](../README.md) · [Phase G Discriminator Tests →](results-phase-g.md)

## ⚡ Speed & Efficiency (Alibaba Coding Plan API)

| Model | Score | Total Tokens | Avg Tok/Test | Speed |
|-------|-------|:---:|:---:|:---:|
| **Qwen3.5+ NT** 🥇 | **482/590 (82%)** | 36K | **609** | ~40 t/s |
| **K2.5 Think** | 473/590 (80%) | 43K | 734 | ~30 t/s |
| **K2.5 NoThink** | 469/590 (80%) | 46K | 774 | ~35 t/s |
| **Qwen3.5+ Think** | 465/590 (79%) | **328K** | **5,562** | ~60 t/s |
| **GLM-5 Think** | 465/590 (79%) | 185K | 3,137 | ~45 t/s |
| **M2.5 Think** | 465/590 (79%) | 125K | 2,112 | **~85 t/s** |
| **GLM-5 NoThink** | 461/590 (78%) | 34K | 578 | ~30 t/s |

> 💡 **Qwen3.5-Plus NoThink is the new Phase F champion** at 482/590 (82%) — beating K2.5 Think by 9 points. It's also the most token-efficient (609 tok/test). MiniMax-M2.5 is the fastest per-token (~85 t/s). Qwen3.5-Plus Think uses the most tokens (328K) due to heavy reasoning.

---

## Phase F — All Cloud Models Compared

| # | Role | K2.5 T | K2.5 NT | GLM T | GLM NT | M2.5 T | Q3.5+ T | Q3.5+ NT |
|---|---|---|---|---|---|---|---|---|
| | **Tier 1 — Utility** | | | | | | | |
| 1 | Router / Triage | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 | 🔴 3 |
| 4 | Notification | 🟢 **9** | 🟢 **9** | 🟢 8 | 🟡 7 | 🟢 **9** | 🟢 **9** | 🟢 **9** |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 7 | 🟡 6 | 🟡 7 | 🔴 2 | 🟡 6 | 🟡 5 | 🟢 **8** |
| 7 | Translation | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | | | | |
| 9 | Research Agent | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟢 **10** | 🟢 9 | 🔴 0 | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟢 **10** | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 8 | 🟡 6 | 🟢 8 |
| 14 | Doc Summary | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** | 🟢 8 | 🟢 8 |
| 15 | Meeting Notes | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 8 | 🟢 9 | 🟢 **10** | 🟢 9 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 10 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 8 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 **6** | 🟡 **6** | 🟡 **6** | 🔴 2 | 🟡 **6** | 🔴 2 | 🔴 4 |
| 22 | Data Analysis | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 3 | 🔴 2 | 🔴 2 | 🟡 **5** |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** | 🟢 8 | 🟢 8 | 🟢 **10** |
| 27 | Sprint Summary | 🟡 7 | 🟡 5 | 🟢 **9** | 🟡 7 | 🟢 **9** | 🟢 **9** | 🟢 **9** |
| 28 | Transaction | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 **10** | 🟢 9 |
| 29 | Home Automation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🔴 0 | 🟢 10 | 🟢 10 |
| 30 | Fitness Tracking | 🟢 8 | 🟢 8 | 🟢 **9** | 🟢 **9** | 🟢 8 | 🟢 **9** | 🟢 8 |
| 31 | Recipe / Cooking | 🔴 1 | 🔴 1 | 🔴 2 | 🔴 1 | 🔴 2 | 🔴 1 | 🟢 **9** |
| 32 | Personal Finance | 🟡 5 | 🟡 5 | 🟡 **7** | 🟡 **7** | 🟡 **7** | 🟡 **7** | 🟡 6 |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 | 🔴 3 | 🟡 7 | 🟢 9 |
| | **Tier 3 — Advanced** | | | | | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 8 | 🟢 10 | 🟢 10 | 🟢 10 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 39 | Task Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🟢 8 | 🟢 8 | 🟢 8 | 🟡 6 | 🟢 **9** | 🟡 6 | 🟡 5 |
| 43 | Synthesizer | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 44 | Curriculum Design | 🟡 6 | 🟡 **7** | 🟡 6 | 🟡 6 | 🟡 6 | 🟡 5 | 🟡 **7** |
| 45 | Prototype Gen | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 **7** | 🔴 2 | 🟡 **7** | 🟡 **7** |
| 46 | DevOps | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 |
| | **Tier 4 — Expert** | | | | | | | |
| 47 | Math / Logic | 🟢 **8** | 🟢 **8** | 🟡 6 | 🔴 4 | 🔴 4 | 🟡 6 | 🟡 6 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🔴 0 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 9 |
| 52 | Debugger | 🟢 **10** | 🟢 **10** | 🟢 8 | 🟢 **10** | 🟢 **10** | 🟡 6 | 🟢 **10** |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 9 | 🟢 10 | 🟢 10 | 🟢 8 |
| 54 | Medical | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 **10** | 🟢 **10** |
| 55 | Financial | 🟢 **10** | 🟢 **10** | 🟡 6 | 🟡 7 | 🟢 **10** | 🟡 6 | 🟢 **10** |
| 56 | Security | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🔴 3 | 🔴 2 | 🔴 4 | 🟡 **6** | 🔴 3 | 🟡 **6** | 🟡 **6** |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟢 8 | 🟢 **9** | 🟡 7 | 🟢 8 | 🟢 **9** | 🟢 8 | 🟢 8 |
| | **TOTAL** | **473** | **469** | **465** | **461** | **465** | **465** | **482** 🥇 |

### Tier Breakdown

| Tier | K2.5 T | K2.5 NT | GLM T | GLM NT | M2.5 T | Q3.5+ T | Q3.5+ NT |
|------|--------|---------|-------|--------|--------|---------|----------|
| 1 — Utility | 59 (74%) | 58 (73%) | 58 (73%) | 53 (66%) | 58 (73%) | 58 (73%) | 59 (74%) |
| 2 — Moderate | 222 (82%) | 218 (81%) | 214 (79%) | 218 (81%) | 209 (77%) | 214 (79%) | **232 (86%)** |
| 3 — Advanced | 91 (83%) | 93 (85%) | 89 (81%) | 88 (80%) | 89 (81%) | 88 (80%) | **91 (83%)** |
| 4 — Expert | **28 (93%)** | **28 (93%)** | 26 (87%) | 24 (80%) | 24 (80%) | 26 (87%) | 16 (53%) |
| 5 — Senior | 83 (83%) | 82 (82%) | 78 (78%) | 78 (78%) | **85 (85%)** | 79 (79%) | **84 (84%)** |

### Key Observations

- **Qwen3.5-Plus NoThink is Phase F champion** (482/590, 82%) — beats K2.5 Think by 9 points
- **Recipe 9/10!** Qwen3.5+ NT is the only model to crack this role (all others score 1-2)
- **STEM 0/10 without thinking** — Qwen needs reasoning for computation-heavy tasks
- **Most token-efficient** (609 tok/test) — 9x fewer tokens than its own Think mode (5,562)
- **MiniMax-M2.5 fastest per-token** (~85 t/s) but Qwen3.5+ NT wins on total wall-clock time

### Notes

- All models tested via Alibaba Coding Plan API (cloud)
- 📝 Manual review tests default to 5/10 pending human review
- Calendar (0/10) is hard for all models
- MiniMax-M2.5 NoThink not supported by API

---

## Phase G — Discriminator Scores (Harder Tests)

See [Phase G Results](results-phase-g.md#%EF%B8%8F-cloud-models) for the 11 harder tests:

**Kimi K2.5:**
- Think: 96/110 (87%) — No test below 7/10
- NoThink: 91/110 (83%)

**GLM-5:**
- Think: 76/110 (69%) — Input Validator timed out (0/10)
- NoThink: 80/110 (73%)

**MiniMax-M2.5:**
- Think: 78/110 (71%) — Content Planner timed out (0/10), NoThink not supported

**Qwen3.5-Plus:**
- Think: 86/110 (78%) — Fact-Check 10/10 (20/20), Algorithm 10/10
- NoThink: 86/110 (78%) — Sentiment 10/10 (19/20), Architect 10/10

---

[← Back to Main Results](../README.md)
