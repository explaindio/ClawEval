# OpenClaw Subagent Types — Complete Reference

## Tier 1 — Lightweight Roles (1–4B models sufficient)

| # | Subagent Role | Function |
|---|---|---|
| 1 | **Router / Triage Agent** | Classifies incoming requests and routes to the correct specialist agent |
| 2 | **Input Validator / Sanitizer** | Checks inputs for format compliance, safety, completeness |
| 3 | **Heartbeat / Health Monitor** | Runs on cron schedule to check system status, send alerts, perform maintenance |
| 4 | **Notification / Alert Agent** | Monitors conditions and sends alerts via messaging channels |
| 5 | **Sentiment Analysis Agent** | Classifies text sentiment for social media monitoring, customer feedback |
| 6 | **FAQ Generation Agent** | Converts documentation into Q&A format |
| 7 | **Translation Agent** | Translates between languages |
| 8 | **Calendar / Scheduling Agent** | Manages calendar bookings, detects conflicts, coordinates meeting times |

## Tier 2 — Mid-Range Roles (8–14B recommended)

| # | Subagent Role | Function |
|---|---|---|
| 9 | **Research / Web Search Agent** | Gathers information using search tools, synthesizes findings into structured notes |
| 10 | **Content Writer / Blog Writer** | Drafts articles and long-form content from research notes |
| 11 | **Editor Agent** | Reviews content for clarity, grammar, coherence, and style |
| 12 | **Content Planner** | Plans content structure, creates outlines and editorial calendars |
| 13 | **Email Drafting / Summarization** | Classifies incoming emails, drafts contextual responses, manages email workflows |
| 14 | **Document Summarization** | Condenses long documents into key points |
| 15 | **Meeting Notes / Transcription Agent** | Processes meeting recordings, extracts summaries and action items |
| 16 | **Social Media Scouting / Monitoring** | Monitors social platforms, generates content, tracks trends |
| 17 | **Social Media Content Agent** | Generates platform-appropriate posts with hashtags and formatting |
| 18 | **News Aggregation Agent** | Collects, categorizes, and summarizes news from multiple sources |
| 19 | **Shopping / Price Comparison** | Compares prices across retailers, tracks deals, makes recommendations |
| 20 | **Memory / Knowledge Management** | Curates long-term facts, decisions, and preferences for other agents |
| 21 | **RAG / Retrieval Agent** | Retrieves relevant chunks from vector stores and knowledge bases |
| 22 | **Data Analysis Agent** | Cleans data, runs statistics, generates plots via code execution |
| 23 | **Website Scraping / Understanding** | Navigates websites, extracts structured information, fills forms |
| 24 | **Image Description / Understanding** | Describes images, reads charts, interprets visual content |
| 25 | **Customer Support Agent** | Handles inquiries, routes to specialists, manages multi-turn support conversations |
| 26 | **Lead Scoring / Prospecting** | Enriches leads with company data, scores them, prioritizes for outreach |
| 27 | **Sprint / Project Summarizer** | Summarizes sprint activities and generates progress reports from PM tools |
| 28 | **Transaction / Approval Agent** | Processes routine transactions, pauses for human approval on high-stakes actions |
| 29 | **Home Automation Agent** | Controls smart home devices, responds to sensor data, runs automation routines |
| 30 | **Fitness / Health Tracking** | Logs workouts, tracks nutrition, provides basic wellness summaries |
| 31 | **Recipe / Cooking Agent** | Suggests recipes based on ingredients, adjusts portions, provides cooking guidance |
| 32 | **Personal Finance Tracking** | Categorizes transactions, tracks budgets, generates spending summaries |
| 33 | **SEO Optimization Agent** | Analyzes content for search optimization, suggests keywords and metadata |
| 34 | **Landing Page Generator** | Creates HTML/CSS pages from concept descriptions |
| 35 | **Travel Planning Agent** | Researches destinations, compares options, creates detailed itineraries |

## Tier 3 — Quality-Limited Roles (14B+ recommended)

| # | Subagent Role | Function |
|---|---|---|
| 36 | **Code Generation Agent** | Writes functions, classes, and modules from specifications |
| 37 | **Code Review Agent** | Reviews code for quality, security, and maintainability |
| 38 | **QA / Test Writing Agent** | Generates unit tests and test cases from specifications |
| 39 | **Task Planning / Decomposition** | Breaks complex tasks into subtasks with dependencies |
| 40 | **Fact-Checking Agent** | Verifies claims against multiple sources, evaluates credibility |
| 41 | **Critic / Review Agent** | Evaluates other agents' outputs against quality criteria |
| 42 | **Market Research Agent** | Conducts competitive analysis, tracks trends, generates market reports |
| 43 | **Synthesizer / Aggregator** | Combines outputs from multiple agents into coherent unified responses |
| 44 | **Curriculum / Course Designer** | Generates lesson plans, educational materials, and instructor guides |
| 45 | **Prototype Generator** | Rapidly builds working prototypes (Streamlit/Gradio apps) from specifications |
| 46 | **DevOps Agent** | Manages deployment pipelines, CI/CD, log analysis |

## Tier 4 — Deep Reasoning Roles (reasoning-specialist models)

| # | Subagent Role | Function |
|---|---|---|
| 47 | **Math / Logic Reasoning** | Solves mathematical problems, proofs, statistical calculations |
| 48 | **STEM Analysis** | Scientific literature interpretation, technical analysis |
| 49 | **Algorithm Exploration** | Generates novel algorithmic approaches, evaluates computational complexity |

## Tier 5 — Not Feasible Locally (require frontier-class models)

| # | Subagent Role | Function |
|---|---|---|
| 50 | **Orchestrator / Manager Agent** | Complex multi-agent workflow coordination with 5+ agents and conditional branching |
| 51 | **Software Architect Agent** | Translates requirements into full system architecture across databases, APIs, scaling, security |
| 52 | **Complex Debugger Agent** | Multi-step error analysis across codebases with non-obvious root causes |
| 53 | **Legal Document Review** | Deep domain expertise, jurisdiction-specific precedent, extreme precision |
| 54 | **Medical / Health Analysis** | Safety-critical health interpretation beyond basic tracking |
| 55 | **Financial Analysis / Stock Research** | Deep fundamental analysis, technical analysis, and investment recommendations |
| 56 | **Security Analyst Agent** | Vulnerability analysis and security auditing |
| 57 | **SRE / Incident Response** | Root-cause analysis across microservices with complex failure modes |
| 58 | **Book Writing Agent** | Coherent long-form narrative maintaining consistency across chapters |
| 59 | **Compliance / Regulatory Agent** | Domain-specific regulatory knowledge, risk modeling, audit-quality reasoning |

---

**Total: 59 distinct subagent roles across 5 feasibility tiers**
