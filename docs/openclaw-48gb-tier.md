# OpenClaw Model Selection — 48GB VRAM Tier

**Part 5: Native 48GB Card & 3× RTX 5060 Ti 16GB Pipeline Split**

> **Critical constraint:** Every model listed as viable must load weights AND KV cache 100% in VRAM. No CPU offloading, no partial offloading, no hybrid RAM modes. These configurations must work even on PCIe 2.0 where any offloading would kill usability.

---

## Executive Summary

Forty-eight gigabytes of VRAM crosses a critical threshold: the 70-billion-parameter class. Llama 3.3 70B, DeepSeek-R1-Distill-70B, and Llama-Nemotron-Super-49B all load fully within this budget, bringing BFCL tool-calling scores of 77%, AIME 2024 reasoning at 70%, and HumanEval code generation at 88% — numbers no 32B model reaches. Every 27–36B model from the 32GB tier now runs at near-lossless Q8_0 quantization with expanded context windows.

Does 48GB unlock genuinely new capabilities for OpenClaw? **Yes — unambiguously.** But with a sharp caveat: the 3×16GB pipeline-split path delivers 70B models at a painful 7–10 t/s, making the native single-card path strongly preferable for interactive agent work.

This analysis covers two deployment paths:
- **(a) Native 48GB GPU** (RTX A6000, RTX 6000 Ada)
- **(b) 3× RTX 5060 Ti 16GB** pooling 48GB via pipeline parallelism

Both paths access the same model roster but at dramatically different speeds.

---

## 1. New Models That Unlock at 48GB

The jump from 32GB to 48GB adds a small but transformative set of models. Only models that fit weights + usable KV cache entirely in VRAM are listed.

### 1.1 Complete 48GB Model Roster

| Model | Params | Architecture | Quant | Weight Size | KV Room | Usable Context | Fits 48GB? |
|-------|--------|-------------|-------|-------------|---------|---------------|------------|
| **Llama 3.3 70B** | 70B | Dense | Q4_K_M | 42.5 GB | 5.5 GB | 8–16K | ✅ Yes |
| **DeepSeek-R1-Distill-Llama-70B** | 70B | Dense | Q4_K_M | 42.5 GB | 5.5 GB | 8–16K | ✅ Yes |
| **Nemotron-Super-49B v1.5** | 49B | Dense (pruned) | Q4_K_M | 30.2 GB | 17.8 GB | 32–64K | ✅ Yes |
| **Nemotron-Super-49B v1.5** | 49B | Dense (pruned) | Q6_K | 40.9 GB | 7.1 GB | 8–16K | ✅ Yes |

**Minimum quantization: Q4_K_M.** No sub-Q4 quantizations are considered viable — quality degradation at Q3 and below is unacceptable for production agent work. Q5_K_M for 70B models (49.95 GB) does NOT fit. The only usable quant for true 70B models at 48GB is Q4_K_M.

### 1.2 Model Details

#### Llama 3.3 70B Instruct — the headline unlock

Meta's 70B dense model is the single most important addition. At Q4_K_M (42.5 GB), it loads with ~5.5 GB remaining for KV cache — enough for 8–16K context with Q8 KV quantization. Context is tight at this tier, but 8–16K is sufficient for most agentic tasks (tool calls, code generation, orchestration). For roles needing longer context, use Nemotron-Super-49B Q4_K_M (30.2 GB, 32–64K context) instead.

Benchmarks position this well above the 32B class: MMLU 86.0%, HumanEval 88.4%, MATH 77.0%, BFCL v2 77.3% (tool calling), IFEval 92.1%. Native function calling via Llama 3 JSON schema format. The 77.3% BFCL v2 score significantly exceeds any 32B model for agentic tool invocation.

#### DeepSeek-R1-Distill-Llama-70B — reasoning transformed

Identical Llama 3.3 70B architecture (42.5 GB at Q4_K_M), fine-tuned with reasoning chains from the full DeepSeek-R1 671B. Dramatic reasoning improvement: AIME 2024 70.0% (vs ~50% for 32B distill, ~20% for base Llama 3.3), MATH-500 94.5%, GPQA Diamond 65.2%.

Does NOT support native tool calling. No BFCL scores. This is a pure reasoning engine, not a general-purpose agent model. Pair with a tool-calling model for OpenClaw roles requiring function execution.

#### Nemotron-Super-49B v1.5 — the unexpected sweet spot

