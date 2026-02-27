# Model Selection for OpenClaw Agent & Subagent Roles — 32GB VRAM Tier

**OpenClaw Agent Framework — Model Analysis (Part 4)**
**Date:** February 14, 2026

---

## Executive Summary

This report maps specific LLM models to OpenClaw agent and subagent roles within the 32GB VRAM tier. Every model is evaluated on its architecture (dense vs MoE), quantization options, context window capacity, speed characteristics under multi-GPU inference, and suitability for each agent role.

**Key findings:**

- **All 27–36B models from Part 3 are deployable** in OpenClaw agent roles at the 32GB tier — including Qwen3-32B, DeepSeek-R1-Distill-32B, Gemma 3 27B, Seed-OSS-36B, and EXAONE 4.0 32B.
- **Pipeline parallelism (layer split) is the method** for running these models across 2× 16GB GPUs when they exceed single-card VRAM. Every model except GPT-oss-20B requires this split.
- **MoE models are the optimal architecture for split deployments** — Qwen3-30B-A3B retains 92% of single-card speed when split, vs only 30% for dense models. This makes MoE the default choice for latency-sensitive agent roles.
- **llama.cpp and Ollama are the recommended inference tools** for multi-GPU pipeline splits. vLLM for production serving, ExLlamaV3 for maximum quantization quality.
- **Qwen3-30B-A3B is the recommended primary workhorse** for most OpenClaw roles, with dense models reserved for specialized tasks (deep reasoning, creative writing).
- **Dual-model serving** enables simultaneous operation of a fast router (8B) alongside a specialist model (14–20B) — eliminating model swap latency in multi-agent pipelines.

---

## 1. Available Models — Architecture & Specifications

### 1.1 Complete Model Roster for 32GB Tier

| Model | Architecture | Total Params | Active Params | Recommended Quant | Weight Size | Max Context on 32GB |
|-------|-------------|-------------|---------------|-------------------|-------------|---------------------|
| **Qwen3-32B** | Dense | 32B | 32B | Q4_K_M / Q5_K_M | 19.8 / 23.2 GB | 16–45K tokens |
| **DeepSeek-R1-Distill-32B** | Dense | 32B | 32B | Q4_K_M | ~20 GB | 8–16K tokens |
| **Gemma 3 27B** | Dense | 27B | 27B | QAT Q4_0 / Q6_K / Q8_0 | 15.6 / 22 / 29 GB | 20–40K+ (Q4) / 4–8K (Q8) |
| **Qwen3-30B-A3B** | MoE | 30.5B | 3.3B | Q4_K_M | ~18.6 GB | 32–131K tokens |
| **Qwen3-Coder-30B-A3.3B** | MoE | 30.5B | 3.3B | Q4_K_M | ~18.6 GB | 32–131K tokens |
| **EXAONE 4.0 32B** | Dense | 32B | 32B | Q4_K_M / Q5_K_M | 19.8 / 23 GB | 12–24K tokens |
| **Seed-OSS-36B** | Dense | 36B | 36B | Q4_K_M / Q5_K_M | 21.5 / 25.6 GB | 8–16K tokens |
| **Nemotron 3 Nano 30B** | Hybrid MoE | 30B | ~8B | UD-Q4_K_XL | ~22.8 GB | 16–32K tokens |
| **GPT-oss-20B** | MoE | 21B | ~4B | MXFP4 / Q4_K_M | ~13.7 GB | Full context (fits single 16GB) |

### 1.2 Why Architecture Matters for Agent Deployment

The choice between dense and MoE models has massive implications for OpenClaw agent performance in multi-GPU configurations:

- **MoE models (Qwen3-30B-A3B, Qwen3-Coder-30B, GPT-oss-20B, Nemotron):** Only a fraction of parameters activate per token (e.g., 3.3B of 30.5B for Qwen3-30B-A3B). This sparse activation dramatically reduces inter-GPU data transfer during inference. Result: **92% speed retention** when split across GPUs at short context.

- **Dense models (Qwen3-32B, R1-Distill-32B, Gemma 3 27B, EXAONE, Seed-OSS):** All parameters activate every token. Full weight data must flow through inter-GPU links. Result: **30% speed retention** when split — functional but significantly slower.

**Practical takeaway:** Default to MoE models for any latency-sensitive OpenClaw role. Reserve dense models for roles where their specific capabilities (deep reasoning, multimodal vision, creative quality) justify the speed tradeoff.

### 1.3 Higher Quantization Options at 32GB

The 32GB tier enables higher-quality quantizations that don't fit at 16GB, directly improving model output quality:

