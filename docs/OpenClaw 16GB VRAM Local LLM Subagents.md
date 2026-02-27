# OpenClaw and local LLM subagents on 16 GB VRAM

**OpenClaw is a real, explosively popular open-source AI agent platform** (MIT license, ~117K GitHub stars) with native support for running multiple isolated agents against local LLMs via Ollama. It supports per-agent model selection and hot-swapping, making it viable for the one-model-at-a-time workflow on an RTX 5060 Ti 16 GB. Of the 17 models evaluated, **10 fit comfortably at 4-bit quantization, 2 fit with severe context limitations, and 5 do not fit at all**. The Qwen3 family dominates local agent tool-calling benchmarks, and most common subagent roles can be served adequately — though orchestration, complex legal/financial reasoning, and full software architecture genuinely require frontier-class models.

---

## OpenClaw is a personal AI agent platform with multi-agent routing

OpenClaw (github.com/openclaw/openclaw) launched in late January 2026 and rapidly became one of the fastest-growing open-source projects on GitHub. Created by **Peter Steinberger** (@steipete), it is written in TypeScript/Node.js under the MIT license, with **130+ contributors** and a Discord community exceeding 12,700 members.

Unlike programmatic multi-agent frameworks such as CrewAI or AutoGen (where you define agent crews in Python code), OpenClaw is a **full personal AI assistant platform** with built-in multi-agent routing. Each agent gets its own isolated workspace, state directory, session store, personality file (`SOUL.md`), long-term memory (`MEMORY.md`), and skill set. A single Gateway instance can host multiple agents, each bound to different messaging channels (WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Matrix, and more).

Key capabilities relevant to local LLM use:

- **First-class Ollama integration** with auto-discovery of tool-capable models — set `OLLAMA_API_KEY="ollama-local"` and it works
- **Per-agent model selection** at runtime via the `/model` command (e.g., Qwen3-8B for a coding agent, Ministral 3B for a routing agent)
- **50+ bundled skills** including browser automation, shell commands, file operations, email, calendar, GitHub, and Obsidian integration
- **Heartbeat daemon** for autonomous scheduled tasks without user prompting
- **ClawHub** skill registry for community-built extensions
- A companion ecosystem including **openclaw-mission-control** (orchestration dashboard), **ClawRouter** (smart LLM router), and **NanoClaw** (lightweight 500-line alternative)

The project's documentation recommends **32B+ parameter models for reliable multi-step agent tasks** and notes that 8B models work for simpler automations. It requires approximately **64K token context** for full functionality — a critical constraint for the 24B-class models that barely fit in 16 GB.

For comparison, the most relevant programmatic alternatives are **CrewAI** (~35K stars, Python, role-based crews), **AutoGen/AG2** (~48K stars, Microsoft, conversational multi-agent), and **LangGraph** (LangChain ecosystem, graph-based workflows). All support local LLMs via OpenAI-compatible APIs.

---

## Which models actually fit in 16 GB at 4-bit quantization

The RTX 5060 Ti 16 GB (Blackwell, GDDR7, 448 GB/s bandwidth) delivers roughly **51 tokens/second on 8B Q4 models** and supports native FP4 inference via its tensor cores. Below is the definitive VRAM assessment for every model the user listed.