NVIDIA's NAS-optimized derivative of Llama 3.3 70B, pruned to ~49B parameters with skip-attention layers and variable FFN widths. Remarkable VRAM efficiency: Q4_K_M at 30.2 GB leaves 17.8 GB for KV cache (32–64K context), and Q6_K at 40.9 GB still leaves 7.1 GB. Q8_0 at 53 GB does NOT fit.

Outperforms many 70B models on reasoning benchmarks thanks to distillation from larger teacher models. Features reasoning ON/OFF toggle via system prompt. Explicitly supports agentic tasks including RAG and tool calling, with NVIDIA providing a custom vLLM tool-call parser.

**For most OpenClaw agent roles, Nemotron-Super-49B at Q4_K_M is the optimal 48GB model** — it provides 70B-class quality with room for 32–64K context.

#### Qwen2.5-72B Instruct — does NOT fit at minimum Q4

Qwen's 72.7B dense model at Q4_K_M reaches 47.4 GB — leaves only 0.6 GB for KV cache, which is effectively unusable. The 152K vocabulary inflates weight size beyond other 70B models. Only viable at Q3_K_M (~39 GB), which violates the minimum Q4 quantization constraint. **Not recommended. Listed in the "doesn't fit" table.**

### 1.3 Key Benchmarks — 48GB Models vs 32GB Models

| Benchmark | Qwen3-32B (32GB tier) | Llama 3.3 70B | R1-Distill-70B | Nemotron-49B | Jump |
|-----------|----------------------|---------------|----------------|-------------|------|
| **MMLU** | ~81% | **86.0%** | ~83% | ~84% | +3–5% |
| **HumanEval** | ~78% | **88.4%** | ~82% | ~85% | +7–10% |
| **MATH** | ~72% | **77.0%** | **94.5%** | ~78% | +5–22% |
| **BFCL v2** (tool calling) | ~65% | **77.3%** | N/A | ~74% | +9–12% |
| **IFEval** | ~85% | **92.1%** | ~88% | ~90% | +5–7% |
| **AIME 2024** | ~35% | ~20% | **70.0%** | ~45% | +10–35% |
| **GPQA Diamond** | ~50% | ~53% | **65.2%** | ~55% | +5–15% |

---

## 2. 32GB-Tier Models That Improve at 48GB

The 48GB budget transforms existing 27–36B models from "adequate at Q4" to "near-lossless at Q8_0." Quantization quality follows a well-established curve: Q4_K_M adds +0.054 perplexity over FP16, Q6_K adds +0.012, Q8_0 adds +0.001. The jump from Q4 to Q8_0 represents ~1% perplexity improvement that blind evaluations consistently detect at 13B+ scales, particularly in code generation accuracy, reasoning chain stability, and instruction-following precision.

| Model | 32GB Tier (quant / ctx) | 48GB Tier (quant / ctx) | What improves |
|-------|------------------------|------------------------|---------------|
| **Qwen3-32B** | Q4_K_M (19.8 GB) / ~42K | Q8_0 (34.8 GB) / 48–96K | Near-lossless + 2× context |
| **DS-R1-Distill-Qwen-32B** | Q4_K_M (20.1 GB) / ~42K | Q8_0 (34.8 GB) / 48–96K | Critical for reasoning chains |
| **Gemma 3 27B** | Q8_0 (28.7 GB) / 4–8K | Q8_0 (28.7 GB) / **full 128K** | 19 GB free; 5:1 local-to-global attention = tiny KV |
| **EXAONE 4.0 32B** | Q4_K_M (19.3 GB) / ~32K | Q8_0 (34.0 GB) / 32–64K | Quality + context |
| **Seed-OSS-36B** | Q4_K_M (21.8 GB) / ~16K | Q6_K (29.7 GB) / 32–64K | Q8_0 tight at 38.4 GB; Q6_K optimal |
| **Qwen3-30B-A3B** (MoE) | Q4_K_M (18.6 GB) / ~128K | Q8_0 (32.5 GB) / 160–320K | Near-lossless + massive context |
| **Qwen3-Coder-30B** (MoE) | Q4_K_M (18.6 GB) / ~128K | Q8_0 (32.5 GB) / 160–320K | Near-lossless coding quality |
| **Nemotron 3 Nano 30B** | Q4_K_M (24.5 GB) / 128K+ | Q8_0 (33.6 GB) / 128K+ | Quality upgrade; tiny KV needs (6 of 52 layers use attention) |
| **GPT-oss-20B** (MoE) | MXFP4 (13.7 GB) | MXFP4 (13.7 GB) + massive ctx room | No quant change needed; more KV headroom |