| Model | Best Quant at 16GB | Best Quant at 32GB | Quality Gain |
|-------|-------------------|-------------------|--------------|
| **Qwen3-32B** | ❌ Doesn't fit | Q4_K_M or Q5_K_M | Enables model entirely; Q5_K_M adds ~2% coding quality |
| **Gemma 3 27B** | Q4_K_M (tight, minimal context) | Q6_K or Q8_0 (near-lossless) | +3–8% quality across benchmarks |
| **DeepSeek-R1-Distill-32B** | ❌ Doesn't fit | Q4_K_M | Enables model entirely |
| **Qwen3-30B-A3B** | Q4_K_M (fits, but no KV room) | Q4_K_M + large KV cache | Context jumps from ~8K to 131K |

---

## 2. Pipeline Parallelism — How Models Exceeding 16GB Get Split

### 2.1 The Problem: 27–36B Models Don't Fit a Single 16GB Card

Every model in section 1 (except GPT-oss-20B) has weights exceeding 16GB at recommended quantization. Qwen3-32B Q4_K_M = 19.8 GB. Gemma 3 27B Q6_K = 22 GB. Seed-OSS-36B Q4_K_M = 21.5 GB. None of these load onto a single 16GB GPU. Pipeline parallelism solves this by distributing model layers across two GPUs.

### 2.2 How Pipeline Parallelism (Layer Split) Works

A model with 64 transformer layers gets split sequentially: layers 0–31 load on GPU 0, layers 32–63 load on GPU 1. During inference:

1. GPU 0 processes its layers, produces activation data (~8–16 KB)
2. Activation data transfers to GPU 1 through the PCIe bus
3. GPU 1 processes its layers, produces the output token
4. For the next token, the cycle repeats

**Key characteristic:** Only one GPU computes at a time — while GPU 1 works, GPU 0 sits idle (the "pipeline bubble"). This means you gain **VRAM capacity** (fit larger models), but **not speed** (token generation ≈ single-GPU speed). The value proposition is fitting 27–36B models that are otherwise impossible at 16GB.

### 2.3 Why MoE Models Suffer Less From Splitting

Dense models activate all parameters every token — the full 32B weights flow through computation. MoE models like Qwen3-30B-A3B only activate 3.3B of 30.5B parameters per token. The inactive experts sit in VRAM but don't participate in the forward pass, dramatically reducing the data that needs to cross the GPU boundary.

This is why the speed difference is so extreme:
- **Qwen3-30B-A3B (MoE):** ~101 t/s on split GPUs vs ~110 t/s on single 32GB card = **92% retained**
- **Qwen3-32B (dense):** ~18 t/s on split GPUs vs ~61 t/s on single 32GB card = **30% retained**

### 2.4 Alternative: Tensor Parallelism

Instead of splitting layers sequentially, tensor parallelism splits each layer's weight matrices across both GPUs so they compute simultaneously. In theory this is faster, but it requires heavy synchronization after every layer. Over consumer PCIe links (~32 GB/s effective), the synchronization overhead usually makes tensor parallelism **slower** than pipeline parallelism for token generation.

**Exception:** ExLlamaV3's tensor parallelism implementation is well-optimized and achieves 86% of single-RTX-3090 speed for MoE models even over PCIe. Worth testing if using EXL2 quantization.

### 2.5 Per-Model Split Behavior

| Model | Weight Size | Fits Single 16GB? | Split Required? | Split Speed Impact |
|-------|-----------|-------------------|-----------------|-------------------|
| **Qwen3-32B** Q4_K_M | 19.8 GB | ❌ No | Yes — pipeline split | ~30% of single-card speed (dense) |
| **Qwen3-32B** Q5_K_M | 23.2 GB | ❌ No | Yes — pipeline split | ~28% of single-card speed (dense) |
| **DeepSeek-R1-Distill-32B** Q4_K_M | ~20 GB | ❌ No | Yes — pipeline split | ~30% est. (dense) |
| **Gemma 3 27B** QAT Q4_0 | 15.6 GB | ⚠️ Barely (no KV room) | Recommended | ~35% est. (dense, smaller model) |
| **Gemma 3 27B** Q6_K | 22 GB | ❌ No | Yes — pipeline split | ~30% est. (dense) |
| **Gemma 3 27B** Q8_0 | 29 GB | ❌ No | Yes — pipeline split | ~25% est. (dense, heavy weights) |
| **Qwen3-30B-A3B** Q4_K_M | 18.6 GB | ❌ No | Yes — pipeline split | **~92% of single-card speed (MoE)** |
| **Qwen3-Coder-30B** Q4_K_M | 18.6 GB | ❌ No | Yes — pipeline split | **~92% est. (MoE)** |
| **EXAONE 4.0 32B** Q4_K_M | 19.8 GB | ❌ No | Yes — pipeline split | ~30% est. (dense) |
| **Seed-OSS-36B** Q4_K_M | 21.5 GB | ❌ No | Yes — pipeline split | ~25% est. (dense, largest model) |
| **Nemotron 3 Nano 30B** UD-Q4_K_XL | 22.8 GB | ❌ No | Yes — pipeline split | ~60% est. (hybrid MoE) |
| **GPT-oss-20B** MXFP4 | 13.7 GB | ✅ Yes | **No — keep on single GPU** | Splitting would reduce speed unnecessarily |