| Model | Total params | Active params | Q4 VRAM | Fits 16 GB? | Tool calling | Speed (est. t/s) |
|---|---|---|---|---|---|---|
| **GPT-OSS-20B** | 21B MoE | 3.6B | ~13.7 GB | ✅ Yes | ✅ Excellent | ~42–82 |
| **GLM-4-9B** | 9B | 9B | ~5–6 GB | ✅ Yes | ✅ Good | ~50+ |
| **GLM-4.6V Flash 9B** | 9B | 9B | ~6–8 GB | ✅ Yes | ✅ Supported | ~45+ |
| **Devstral Small 2 24B** | 24B | 24B | ~14–15 GB | ⚠️ Tight | ✅ Excellent | ~20–30 |
| **Ministral 3 3B** | 3B | 3B | ~2–3 GB | ✅ Yes | ✅ Native | ~100+ |
| **Gemma 3 27B** | 27B | 27B | ~15.6 GB | ❌ No* | ⚠️ Limited | N/A |
| **Gemma 3 12B** | 12B | 12B | ~6.6 GB | ✅ Yes | ⚠️ Limited | ~30–45 |
| **Mistral Small 3.1 24B** | 24B | 24B | ~14–15 GB | ⚠️ Tight | ✅ Excellent | ~20–30 |
| **Phi-4 14B** | 14B | 14B | ~8–9 GB | ✅ Yes | ⚠️ Basic | ~30–40 |
| **Phi-4-mini 3.8B** | 3.8B | 3.8B | ~2.5–3 GB | ✅ Yes | ⚠️ Limited | ~80+ |
| **Qwen3-8B** | 8B | 8B | ~5–6 GB | ✅ Yes | ✅ Excellent | ~51 |
| **Qwen3-4B** | 4B | 4B | ~2.5–3 GB | ✅ Yes | ✅ Good | ~70+ |
| **DeepSeek-R1-Distill-Qwen-14B** | 14B | 14B | ~9 GB | ✅ Yes | ⚠️ Unstable | ~30–40 |
| **Llama 3.2 3B** | 3B | 3B | ~2–3 GB | ✅ Yes | ⚠️ Basic | ~80+ |
| **Qwen3-30B-A3B** | 30B MoE | 3B | ~17–18 GB | ❌ No | ✅ Excellent | N/A |
| **Qwen3-Coder 30B-A3.3B** | 30B MoE | 3.3B | ~17–18 GB | ❌ No | ✅ Excellent | N/A |
| **Nemotron 30B MoE** | 30B hybrid | 3.5B | ~17–20 GB | ❌ No | ✅ Excellent | N/A |

*Gemma 3 27B at Q4 QAT loads ~15.6 GB of weights, leaving virtually zero headroom for KV cache. Community consensus: needs 24 GB+.*

**Important correction**: GPT-OSS-20B is actually a MoE model (21B total, 3.6B active), not dense as categorized. This is why it fits so comfortably at **13.7 GB in MXFP4** — it was designed specifically for 16 GB consumer GPUs. It is the single strongest model available in this VRAM class.

The three 30B MoE models (Qwen3-30B-A3B, Qwen3-Coder 30B-A3.3B, Nemotron 3 Nano 30B) all require **17–20 GB at Q4** because every parameter must be loaded into memory regardless of activation sparsity. Partial CPU offloading is possible via llama.cpp but degrades speed to ~10–15 t/s — generally too slow for interactive agent use.

---

## Comprehensive model-to-subagent matching across 40+ roles

Below is a thorough matching of community-discussed subagent roles to the models that can serve them on 16 GB. Roles are grouped by feasibility tier. For each, the **minimum quality tier** and **recommended model(s)** are stated honestly — roles that cannot be served well locally are marked clearly.

### Tier 1 — Highly feasible with small models (1–4B sufficient)

These roles involve classification, routing, simple extraction, or short-form generation. They run lightning-fast on tiny models and are ideal candidates for Ministral 3 3B, Qwen3-4B, or Phi-4-mini 3.8B.

