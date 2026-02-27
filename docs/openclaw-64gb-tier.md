# OpenClaw Model Selection — 64GB VRAM Tier

**Part 6: 2× RTX 5090 32GB & 4× RTX 5060 Ti 16GB Pipeline Split**
**Date:** February 23, 2026

> **Critical constraint:** Every model listed as viable must load weights AND KV cache 100% in VRAM. No CPU offloading, no partial offloading, no hybrid RAM modes. Minimum Q4 quantization — no sub-Q4 quants are considered viable.

---

## Executive Summary

Sixty-four gigabytes of VRAM is an incremental tier with a brutally honest finding: **no new model released between November 2025 and February 2026 fits at 64GB at Q4 minimum quantization.** Every major release in this window — Devstral 2 123B (Dec 2025), DeepSeek V3.2 685B (Dec 2025), Nemotron 3 Nano 30B (Dec 2025), GLM-4.7-Flash 30B (Jan 2026), Kimi K2.5 1T (Feb 2026), Qwen3.5 397B (Feb 2026), MiniMax M2.5 230B, MiMo-V2-Flash 309B, GLM-5 744B (Feb 2026) — either far exceeds the VRAM budget or is a small model already covered at lower tiers.

The closest miss: **Devstral 2 123B** (Mistral, December 10, 2025), a dense coding specialist with 72.2% SWE-bench Verified — its Q4_K_M GGUF weighs **74.9 GB**, 11 GB over the 64GB limit. This model requires the 96GB tier.

**What 64GB actually provides** is quantization upgrades for pre-November 2025 models: Q5_K_M for 70B dense models, Q8_0 for 49B models, and genuine KV headroom for 72B models that were unusable at 48GB. These are meaningful quality improvements, but they aren't new model unlocks.

No native 64GB GPU exists. Both deployment paths — **2× RTX 5090 32GB** and **4× RTX 5060 Ti 16GB** — require pipeline parallelism, with the 2× RTX 5090 delivering **4–5× faster inference** than 4× 5060 Ti on dense models.

**Is 64GB worth it over 48GB?** Marginally. 12 of 59 roles see quality improvements from higher quantization, but no fundamentally new capabilities unlock. The 48GB→64GB jump is the weakest in the entire series. For builders who can stretch to 96GB (RTX PRO 6000 Blackwell), the GPT-oss-120B and Qwen3-Next-80B-A3B models that unlock there represent a far more transformative investment.

---

## 1. New Model Releases — November 2025 to February 2026

### 1.1 Comprehensive Discovery Results

Every significant open-weight LLM released between November 2025 and February 23, 2026 was evaluated for 64GB viability:

| Model | Release Date | Params | Architecture | Active | Q4_K_M Size | Fits 64GB? | Why Not |
|-------|-------------|--------|-------------|--------|-------------|------------|---------|
| **Devstral 2** | Dec 10, 2025 | 123B | Dense | 123B | **74.9 GB** | ❌ No | 11 GB over limit |
| **Nemotron 3 Nano 30B** | Dec 15, 2025 | 31.6B | Hybrid MoE | ~8B | 22.9 GB | ✅ Fits — but already covered at 24GB tier | Lower-tier model |
| **DeepSeek V3.2** | Dec 15, 2025 | 685B | MoE | 37B | ~377–404 GB | ❌ No | 6× over limit |
| **GLM-4.7-Flash** | Jan 2026 | 30B | MoE | ~3B | ~15 GB | ✅ Fits — but already covered at 24GB tier | Lower-tier model |
| **GLM-5** | Feb 2026 | 744B | MoE | — | ~400+ GB | ❌ No | Datacenter only |
| **Kimi K2.5** | Feb 17, 2026 | 1.04T | MoE | 32B | ~544 GB | ❌ No | Datacenter only |
| **Qwen3.5-397B-A17B** | Feb 16, 2026 | 397B | MoE | 17B | ~240+ GB | ❌ No | 4× over limit |
| **MiniMax M2.5** | Feb 2026 | 230B | MoE | 10B | ~128.8 GB | ❌ No | 2× over limit |
| **MiMo-V2-Flash** | 2026 | 309B | MoE | 15B | ~187 GB | ❌ No | 3× over limit |