---

## 3. Inference Tools for Multi-GPU Model Splitting

### 3.1 Which Tools Support Pipeline Parallelism for Split Models?

Not every inference engine handles multi-GPU splitting. Below is the compatibility matrix focused on what matters for OpenClaw deployment: can it split a 27–36B model across two 16GB GPUs, and how well does it work?

| Tool | Split Method | Quantization Formats | Auto-Split? | Recommended For |
|------|-------------|---------------------|-------------|-----------------|
| **llama.cpp** | Pipeline (`-sm layer`) + Row (`-sm row`) + Graph (`-sm graph` in ik_llama.cpp fork) | GGUF (Q4_K_M, Q5_K_M, Q6_K, Q8_0) | Manual (`--tensor-split`) | Default choice — widest model support, mature multi-GPU |
| **Ollama** | Pipeline (auto, via llama.cpp backend) | GGUF (auto-downloaded from registry) | ✅ Fully automatic | Simplest path — auto-detects GPUs, auto-distributes layers |
| **vLLM** | Pipeline (`--pipeline-parallel-size 2`) or Tensor (`--tensor-parallel-size 2`) | Safetensors, AWQ, GPTQ, FP8 | Manual config | Production serving — OpenAI-compatible API, batched inference |
| **ExLlamaV2/V3** | Tensor (`--gpu_split auto`) | EXL2 (adaptive quantization) | ✅ Auto GPU split | Best quant quality per bit — EXL2 outperforms GGUF at same bpw |
| **SGLang** | Pipeline, Tensor, Expert Parallelism, Data Parallelism | Safetensors, AWQ, GPTQ, FP8 | Manual config | MoE-optimized expert parallelism — overkill for most setups |
| **TensorRT-LLM** | Tensor + Pipeline | FP8, INT8, INT4 (compiled engines) | No — requires engine compilation | Maximum speed — but hard setup, compile per model |

### 3.2 Tool Recommendations by OpenClaw Use Case

**Starting out / quick testing → Ollama**
Zero configuration. Install Ollama, run `ollama run qwen3:30b-a3b`, it auto-detects both GPUs and splits the model. Downside: only pipeline parallelism, no fine-tuning of split ratios.

**Daily OpenClaw deployment → llama.cpp server**
Best balance of control and simplicity. Pipeline split with `-sm layer` is the recommended mode for consumer PCIe. Supports explicit VRAM allocation per GPU via `--tensor-split`. Runs as OpenAI-compatible API server for agent integration. Widest GGUF model selection.

**Production / multi-user serving → vLLM**
Use `--pipeline-parallel-size 2` (not tensor parallel) for consumer GPUs — pipeline has lower communication overhead on PCIe. Continuous batching, OpenAI-compatible API. Best when OpenClaw runs as a service handling concurrent requests.

**Maximum model quality → ExLlamaV3 + TabbyAPI**
EXL2 quantization delivers superior quality per bit vs GGUF. Tensor parallelism via `--gpu_split auto`. Benchmark: Qwen3-30B-A3B 5-bit on dual GPUs achieved 86% of single-RTX-3090 speed (44 t/s vs 51 t/s at 32K context). Use when output quality matters more than ecosystem convenience.

**MoE-heavy workloads → SGLang**
Expert parallelism distributes MoE experts across GPUs more efficiently than simple layer split. If running Qwen3-30B-A3B or Qwen3-Coder-30B as the primary agent and want maximum MoE throughput, SGLang's expert parallelism is worth the setup complexity.

### 3.3 Tool Selection per Model

| Model | Best Tool | Why | Alternative |
|-------|----------|-----|-------------|
| **Qwen3-30B-A3B** Q4_K_M | llama.cpp / Ollama | GGUF ecosystem, pipeline split works great for MoE | SGLang (expert parallelism) |
| **Qwen3-Coder-30B** Q4_K_M | llama.cpp / Ollama | Same MoE architecture, same tool recommendation | vLLM (production serving) |
| **Qwen3-32B** Q4_K_M/Q5_K_M | llama.cpp | Pipeline split, GGUF — dense model, accept speed penalty | ExLlamaV3 (EXL2 for quality) |
| **DeepSeek-R1-Distill-32B** Q4_K_M | llama.cpp | Pipeline split, reasoning model — speed not critical | vLLM (if serving as API) |
| **Gemma 3 27B** Q6_K/Q8_0 | llama.cpp / Ollama | GGUF, pipeline split, straightforward | ExLlamaV3 (EXL2 quality edge) |
| **EXAONE 4.0 32B** Q4_K_M | llama.cpp | GGUF pipeline split | vLLM (safetensors) |
| **Seed-OSS-36B** Q4_K_M | llama.cpp | Largest dense model at tier, needs reliable split | — |
| **Nemotron 3 Nano 30B** | llama.cpp | Hybrid MoE, GGUF support | SGLang (expert parallelism) |
| **GPT-oss-20B** MXFP4 | llama.cpp (single GPU) | Fits one card — do NOT split | Ollama (single GPU) |

