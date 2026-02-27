# HANDOFF DOCUMENT — OpenClaw 64GB VRAM Tier (Part 6)

## Session Goal

Create a report covering the **64GB VRAM tier** for the OpenClaw AI agent framework. This tier is achieved exclusively via multi-GPU configurations — there is NO native 64GB VRAM card. The two deployment paths are:

- **(a) 2× RTX 5090 32GB** = 64GB via pipeline parallelism (2-way split)
- **(b) 4× RTX 5060 Ti 16GB** = 64GB via pipeline parallelism (4-way split)

---

## CRITICAL CONSTRAINTS — ENFORCE STRICTLY

1. **Minimum Q4 quantization.** No model may be listed as viable at Q3_K_M, Q2_K, IQ2, IQ3, IQ1, or any sub-4-bit quantization. If a model only fits at Q3 or below, it goes in the "doesn't fit" table.

2. **100% VRAM only.** Every model listed must load weights AND KV cache entirely in combined GPU VRAM. No CPU offloading, no partial offloading, no hybrid RAM modes, no `--n-cpu-moe`, no system RAM. Must work even on PCIe 2.0 where any offloading kills usability.

3. **No hardware content.** Zero GPU specs, PCIe bandwidth math, motherboard requirements, power supply info, thermal considerations, driver setup, or installation guides. Report covers ONLY: models, quantizations, VRAM usage, inference tools for splitting, speed estimates, and OpenClaw agent role mapping.

4. **All 57 agent/subagent roles must be mapped.** Every single role gets a model recommendation. See complete list below.

5. **DISCOVER NEW MODELS FIRST.** Before writing the report, run extensive web searches for any new open-weight LLMs released between November 2025 and February 14, 2026. The AI model landscape moves fast — new 40B–120B models may exist that weren't available when previous parts were written. See the "MANDATORY FIRST STEP" section below for specific search queries. This was not done thoroughly enough in earlier parts and models may have been missed.

---

## MANDATORY FIRST STEP: Discover New Models (Nov 2025 – Feb 14, 2026)

**Before writing anything, the session MUST search the web extensively for new open-weight LLM models released between November 2025 and February 14, 2026.** Previous reports were built on models known at the time but the LLM landscape changes rapidly. New 40B–120B models may have been released that are perfect for the 64GB tier.

**Search targets (run ALL of these searches before starting the report):**
- "new open source LLM 2026" / "new open weight model January 2026" / "new open weight model February 2026"
- "new 70B model 2026" / "new 100B model 2026" / "new MoE model 2026"
- r/LocalLLaMA new releases December 2025, January 2026, February 2026
- HuggingFace trending models January 2026, February 2026
- "Qwen3 72B" or "Qwen3 70B" — does a larger Qwen3 dense model exist now?
- "Llama 4" new variants — any new Llama 4 models beyond Maverick?
- "Mistral Large 3" / "Mistral Medium" — any new Mistral releases?
- "DeepSeek V4" or "DeepSeek R2" — any new DeepSeek releases?
- "Gemma 3" larger variants — anything beyond 27B?
- "NVIDIA Nemotron" new variants — anything beyond Super-49B and Nano-30B?
- "Cohere Command R" new versions
- "MiniMax M2.5" / "MiniMax" new large models — MiniMax M2.5 was JUST released, check size and benchmarks
- "Moonshot" / "Kimi" new large models — Moonshot is a major lab, check for 40B+ releases
- "Zhipu" / "GLM" / "Z.ai" / "ChatGLM" new large models — Zhipu AI is a major Chinese lab
- "NVIDIA" LLM releases — NVIDIA makes LLMs beyond Nemotron (check for new NVIDIA foundation models)
- "Devstral 2" / "Devstral" — Mistral's coding specialist, check for new versions
- "Qwen3 Coder Next" / "Qwen3-Coder" larger variants — any coding model beyond the 30B MoE?
- "Codestral" new versions — Mistral's coding line
- "StarCoder" / "BigCode" new large coding models
- "Yi" / "01.AI" new large models
- "Falcon 3" large variants
- "InternLM3" or "InternLM" large models
- "Phi-4" larger variants (beyond 14B)
- "EXAONE" new versions beyond 4.0 32B
- "Seed" new versions beyond Seed-OSS-36B
- "Alibaba" / "Baichuan" / "MiniMax" / "Stepfun" / "DeepSeek" new large models
- Any model 40B–120B range released in this window
- New MoE models in 60–120B total params range (these are the sweet spot for 64GB)
- New coding-specialist models in the 40B+ range (Devstral, Codestral, Qwen3-Coder larger, StarCoder)
- New reasoning-specialist models in the 40B+ range