### 1.2 The Devstral 2 Near-Miss

Devstral 2 (Mistral, December 10, 2025) is the most consequential model to miss the 64GB threshold. At 123B dense parameters with 256K native context and 72.2% SWE-bench Verified, it is the best open-weight coding model available. Its Q4_K_M GGUF is 74.9 GB — even with Q4_K_S (~72 GB estimated), it leaves zero room for KV cache on 64GB. Modified MIT license (commercial restriction for >$20M monthly revenue entities).

**Verdict:** Requires 96GB tier minimum. At Q4_K_M on the RTX PRO 6000 (96GB), it would load with ~21 GB KV room (32–48K context). This is the single strongest argument for jumping from 64GB to 96GB.

### 1.3 Models Already Covered at Lower Tiers

Two new releases from the window (Nemotron 3 Nano 30B and GLM-4.7-Flash) fit well within 64GB but were already viable at 24GB and are already mapped to Tier 1–2 agent roles in previous reports. They don't benefit from the extra VRAM — their Q4_K_M fits comfortably at 24GB with generous context.

### 1.4 The Trend: Open-Weight Models Are Getting Massive

The November 2025 – February 2026 window saw an explosion in model scale. The new releases cluster in two size ranges:
- **Small (≤36B):** GLM-4.7-Flash 30B, Nemotron 3 Nano 30B — fit at 24–32GB tiers
- **Massive (≥120B):** Everything else — 123B to 1T parameters, requiring 96GB to datacenter-class hardware

The **40–80B range that would be the sweet spot for 64GB** saw no new open-weight releases in this window. The industry jumped from "efficient small models" straight to "frontier-class massive MoE models."

---

## 2. Pre-November 2025 Models — Quantization Upgrades at 64GB

Since no new models unlock, the 64GB tier's value lies in running existing models at higher quantization with expanded context windows.

| Model | Released | 48GB Tier (quant / ctx) | 64GB Tier (quant / ctx) | What Improves |
|-------|---------|------------------------|------------------------|---------------|
| **Llama 3.3 70B** | Dec 2024 | Q4_K_M (42.5 GB) / 8–16K | Q5_K_M (49.9 GB) / 16–32K | Perplexity: +0.054→+0.025; 2× context |
| **R1-Distill-Llama-70B** | Jan 2025 | Q4_K_M (42.5 GB) / 8–16K | Q5_K_M (49.9 GB) / 16–32K | Reasoning chain fidelity + context |
| **Qwen2.5-72B** | Sep 2024 | ❌ Unusable (0.6 GB KV) | Q4_K_M (47.4 GB) / 16–32K | Enables model entirely; 152K vocab, 29+ langs |
| **Nemotron-Super-49B** | Mar–Oct 2025 | Q6_K (40.9 GB) / 8–16K | Q8_0 (53 GB) / 16–32K | Near-lossless (+0.001 ppl) |
| **GPT-oss-120B** | Aug 2025 | ❌ Doesn't fit | MXFP4 (~61–65 GB) / 4–8K | ⚠️ Fits but extremely tight KV; short-context only |
| **All MoE 30B** | May–Jul 2025 | Q8_0 / 160K+ | Q8_0 + ~31 GB KV headroom | Already at max quality; more multi-model room |
| **Gemma 3 27B** | Mar 2025 | Q8_0 (28.7 GB) / 128K | Q8_0 + ~35 GB spare | Already at max; enables dual-model serving |

### 2.1 GPT-oss-120B — Frontier MoE at the Edge of Feasibility

The GGML MXFP4 weights (~61 GB) leave ~3 GB for KV cache on 64GB. With Q8 KV quantization and Flash Attention, practical context is **4–8K tokens**. This enables single-turn tool calls and short agent interactions, but not multi-turn conversations or document analysis.

**Best use at 64GB:** Short-context orchestrator decisions and single-turn code generation where frontier-class reasoning matters more than context length. **Not recommended as primary workhorse** — context is too constrained. This model's true home is the 96GB tier where it has 31–33 GB KV headroom.

### 2.2 The Q5_K_M Quality Case