---

## 4. Complete Agent Role Mapping — All 5 Tiers (40+ Roles)

All speeds below are for models split via pipeline parallelism across 2× 16GB GPUs. For models that fit a single 16GB card (8B and below), speeds reflect single-GPU operation. Roles marked **⬆ UPGRADE** benefit meaningfully from the 32GB tier vs 16GB single-card. Roles marked **➡ SAME** run identically to 16GB — the 8B/14B model already handles them well and doesn't need splitting.

### 4.1 Tier 1 — Simple Roles (8 roles)

Simple classification, routing, or template-based tasks. Small models (0.6B–14B) handle these on a single 16GB card — no pipeline split needed. These roles do NOT benefit from the 32GB tier.

| Role | Recommended Model | Quant | Speed | Split? | Status |
|------|------------------|-------|-------|--------|--------|
| **Router/triage** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME |
| **Input validator** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME |
| **Heartbeat/health** | Qwen3-0.6B | Q8_0 | ~500+ t/s | No — single GPU | ➡ SAME |
| **Notification/alert** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME |
| **Sentiment analysis** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME |
| **FAQ generation** | Qwen3-14B | Q4_K_M | ~124 t/s | No — single GPU | ➡ SAME |
| **Translation** | Qwen3-14B | Q4_K_M | ~124 t/s | No — single GPU | ➡ SAME |
| **Calendar/scheduling** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME |

**Tier 1 summary:** All 8 roles stay on a single 16GB card. No pipeline split needed. Second GPU is free for a second simultaneous model.

### 4.2 Tier 2 — Moderate Roles (25 roles)

Tasks requiring better comprehension, longer context, or more nuanced generation. Several roles upgrade at 32GB due to access to 27–36B models via pipeline split, especially document-heavy and analytical tasks.

| Role | Recommended Model | Quant | Speed | Split? | Status | Notes |
|------|------------------|-------|-------|--------|--------|-------|
| **Research/web search** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | MoE speed + 131K context for multi-source synthesis |
| **Content writing** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Better prose quality at Q5. Dense = slow but worth it for writing |
| **Editing/proofreading** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | More consistent style corrections at higher quant |
| **Email drafting** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | 14B sufficient for email |
| **Document summarization** | Gemma 3 27B | Q6_K | ~20 t/s | Yes — pipeline split | ⬆ UPGRADE | Q6_K quality + 20–40K context handles longer docs |
| **Meeting notes** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | 131K context for long meeting transcripts |
| **Social media** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Short-form content, 14B sufficient |
| **News aggregation** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Classification + summary, 14B handles well |
| **Shopping/price comparison** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME | Structured data extraction, small model fine |
| **Memory/knowledge mgmt** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | 131K context + better retrieval accuracy |
| **RAG/retrieval** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | Long context for retrieved chunks, higher extraction precision |
| **Data analysis** | Qwen3-32B | Q4_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Better numerical reasoning at 32B |
| **Website scraping** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME | HTML parsing, structured extraction |
| **Image description** | Gemma 3 27B | Q8_0 | ~15 t/s | Yes — pipeline split | ⬆ UPGRADE | Near-lossless multimodal — major quality jump vs Q4 on 16GB |
| **Customer support** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Conversation management, 14B sufficient |
| **Lead scoring** | Qwen3-14B | Q4_K_M | ~124 t/s | No — single GPU | ➡ SAME | Classification task |
| **Project summarization** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | 131K context for full project docs |
| **Transaction/approval** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME | Simple validation/routing |
| **Home automation** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME | Command parsing, structured output |
| **Fitness tracking** | Qwen3-8B | Q4_K_M | ~186 t/s | No — single GPU | ➡ SAME | Data logging + simple analysis |
| **Recipe/cooking** | Qwen3-14B | Q4_K_M | ~124 t/s | No — single GPU | ➡ SAME | Knowledge retrieval + generation |
| **Personal finance** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Calculation + advice, 14B handles well |
| **SEO optimization** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Content analysis + suggestions |
| **Landing page generation** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Better code + copy quality at 32B |
| **Travel planning** | Qwen3-14B | Q6_K | ~100 t/s | No — single GPU | ➡ SAME | Itinerary generation, 14B sufficient |

**Tier 2 summary:** 12 of 25 roles upgrade at 32GB. The upgrades are concentrated in document-heavy, analytical, and content creation roles where 27–36B models via pipeline split provide meaningfully better output. 13 roles remain on single-GPU 8B/14B models.

### 4.3 Tier 3 — Complex Roles (11 roles)