**For every new model found, check:**
- Parameter count (total and active for MoE)
- Architecture (dense vs MoE)
- GGUF availability and Q4_K_M weight size
- Does it fit 64GB at Q4_K_M minimum with KV cache room?
- Key benchmarks (MMLU, HumanEval, MATH, BFCL, IFEval, AIME, GPQA)
- Tool calling / function calling support
- Context window
- Any community speed benchmarks on multi-GPU

**This research step is NOT optional. It was skipped in earlier parts and may have caused models to be missed. Run at least 10-15 web searches for new model releases before starting the report.**

---

## What 64GB Should Unlock (Research Targets)

Models that did NOT fit at 48GB but should fit at 64GB (Q4_K_M minimum):

| Candidate Model | Params | Architecture | Est. Q4_K_M Size | Fits 64GB? |
|----------------|--------|-------------|------------------|------------|
| **Llama 3.3 70B** | 70B | Dense | 42.5 GB | ✅ Already fit at 48GB — now with Q5_K_M (49.95 GB) + room for context |
| **R1-Distill-70B** | 70B | Dense | 42.5 GB | ✅ Same — Q5_K_M now possible |
| **Nemotron-Super-49B** | 49B | Dense | 30.2 GB | ✅ Q8_0 (53 GB) now fits! |
| **Qwen2.5-72B** | 72.7B | Dense | 47.4 GB | ✅ Q4_K_M now fits with context room |
| **GPT-oss-120B** | 117B | MoE | ~59 GB MXFP4 | ✅ Possibly fits — RESEARCH NEEDED |
| **Mixtral 8x22B** | 141B | MoE | ~80 GB Q4_K_M | ❌ Probably doesn't fit |
| **Command R+** | 104B | Dense | ~60 GB Q4_K_M | ⚠️ Research exact size |
| **DBRX** | 132B | MoE | ~75 GB Q4_K_M | ❌ Probably doesn't fit |

**Key research questions:**
- Does GPT-oss-120B at MXFP4 (59 GB) fit 64GB with usable KV cache?
- Any new 80–120B models released Nov 2025 – Feb 2026 that fit?
- Qwen3 larger variants — does a Qwen3-72B exist?
- What about Mistral Large variants in this range?

**Quantization upgrades for existing models:**
- Llama 3.3 70B: Q5_K_M (49.95 GB) — massive quality improvement over Q4
- R1-Distill-70B: Q5_K_M (49.95 GB) — better reasoning chain quality
- Nemotron-Super-49B: Q8_0 (53 GB) — near-lossless at 48GB-class model
- Qwen2.5-72B: Q4_K_M (47.4 GB) — with actual KV cache room now
- All 32B models: FP16 or BF16 (possible at 64GB) — true lossless?

---

## Models From Previous Tiers (Reference)