The jump from Q4_K_M to Q5_K_M for 70B dense models is the core value proposition of 64GB:
- Perplexity degradation: +0.054 (Q4) → +0.025 (Q5) vs FP16
- Community reports: noticeably better instruction-following, reduced phrase repetition
- Context roughly doubles: 8–16K → 16–32K
- File size increase: 42.5 GB → 49.9 GB (+7.4 GB for meaningful quality gain)

For agentic roles where output precision matters — orchestration, code generation, fact-checking — Q5_K_M is a genuine upgrade over Q4_K_M.

### 2.3 Context Window Expansion — 48GB Models With More Room

Beyond quantization upgrades, the extra 16 GB of KV headroom at 64GB allows 48GB-tier models to reach significantly longer context — in several cases approaching or hitting their full native window for the first time:

| Model | Quant | Weights | Context at 48GB | KV Room at 64GB | Est. Context at 64GB | Multiplier |
|-------|-------|---------|----------------|-----------------|---------------------|-----------|
| **Nemotron-Super-49B** | Q4_K_M | 30.2 GB | 32–64K | ~34 GB | **64–128K** (approaching native) | 2× |
| **Qwen3-32B** | Q8_0 | 34.8 GB | 48–96K | ~29 GB | **64–128K** (approaching native) | ~1.5× |
| **DS-R1-Distill-32B** | Q8_0 | 34.8 GB | 48–96K | ~29 GB | **64–128K** (approaching native) | ~1.5× |
| **Nemotron-Super-49B** | Q6_K | 40.9 GB | 8–16K | ~23 GB | **24–48K** | 3× |
| **Llama 3.3 70B** | Q4_K_M | 42.5 GB | 8–16K | ~21.5 GB | **16–32K** | 2× |
| **R1-Distill-70B** | Q4_K_M | 42.5 GB | 8–16K | ~21.5 GB | **16–32K** | 2× |

The standout: **Nemotron-Super-49B Q4_K_M** jumps from 32–64K at 48GB to potentially **full 128K native context** at 64GB — a transformative improvement for document-heavy agent roles (research, legal review, book writing, RAG) that were previously context-starved. Combined with its near-lossless reasoning toggle and native tool calling, this makes the Nemotron-Super-49B Q4_K_M the strongest argument for the 64GB tier: you get the same model and weights as the 48GB tier, but with **2–4× the usable context**.

---

## 3. Pipeline Parallelism — 2-Way and 4-Way Splits

### 3.1 No Native 64GB Card

Consumer: RTX 5090 = 32GB (max). Professional: RTX 6000 Ada = 48GB. Next native step: RTX PRO 6000 Blackwell at 96GB.

### 3.2 Speed Characteristics

| Config | Dense 70B Q5_K_M | Dense 70B Q4_K_M | MoE 30B Q8_0 | GPT-oss-120B |
|--------|-----------------|-----------------|-------------|-------------|
| **2× RTX 5090** | ~24–26 t/s | ~27 t/s | ~100+ t/s | ~40–60 t/s |
| **4× RTX 5060 Ti** | ~4–7 t/s | ~5–8 t/s | ~95 t/s (fits 2 cards) | ~15–25 t/s |

**2× RTX 5090** delivers 4–5× faster dense inference than 4× 5060 Ti due to fewer pipeline hops and 4× higher per-card bandwidth (1,792 vs 448 GB/s).

MoE models (Qwen3-30B-A3B, GPT-oss-120B) suffer far less from pipeline splits — only active parameters cross GPU boundaries.

With **ik_llama.cpp** (graph-level tensor parallelism), both configurations see estimated 2–3× speedups: 70B Q5_K_M on 2× 5090 could reach 35–45 t/s, on 4× 5060 Ti could reach 15–25 t/s.

### 3.3 4× 5060 Ti Unique Advantage: Multi-Model Serving

The 4-card config can run models simultaneously: e.g., 70B Q4_K_M across 3 cards + Qwen3-14B on the 4th card. This eliminates swap latency for multi-agent pipelines — the router and workhorse can serve concurrently.

---

## 4. Inference Tools — Compatibility Matrix