**Gemma 3 27B** deserves special mention. Its 5:1 local-to-global attention ratio means only ~10 of 62 layers maintain full-context KV cache, reducing per-token cost to ~15–20% of standard transformers. At Q8_0 (28.7 GB) on 48GB, it runs its full **128K native context** comfortably with 19 GB to spare.

---

## 3. Pipeline Parallelism — How 3-Way Splitting Works

### 3.1 The Problem: 70B Models Need 3 Cards

At Q4_K_M, Llama 3.3 70B requires 42.5 GB. Two 16GB cards provide 32GB — not enough. Three 16GB cards provide 48GB — the minimum. Pipeline parallelism distributes layers sequentially: GPU 0 processes layers 0–26, GPU 1 handles 27–53, GPU 2 finishes 54–80.

Same principle as 2-way split: only one GPU computes at a time ("pipeline bubble"). Adding a third GPU adds VRAM capacity but does NOT add speed. In fact, the extra pipeline hop slightly reduces throughput vs 2-way.

### 3.2 MoE vs Dense on 3-Way Split

MoE models don't benefit from 3 GPUs — they already fit on 2 cards (18.6 GB). Adding a third card for an MoE model is wasteful; it adds a pipeline stage that only slows things down.

Dense 70B models REQUIRE 3 cards but suffer the full pipeline penalty: each token must traverse all 3 GPUs sequentially. Expected speed for Llama 3.3 70B Q4_K_M on 3× RTX 5060 Ti: **~7–10 t/s**.

### 3.3 Per-Model Split Behavior on 3× 16GB

| Model | Weight Size | Cards Needed | Speed (3× 5060 Ti) | Speed Retention |
|-------|-----------|-------------|--------------------|--------------------|
| **Llama 3.3 70B** Q4_K_M | 42.5 GB | 3 | ~7–10 t/s | ~25% (dense, 3-way) |
| **R1-Distill-70B** Q4_K_M | 42.5 GB | 3 | ~7–10 t/s | ~25% (dense, 3-way) |
| **Nemotron-Super-49B** Q4_K_M | 30.2 GB | 2 | ~12–15 t/s | ~30% (dense, 2-way) |
| **Qwen3-32B** Q8_0 | 34.8 GB | 3 | ~10–14 t/s | ~28% (dense, 3-way) |
| **DS-R1-Distill-32B** Q8_0 | 34.8 GB | 3 | ~10–14 t/s | ~28% (dense, 3-way) |
| **Qwen3-30B-A3B** Q8_0 | 32.5 GB | 3 | ~90–95 t/s | ~85% (MoE — but 2 cards was fine) |
| **Gemma 3 27B** Q8_0 | 28.7 GB | 2 | ~15–20 t/s | ~30% (dense, 2-way) |
| **Seed-OSS-36B** Q6_K | 29.7 GB | 2 | ~15–18 t/s | ~30% (dense, 2-way) |

**Key insight for 3× 16GB:** The third card's biggest value is enabling 70B models and running 32B at Q8_0 — NOT speeding up MoE models that already fit on 2 cards.

---

## 4. Inference Tools for 3-Way Pipeline Split

Every major framework supports 3-GPU pipeline parallelism. Tensor parallelism with 3 GPUs fails for most models (attention head counts not divisible by 3). **PP=3 is the universal 3-GPU strategy.**

### 4.1 Tool Compatibility Matrix

| Tool | 3-GPU Support | Mode | Configuration | Format |
|------|--------------|------|---------------|--------|
| **llama.cpp** | ✅ Full | Pipeline (layer split) | `-sm layer -ts 0.33,0.33,0.34` | GGUF |
| **ik_llama.cpp** (fork) | ✅ Full | True tensor parallel | `-sm graph` (3–4× faster than layer split) | GGUF |
| **Ollama** | ✅ Auto | Pipeline (auto-splits) | No config needed; detects 3 GPUs | GGUF |
| **vLLM** | ✅ PP only | Pipeline parallel | `--pipeline-parallel-size 3` | HF/AWQ/GPTQ/FP8 |
| **ExLlamaV2** | ✅ Full | Layer split + TP | `--gpu_split 16,16,16` or `-gs auto` | EXL2/GPTQ |
| **ExLlamaV3** | ✅ Full | TP + expert parallel | `--gpu_split auto` | EXL3/HF |
| **SGLang** | ✅ PP only | Pipeline parallel | `--pp-size 3` | HF/AWQ/GPTQ/FP8 |
| **TensorRT-LLM** | ✅ Full | PP and TP | `--pp_size 3` (complex build process) | HF/FP8/INT4 |
| **KoboldCpp** | ✅ Full | Layer split | `--tensor_split 3,3,3 --gpulayers 999` | GGUF |
| **TabbyAPI** | ✅ Full | Via ExLlamaV2/V3 | `gpu_split: [16, 16, 16]` in config.yml | EXL2/EXL3 |