### Already covered at 48GB tier (carry forward):
- Llama 3.3 70B Q4_K_M (42.5 GB) — MMLU 86%, HumanEval 88.4%, BFCL 77.3%
- DeepSeek-R1-Distill-Llama-70B Q4_K_M (42.5 GB) — AIME 70%, MATH-500 94.5%
- Nemotron-Super-49B Q4_K_M (30.2 GB) / Q6_K (40.9 GB) — reasoning toggle + tool calling
- Qwen3-32B Q4_K_M (19.8 GB) to Q8_0 (34.8 GB)
- Qwen3-30B-A3B MoE Q4_K_M (18.6 GB) to Q8_0 (32.5 GB) — 101 t/s on 2×16GB
- Qwen3-Coder-30B-A3.3B MoE Q4_K_M (18.6 GB) to Q8_0 (32.5 GB)
- DS-R1-Distill-Qwen-32B Q4_K_M (20.1 GB) to Q8_0 (34.8 GB)
- Gemma 3 27B Q4 (15.6 GB) to Q8_0 (28.7 GB) — multimodal, 128K context
- EXAONE 4.0 32B Q4_K_M (19.3 GB) to Q8_0 (34.0 GB)
- Seed-OSS-36B Q4_K_M (21.8 GB) to Q6_K (29.7 GB)
- Nemotron 3 Nano 30B Q4_K_M (24.5 GB) to Q8_0 (33.6 GB)
- GPT-oss-20B MXFP4 (13.7 GB) — only model fitting single 16GB

### Key architecture facts:
- MoE models retain ~92% speed when pipeline split (only active params cross GPU boundary)
- Dense models retain ~25–35% speed when pipeline split (all params cross boundary)
- Pipeline parallelism: layers distributed sequentially across GPUs, only one GPU computes at a time
- ik_llama.cpp graph split: true tensor parallelism, 3–4× faster than pipeline, but emerging

---

## Pipeline Parallelism Notes for 64GB

### 2× RTX 5090 (32GB + 32GB)
- 2-way pipeline split — same as 2× 16GB from Part 4 but each card has 2× the bandwidth
- RTX 5090 has ~1,792 GB/s memory bandwidth vs ~448 GB/s for RTX 5060 Ti
- Dense 70B models should be MUCH faster on 2× 5090 than on 3× 5060 Ti
- Llama 3.3 70B on 2× RTX 5090: community reports ~27 t/s (Ollama)
- MoE models that fit single 5090 (32GB) DON'T NEED splitting — keep them on one card

### 4× RTX 5060 Ti (16GB × 4)
- 4-way pipeline split — each card holds 16GB of layers
- 70B Q4_K_M (42.5 GB) fits across 3 of 4 cards, leaving 4th card free
- Or 70B Q5_K_M (50 GB) fits across 4 cards with ~14 GB spare for KV
- 4 pipeline hops = slower than 3 hops = slower than 2 hops
- Speed penalty is brutal for dense models: expect ~5–8 t/s for 70B on 4×16GB pipeline
- But: can run 2 models simultaneously (e.g., 70B on 3 cards + 14B on 4th card)

### Research needed:
- Tools that support 4-GPU pipeline: llama.cpp, vLLM PP=4, Ollama, ExLlamaV2/V3, SGLang, ik_llama.cpp
- Real benchmarks for 4× consumer GPU setups
- Does ik_llama.cpp graph split work with 4 GPUs?
- Any special considerations for 4-GPU vs 2-GPU or 3-GPU?

---

## Inference Tools to Cover (Same framework as previous reports)

| Tool | Check for 2-GPU support | Check for 4-GPU support |
|------|------------------------|------------------------|
| llama.cpp | ✅ Known good | Research |
| ik_llama.cpp (graph split) | ✅ Known good | Research |
| Ollama | ✅ Known good | Research |
| vLLM | PP=2 ✅ | PP=4 Research |
| ExLlamaV2/V3 | ✅ Known good | Research |
| SGLang | PP=2 ✅ | PP=4 Research |
| TensorRT-LLM | ✅ Known good | Research |
| KoboldCpp | ✅ Known good | Research |
| TabbyAPI | ✅ Known good | Research |

---

## Complete OpenClaw Agent/Subagent Role List (57 Roles, 5 Tiers)

Map EVERY role to a model recommendation at 64GB. Mark upgrades from 48GB tier.

### Tier 1 — Simple (8 roles)
1. Router / triage
2. Input validator
3. Heartbeat / health monitor
4. Notification / alert
5. Sentiment analysis
6. FAQ generation
7. Translation
8. Calendar / scheduling