| Tool | 2-GPU | 4-GPU | Mode | Format |
|------|-------|-------|------|--------|
| **llama.cpp** | ✅ | ✅ | Pipeline (`-sm layer`) | GGUF |
| **ik_llama.cpp** | ✅ | ✅ (emerging) | True TP (`-sm graph`) | GGUF |
| **Ollama** | ✅ Auto | ✅ Auto | Pipeline | GGUF |
| **vLLM** | ✅ PP=2 | ✅ PP=4 | Pipeline parallel | HF/AWQ/GPTQ/FP8 |
| **ExLlamaV2/V3** | ✅ | ✅ | Layer split + TP | EXL2/EXL3 |
| **SGLang** | ✅ PP=2 | ✅ PP=4 | Pipeline parallel | HF/AWQ/GPTQ/FP8 |
| **TensorRT-LLM** | ✅ | ✅ | PP and TP | HF/FP8/INT4 |
| **KoboldCpp** | ✅ | ✅ | Layer split | GGUF |
| **TabbyAPI** | ✅ | ✅ | Via ExLlamaV2/V3 | EXL2/EXL3 |

**Recommendations:** Ollama for quick testing. ik_llama.cpp for maximum speed. vLLM PP=N for production serving.

---

## 5. Complete Agent Role Mapping — All 59 Roles at 64GB

Since no genuinely new model unlocks at this tier, upgrades come from quantization improvements. Roles marked **⬆ UPGRADE** benefit from Q5_K_M or Q8_0 upgrades.

### 5.1 Tier 1 — Simple Roles (8 roles) — No Upgrades

| Role | Model | Quant | Speed | Upgrade? |
|------|-------|-------|-------|----------|
| Router/triage | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Input validator | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Heartbeat/health | Qwen3-0.6B | Q8_0 | ~500+ t/s | ➡ No |
| Notification/alert | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Sentiment analysis | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| FAQ generation | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No |
| Translation | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No |
| Calendar/scheduling | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |

### 5.2 Tier 2 — Moderate Roles (27 roles) — 3 Upgrades

| Role | 64GB Model | Quant | Upgrade? | Why |
|------|-----------|-------|----------|-----|
| Research/web search | Nemotron-Super-49B | Q8_0 | ⬆ YES | Near-lossless reasoning, 16–32K ctx |
| Content writing | Nemotron-Super-49B | Q8_0 | ⬆ YES | Better prose quality at Q8_0 |
| Editing | Qwen3-32B | Q8_0 | ➡ No | Already Q8_0 at 48GB |
| Content planner | Qwen3-32B | Q8_0 | ➡ No | Already Q8_0 |
| Email drafting | Qwen3-32B | Q4_K_M | ➡ No | Sufficient |
| Document summarization | Nemotron-Super-49B | Q8_0 | ⬆ YES | Near-lossless + ctx upgrade |
| Meeting notes | Qwen3-30B-A3B | Q8_0 | ➡ No | Already excellent |
| Social media scouting | Qwen3-14B | Q4_K_M | ➡ No | Short-form, sufficient |
| Social media content | Qwen3-14B | Q4_K_M | ➡ No | Short-form, sufficient |
| News aggregation | Qwen3-14B | Q4_K_M | ➡ No | Sufficient |
| Shopping/price comparison | Qwen3-8B | Q4_K_M | ➡ No | Structured extraction |
| Memory/knowledge mgmt | Qwen3-30B-A3B | Q8_0 | ➡ No | Already Q8_0 |
| RAG/retrieval | Qwen3-30B-A3B | Q8_0 | ➡ No | Already Q8_0 + 160K ctx |
| Data analysis | Nemotron-Super-49B | Q8_0 | ➡ Marginal | Quality bump |
| Website scraping | Qwen3-8B | Q4_K_M | ➡ No | Parsing only |
| Image description | Gemma 3 27B | Q8_0 | ➡ No | Already Q8_0 |
| Customer support | Qwen3-32B | Q4_K_M | ➡ No | Sufficient |
| Lead scoring | Qwen3-14B | Q4_K_M | ➡ No | Classification |
| Project summarization | Qwen3-32B | Q8_0 | ➡ No | Already Q8_0 |
| Transaction/approval | Qwen3-8B | Q4_K_M | ➡ No | Rule-heavy |
| Home automation | Qwen3-8B | Q4_K_M | ➡ No | Command parsing |
| Fitness tracking | Qwen3-8B | Q4_K_M | ➡ No | Data logging |
| Recipe/cooking | Qwen3-14B | Q4_K_M | ➡ No | Knowledge retrieval |
| Personal finance | Qwen3-14B | Q4_K_M | ➡ No | 14B handles well |
| SEO optimization | Qwen3-14B | Q4_K_M | ➡ No | Content analysis |
| Landing page generation | Qwen3-32B | Q8_0 | ➡ No | Already Q8_0 |
| Travel planning | Qwen3-14B | Q4_K_M | ➡ No | Sufficient |