Tasks requiring strong coding, analytical reasoning, or multi-step synthesis. Almost all roles benefit from 27–36B models at 32GB. These are the roles that most justify the pipeline split.

| Role | Recommended Model | Quant | Speed | Split? | Status | Notes |
|------|------------------|-------|-------|--------|--------|-------|
| **Code generation** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | ⬆ UPGRADE | Purpose-built MoE coder. 131K context for large codebases |
| **Code review** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | ⬆ UPGRADE | Better at spotting subtle bugs at 30B vs 14B |
| **QA/test writing** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | ⬆ UPGRADE | More consistent test coverage generation |
| **Task planning** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | MoE speed for rapid planning iterations |
| **Fact-checking** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Reduced hallucination at higher quant |
| **Critic/review** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | More nuanced analytical output |
| **Market research** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | 131K context for multi-source synthesis |
| **Synthesizer/aggregator** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | ⬆ UPGRADE | Handles more input documents in single pass |
| **Curriculum design** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Better coherence in structured educational content |
| **Prototype generation** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | ⬆ UPGRADE | Fast MoE coding for rapid prototyping |
| **DevOps** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | ⬆ UPGRADE | More reliable YAML/config/IaC generation |

**Tier 3 summary:** All 11 roles upgrade at 32GB. MoE models (Qwen3-Coder-30B, Qwen3-30B-A3B) handle 7 of 11 roles at ~100 t/s with pipeline split — excellent speed despite dual-GPU. Dense models (Qwen3-32B) serve 4 roles at ~18 t/s — slower but the quality gain justifies the tradeoff.

### 4.4 Tier 4 — Reasoning Roles (3 roles)

Deep multi-step reasoning, mathematical proofs, scientific analysis. Latency tolerance is high — quality trumps speed. Dense models are mandatory here because chain-of-thought reasoning benefits from full parameter activation.

| Role | Recommended Model | Quant | Speed | Split? | Status | Notes |
|------|------------------|-------|-------|--------|--------|-------|
| **Math/logic reasoning** | DeepSeek-R1-Distill-32B | Q4_K_M | ~15–18 t/s | Yes — pipeline split | ⬆ UPGRADE | R1-distilled chain-of-thought. Alt: EXAONE 4.0 32B (AIME 85.3%) |
| **STEM analysis** | DeepSeek-R1-Distill-32B | Q4_K_M | ~15–18 t/s | Yes — pipeline split | ⬆ UPGRADE | Better scientific reasoning fidelity at 32B |
| **Algorithm exploration** | Qwen3-32B (thinking mode) | Q4_K_M | ~18 t/s | Yes — pipeline split | ⬆ UPGRADE | Higher-quality code + reasoning combination |

**Tier 4 summary:** All 3 roles upgrade at 32GB. Speed is slow (~15–18 t/s) because these are dense models on pipeline split, but reasoning chains are background tasks where quality matters far more than latency. These roles are impossible on a single 16GB card — the models simply don't fit.

### 4.5 Tier 5 — Frontier Roles (10 roles)

The hardest agent tasks: orchestrating complex multi-agent workflows, novel architecture decisions, legal/medical/financial analysis. These roles benefit from 32GB upgrades but cloud APIs (Claude, GPT-4.1, Gemini 2.5 Pro) still outperform local models for the most demanding instances.

| Role | Recommended Model | Quant | Speed | Split? | Cloud still better? | Status |
|------|------------------|-------|-------|--------|---------------------|--------|
| **Orchestrator/manager** | Qwen3-30B-A3B | Q4_K_M | ~101 t/s | Yes — pipeline split | Yes, for complex orchestration | ⬆ UPGRADE |
| **Software architect** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, for novel architectures | ⬆ UPGRADE |
| **Complex debugger** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | Yes, for deep debugging | ⬆ UPGRADE |
| **Legal document review** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, strongly | ⬆ UPGRADE |
| **Medical/health analysis** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, always verify | ⬆ UPGRADE |
| **Financial analysis** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, for complex analysis | ⬆ UPGRADE |
| **Security analyst** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | Yes, for novel threats | ⬆ UPGRADE |
| **SRE/incident response** | Qwen3-Coder-30B-A3.3B | Q4_K_M | ~100 t/s | Yes — pipeline split | Partially | ⬆ UPGRADE |
| **Book writing** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, for style/coherence | ⬆ UPGRADE |
| **Compliance/regulatory** | Qwen3-32B | Q5_K_M | ~18 t/s | Yes — pipeline split | Yes, strongly | ⬆ UPGRADE |

**Tier 5 summary:** All 10 roles upgrade at 32GB. MoE models cover 4 roles (orchestrator, debugger, security, SRE) at ~100 t/s. Dense Qwen3-32B covers 6 roles at ~18 t/s — the quality gain from Q5_K_M is essential for these precision-critical tasks. No role transitions from "requires cloud API" to "fully solved locally" — the upgrade is incremental, not transformational.