### Tier 2 — Moderate (25 roles)
9. Research / web search
10. Content writing
11. Editing / proofreading
12. Email drafting
13. Document summarization
14. Meeting notes
15. Social media
16. News aggregation
17. Shopping / price comparison
18. Memory / knowledge management
19. RAG / retrieval
20. Data analysis
21. Website scraping
22. Image description
23. Customer support
24. Lead scoring
25. Project summarization
26. Transaction / approval
27. Home automation
28. Fitness tracking
29. Recipe / cooking
30. Personal finance
31. SEO optimization
32. Landing page generation
33. Travel planning

### Tier 3 — Complex (11 roles)
34. Code generation
35. Code review
36. QA / test writing
37. Task planning
38. Fact-checking
39. Critic / review
40. Market research
41. Synthesizer / aggregator
42. Curriculum design
43. Prototype generation
44. DevOps

### Tier 4 — Reasoning (3 roles)
45. Math / logic reasoning
46. STEM analysis
47. Algorithm exploration

### Tier 5 — Frontier (10 roles)
48. Orchestrator / manager
49. Software architect
50. Complex debugger
51. Legal document review
52. Medical / health analysis
53. Financial analysis
54. Security analyst
55. SRE / incident response
56. Book writing
57. Compliance / regulatory

---

## Report Structure (Follow Same Format as Parts 4 & 5)

1. **Executive Summary**
2. **New Models That Unlock at 64GB** — only models that didn't fit at 48GB
3. **32GB/48GB Models That Improve at 64GB** — quantization upgrades, context expansion
4. **Pipeline Parallelism for 2-Way and 4-Way Splits** — mechanics, speed impact, MoE vs dense
5. **Inference Tools** — compatibility matrix for 2-GPU and 4-GPU splitting
6. **Speed Comparison: 2× RTX 5090 vs 4× RTX 5060 Ti** — per-model estimates
7. **Complete Agent Role Mapping — All 57 Roles** — with upgrade status from 48GB
8. **Deployment Architectures** — multi-model configs for both GPU setups
9. **Models That Don't Fit at 64GB** — what still requires 96GB+ or cloud
10. **Conclusion & Recommended Model Stack**

---

## Key Questions the Report Must Answer

1. What new models become available at 64GB that weren't at 48GB? (GPT-oss-120B? MiniMax M2.5? Command R+? New releases?)
2. Does 70B at Q5_K_M meaningfully outperform 70B at Q4_K_M? Worth the extra VRAM?
3. Is Nemotron-Super-49B at Q8_0 (53 GB) the best single model at this tier?
4. How does 2× RTX 5090 speed compare to 4× RTX 5060 Ti for the same model?
5. Which roles upgrade from 48GB → 64GB? (Fewer than 32→48GB, likely)
6. Is there a "diminishing returns" argument — does 64GB add enough over 48GB to justify the cost?
7. Can 4× 5060 Ti run 2 models simultaneously (e.g., 70B on 3 cards + small model on 4th)?
8. What's the optimal multi-model architecture for each GPU configuration?
9. Does 64GB start to close the gap with cloud APIs for any remaining roles?

---

## File Locations

- **32GB report (Part 4):** `/mnt/user-data/outputs/openclaw-model-selection-32gb-tier.md`
- **48GB report (Part 5):** `/mnt/user-data/outputs/openclaw-48gb-tier.md`
- **This handoff:** `/mnt/user-data/outputs/handoff-64gb-tier.md`
- **Transcripts:** `/mnt/transcripts/` (check for earlier parts)

---

## Confirmed: No Native 64GB GPU Exists

Consumer: RTX 5090 = 32GB (max). Professional: RTX 6000 Ada = 48GB. Next step up is datacenter A100 40GB or A100 80GB / H100 80GB. There is no 64GB card. The 64GB tier is purely multi-GPU. The 96GB tier (separate future report) will cover native cards like the A100 80GB or professional options.