### 5.3 Tier 3 — Complex Roles (11 roles) — 5 Upgrades

| Role | 64GB Model | Quant | Speed (2× 5090) | Upgrade? | Why |
|------|-----------|-------|-----------------|----------|-----|
| **Code generation** | Llama 3.3 70B | Q5_K_M | ~25 t/s | ⬆ YES | Q5 quality for code precision |
| **Code review** | Llama 3.3 70B | Q5_K_M | ~25 t/s | ⬆ YES | Better subtle bug detection |
| **QA/test writing** | Llama 3.3 70B | Q5_K_M | ~25 t/s | ⬆ YES | Better edge-case generation |
| Task planning | Qwen3-30B-A3B | Q8_0 | ~100 t/s | ➡ No | MoE speed already optimal |
| **Fact-checking** | Llama 3.3 70B | Q5_K_M | ~25 t/s | ⬆ YES | Reduced hallucination at Q5 |
| Critic/review | Nemotron-Super-49B | Q8_0 | ~22 t/s | ➡ Marginal | Already Q6_K available |
| Market research | Qwen3-30B-A3B | Q8_0 | ~100 t/s | ➡ No | Already excellent |
| Synthesizer/aggregator | Qwen3-30B-A3B | Q8_0 | ~100 t/s | ➡ No | 160K ctx + speed optimal |
| Curriculum design | Qwen3-32B | Q8_0 | ~30 t/s | ➡ No | Already Q8_0 |
| **Prototype generation** | Llama 3.3 70B | Q5_K_M | ~25 t/s | ⬆ YES | Better full-stack code gen at Q5 |
| DevOps | Qwen3-32B | Q8_0 | ~30 t/s | ➡ No | Sufficient |

### 5.4 Tier 4 — Reasoning Roles (3 roles) — 1 Upgrade

| Role | 64GB Model | Quant | Speed (2× 5090) | Upgrade? | Why |
|------|-----------|-------|-----------------|----------|-----|
| **Math/logic reasoning** | R1-Distill-70B | Q5_K_M | ~25 t/s | ⬆ YES | Chain-of-thought fidelity at Q5 |
| STEM analysis | R1-Distill-70B | Q5_K_M | ~25 t/s | ➡ Marginal | Was already Q4_K_M at 48GB |
| Algorithm exploration | Qwen3-32B (thinking) | Q8_0 | ~30 t/s | ➡ No | Already Q8_0 |

### 5.5 Tier 5 — Frontier Roles (10 roles) — 3 Upgrades

| Role | 64GB Model | Quant | Speed (2× 5090) | Cloud still better? | Upgrade? |
|------|-----------|-------|-----------------|---------------------|----------|
| **Orchestrator/manager** | Llama 3.3 70B | Q5_K_M | ~25 t/s | Yes, for complex | ⬆ YES |
| **Software architect** | Llama 3.3 70B | Q5_K_M | ~25 t/s | Yes | ⬆ YES |
| Complex debugger | Qwen3-Coder-30B | Q8_0 | ~100 t/s | Yes | ➡ No |
| Legal document review | Nemotron-Super-49B | Q8_0 | ~22 t/s | Yes, strongly | ➡ Marginal |
| Medical/health analysis | Nemotron-Super-49B | Q8_0 | ~22 t/s | Yes, always | ➡ Marginal |
| Financial analysis | Nemotron-Super-49B | Q8_0 | ~22 t/s | Yes | ➡ Marginal |
| Security analyst | Qwen3-Coder-30B | Q8_0 | ~100 t/s | Yes | ➡ No |
| SRE/incident response | Qwen3-Coder-30B | Q8_0 | ~100 t/s | Partially | ➡ No |
| **Book writing** | Llama 3.3 70B | Q5_K_M | ~25 t/s | Yes | ⬆ YES |
| Compliance/regulatory | Qwen3-32B | Q8_0 | ~30 t/s | Yes, strongly | ➡ No |