### 4.6 Complete Summary — All Roles by Tier

| Tier | Total Roles | Upgrade at 32GB | Stay Same | Need Pipeline Split | Best Architecture |
|------|------------|----------------|-----------|--------------------|--------------------|
| **Tier 1** (simple) | 8 | 0 | 8 | 0 | Single GPU (8B/14B) |
| **Tier 2** (moderate) | 25 | 12 | 13 | 12 | Mixed: single GPU + split |
| **Tier 3** (complex) | 11 | 11 | 0 | 11 | Pipeline split (MoE preferred) |
| **Tier 4** (reasoning) | 3 | 3 | 0 | 3 | Pipeline split (dense required) |
| **Tier 5** (frontier) | 10 | 10 | 0 | 10 | Pipeline split (mixed MoE + dense) |
| **Total** | **57** | **36** | **21** | **36** | — |

**Key takeaway:** 36 of 57 roles (63%) benefit from the 32GB pipeline-split tier. All Tier 3–5 roles upgrade. The remaining 21 roles (all Tier 1 and half of Tier 2) run fine on single-GPU 8B/14B models and don't need splitting at all.

### 4.7 Model Usage Across All Roles

| Model | Roles Served | Tier Coverage | Why It's Used |
|-------|-------------|--------------|---------------|
| **Qwen3-30B-A3B** Q4_K_M (MoE) | 12 roles | T2–T5 | Primary workhorse. 101 t/s MoE speed + 131K context. Orchestrator, research, planning, RAG, memory, meetings, market research, synthesis |
| **Qwen3-Coder-30B-A3.3B** Q4_K_M (MoE) | 8 roles | T3–T5 | Coding specialist. ~100 t/s MoE speed. Code gen, review, QA, prototyping, DevOps, debugging, security, SRE |
| **Qwen3-32B** Q5_K_M (dense) | 12 roles | T2–T5 | Quality-critical tasks. ~18 t/s (slow). Writing, editing, fact-checking, critic, legal, medical, financial, compliance, book writing, architecture, landing pages |
| **DeepSeek-R1-Distill-32B** Q4_K_M (dense) | 2 roles | T4 | Reasoning specialist. ~15–18 t/s. Math/logic, STEM analysis |
| **Gemma 3 27B** Q6_K/Q8_0 (dense) | 3 roles | T2 | Multimodal + docs. ~15–20 t/s. Image description (Q8_0), document summarization (Q6_K), project summary |
| **Qwen3-14B** Q4_K_M/Q6_K | 12 roles | T1–T2 | Mid-range single GPU. ~100–124 t/s. Email, social media, customer support, finance, SEO, travel, recipes, news |
| **Qwen3-8B** Q4_K_M | 8 roles | T1–T2 | Fast single GPU. ~186 t/s. Router, validator, notifications, sentiment, scheduling, scraping, home automation, shopping |
| **Qwen3-0.6B** Q8_0 | 1 role | T1 | Heartbeat/health monitor. ~500+ t/s. Ultra-lightweight |
| **GPT-oss-20B** MXFP4 (MoE) | Backup for multiple | T2–T3 | Fits single 16GB card. Alternative workhorse when pipeline split not desired |

---

## 5. Deployment Architectures for Multi-Agent Pipelines

### 5.1 Architecture A — Single Large Model (Split Across GPUs)

Both GPUs cooperate to run one 27–36B model via pipeline parallelism. Swap models between tasks.

**Best for:** Workloads dominated by a single role (e.g., heavy coding sessions using Qwen3-Coder-30B all day).

**Model loading strategy:**
1. Load Qwen3-30B-A3B as default workhorse (covers orchestrator, research, planning)
2. Swap to Qwen3-Coder-30B for coding sessions
3. Swap to R1-Distill-32B for deep reasoning tasks
4. Swap to Gemma 3 27B Q8_0 for vision tasks

**Swap time:** ~5–15 seconds per model load depending on storage speed (NVMe recommended).

### 5.2 Architecture B — Dual Independent Models (One Per GPU)

Each GPU runs a separate model simultaneously. Zero swap latency between roles.

**Example configurations:**

| GPU 0 (16GB) | GPU 1 (16GB) | Use Case |
|-------------|-------------|----------|
| Qwen3-8B Q4_K_M (~5.5 GB) | GPT-oss-20B MXFP4 (~13.7 GB) | Fast router + specialist workhorse |
| Qwen3-14B Q4_K_M (~9 GB) | Gemma 3 27B QAT Q4_0 (~15.6 GB) | General assistant + vision/multilingual |
| Qwen3-Coder-8B Q4_K_M (~5.5 GB) | Qwen3-14B Q5_K_M (~10.5 GB) | Code specialist + general reasoning |
| Qwen3-0.6B draft (~0.5 GB) | Qwen3-14B Q4_K_M (~9 GB) | Speculative decoding (1.5–2× throughput) |