| Subagent role | What it does | Recommended model(s) | Why |
|---|---|---|---|
| **Router / triage agent** | Classifies incoming requests and routes to the correct specialist agent | **Qwen3-4B** or **Ministral 3 3B** | Intent classification is simple; Qwen3-4B has native tool calling; ~70–100+ t/s means near-instant routing |
| **Input validator / sanitizer** | Checks inputs for format compliance, safety, completeness before passing to work agents | **Qwen3-4B** or **Phi-4-mini 3.8B** | Pattern matching and classification; doesn't need deep reasoning |
| **Heartbeat / health monitor** | Runs on a cron schedule to check system status, send alerts, perform maintenance tasks | **Ministral 3 3B** | Needs speed and reliability over intelligence; Ministral has native function calling; OpenClaw's heartbeat daemon is designed for this |
| **Notification / alert agent** | Monitors conditions and sends alerts via messaging channels | **Ministral 3 3B** or **Qwen3-4B** | Threshold checking and message formatting are simple tasks |
| **Sentiment analysis agent** | Classifies text sentiment for social media monitoring, customer feedback | **Qwen3-4B** or **Phi-4-mini 3.8B** | Classification task; small models handle this reliably |
| **FAQ generation agent** | Converts documentation into Q&A format | **Qwen3-4B** | Structured extraction + simple reformulation |
| **Translation agent** | Translates between languages | **Qwen3-8B** (for quality) or **Qwen3-4B** (common pairs) | Qwen3 models support 119 languages natively; 8B gives much better quality for less-common language pairs |
| **Calendar / scheduling agent** | Manages calendar bookings, detects conflicts, coordinates meeting times | **Qwen3-4B** with tool calling | The LLM reasoning is simple; tool integration (calendar API) does the heavy lifting |

### Tier 2 — Feasible with mid-range models (8–14B recommended)

These roles require multi-step reasoning, summarization, or moderate tool orchestration. The **Qwen3-8B** is the workhorse here — it achieves an **F1 score of 0.919 on Docker's tool-calling benchmark** at Q4_K_M, outperforming GPT-3.5-turbo. For roles needing deeper reasoning, **GPT-OSS-20B** or **Phi-4 14B** step up.