### 4.2 ik_llama.cpp — The 3-GPU Breakthrough

The ik_llama.cpp fork (January 2026) implements true tensor parallelism at the GGML graph level using NCCL for topology-aware GPU communication, keeping all GPUs at 100% utilization simultaneously. Community reports claim 3–4× performance gains over standard llama.cpp layer split mode. This fork is not yet merged into mainline llama.cpp but is the recommended tool for anyone running 3 consumer GPUs who needs maximum speed from GGUF models.

With ik_llama.cpp `-sm graph`, estimated 70B Q4_K_M speeds on 3× RTX 5060 Ti could reach **15–25 t/s** — a dramatic improvement over the 7–10 t/s from standard pipeline split. However, real-world 3-card consumer benchmarks with this fork are still scarce.

### 4.3 Tool Recommendations by Use Case

| Use Case | Recommended Tool | Why |
|----------|-----------------|-----|
| Quick testing | Ollama | Auto-detects 3 GPUs, zero config |
| Daily deployment (GGUF) | ik_llama.cpp server | Fastest 3-GPU performance via graph split |
| Daily deployment (GGUF, stable) | llama.cpp server | Mature, well-tested 3-GPU pipeline |
| Production serving | vLLM with PP=3 | OpenAI-compatible API, continuous batching |
| Maximum quant quality | ExLlamaV3 via TabbyAPI | Best quant quality per bit (EXL3) |
| MoE-heavy workloads | SGLang | Expert parallelism for MoE models |

---

## 5. Speed Comparison: Native 48GB vs 3×16GB

### 5.1 Llama 3.3 70B Q4_K_M Speed

| Deployment | Token Generation | Prompt Processing | Notes |
|-----------|-----------------|-------------------|-------|
| **RTX A6000** (native 48GB) | **~14.6 t/s** | ~467 t/s | 768 GB/s bandwidth, single bus |
| **RTX 6000 Ada** (native 48GB) | **~18.4 t/s** | ~547 t/s | 960 GB/s bandwidth, single bus |
| **3× RTX 5060 Ti** (48GB pipeline) | **~7–10 t/s** | ~200–300 t/s | Pipeline overhead, 3 hops |
| **3× RTX 5060 Ti + ik_llama** (graph) | **~15–25 t/s est.** | ~400+ t/s | True TP, still emerging |
| 2× RTX 4090 (48GB reference) | ~19.1 t/s | ~905 t/s | High-bandwidth reference |
| A100 80GB PCIe (datacenter reference) | ~22.1 t/s | ~727 t/s | Datacenter reference |

**Pipeline parallelism provides zero token-generation speed improvement from additional GPUs.** Benchmark data is unambiguous: 2× RTX 4090 achieves 19.06 t/s on 70B Q4_K_M, 4× RTX 4090 achieves 18.83 t/s, 8× RTX 4090 achieves 18.76 t/s. Adding GPUs pools VRAM but does not accelerate single-request inference because layers execute sequentially.

### 5.2 Which Path for Which Workload

| Workload Pattern | Best Path | Why |
|-----------------|-----------|-----|
| Single orchestrator, frontier tasks | Native 48GB | 70B at 14–18 t/s, simple setup |
| Multiple concurrent agent roles | 3×16GB | Split models across cards, serve in parallel |
| Background batch processing | Either | 3×16GB cost-effective; native faster |
| Real-time interactive coding | Native 48GB | Speed matters for developer experience |
| Maximum model quality | Native 48GB | Fewer pipeline hops, fewer failure modes |
| Budget-constrained multi-model setup | 3×16GB | ~$1,300 vs $3,500–5,000; more flexible |

---

## 6. Complete Agent Role Mapping — All 57 Roles at 48GB

### 6.1 Tier 1 — Simple Roles (8 roles) — No Upgrades

Every Tier 1 role was already well-served by 8–14B models at 32GB. The extra VRAM is wasted on these tasks.

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

### 6.2 Tier 2 — Moderate Roles (25 roles) — 6 Upgrades