### 5.6 Upgrade Summary — All 59 Roles

| Tier | Total Roles | Upgraded at 64GB | Unchanged | Key Driver |
|------|------------|-----------------|-----------|------------|
| Tier 1 (simple) | 8 | 0 | 8 | 8–14B already sufficient |
| Tier 2 (moderate) | 27 | 3 | 24 | Nemotron-49B Q8_0 |
| Tier 3 (complex) | 11 | 5 | 6 | Llama 70B Q5_K_M quality |
| Tier 4 (reasoning) | 3 | 1 | 2 | R1-Distill-70B Q5_K_M chain fidelity |
| Tier 5 (frontier) | 10 | 3 | 7 | Precision-critical roles benefit from Q5 |
| **Total** | **59** | **12** | **47** | |

---

## 6. Deployment Architectures

### 6.1 2× RTX 5090 (~$4,000)

**Architecture A — Single 70B at Q5_K_M:**
Split Llama 3.3 70B Q5_K_M (49.9 GB) across both cards. ~14 GB KV room (16–32K ctx). Swap to R1-Distill-70B Q5_K_M for reasoning. ~24–27 t/s.

**Architecture B — 49B Q8_0 + Router:**
Nemotron-Super-49B Q8_0 (53 GB) split across both cards + no room for sidecar. Or: Nemotron-Super-49B Q6_K (40.9 GB) on one card + Qwen3-14B on the other. Zero-swap dual model.

**Architecture C — MoE Workhorse (no split needed):**
Qwen3-30B-A3B Q8_0 (32.5 GB) fits entirely on one 5090 card at ~100+ t/s. Second card free for Qwen3-32B Q8_0 (34.8 GB). Two quality models, no pipeline split, independent GPUs.

### 6.2 4× RTX 5060 Ti (~$1,300)

**Architecture A — 3+1 Split:**
Llama 3.3 70B Q4_K_M across 3 cards + Qwen3-8B on 4th card for routing. ~5–8 t/s for 70B, ~186 t/s for routing.

**Architecture B — 2+2 Independent:**
Qwen3-30B-A3B Q8_0 across 2 cards (~100 t/s) + Gemma 3 27B Q8_0 on 1 card + Qwen3-8B on 1 card. Three simultaneous models.

**Architecture C — Maximum Model Diversity:**
GPU 0: Qwen3-14B Q6_K. GPU 1: GPT-oss-20B MXFP4. GPU 2: Gemma 3 27B Q4. GPU 3: Qwen3-8B. Four independent models, zero swap latency.

### 6.3 Recommended Architecture by Workload

| Workload | 2× RTX 5090 | 4× RTX 5060 Ti |
|----------|-------------|----------------|
| Quality-critical coding | Arch A: 70B Q5_K_M | Arch A: 70B Q4_K_M on 3+1 |
| Multi-agent pipeline | Arch C: MoE + 32B independent | Arch B: 2+2 independent |
| Deep reasoning | Swap to R1-Distill-70B Q5_K_M | 3-card R1 split (slow) |
| Mixed diverse roles | Arch C with model rotation | Arch C: 4 independent models |

---

## 7. Models That Do NOT Fit at 64GB

| Model | Release | Params | Architecture | Q4_K_M Size | Verdict |
|-------|---------|--------|-------------|-------------|---------|
| **Devstral 2** | Dec 2025 | 123B | Dense | 74.9 GB | ❌ 11 GB over limit |
| **DeepSeek V3.2** | Dec 2025 | 685B | MoE | ~377 GB | ❌ Datacenter only |
| **GLM-5** | Feb 2026 | 744B | MoE | ~400+ GB | ❌ Datacenter only |
| **Kimi K2.5** | Feb 2026 | 1.04T | MoE | ~544 GB | ❌ Datacenter only |
| **Qwen3.5-397B** | Feb 2026 | 397B | MoE | ~240+ GB | ❌ 4× over limit |
| **MiniMax M2.5** | Feb 2026 | 230B | MoE | ~128.8 GB | ❌ 2× over limit |
| **MiMo-V2-Flash** | 2026 | 309B | MoE | ~187 GB | ❌ 3× over limit |
| **Qwen3-235B-A22B** | Jul 2025 | 235B | MoE | ~140+ GB | ❌ Far too large |
| **Llama 4 Scout** | Apr 2025 | 109B | MoE | 65.4 GB | ⚠️ Barely fits weights, ≤2K ctx — unusable |
| **Command R+** | Apr 2024 | 104B | Dense | ~62.8 GB | ⚠️ Fits weights, ~1.2 GB KV — unusable |