| Subagent role | What it does | Recommended model(s) | Why |
|---|---|---|---|
| **Research / web search agent** | Gathers information using search tools, synthesizes findings into structured notes | **Qwen3-8B** or **GPT-OSS-20B** | Tool calling is critical; Qwen3-8B's excellent tool F1 and 128K context make it ideal. GPT-OSS is better for synthesis quality. Community reports good results with 8B models when paired with search tools |
| **Content writer / blog writer** | Drafts articles and long-form content from research notes | **GPT-OSS-20B** or **Qwen3-8B** | GPT-OSS gives notably better prose quality; Qwen3-8B is adequate for routine content. r/LocalLLaMA users report decent blog writing at 8B |
| **Editor agent** | Reviews content for clarity, grammar, coherence, and style | **Qwen3-8B** or **Gemma 3 12B** | Editing is well within 8B capability; Gemma 3 12B adds multimodal document review |
| **Content planner** | Plans content structure, creates outlines and editorial calendars | **Qwen3-8B** | Moderate planning; 8B handles topic analysis and outline generation well |
| **Email drafting / summarization** | Classifies incoming emails, drafts contextual responses, manages email workflows | **Qwen3-8B** | Tool calling (email API) + moderate writing quality; community reports good results at 8B |
| **Document summarization** | Condenses long documents into key points | **GPT-OSS-20B** (best quality) or **Qwen3-8B** | Summarization is one of the best local use cases; 128K context on both models handles long documents. GPT-OSS's stronger reasoning produces tighter summaries |
| **Meeting notes / transcription agent** | Processes meeting recordings, extracts summaries and action items | **Qwen3-8B** | Structured extraction + summarization; well within 8B capability. Transcription itself handled by Whisper (separate model) |
| **Social media scouting / monitoring** | Monitors social platforms, generates content, tracks trends | **Qwen3-8B** | Needs tool calling (API access) + short-form writing; 8B is plenty |
| **Social media content agent** | Generates platform-appropriate posts with hashtags and formatting | **Qwen3-4B** or **Qwen3-8B** | Short-form creative writing; even 4B handles tweets and captions |
| **News aggregation agent** | Collects, categorizes, and summarizes news from multiple sources | **Qwen3-8B** | Tool calling (RSS, search) + summarization; 8B handles the synthesis well |
| **Shopping / price comparison** | Compares prices across retailers, tracks deals, makes recommendations | **Qwen3-8B** | Primarily tool-driven (scraping/APIs); LLM role is comparison and recommendation |
| **Memory / knowledge management** | Curates long-term facts, decisions, and preferences for other agents | **Qwen3-8B** or **GPT-OSS-20B** | OpenClaw uses MEMORY.md files; this agent needs good extraction and deduplication. RAG integration benefits from Qwen3's tool calling |
| **RAG / retrieval agent** | Retrieves relevant chunks from vector stores and knowledge bases | **Qwen3-8B** | Query formulation + source citation; tool calling essential. Local embedding models (separate) handle the vector search |
| **Data analysis agent** | Cleans data, runs statistics, generates plots via code execution | **Qwen3-8B** or **Phi-4 14B** | Needs code generation (pandas/matplotlib) + reasoning about results. Phi-4's stronger STEM reasoning helps with statistical interpretation |
| **Website scraping / understanding** | Navigates websites, extracts structured information, fills forms | **Qwen3-8B** (text) or **Gemma 3 12B** (with vision) | Browser automation tools do the navigation; LLM interprets HTML and extracts data. Vision capability helps with layout understanding |
| **Image description / understanding** | Describes images, reads charts, interprets visual content | **Gemma 3 12B** or **GLM-4.6V Flash 9B** | Requires multimodal (vision+text) capability. Both fit comfortably and handle visual QA. Gemma 3 12B at QAT Q4 uses only ~6.6 GB |
| **Customer support agent** | Handles inquiries, routes to specialists, manages multi-turn support conversations | **Qwen3-8B** or **GPT-OSS-20B** | FAQ-style support works at 8B; complex issue resolution benefits from GPT-OSS's stronger reasoning |
| **Lead scoring / prospecting** | Enriches leads with company data, scores them, prioritizes for outreach | **Qwen3-8B** | Classification + tool use (CRM APIs); LLM scoring logic is straightforward |
| **Sprint / project summarizer** | Summarizes sprint activities and generates progress reports from PM tools | **Qwen3-8B** | Data extraction + summarization; well within 8B capability |
| **Transaction / approval agent** | Processes routine transactions, pauses for human approval on high-stakes actions | **Qwen3-4B** or **Qwen3-8B** | Classification (routine vs. high-stakes) is simple; tool execution is model-agnostic |
| **Home automation agent** | Controls smart home devices, responds to sensor data, runs automation routines | **Qwen3-4B** with tool calling | Simple intent parsing + API calls; speed matters more than reasoning depth |
| **Fitness / health tracking** | Logs workouts, tracks nutrition, provides basic wellness summaries | **Qwen3-4B** or **Qwen3-8B** | Structured data logging + simple analysis; doesn't need deep reasoning |
| **Recipe / cooking agent** | Suggests recipes based on ingredients, adjusts portions, provides cooking guidance | **Qwen3-8B** | Moderate knowledge retrieval + structured output; 8B handles recipe generation well |
| **Personal finance tracking** | Categorizes transactions, tracks budgets, generates spending summaries | **Qwen3-8B** | Classification + basic math + structured reporting |
| **SEO optimization agent** | Analyzes content for search optimization, suggests keywords and metadata | **Qwen3-8B** | Domain-specific but not deep reasoning; keyword analysis and metadata generation |
| **Landing page generator** | Creates HTML/CSS pages from concept descriptions | **Qwen3-8B** or **Devstral Small 2 24B** (if tight fit acceptable) | Code generation task; Qwen3-8B handles basic HTML well; Devstral excels at multi-file web projects |
| **Travel planning agent** | Researches destinations, compares options, creates detailed itineraries | **GPT-OSS-20B** or **Qwen3-8B** | Multi-step tool use (search, comparison) + structured output; GPT-OSS's reasoning helps with complex multi-city itineraries |

### Tier 3 — Feasible but quality-limited (14B+ recommended, stretches local capability)

These roles need stronger reasoning, coding, or planning abilities. **GPT-OSS-20B** (the standout for this VRAM class), **Phi-4 14B** (for STEM reasoning), and **Devstral Small 2 24B** (for coding) are the candidates — but expect noticeable quality gaps versus frontier models.