| Role | 48GB Model | Quant | Upgrade? | Why |
|------|-----------|-------|----------|-----|
| **Research/web search** | **Nemotron-Super-49B** | Q4_K_M | ⬆ YES | Broader knowledge, better synthesis, 32–64K ctx |
| **Content writing** | **Nemotron-Super-49B** | Q4_K_M | ⬆ YES | Noticeably better prose at 49B |
| **Editing** | **Qwen3-32B** | Q8_0 | ⬆ YES | Near-lossless catches subtle errors |
| Email drafting | Qwen3-32B | Q4_K_M | ➡ No | 32B Q4 already excellent |
| **Document summarization** | **Qwen3-32B** | Q8_0 | ⬆ YES | Q8_0 + 96K context = longer docs |
| Meeting notes | Qwen3-30B-A3B | Q8_0 | ➡ Marginal | Q8_0 quality improvement, same model |
| Social media | Qwen3-14B | Q4_K_M | ➡ No | Short-form, 14B sufficient |
| News aggregation | Qwen3-14B | Q4_K_M | ➡ No | Classification + summary |
| Shopping/price comparison | Qwen3-8B | Q4_K_M | ➡ No | Structured extraction |
| Memory/knowledge mgmt | Qwen3-30B-A3B | Q8_0 | ➡ Marginal | Q8_0 + extended context |
| **RAG/retrieval** | **Qwen3-30B-A3B** | Q8_0 | ⬆ YES | 160K+ context at Q8_0 = massive RAG windows |
| **Data analysis** | **Nemotron-Super-49B** | Q4_K_M | ⬆ YES | Complex data patterns need 49B+ reasoning |
| Website scraping | Qwen3-8B | Q4_K_M | ➡ No | Parsing, not reasoning |
| Image description | Gemma 3 27B | Q8_0 | ➡ Marginal | Q8_0 was available at 32GB; now with full 128K ctx |
| Customer support | Qwen3-32B | Q4_K_M | ➡ No | 32B sufficient |
| Lead scoring | Qwen3-14B | Q4_K_M | ➡ No | Classification task |
| Project summarization | Qwen3-32B | Q8_0 | ➡ Marginal | Quality bump |
| Transaction/approval | Qwen3-8B | Q4_K_M | ➡ No | Rule-heavy |
| Home automation | Qwen3-8B | Q4_K_M | ➡ No | Command parsing |
| Fitness tracking | Qwen3-8B | Q4_K_M | ➡ No | Data logging |
| Recipe/cooking | Qwen3-14B | Q4_K_M | ➡ No | Knowledge retrieval |
| Personal finance | Qwen3-14B | Q4_K_M | ➡ No | 14B handles well |
| SEO optimization | Qwen3-14B | Q4_K_M | ➡ No | Content analysis |
| Landing page generation | Qwen3-32B | Q8_0 | ➡ Marginal | Q8_0 quality bump |
| Travel planning | Qwen3-14B | Q4_K_M | ➡ No | 14B sufficient |

### 6.3 Tier 3 — Complex Roles (11 roles) — 8 Upgrades

This tier sees the largest number of role upgrades. Llama 3.3 70B's HumanEval 88.4% is a substantial jump over any 32B model's ~75–80% for coding roles.

| Role | 48GB Model | Quant | Speed (native) | Speed (3×16GB) | Upgrade? |
|------|-----------|-------|---------------|----------------|----------|
| **Code generation** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — HumanEval 88.4% vs ~78% |
| **Code review** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — catches more subtle bugs |
| **QA/test writing** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — better edge-case generation |
| **Task planning** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — reasoning toggle improves planning |
| **Fact-checking** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — broader knowledge, better calibration |
| **Critic/review** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — nuanced evaluation at 49B |
| **Market research** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — synthesis across more data |
| **Synthesizer/aggregator** | **Qwen3-30B-A3B** | Q8_0 | ~34 t/s | ~101 t/s (2 cards) | ⬆ YES — Q8_0 + 160K ctx ideal for synthesis |
| Curriculum design | Qwen3-32B | Q8_0 | ~25 t/s | ~12 t/s | ➡ Marginal |
| **Prototype generation** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — full-stack code gen benefits from 70B |
| DevOps | Qwen3-32B | Q8_0 | ~25 t/s | ~12 t/s | ➡ Marginal |

**Note on synthesizer/aggregator:** Qwen3-30B-A3B at Q8_0 is preferred over a 70B model here. Its 160K+ context window at near-lossless quality makes it ideal for ingesting large volumes of text, and at ~101 t/s on 2 cards it's dramatically faster than any 70B model. Speed and context matter more than raw intelligence for aggregation tasks.

### 6.4 Tier 4 — Reasoning Roles (3 roles) — ALL Transformative Upgrades

