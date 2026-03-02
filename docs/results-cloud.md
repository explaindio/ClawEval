# ☁️ Cloud Models — Phase F (59-Role Evaluation)

[← Back to Main Results](../README.md) · [Phase G Discriminator Tests →](results-phase-g.md)

## ⚡ Speed & Efficiency (Alibaba Coding Plan API)

| Model | Score | Total Tokens | Avg Tokens/Test | Speed |
|-------|-------|:---:|:---:|:---:|
| **K2.5 Think** | 473/590 (80%) | 43K | 734 | ~30 t/s |
| **K2.5 NoThink** | 469/590 (80%) | 46K | 774 | ~35 t/s |
| **GLM-5 Think** | 465/590 (79%) | **185K** | **3,137** | ~45 t/s |
| **GLM-5 NoThink** | 461/590 (78%) | 34K | 578 | ~30 t/s |

> 💡 **GLM-5 Think uses 4.3x more tokens** than Kimi K2.5 due to heavy internal reasoning — despite faster per-token speed, tests take 2-3x longer wall-clock time. GLM-5 NoThink is very efficient (578 tok/test vs K2.5's 774).

---

## Phase F — All Cloud Models Compared

| # | Agent Role | K2.5 Think | K2.5 NoThink | GLM-5 Think | GLM-5 NoThink |
|---|---|---|---|---|---|
| | | Kimi-K2.5 | Kimi-K2.5 | GLM-5 | GLM-5 |
| | | Alibaba | `thinking: False` | Alibaba | `enable_thinking: false` |
| | **Tier 1 — Utility** | | | | |
| 1 | Router / Triage | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 **10** |
| 2 | Input Validator | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 3 | Health Monitor | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 5 |
| 4 | Notification | 🟢 **9** | 🟢 **9** | 🟢 8 | 🟡 7 |
| 5 | Sentiment | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 6 | FAQ Generation | 🟡 **7** | 🟡 6 | 🟡 **7** | 🔴 2 |
| 7 | Translation | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 8 | Calendar | 🔴 0 | 🔴 0 | 🔴 0 | 🔴 0 |
| | **Tier 2 — Moderate** | | | | |
| 9 | Research Agent | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 10 | Content Writer | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 11 | Editor | 🟢 **10** | 🟢 9 | 🔴 0 | 🟢 **10** |
| 12 | Content Planner | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 13 | Email Drafting | 🟢 **10** | 🟢 9 | 🟢 8 | 🟢 **9** |
| 14 | Doc Summary | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 15 | Meeting Notes | 🟢 10 | 🟢 10 | 🟢 **9** | 🟢 8 |
| 16 | Social Scouting | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 17 | Social Content | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 18 | News Aggregation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 19 | Shopping | 🟢 10 | 🟢 10 | 🟢 **10** | 🟢 8 |
| 20 | Memory Mgmt | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 21 | RAG / Retrieval | 🟡 **6** | 🟡 **6** | 🟡 **6** | 🔴 2 |
| 22 | Data Analysis | 🔴 2 | 🔴 2 | 🔴 2 | 🔴 **3** |
| 23 | Web Scraping | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 24 | Image Description | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 25 | Customer Support | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 26 | Lead Scoring | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 **10** |
| 27 | Sprint Summary | 🟡 7 | 🟡 5 | 🟢 **9** | 🟡 7 |
| 28 | Transaction | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 **10** |
| 29 | Home Automation | 🟢 10 | 🟢 10 | 🟢 **10** | 🟢 9 |
| 30 | Fitness Tracking | 🟢 8 | 🟢 8 | 🟢 **9** | 🟢 **9** |
| 31 | Recipe / Cooking | 🔴 1 | 🔴 1 | 🔴 2 | 🔴 1 |
| 32 | Personal Finance | 🟡 5 | 🟡 5 | 🟡 **7** | 🟡 **7** |
| 33 | SEO Optimization | 🟢 9 | 🟢 9 | 🟢 9 | 🟢 9 |
| 34 | Landing Page | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 35 | Travel Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 |
| | **Tier 3 — Advanced** | | | | |
| 36 | Code Generation | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 37 | Code Review | 🟢 10 | 🟢 10 | 🟢 **10** | 🟢 8 |
| 38 | QA / Test Writing | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 39 | Task Planning | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 9 |
| 40 | Fact-Checking | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 41 | Critic / Review | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 42 | Market Research | 🟢 8 | 🟢 8 | 🟢 **8** | 🟡 6 |
| 43 | Synthesizer | 🟢 9 | 🟢 **10** | 🟢 9 | 🟢 **10** |
| 44 | Curriculum Design | 🟡 6 | 🟡 **7** | 🟡 6 | 🟡 6 |
| 45 | Prototype Gen | 🟡 5 | 🟡 5 | 🟡 5 | 🟡 **7** |
| 46 | DevOps | 🟢 **10** | 🟢 **10** | 🟢 9 | 🟢 **10** |
| | **Tier 4 — Expert** | | | | |
| 47 | Math / Logic | 🟢 **8** | 🟢 **8** | 🟡 6 | 🔴 4 |
| 48 | STEM Analysis | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 49 | Algorithm | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| | **Tier 5 — Senior** | | | | |
| 50 | Orchestrator | 🟢 8 | 🟢 8 | 🟢 8 | 🟢 8 |
| 51 | Architect | 🟢 **10** | 🟢 9 | 🟢 **10** | 🟢 9 |
| 52 | Debugger | 🟢 **10** | 🟢 **10** | 🟢 8 | 🟢 **10** |
| 53 | Legal Review | 🟢 10 | 🟢 10 | 🟢 **10** | 🟢 9 |
| 54 | Medical | 🟢 9 | 🟢 9 | 🟢 **10** | 🟢 9 |
| 55 | Financial | 🟢 **10** | 🟢 **10** | 🟡 6 | 🟡 **7** |
| 56 | Security | 🟢 10 | 🟢 10 | 🟢 10 | 🟢 10 |
| 57 | SRE / Incident | 🔴 3 | 🔴 2 | 🔴 4 | 🟡 **6** |
| 58 | Book Writing | 📝 5 | 📝 5 | 📝 5 | 📝 5 |
| 59 | Compliance | 🟢 8 | 🟢 **9** | 🟡 7 | 🟢 **8** |
| | **TOTAL** | **473/590 (80%)** | **469/590 (80%)** | **465/590 (79%)** | **461/590 (78%)** |

### Tier Breakdown

| Tier | K2.5 Think | K2.5 NoThink | GLM-5 Think | GLM-5 NoThink |
|------|-----------|-------------|-------------|---------------|
| 1 — Utility | 59/80 (74%) | 58/80 (73%) | 58/80 (73%) | 53/80 (66%) |
| 2 — Moderate | 222/270 (82%) | 218/270 (81%) | 214/270 (79%) | 218/270 (81%) |
| 3 — Advanced | 91/110 (83%) | 93/110 (85%) | 89/110 (81%) | 88/110 (80%) |
| 4 — Expert | 28/30 (**93%**) | 28/30 (**93%**) | 26/30 (87%) | 24/30 (80%) |
| 5 — Senior | 83/100 (83%) | 82/100 (82%) | 78/100 (78%) | 78/100 (78%) |

### Key Observations

- **Kimi K2.5 leads overall** (473 Think / 469 NoThink) — most consistent cloud model
- **GLM-5 Think vs NoThink is volatile** — 23 tests differ (vs only 9 for Kimi K2.5)
- **GLM-5 Editor bug**: Think scored 0/10 but NoThink scored 10/10 — formatting issue
- **GLM-5 excels at**: Sprint Summary (9), Transaction (10), Personal Finance (7), Medical (10)
- **GLM-5 struggles with**: FAQ Gen NoThink (2), RAG NoThink (2), Math NoThink (4)
- **Thinking hurts GLM-5** on some tests more than it helps — NoThink is sometimes better

### Notes

- All models tested via Alibaba Coding Plan API (cloud)
- 📝 Manual review tests default to 5/10 pending human review
- Calendar (0/10) and Recipe (1-2/10) are hard for all models

---

## Phase G — Discriminator Scores (Harder Tests)

See [Phase G Results](results-phase-g.md#%EF%B8%8F-cloud-models) for the 11 harder tests:

**Kimi K2.5:**
- Think: 96/110 (87%) — No test below 7/10
- NoThink: 91/110 (83%)

**GLM-5:**
- Think: 76/110 (69%) — Input Validator timed out (0/10)
- NoThink: 80/110 (73%) — Better than Think due to no timeout issues

---

[← Back to Main Results](../README.md)