| Subagent role | What it does | Recommended model(s) | Honest assessment |
|---|---|---|---|
| **Code generation agent** | Writes functions, classes, and modules from specifications | **Devstral Small 2 24B** (tight fit, short context) or **GPT-OSS-20B** | Devstral hits 68% SWE-bench Verified — SOTA among open models its size. Limited to ~4–8K context on 16 GB. GPT-OSS is more comfortable on VRAM and handles moderate coding well. **Qwen3-8B** is a safer fallback with full context |
| **Code review agent** | Reviews code for quality, security, and maintainability | **GPT-OSS-20B** or **Devstral Small 2 24B** | Works for focused reviews of individual files. Full codebase review exceeds the context limitations of 24B models on 16 GB |
| **QA / test writing agent** | Generates unit tests and test cases from specifications | **Devstral Small 2 24B** or **Qwen3-8B** | Unit test generation for individual functions works well; test suite design for complex systems is weaker |
| **Task planning / decomposition** | Breaks complex tasks into subtasks with dependencies | **GPT-OSS-20B** | Planning quality scales strongly with model capability. GPT-OSS's reasoning (comparable to o3-mini) handles moderate task decomposition. Complex multi-dependency planning will be noticeably worse than frontier models |
| **Fact-checking agent** | Verifies claims against multiple sources, evaluates credibility | **GPT-OSS-20B** with search tools | Tool-augmented fact-checking works; the reasoning about source quality and contradiction detection benefits from GPT-OSS's stronger reasoning |
| **Critic / review agent** | Evaluates other agents' outputs against quality criteria | **GPT-OSS-20B** or **Phi-4 14B** | Quality evaluation requires good judgment; GPT-OSS handles this reasonably for straightforward criteria |
| **Market research agent** | Conducts competitive analysis, tracks trends, generates market reports | **GPT-OSS-20B** with search tools | Basic market overviews work; nuanced competitive intelligence benefits from stronger reasoning |
| **Synthesizer / aggregator** | Combines outputs from multiple agents into coherent unified responses | **GPT-OSS-20B** | Requires understanding multiple inputs and resolving contradictions; GPT-OSS handles moderate synthesis tasks |
| **Curriculum / course designer** | Generates lesson plans, educational materials, and instructor guides | **GPT-OSS-20B** or **Qwen3-8B** | Lesson outlines work at 8B; pedagogically sound curriculum design benefits from stronger models |
| **Prototype generator** | Rapidly builds working prototypes (Streamlit/Gradio apps) from specifications | **Devstral Small 2 24B** | Code generation specialized; handles simple app prototypes well within its context limitations |
| **DevOps agent** | Manages deployment pipelines, CI/CD, log analysis | **GPT-OSS-20B** | Shell command generation works; complex infrastructure reasoning is marginal |

### Tier 4 — Deep reasoning roles where DeepSeek-R1-Distill shines (but with caveats)

**DeepSeek-R1-Distill-Qwen-14B** (~9 GB at Q4) delivers exceptional chain-of-thought reasoning comparable to o1-class models. However, its **tool calling is unstable** — community patches exist but produce "looped calls or empty responses." Use it exclusively for reasoning-only roles where tool calling isn't needed.

| Subagent role | What it does | Recommended model | Caveats |
|---|---|---|---|
| **Math / logic reasoning** | Solves mathematical problems, proofs, statistical calculations | **DeepSeek-R1-Distill-Qwen-14B** | Exceptional math reasoning at this size. Set temperature 0.5–0.7 to avoid repetition. No system prompt support. Thinking tokens add 5–10× latency |
| **STEM analysis** | Scientific literature interpretation, technical analysis | **Phi-4 14B** or **DeepSeek-R1-Distill-Qwen-14B** | Phi-4 scores 84.8 MMLU and excels on GPQA/MATH. Better tool-calling support than DeepSeek-R1 |
| **Algorithm exploration** | Generates novel algorithmic approaches, evaluates computational complexity | **DeepSeek-R1-Distill-Qwen-14B** | Community reports working on AutoGen algorithm discovery experiments. Results are modest but show local feasibility |

### Tier 5 — Not feasible with these local models (honest assessment)

These roles genuinely require frontier-level intelligence, massive context, specialized domain expertise, or real-time capabilities that no model in the 16 GB VRAM class can provide adequately. **Do not force a match.**