The most dramatic improvement at 48GB. DeepSeek-R1-Distill-70B's AIME 2024 score of 70.0% represents a quantum leap over the 32B distill's ~50%.

| Role | 48GB Model | Quant | Speed (native) | Speed (3×16GB) | Upgrade? |
|------|-----------|-------|---------------|----------------|----------|
| **Math/logic reasoning** | **R1-Distill-70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆⬆ TRANSFORMATIVE — AIME 70% vs ~50% |
| **STEM analysis** | **R1-Distill-70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆⬆ TRANSFORMATIVE — GPQA Diamond 65.2% |
| **Algorithm exploration** | **R1-Distill-70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆⬆ TRANSFORMATIVE — CodeForces 1633 |

**Tool-calling workaround:** R1-Distill-70B lacks native tool calling. For roles requiring function execution, pair it with a tool-calling router: R1-Distill-70B generates the reasoning chain → Qwen3-8B or Llama 3.3 70B executes required function calls.

### 6.5 Tier 5 — Frontier Roles (10 roles) — 8 Upgrades

| Role | 48GB Model | Quant | Speed (native) | Speed (3×16GB) | Upgrade? |
|------|-----------|-------|---------------|----------------|----------|
| **Orchestrator/manager** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — BFCL 77.3% critical for delegation |
| **Software architect** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — broader system design knowledge |
| **Complex debugger** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — HumanEval 88.4%, multi-file reasoning |
| **Legal document review** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — reasoning toggle + long context |
| **Medical/health analysis** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — broader medical knowledge |
| **Financial analysis** | **Nemotron-Super-49B** | Q4_K_M | ~20 t/s | ~12 t/s | ⬆ YES — numerical reasoning improved |
| **Security analyst** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — broader threat knowledge |
| **SRE/incident response** | **Llama 3.3 70B** | Q4_K_M | ~16 t/s | ~8 t/s | ⬆ YES — tool calling + system knowledge |
| Book writing | Qwen3-30B-A3B | Q8_0 | ~34 t/s | ~101 t/s | ➡ No — 30B-A3B Q8_0 with 160K ctx optimal for long-form |
| Compliance/regulatory | Qwen3-32B | Q8_0 | ~25 t/s | ~12 t/s | ➡ Marginal |

**The orchestrator role is the most consequential upgrade.** Llama 3.3 70B's BFCL 77.3% tool-calling score and IFEval 92.1% instruction-following make it substantially more reliable at meta-cognitive coordination than any 32B model. A 32B orchestrator occasionally misroutes tasks or misparses tool outputs; a 70B orchestrator does so measurably less often.

### 6.6 Upgrade Summary — All 57 Roles

| Tier | Total Roles | Upgraded at 48GB | Unchanged | Key Driver |
|------|------------|-----------------|-----------|------------|
| Tier 1 (simple) | 8 | 0 | 8 | 8–14B already sufficient |
| Tier 2 (moderate) | 25 | 6 | 19 | Context windows + prose quality |
| Tier 3 (complex) | 11 | 8 | 3 | Code gen (HumanEval 88%) + tool calling |
| Tier 4 (reasoning) | 3 | 3 | 0 | R1-Distill-70B reasoning leap |
| Tier 5 (frontier) | 10 | 8 | 2 | 70B judgment + knowledge breadth |
| **Total** | **57** | **25** | **32** | |

### 6.7 Model Usage Across All Roles

| Model | Roles Served | Tier Coverage | Why It's Used |
|-------|-------------|--------------|---------------|
| **Llama 3.3 70B** Q4_K_M | 10 roles | T3–T5 | Highest tool-calling (BFCL 77.3%) + coding (HumanEval 88.4%). Orchestrator, coding, debugging, security, SRE, fact-checking |
| **DS-R1-Distill-70B** Q4_K_M | 3 roles | T4 | Reasoning specialist. AIME 70%, MATH-500 94.5%. Math, STEM, algorithms |
| **Nemotron-Super-49B** Q4_K_M | 8 roles | T2–T5 | Sweet spot: 70B-class quality, 32–64K context, tool calling + reasoning toggle. Research, planning, legal, medical, financial |
| **Qwen3-30B-A3B** Q8_0 (MoE) | 4 roles | T2–T5 | Speed king at 101 t/s (2 cards). 160K+ ctx at near-lossless. Synthesis, RAG, book writing, meetings |
| **Qwen3-32B** Q8_0 | 5 roles | T2–T3 | Near-lossless general quality. Editing, document summary, curriculum, DevOps, landing pages |
| **Qwen3-Coder-30B** Q8_0 (MoE) | Available as alt | T3 | Alternative to Llama 70B for coding when MoE speed preferred over 70B quality |
| **Qwen3-14B** Q4_K_M | 12 roles | T1–T2 | Mid-range single GPU. Email, social media, customer support, finance, SEO, travel |
| **Qwen3-8B** Q4_K_M | 8 roles | T1–T2 | Fast single GPU. Router, validator, notifications, sentiment, scheduling, scraping |
| **Qwen3-0.6B** Q8_0 | 1 role | T1 | Heartbeat/health monitor. Ultra-lightweight |