---

## 8. Conclusion & Recommended OpenClaw Model Stack at 64GB

### 8.1 Honest Assessment: The Weakest Tier Jump

The 48GB → 64GB transition is the smallest upgrade in the OpenClaw tier series:

| Tier Jump | Roles Upgraded | New Models | Qualitative Leap |
|-----------|---------------|------------|-----------------|
| 16GB → 24GB | ~15 | 4 (Qwen3-32B, MoE 30B, Gemma 27B, R1-Distill-32B) | Orchestration becomes viable |
| 24GB → 32GB | 36 | 3 (via pipeline split) | Complex roles unlock |
| 32GB → 48GB | 25 | 3 (Llama 70B, R1-Distill-70B, Nemotron-49B) | 70B class unlocks |
| **48GB → 64GB** | **12 of 59** | **0 new** | **Quantization upgrades only** |
| 64GB → 96GB | 20 | 3 (GPT-oss-120B, Qwen3-Next-80B, Llama 4 Scout) | Frontier MoE unlocks |

### 8.2 Primary Model Stack

| Priority | Model | Roles Covered | Key Advantage |
|----------|-------|--------------|---------------|
| **Quality workhorse** | Llama 3.3 70B Q5_K_M | 8 roles (T3–T5): coding, review, QA, fact-checking, orchestrator, architect, prototyping, book writing | Q5 quality at 70B, BFCL 77.3% |
| **Reasoning specialist** | R1-Distill-70B Q5_K_M | 1 role (T4): math/logic | Q5 chain-of-thought fidelity, AIME 70% |
| **Analytical workhorse** | Nemotron-Super-49B Q8_0 | 3 roles (T2): research, content, docs | Near-lossless, reasoning toggle, tool calling |
| **Fast MoE general** | Qwen3-30B-A3B Q8_0 | 6+ roles (T2–T5): planning, synthesis, RAG, meetings | 100+ t/s, 160K+ ctx |
| **Coding specialist** | Qwen3-Coder-30B Q8_0 | 3 roles (T3–T5): debugging, security, SRE | MoE speed, coding-optimized |
| **Quality general** | Qwen3-32B Q8_0 | 6+ roles (T2–T5): editing, compliance, curriculum | Near-lossless quality |
| **Mid-range** | Qwen3-14B Q4_K_M | 12 roles (T1–T2) | Fast single-GPU |
| **Fast lightweight** | Qwen3-8B Q4_K_M | 8 roles (T1) | 186 t/s, routing |
| **Heartbeat** | Qwen3-0.6B Q8_0 | 1 role (T1) | 500+ t/s |

### 8.3 Recommendation: Skip 64GB or Save for 96GB

For builders currently at 48GB:
- **If you have 2× RTX 5090:** The Q5_K_M quality upgrade for 70B models is real but incremental. Consider whether 12 role improvements justify the hardware investment.
- **If you're considering 4× RTX 5060 Ti:** The brutal 5–8 t/s speeds for dense 70B models make this hard to recommend unless you need multi-model serving via the 4-card flexibility.
- **If you can stretch the budget:** The 96GB tier (RTX PRO 6000 Blackwell, ~$8,000) unlocks GPT-oss-120B at 120+ t/s, Qwen3-Next-80B-A3B with 128K+ context, and Devstral 2 123B — all genuinely transformative models that represent a far larger capability jump than anything available at 64GB.

**12 of 59 roles upgrade at 64GB — all through quantization improvements, not new model access.** The upgrades concentrate in Tier 3–5 coding and precision-critical roles where Q5_K_M's reduced quantization tax produces measurable quality gains. For most OpenClaw deployments, the 48GB tier provides adequate quality, and the next meaningful jump is 96GB.