| Subagent role | Why it doesn't work locally | What would be needed |
|---|---|---|
| **Orchestrator / manager agent** (for complex multi-agent workflows) | Community consensus: the orchestrator needs the strongest model in the system. It must understand all sub-agent capabilities, decompose ambiguous goals, handle failures gracefully, and maintain coherent state across many turns. GPT-OSS-20B can handle simple orchestration, but complex workflows with 5+ agents and conditional branching degrade significantly | 70B+ model or cloud API (Claude Sonnet, GPT-4o). Community pattern: "big model for routing, small models for execution" |
| **Software architect agent** | Translating requirements into full system architecture requires holistic reasoning across databases, APIs, scaling, security, and tradeoffs. Community reports poor results under 13B, and even 14B produces shallow architectures | 70B+ or frontier API |
| **Complex debugger agent** | Multi-step error analysis across codebases with non-obvious root causes. Requires maintaining mental models of runtime state, data flow, and side effects | 34B+ with long context; frontier models preferred |
| **Legal document review** | Requires deep domain expertise, understanding of jurisdiction-specific precedent, and extreme precision. Liability risk makes this inappropriate for small models regardless of capability | Frontier API + human review; not suitable for any local model at this scale |
| **Medical / health analysis** (beyond basic tracking) | Safety-critical domain where hallucinations cause real harm. Community strongly advises against relying on local models for medical interpretation | Frontier API + mandatory human oversight |
| **Financial analysis / stock research** | Deep fundamental analysis, technical analysis, and investment recommendations require strong numerical reasoning plus domain expertise. Community reports significantly better results with API models | Frontier API for serious analysis; GPT-OSS-20B handles basic financial summaries |
| **Security analyst agent** | Vulnerability analysis and security auditing require specialized knowledge that general-purpose models lack at 8–14B | Specialized security models or frontier API |
| **SRE / incident response** | Root-cause analysis across microservices with complex failure modes. Requires correlating logs, metrics, and traces across systems | Frontier API + monitoring tool integration |
| **Book writing agent** (coherent long-form) | Maintaining narrative coherence across chapters requires long-horizon planning far beyond what 8–14B models handle | 70B+ with 128K+ context |
| **Compliance / regulatory agent** | Domain-specific regulatory knowledge, risk modeling, and audit-quality reasoning are beyond general local models | Frontier API + domain-specific fine-tuning |

---

## Practical integration: hot-swapping, backends, and latency

### Model swapping is the dominant bottleneck on single-GPU setups

On the RTX 5060 Ti with an NVMe SSD, model loading times are approximately:

- **1–4B models**: 1–3 seconds
- **8B models**: 2–5 seconds  
- **14B models**: 5–10 seconds
- **24B models** (tight fit): 10–15 seconds

A five-agent workflow using three different models adds **9–21 seconds of pure swap overhead per cycle**. Three strategies minimize this cost:

1. **Use the same model for all agents** — different system prompts customize behavior without swapping. A single Qwen3-8B instance can serve as researcher, writer, and summarizer simultaneously
2. **Keep two small models loaded simultaneously** — Ollama can hold a 4B routing model (~2.5 GB) alongside an 8B work model (~5.5 GB) within 16 GB, with room for KV cache. Set `OLLAMA_MAX_LOADED_MODELS=2`
3. **Use vLLM Sleep Mode** (v0.11.0+) — offloads model weights to CPU RAM instead of fully unloading. Wake time drops to **0.1–2.6 seconds** versus 10–45 seconds for cold starts

### Ollama is the pragmatic backend for OpenClaw

OpenClaw has first-class Ollama integration. Configuration is minimal: export `OLLAMA_API_KEY="ollama-local"` and OpenClaw auto-discovers available models. For agent workflows, set `OLLAMA_KEEP_ALIVE=-1` to prevent mid-conversation model unloads. Ollama's default behavior keeps models loaded for 5 minutes after last use and supports up to **3× GPU count** models simultaneously.