---

## 7. Deployment Architectures at 48GB

### 7.1 Native 48GB Card — Architectures

**Architecture A — Single 70B Model:**
Load Llama 3.3 70B Q4_K_M (42.5 GB) with 5.5 GB for KV cache. Swap to R1-Distill-70B for reasoning tasks. Swap time ~10–20 seconds for 70B models.

**Architecture B — 49B + Sidecar:**
Load Nemotron-Super-49B Q4_K_M (30.2 GB) + Qwen3-8B Q4_K_M (5.5 GB) simultaneously. Leaves ~12 GB for KV cache. Router on 8B model, workhorse on 49B. No swapping needed for most tasks.

**Architecture C — 32B at Q8_0 + Generous Context:**
Load Qwen3-32B Q8_0 (34.8 GB) with 13.2 GB for KV cache (48–96K context). Near-lossless quality with massive context for document-heavy workflows.

### 7.2 3× RTX 5060 Ti — Architectures

**Architecture A — 70B Across All 3 Cards:**
Llama 3.3 70B Q4_K_M split across 3 GPUs (~14.2 GB per card). Speed: ~7–10 t/s (pipeline) or ~15–25 t/s (ik_llama.cpp graph). Best for quality-critical background tasks.

**Architecture B — 32B on 2 Cards + Small Model on 3rd:**
Qwen3-32B Q8_0 (34.8 GB) split across GPU 0 + GPU 1, Qwen3-8B Q4_K_M on GPU 2 for routing/triage. Speed: ~10–14 t/s for 32B tasks, ~186 t/s for routing. Best for multi-agent pipelines.

**Architecture C — MoE Workhorse on 2 Cards + 14B on 3rd:**
Qwen3-30B-A3B Q8_0 (32.5 GB) split across GPU 0 + GPU 1 at ~101 t/s, Qwen3-14B Q4_K_M (9 GB) on GPU 2. Simultaneous fast MoE + mid-range general model. Best for high-throughput mixed workloads.

**Architecture D — Dual Independent + Small Router:**
GPU 0: Qwen3-14B Q6_K (~11 GB), GPU 1: Gemma 3 27B QAT Q4_0 (~15.6 GB), GPU 2: Qwen3-8B Q4_K_M (~5.5 GB) for routing. Three simultaneous models, zero swap latency. Best for diverse multi-agent pipelines.

### 7.3 Recommended Architecture by Workload

| Workload | Native 48GB | 3× RTX 5060 Ti |
|----------|------------|----------------|
| Heavy coding sessions | Arch A: Llama 70B all day | Arch A: 70B on 3 cards (slower) |
| Multi-agent pipeline | Arch B: 49B + 8B sidecar | Arch C: MoE on 2 + 14B on 3rd |
| Document-heavy analysis | Arch C: 32B Q8_0 with huge ctx | Arch B: 32B Q8_0 on 2 + router on 3rd |
| Deep reasoning tasks | Swap to R1-Distill-70B | Arch A: R1-Distill-70B on 3 cards |
| Mixed diverse roles | Arch B: 49B + 8B | Arch D: 3 independent models |

---

## 8. Models That Do NOT Fit at 48GB

**No CPU offloading. No partial fits. If it exceeds 48GB in weights, it's out.**