**Best for:** Multi-agent pipelines where different subagents need different models and model swap latency is unacceptable. The orchestrator can route to whichever GPU hosts the appropriate model.

### 5.3 Architecture C — Hybrid (Split + Small Sidecar)

Split a 20–25GB model across both GPUs, leaving room for a small sidecar model on one GPU.

**Example:** Qwen3-30B-A3B Q4_K_M (~18.6 GB split) + Qwen3-0.6B (~0.5 GB on GPU 0) for speculative decoding. The draft model proposes tokens, the split model verifies — potential 1.5–2× throughput improvement.

### 5.4 Recommended Architecture by Workload

| Workload Pattern | Best Architecture | Why |
|-----------------|-------------------|-----|
| Single-role focus (coding all day) | A — Single split model | Maximum model quality, no switching overhead |
| Multi-agent pipeline (OpenClaw full stack) | B — Dual independent | Zero swap latency, parallel subagent serving |
| High-throughput single model | C — Hybrid with speculative decoding | 1.5–2× throughput boost |
| Mixed workloads with vision | A — Swap between Qwen3-30B-A3B and Gemma 3 27B | Different models for different tasks |

---

## 6. Model Performance by Agent Role — Detailed Analysis

### 6.1 Speed Tiers for Multi-GPU Deployment

Models fall into distinct speed tiers that determine their suitability for interactive vs background agent roles:

**Tier 1 — Fast Interactive (~80–110 t/s on multi-GPU):**
- Qwen3-30B-A3B Q4_K_M: ~101 t/s
- Qwen3-Coder-30B-A3.3B Q4_K_M: ~100 t/s (est.)
- Nemotron 3 Nano 30B: ~60 t/s (est.)

These models are suitable for **interactive agent roles** where the user is waiting: orchestrator, code generation, planning, real-time chat.

**Tier 2 — Moderate (~20–35 t/s on multi-GPU):**
- Gemma 3 27B QAT Q4_0: ~25 t/s (est.)
- Gemma 3 27B Q6_K: ~20 t/s (est.)

Suitable for **semi-interactive roles** with moderate latency tolerance: document summary, multilingual processing, research analysis.

**Tier 3 — Slow (~15–18 t/s on multi-GPU):**
- Qwen3-32B Q4_K_M/Q5_K_M: ~18 t/s
- DeepSeek-R1-Distill-32B Q4_K_M: ~15–18 t/s (est.)
- EXAONE 4.0 32B Q4_K_M: ~18 t/s (est.)
- Seed-OSS-36B Q4_K_M: ~15 t/s (est.)
- Gemma 3 27B Q8_0: ~15 t/s (est.)

Suitable for **background agent roles** where quality trumps speed: deep reasoning, creative writing, vision tasks, specialized analysis.

### 6.2 Context Window Analysis by Role

Context length determines how much information an agent can process in a single pass. This is critical for OpenClaw roles handling large inputs.

| Agent Role | Context Needed | Best Model | Available Context |
|-----------|---------------|-----------|-------------------|
| Research (full documents) | 32K–128K | Qwen3-30B-A3B Q4_K_M | **131K** ✅ |
| Code Generation (large repos) | 16K–64K | Qwen3-Coder-30B Q4_K_M | **131K** ✅ |
| Orchestrator (task state) | 8K–32K | Qwen3-30B-A3B Q4_K_M | **131K** ✅ |
| Document Summary | 16K–48K | Gemma 3 27B Q6_K | **20–40K** ✅ |
| Deep Reasoning | 4K–16K | R1-Distill-32B Q4_K_M | **8–16K** ✅ |
| Creative Writing | 4K–16K | Qwen3-32B Q5_K_M | **16–32K** ✅ |
| Vision (image + text) | 2K–8K | Gemma 3 27B Q8_0 | **4–8K** ✅ |
| Planning | 8K–32K | Qwen3-30B-A3B Q4_K_M | **131K** ✅ |

**Key observation:** Qwen3-30B-A3B's 131K context at MoE speed is a standout advantage. No dense model in this tier comes close to that context-to-speed ratio.

### 6.3 Quality Benchmarks by Domain

Relative model quality rankings for each agent domain (based on public benchmark data and community evaluations):

**Coding (HumanEval, MBPP, LiveCodeBench):**
1. Qwen3-Coder-30B-A3.3B — purpose-built, top coding MoE
2. Qwen3-32B Q5_K_M — strong all-rounder, benefits from Q5 quant
3. DeepSeek-R1-Distill-32B — good at complex algorithmic reasoning
4. Seed-OSS-36B — competitive, benefits from larger parameter count

**Reasoning (MATH, GPQA, ARC-Challenge):**
1. DeepSeek-R1-Distill-32B — distilled from R1, chain-of-thought specialist
2. Qwen3-32B — strong general reasoning
3. Seed-OSS-36B — competitive at 36B scale
4. Qwen3-30B-A3B — good but MoE routing adds slight overhead for deep chains