Alternative backends (llama.cpp server, vLLM, LM Studio, LocalAI) all expose OpenAI-compatible APIs and work with OpenClaw, CrewAI, AutoGen, and LangGraph. **vLLM** offers 3–35× higher throughput than Ollama under concurrency but only serves one model per instance. **LM Studio** provides the best desktop GUI experience for model management.

### Tool calling is the make-or-break capability for agents

Docker's benchmark of **21 models across 3,570 test cases** reveals a stark divide in tool-calling reliability:

- **Qwen3-14B Q4_K_M**: F1 0.971 (nearly matches GPT-4's 0.974)
- **Qwen3-8B Q4_K_M**: F1 0.919 (outperforms GPT-3.5-turbo's 0.899)
- **Llama 3.1 8B Q4_K_M**: F1 0.793 (marginal for agent use)
- **Gemma 3 4B**: F1 0.733 (unreliable)
- **Sub-4B models**: "Significant reliability issues" — hallucinated tool names, malformed arguments, infinite loops

**Qwen3-8B is the minimum viable model for reliable agent tool calling.** Below this threshold, agents frequently hallucinate tool names, generate malformed arguments, or enter call loops. For roles where tool calling is non-negotiable (research, email, calendar, browser automation), Qwen3-8B or GPT-OSS-20B should be the default.

Models without native tool calling (DeepSeek-R1-Distill, base Phi-4, Llama 3.2 3B) can still participate in agent workflows via **ReAct prompting** (Thought/Action/Observation format with regex parsing) or **constrained generation** (grammar-guided JSON output via llama.cpp or SGLang). These workarounds add latency and reduce reliability but make reasoning-focused models usable as non-tool-calling subagents.

### The recommended one-GPU agent stack

For an RTX 5060 Ti 16 GB running OpenClaw with model hot-swapping:

- **Primary work model**: **GPT-OSS-20B** at MXFP4 (~13.7 GB) — best overall quality, excellent tool calling, designed for 16 GB GPUs, ~42 t/s. Use for research, writing, planning, coding, and most agent roles
- **Fast routing model**: **Qwen3-4B** at Q4 (~2.5 GB) — native tool calling, ~70 t/s. Use for triage, classification, heartbeat tasks, and notifications. Can coexist in VRAM alongside GPT-OSS-20B if VRAM allows after KV cache
- **Vision model** (swap in when needed): **Gemma 3 12B QAT** (~6.6 GB) or **GLM-4.6V Flash 9B** (~6–8 GB) — for image understanding, document analysis, visual QA
- **Deep reasoning model** (swap in when needed): **DeepSeek-R1-Distill-Qwen-14B** (~9 GB) — for math, logic, and STEM tasks where chain-of-thought reasoning matters more than tool use
- **Coding specialist** (swap in for intensive coding sessions): **Devstral Small 2 24B** (~14–15 GB) — tight fit, short context, but SOTA agentic coding. Only load when doing substantial code generation

This stack covers the vast majority of subagent roles with **3–4 model swaps** rather than 17 different models, keeping swap overhead manageable.

---

## Conclusion

OpenClaw's architecture is well-suited for this single-GPU workflow. Its per-agent model selection, Ollama auto-discovery, and skill-based architecture mean you can map different subagent roles to appropriately-sized models and swap them in as needed. The **GPT-OSS-20B** is the breakout star of the 16 GB VRAM class — a MoE model with only 3.6B active parameters that fits at 13.7 GB while delivering reasoning comparable to o3-mini and excellent tool calling. Paired with **Qwen3-8B** (the tool-calling champion at its size) and specialized models for vision and reasoning, roughly **30 of 40+ community-discussed agent roles can be served adequately on this hardware**.

The honest gaps are in orchestration of complex multi-agent workflows, domain-expert roles (legal, medical, financial, security), and tasks requiring sustained coherence over very long contexts. For these, a hybrid approach — local models for the majority of agent roles, cloud API calls for the orchestrator and frontier-demanding tasks — delivers the best practical result. OpenClaw's model fallback chains and auth profile rotation make this hybrid pattern straightforward to configure.