| Model | Params | Architecture | Smallest Viable Quant | Weight Size | Verdict |
|-------|--------|-------------|----------------------|-------------|---------|
| DeepSeek-R1 | 671B | MoE | Q2_K | ~250 GB | ❌ Datacenter only (8× H100) |
| DeepSeek-V3 / V3.2 | 685B | MoE | Q2_K | ~260 GB | ❌ Datacenter only |
| Qwen3-235B-A22B | 235B | MoE | Q2_K | ~85.7 GB | ❌ Needs 2× 48GB minimum |
| GPT-oss-120B | 117B | MoE | MXFP4 | ~59 GB | ❌ 11 GB over limit |
| Llama 4 Scout | 109B | MoE | Q4_K_M | ~65 GB | ❌ 17 GB over limit |
| Llama 4 Scout | 109B | MoE | IQ2_XXS | ~30–37 GB | ❌ Fits VRAM but quality destroyed at 2-bit — unusable |
| Llama 4 Maverick | 400B | MoE | IQ1_S | ~122 GB | ❌ Not remotely close |
| Command R+ | 104B | Dense | Q3_K_M | ~51 GB | ❌ 3 GB over limit |
| Mixtral 8x22B | 141B | MoE | Q4_K_M | ~80 GB | ❌ 32 GB over limit |
| Llama 3.3 70B | 70B | Dense | Q5_K_M | 49.95 GB | ❌ 2 GB over limit |
| Qwen2.5-72B | 72.7B | Dense | Q4_K_M | 47.4 GB | ❌ Fits weights but 0.6 GB KV = unusable |
| Nemotron-Super-49B | 49B | Dense | Q8_0 | 53 GB | ❌ 5 GB over limit |

---

## 9. Conclusion & Recommended OpenClaw Model Stack at 48GB

### 9.1 Primary Recommendation

| Priority | Model | Roles Covered | Key Advantage |
|----------|-------|--------------|---------------|
| **Frontier workhorse** | Llama 3.3 70B Q4_K_M | 10 roles (T3–T5): orchestrator, coding, debugging, security, SRE, fact-checking | BFCL 77.3% + HumanEval 88.4% |
| **Deep reasoning** | DS-R1-Distill-70B Q4_K_M | 3 roles (T4): math, STEM, algorithms | AIME 70%, MATH-500 94.5% |
| **Analytical sweet spot** | Nemotron-Super-49B Q4_K_M | 8 roles (T2–T5): research, planning, legal, medical, financial | 70B-class quality + 32–64K ctx + tool calling |
| **Fast MoE general** | Qwen3-30B-A3B Q8_0 | 4 roles (T2–T5): synthesis, RAG, book writing | 101 t/s + 160K+ ctx at near-lossless |
| **Quality general** | Qwen3-32B Q8_0 | 5 roles (T2–T3): editing, documents, curriculum | Near-lossless quality at 48GB |
| **Mid-range** | Qwen3-14B Q4_K_M | 12 roles (T1–T2): email, support, social | Fast single-GPU |
| **Fast lightweight** | Qwen3-8B Q4_K_M | 8 roles (T1): routing, validation, alerts | 186 t/s |

### 9.2 Core Insight: 48GB Is Where Local Matches Cloud

The 70B class brings three capabilities absent at 32GB:
- **Tool-calling reliability above 77% BFCL** — critical for the orchestrator delegating to all other agents
- **HumanEval code generation above 88%** — lifting all coding agent roles substantially
- **Mathematical reasoning at AIME 70%** — making Tier 4 roles genuinely capable rather than aspirational

48GB is the first tier where local inference stops being a compromise and starts being a genuine alternative to cloud APIs for production agent workloads.

### 9.3 Minimum Viable Stack

For the simplest effective OpenClaw deployment at 48GB:

1. **Nemotron-Super-49B Q4_K_M** (30.2 GB) — covers orchestrator, planning, research, coding, reasoning-toggle tasks. Fits with 17.8 GB for 32–64K context. Handles majority of T2–T5 roles.
2. **Qwen3-8B Q4_K_M** — fast router for all Tier 1 roles
3. Swap to **Llama 3.3 70B Q4_K_M** for heavy coding sessions or complex orchestration requiring maximum tool-calling reliability
4. Swap to **R1-Distill-70B Q4_K_M** for deep reasoning tasks

This rotation covers all 57 roles. Nemotron-Super-49B as the default workhorse handles 80%+ of tasks with its combination of quality, tool calling, reasoning toggle, and manageable VRAM footprint.

### 9.4 Honest Assessment: What 48GB Does NOT Solve

- Cloud APIs (Claude, GPT-4.1, Gemini 2.5 Pro, o3) still outperform on the hardest multi-step reasoning
- Full DeepSeek-R1 (671B) and DeepSeek-V3 quality remains datacenter-only
- Legal, medical, and compliance roles still benefit from cloud verification on critical decisions
- Context windows at 70B Q4_K_M (8–16K) are tight — use Nemotron-Super-49B Q4_K_M (32–64K) when context matters

**25 of 57 roles upgrade at 48GB. All Tier 4 reasoning roles transform. The remaining 32 roles were already well-served at 32GB.** The upgrades concentrate in Tiers 3–5 where task complexity exceeds what 32B models handle reliably.