**General Language (MMLU, HellaSwag, WinoGrande):**
1. Qwen3-32B — best general language at this tier
2. EXAONE 4.0 32B — competitive, strong multilingual
3. Gemma 3 27B — excellent comprehension
4. Seed-OSS-36B — broad capability

**Vision/Multimodal (MMMU, DocVQA, ChartQA):**
1. Gemma 3 27B Q8_0 — near-lossless vision, best quality
2. Gemma 3 27B Q6_K — very close to Q8, more context room
3. Gemma 3 27B QAT Q4_0 — acceptable for basic visual tasks

**Multilingual (Flores, multilingual MMLU):**
1. Gemma 3 27B — 100+ languages
2. EXAONE 4.0 32B — excellent CJK languages
3. Qwen3-32B — strong Chinese/English bilingual

---

## 7. Models That Don't Fit the 32GB Tier

For reference, these models from adjacent tiers cannot be deployed at 32GB:

| Model | Total Size (Q4_K_M) | Minimum VRAM | Notes |
|-------|---------------------|-------------|-------|
| Llama 4 Scout (109B MoE) | ~65 GB | 4× 16GB (64GB) | MoE but too many total params |
| Llama 3.3 70B (dense) | ~40 GB | 48GB+ | Needs 2× 24GB or single 48GB |
| Qwen3-235B-A22B (MoE) | ~85.7 GB (Q2_K) | 6+ GPUs | Datacenter scale |
| GPT-oss-120B (MoE) | ~59 GB | 4× 16GB (64GB) | Large MoE |
| DeepSeek-R1 (671B MoE) | ~140 GB+ | Datacenter | Multi-node deployment |

---

## 8. Conclusion & Recommended OpenClaw Model Stack

### 8.1 Primary Recommendation

The optimal model stack for OpenClaw at the 32GB tier covers all 57 agent roles across 5 tiers. MoE models handle speed-sensitive roles; dense models serve quality-critical tasks:

| Priority | Model | Roles Covered | Key Advantage |
|----------|-------|--------------|---------------|
| **Primary workhorse** | Qwen3-30B-A3B Q4_K_M | 12 roles (T2–T5): orchestrator, research, planning, RAG, memory, meetings, market research, synthesis | 101 t/s + 131K context |
| **Coding specialist** | Qwen3-Coder-30B-A3.3B Q4_K_M | 8 roles (T3–T5): code gen, review, QA, prototyping, DevOps, debugging, security, SRE | Purpose-built MoE coder, ~100 t/s |
| **Quality writer** | Qwen3-32B Q5_K_M | 12 roles (T2–T5): writing, editing, fact-checking, legal, medical, financial, compliance, architecture, book writing | Best language quality at tier |
| **Deep reasoning** | DeepSeek-R1-Distill-32B Q4_K_M | 2 roles (T4): math/logic, STEM analysis | R1-distilled chain-of-thought |
| **Multimodal + docs** | Gemma 3 27B Q6_K/Q8_0 | 3 roles (T2): image description, document summary, project summary | Near-lossless vision at Q8_0 |
| **Mid-range general** | Qwen3-14B Q4_K_M/Q6_K | 12 roles (T1–T2): email, social media, customer support, finance, SEO, travel | Fast single-GPU, no split needed |
| **Fast lightweight** | Qwen3-8B Q4_K_M | 8 roles (T1): router, validator, notifications, sentiment, scheduling, scraping | 186 t/s, single GPU |

### 8.2 Core Insight: MoE-First Strategy

The single most important principle for OpenClaw model selection at 32GB in multi-GPU configurations:

- **Qwen3-30B-A3B (MoE):** 92% speed retention when split across GPUs
- **Qwen3-32B (dense):** 30% speed retention when split across GPUs

This 3× difference in speed retention means the optimal strategy is **Qwen3-30B-A3B as primary workhorse** for most agent roles, reserving dense models only for roles where their specific capabilities are irreplaceable.

### 8.3 Minimum Viable Stack

For the simplest effective OpenClaw deployment at 32GB:

1. **Qwen3-30B-A3B Q4_K_M** — covers orchestrator, planning, research, general tasks, and serviceable coding (20+ roles across T2–T5)
2. **Gemma 3 27B Q6_K** — covers vision, multilingual, and document processing (3+ roles)
3. **Qwen3-8B Q4_K_M** on single GPU — handles all Tier 1 simple roles simultaneously (8 roles)
4. Swap to Qwen3-32B Q5_K_M or R1-Distill-32B when quality-critical writing or deep reasoning is needed

This three-model rotation covers all 57 roles. Load Qwen3-30B-A3B as the default split model and keep Qwen3-8B on one GPU as a fast router — the MoE workhorse handles the majority of tasks at 101 t/s.
