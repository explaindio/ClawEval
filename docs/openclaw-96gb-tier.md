# OpenClaw Model Selection — 96GB VRAM Tier

**Part 7a: RTX PRO 6000 Blackwell (Native 96GB)**

> **Critical constraint:** Every model listed as viable must load weights AND KV cache 100% in VRAM. No CPU offloading, no partial offloading, no hybrid RAM modes. Minimum Q4 quantization — no sub-Q4 quants are considered viable.

---

## Executive Summary

Ninety-six gigabytes of VRAM on a single card is a qualitative threshold: the point where models designed for datacenter H100s run locally on a workstation GPU. The RTX PRO 6000 Blackwell — the only native 96GB card available — loads **GPT-oss-120B at 120–163 tokens/second**, runs **Qwen3-Next-80B-A3B with 256K context and room to spare**, and fits **Llama 3.3 70B at near-lossless Q8_0 with 32K+ context**. Three entirely new model classes unlock at this tier that were impossible at 64GB: 100B+ MoE models (GPT-oss-120B, Llama 4 Scout 109B), next-generation hybrid-attention MoE (Qwen3-Next-80B-A3B), and 70B dense models at quality-preserving Q8_0 quantization with generous context windows.

**Key findings:**

- **GPT-oss-120B is the headline model** — 117B MoE with only 5.1B active parameters, MXFP4 weights at ~63–65 GB, delivering 120–163 t/s on the RTX PRO 6000. It outperforms o4-mini on AIME and achieves 90% MMLU with configurable reasoning depth and native tool calling.
- **Qwen3-Next-80B-A3B is the efficiency revelation** — 80B MoE with 3B active, Q4_K_M at 48.5 GB, leaving ~47 GB for KV cache (128K+ practical context). Its hybrid Gated DeltaNet + Gated Attention architecture delivers 10× the inference throughput of Qwen3-32B on long contexts. Outperforms Gemini-2.5-Flash-Thinking on multiple benchmarks.
- **Llama 3.3 70B at Q8_0** (~60 GB) delivers near-lossless quality with 32K+ context — a transformative upgrade over the Q4_K_M version at 48GB that was limited to 8–16K context.
- **20 of 57 roles upgrade at 96GB.** The upgrades concentrate in Tiers 3–5 where the jump from 70B-Q4 to 120B-MoE or 70B-Q8 produces measurable quality gains, particularly in coding (HumanEval 88%+), orchestration, and deep reasoning.
- **Diminishing returns are real but the new MoE models change the calculus.** Without GPT-oss-120B and Qwen3-Next-80B-A3B, the 96GB tier would be a marginal upgrade. With them, it represents the first tier where a single local GPU genuinely competes with cloud API quality for production agent workloads.

---

## 1. RTX PRO 6000 Blackwell — The Only Native 96GB Card

The NVIDIA RTX PRO 6000 Blackwell Workstation Edition is the sole GPU offering 96GB of VRAM in a single card. No consumer GPU reaches this capacity — the RTX 5090 tops out at 32GB.

| Specification | RTX PRO 6000 Blackwell |
|---|---|
| VRAM | 96 GB GDDR7 with ECC |
| Memory interface | 512-bit |
| Memory bandwidth | 1,792 GB/s |
| CUDA cores | 24,064 |
| Tensor cores | 5th Generation (native FP4/FP8/INT8/BF16) |
| PCIe interface | PCIe 5.0 x16 |
| TDP | 600W |
| Compute capability | 12.0 (Blackwell architecture) |
| Price (Feb 2026) | ~$7,950–8,000 |

**Native FP4 matters at this tier.** The RTX PRO 6000's Blackwell tensor cores natively accelerate MXFP4 operations — the exact format GPT-oss-120B ships in. This means the 120B model runs at hardware-native precision rather than through software dequantization, yielding the 120–163 t/s speeds benchmarked by StorageReview and Hardware Corner. No previous-generation workstation card (RTX 6000 Ada at 48GB) supports this format.

---

## 2. New Models That Unlock at 96GB

The jump from 64GB to 96GB adds four models that were completely inaccessible at lower tiers. Two are genuinely transformative.

### 2.1 Complete 96GB-Exclusive Model Roster

| Model | Params | Architecture | Active Params | Quant | Weight Size | KV Room | Usable Context | Fits 96GB? |
|---|---|---|---|---|---|---|---|---|
| **GPT-oss-120B** | 117B | MoE | 5.1B | MXFP4 (native) | ~63–65 GB | ~31–33 GB | 64–131K | ✅ Yes |
| **Llama 4 Scout** | 109B | MoE (16 experts) | 17B | Q4_K_M | 65.4 GB | ~30.6 GB | 32–64K | ✅ Yes |
| **Qwen3-Next-80B-A3B** | 80B | MoE (512 experts) | 3B | Q4_K_M | 48.5 GB | ~47.5 GB | 128K+ | ✅ Yes |
| **Qwen3-Next-80B-A3B** | 80B | MoE (512 experts) | 3B | Q6_K | 65.5 GB | ~30.5 GB | 64–128K | ✅ Yes |
| **Qwen3-Next-80B-A3B** | 80B | MoE (512 experts) | 3B | Q8_0 | 84.8 GB | ~11.2 GB | 16–32K | ✅ Yes (tight) |
| **Command R+ 104B** | 104B | Dense | 104B | Q4_K_M | ~62 GB | ~34 GB | 16–32K | ✅ Yes |

**Mixtral 8x22B** (141B MoE, Q4_K_M ~85.6 GB) technically loads but leaves only ~10.4 GB for KV cache — marginal for agentic use. Listed in the "doesn't fit" table due to insufficient context headroom.

### 2.2 Model Details

#### GPT-oss-120B — The Headline Unlock

OpenAI's first open-weight model since 2019, released August 2025 under Apache 2.0. This is a 117B-parameter MoE model with only 5.1B active parameters per token, shipped natively in MXFP4 quantization — a format the RTX PRO 6000's Blackwell tensor cores accelerate at hardware speed.

**VRAM profile:** The MXFP4 GGUF weights are ~63–65 GB. With Flash Attention enabled, total VRAM at 131K context drops from ~91 GB to ~67 GB — well within 96 GB with headroom. Without Flash Attention, 131K context consumes ~83 GB, still fitting but tighter.

**Performance on RTX PRO 6000:**
- StorageReview benchmark: **163.1 t/s** token generation (LM Studio, 500-word generation)
- Community reports: **~120 t/s** in common configurations
- vLLM with Flash Attention: **~180 t/s** at 131K context (RTX 6000 Max-Q variant)
- Prompt processing: fast enough for interactive agent use at all context lengths

**Key benchmarks:**
- MMLU: 90%
- AIME 2025: 98.7% (gpt-oss-20b) — the 120B exceeds o4-mini on math competitions
- HealthBench: outperforms o4-mini
- Native tool calling via Harmony 8 response format
- Configurable reasoning: low/medium/high intensity settings
- 128K native context window

**Why it matters for OpenClaw:** GPT-oss-120B combines frontier-class reasoning with native tool calling and configurable reasoning depth in a model that runs at 120+ t/s on a single workstation GPU. The configurable reasoning is particularly valuable for agent architectures — the orchestrator can dial up reasoning intensity for complex delegation decisions and dial it down for routine tool calls, optimizing both quality and latency.

#### Qwen3-Next-80B-A3B — The Efficiency Breakthrough

Released September 2025 by Alibaba, this is the first model in the Qwen3-Next series. It represents a new architectural paradigm: Hybrid Attention (Gated DeltaNet + Gated Attention) combined with ultra-sparse MoE (512 experts, 10 active + 1 shared per token = 3B active of 80B total).

**The architectural innovation:** Standard transformer attention scales quadratically with context length. Qwen3-Next's Gated DeltaNet layers provide linear-complexity context modeling, while periodic Gated Attention layers handle global information flow. The result: 10× inference throughput versus Qwen3-32B on contexts longer than 32K tokens, at 10% of the training cost.

**VRAM profile on RTX PRO 6000:**

| Quantization | Weight Size | KV Room | Usable Context |
|---|---|---|---|
| Q4_K_M | 48.5 GB | 47.5 GB | 128K+ (massive headroom) |
| Q5_K_M | 56.7 GB | 39.3 GB | 96–128K |
| Q6_K | 65.5 GB | 30.5 GB | 64–128K |
| Q8_0 | 84.8 GB | 11.2 GB | 16–32K |

The Q4_K_M sweet spot is remarkable: 48.5 GB of weights leaves nearly half the 96 GB card for KV cache, enabling **128K+ context at MoE inference speeds**. The hybrid attention architecture has inherently lower KV cache overhead than standard transformers (~2 GB additional per 100K tokens), making these context estimates conservative.

**Available variants:**
- **Instruct** — general-purpose, non-thinking mode, tool calling support
- **Thinking** — chain-of-thought reasoning, outperforms Gemini-2.5-Flash-Thinking

**Key benchmarks (Thinking variant):**

| Benchmark | Qwen3-Next-80B-A3B-Thinking | Qwen3-32B Thinking | Qwen3-235B Thinking | Gemini-2.5-Flash Thinking |
|---|---|---|---|---|
| MMLU-Pro | **82.7** | 79.1 | 84.4 | 81.9 |
| MMLU-Redux | **92.5** | 90.9 | 93.8 | 92.1 |
| GPQA | **77.2** | 68.4 | 81.1 | 82.8 |
| AIME 2025 | **87.8** | 72.9 | 92.3 | 72.0 |
| LiveCodeBench v6 | **68.7** | 60.6 | 74.1 | 61.2 |
| IFEval | **88.9** | 85.0 | 87.8 | 89.8 |

The Instruct variant benchmarks:
- MMLU-Pro: 80.6
- AIME 2025: 69.5
- HumanEval: 90%+ pass@1
- Arena-Hard v2: 82.7 (higher than Qwen3-235B's 79.2)
- MultiPL-E: 87.8

**Why it matters for OpenClaw:** This model offers Qwen3-235B-class performance in a package that fits on a single 96GB card with massive context headroom. The MoE architecture means inference is fast (comparable to the 30B-A3B models from lower tiers), and the 256K native context enables repository-scale code understanding and full-document analysis in a single pass. The Thinking variant's AIME 87.8% and LiveCodeBench 68.7% make it a genuine competitor to the R1-Distill models for reasoning tasks, but with tool calling support that the R1 distills lack.

#### Llama 4 Scout 109B — Multimodal MoE

Meta's Llama 4 Scout released April 2025, featuring 109B total parameters across 16 experts with 17B active per token. Multimodal (text + vision), with a theoretical 10M token context window.

**VRAM profile:** Q4_K_M at 65.4 GB (official ggml-org GGUF, split across 2 files). Leaves ~30.6 GB for KV cache — sufficient for 32–64K practical context.

**Caveats:** Community reception has been mixed. Early llama.cpp support was buggy, and benchmark performance, while strong for its generation, has been surpassed by GPT-oss-120B and Qwen3-Next-80B-A3B in most categories. The multimodal vision capability is its unique selling point — no other 100B+ model in this tier offers native image understanding.

**Best role:** Vision-heavy agent tasks where image understanding needs to be paired with strong language reasoning. For text-only tasks, GPT-oss-120B and Qwen3-Next-80B-A3B are superior choices.

#### Command R+ 104B — RAG Specialist (Legacy)

Cohere's 104B dense model (April 2024), designed specifically for enterprise RAG and tool use. At Q4_K_M (~62 GB), it fits with ~34 GB for KV cache.

**Caveats:** This is the oldest model in the 96GB roster. Licensed CC-BY-NC 4.0 (non-commercial default, commercial license available from Cohere). It has been surpassed by newer models on most benchmarks, but retains niche value for its 10-language multilingual RAG optimization and sophisticated citation generation. Its tool-use capabilities were strong for its generation but don't match GPT-oss-120B's Harmony 8 format or Qwen3-Next's Qwen-Agent integration.

**Best role:** Multilingual RAG pipelines requiring citation tracking. For most other tasks, newer models are preferable.

### 2.3 Key Benchmarks — 96GB Models vs 48GB Models

| Benchmark | Qwen3-32B (32GB best) | Llama 3.3 70B Q4 (48GB) | GPT-oss-120B | Qwen3-Next-80B (Thinking) | Jump from 48GB |
|---|---|---|---|---|---|
| **MMLU** | ~81% | 86.0% | **90%** | 92.5 (Redux) | +4–6% |
| **HumanEval** | ~78% | 88.4% | ~90%+ | 90%+ | +2–5% |
| **AIME 2025** | ~35% | ~20% | 98.7% (20B) | **87.8%** | +18–68% |
| **LiveCodeBench v6** | ~55% | ~60% | — | **68.7%** | +9–13% |
| **IFEval** | ~85% | 92.1% | — | **88.9%** | ~same |
| **GPQA** | ~50% | ~53% | — | **77.2%** | +24% |

The reasoning benchmarks show the most dramatic jumps. Qwen3-Next-80B-A3B-Thinking at 87.8% AIME 2025 is in a different league from any model available at 48GB or 64GB.

---

## 3. 48GB/64GB-Tier Models That Improve at 96GB

The extra VRAM budget transforms existing models through higher quantization and expanded context windows.

### 3.1 Quantization Upgrades

| Model | 48GB Tier (quant / ctx) | 96GB Tier (quant / ctx) | What Improves |
|---|---|---|---|
| **Llama 3.3 70B** | Q4_K_M (42.5 GB) / 8–16K | **Q8_0 (~60 GB)** / 32–48K | Near-lossless quality + 3× context |
| **R1-Distill-Llama-70B** | Q4_K_M (42.5 GB) / 8–16K | **Q8_0 (~60 GB)** / 32–48K | Critical: reasoning chains preserve fidelity |
| **Nemotron-Super-49B** | Q4_K_M (30.2 GB) / 32–64K | **Q8_0 (53 GB)** / 64–128K | Near-lossless + extended context |
| **Qwen3-30B-A3B** (MoE) | Q8_0 (32.5 GB) / 160K+ | Q8_0 (32.5 GB) / **160K+ with massive KV room** | Already Q8 at 48GB; now with ~63 GB KV headroom |
| **Qwen3-Coder-30B** (MoE) | Q8_0 (32.5 GB) / 160K+ | Q8_0 (32.5 GB) / **160K+ with massive KV room** | Same as above |
| **Qwen3-32B** | Q8_0 (34.8 GB) / 48–96K | **BF16 (~64 GB)** / 32–48K | True lossless precision (but less context) |

### 3.2 The Q8_0 70B Breakthrough

The single most impactful upgrade at 96GB for existing models: **Llama 3.3 70B at Q8_0** (~60 GB) with ~36 GB for KV cache. Q8_0 adds only +0.001 perplexity over FP16 — effectively lossless. At Q4_K_M (the 48GB format), the perplexity penalty is +0.054. For agent roles where output precision matters — legal reasoning, code generation, orchestration decisions — this quality delta is measurable and meaningful.

The context window roughly triples: from 8–16K at Q4_K_M to 32–48K at Q8_0 on 96GB. This transforms Llama 3.3 70B from a tight-context specialist into a full-featured agent model.

**R1-Distill-Llama-70B at Q8_0** sees an even larger quality impact. Chain-of-thought reasoning is particularly sensitive to quantization — small precision losses compound across long reasoning traces. Q8_0 preserves reasoning chain fidelity that Q4_K_M noticeably degrades on the hardest mathematical problems.

---

## 4. Inference Speed on RTX PRO 6000

All models load on a single card — no pipeline parallelism needed. This eliminates the speed penalties that plagued multi-GPU tiers. Single-card inference with 1,792 GB/s bandwidth and native FP4 tensor core support delivers excellent throughput.

### 4.1 Per-Model Speed Estimates

| Model | Quant | Weight Size | Architecture | Est. Token Gen | Est. Prompt Processing | Notes |
|---|---|---|---|---|---|---|
| **GPT-oss-120B** | MXFP4 | ~63–65 GB | MoE (5.1B active) | **120–163 t/s** | ~1,000+ t/s | Benchmarked by StorageReview, Hardware Corner |
| **Qwen3-Next-80B-A3B** | Q4_K_M | 48.5 GB | MoE (3B active) | **~100–140 t/s** | ~800+ t/s | Est. from MoE activation ratio + bandwidth |
| **Qwen3-Next-80B-A3B** | Q6_K | 65.5 GB | MoE (3B active) | **~80–110 t/s** | ~700+ t/s | Slightly slower from larger weights |
| **Qwen3-Next-80B-A3B** | Q8_0 | 84.8 GB | MoE (3B active) | **~60–80 t/s** | ~500+ t/s | Near-lossless quality trade |
| **Llama 4 Scout 109B** | Q4_K_M | 65.4 GB | MoE (17B active) | **~40–60 t/s** | ~500+ t/s | Higher active params = slower than GPT-oss |
| **Llama 3.3 70B** | Q8_0 | ~60 GB | Dense | **~25–30 t/s** | ~400+ t/s | Dense model, all 70B params active |
| **R1-Distill-70B** | Q8_0 | ~60 GB | Dense | **~25–30 t/s** | ~400+ t/s | Same architecture as Llama 3.3 70B |
| **Nemotron-Super-49B** | Q8_0 | 53 GB | Dense (pruned) | **~30–35 t/s** | ~500+ t/s | Smaller dense = faster than 70B |
| **Command R+ 104B** | Q4_K_M | ~62 GB | Dense | **~20–25 t/s** | ~300+ t/s | 104B dense, all params active |
| **Qwen3-30B-A3B** | Q8_0 | 32.5 GB | MoE (3.3B active) | **~140–180 t/s** | ~1,200+ t/s | Fastest model at tier, huge KV room |

### 4.2 Speed Tiers for Agent Role Assignment

**Ultra-fast (100+ t/s):** GPT-oss-120B, Qwen3-Next-80B Q4_K_M, Qwen3-30B-A3B Q8_0 — suitable for all interactive agent roles including orchestrator, real-time coding, and rapid tool-calling loops.

**Fast (40–80 t/s):** Qwen3-Next-80B Q6_K/Q8_0, Llama 4 Scout — suitable for interactive roles with minor latency tolerance.

**Moderate (25–35 t/s):** Llama 3.3 70B Q8_0, R1-Distill-70B Q8_0, Nemotron-Super-49B Q8_0 — suitable for semi-interactive roles where quality precision matters more than speed.

**Slow (20–25 t/s):** Command R+ 104B — background tasks only.

---

## 5. Inference Tools

The RTX PRO 6000 runs all major inference frameworks as a single-card deployment. No multi-GPU configuration needed.

### 5.1 Tool Compatibility

| Tool | Single-GPU Support | Native FP4 | Best For |
|---|---|---|---|
| **llama.cpp** | ✅ Full | ✅ MXFP4 via Blackwell kernels | GGUF models, quick testing, daily use |
| **Ollama** | ✅ Full | ✅ Via llama.cpp backend | Zero-config deployment, OpenClaw integration |
| **vLLM** | ✅ Full | ✅ FP8 + MXFP4 support | Production serving, continuous batching |
| **LM Studio** | ✅ Full | ✅ Via llama.cpp backend | Desktop GUI, easy model switching |
| **ExLlamaV3** | ✅ Full | Partial | Maximum quantization quality (EXL3) |
| **SGLang** | ✅ Full | ✅ | MoE-optimized expert parallelism |
| **TensorRT-LLM** | ✅ Full | ✅ Native Blackwell support | Maximum throughput (compiled engines) |

### 5.2 Tool Recommendations

**For OpenClaw daily deployment → Ollama or llama.cpp server.** First-class OpenClaw integration via `OLLAMA_API_KEY="ollama-local"`. Single command to run any model: `ollama run gpt-oss:120b`. The simplicity of single-card deployment means no multi-GPU configuration headaches.

**For maximum GPT-oss-120B performance → vLLM or TensorRT-LLM.** The 180 t/s achieved via vLLM with Flash Attention significantly exceeds the ~120 t/s from llama.cpp. TensorRT-LLM's MoE backend (supported on Blackwell) offers even higher throughput for production workloads.

**For Qwen3-Next-80B-A3B → SGLang.** Expert parallelism in SGLang is well-optimized for high-sparsity MoE models. With 512 experts and only 10 active, SGLang's routing can be particularly efficient. vLLM also supports Qwen3-Next natively (v0.10.2+) with Multi-Token Prediction for additional speed.

### 5.3 Dual-Model Serving on Single Card

With 96GB, simultaneous dual-model serving becomes practical for many model combinations:

| Model A | Size | Model B | Size | Total | KV Room | Use Case |
|---|---|---|---|---|---|---|
| GPT-oss-120B | ~65 GB | Qwen3-8B Q4 | ~5.5 GB | ~70.5 GB | ~25.5 GB | Frontier workhorse + fast router |
| Qwen3-Next-80B Q4_K_M | 48.5 GB | Qwen3-14B Q4 | ~9 GB | ~57.5 GB | ~38.5 GB | Next-gen MoE + general mid-range |
| Nemotron-Super-49B Q8_0 | 53 GB | Qwen3-8B Q4 | ~5.5 GB | ~58.5 GB | ~37.5 GB | Reasoning workhorse + router |
| Qwen3-30B-A3B Q8_0 | 32.5 GB | Llama 3.3 70B Q4_K_M | 42.5 GB | ~75 GB | ~21 GB | Fast MoE + frontier dense |

The first configuration — GPT-oss-120B + Qwen3-8B router — is particularly powerful for OpenClaw. The 8B model handles all Tier 1 routing and classification at ~186 t/s while the 120B handles all complex tasks at ~120 t/s, with zero model swap latency between them.

---

## 6. Complete Agent Role Mapping — All 57 Roles at 96GB

### 6.1 Tier 1 — Simple Roles (8 roles) — No Upgrades

Every Tier 1 role was well-served at 32GB. The 96GB VRAM is wasted on these tasks.

| Role | Model | Quant | Speed | Upgrade? |
|---|---|---|---|---|
| Router/triage | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Input validator | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Heartbeat/health | Qwen3-0.6B | Q8_0 | ~500+ t/s | ➡ No |
| Notification/alert | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| Sentiment analysis | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |
| FAQ generation | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No |
| Translation | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No |
| Calendar/scheduling | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No |

### 6.2 Tier 2 — Moderate Roles (25 roles) — 4 Upgrades

| Role | 96GB Model | Quant | Speed | Upgrade? | Why |
|---|---|---|---|---|---|
| **Research/web search** | **Qwen3-Next-80B-A3B** | Q4_K_M | ~120 t/s | ⬆ YES | 128K+ context + AIME 69.5% reasoning depth |
| **Content writing** | **Qwen3-Next-80B-A3B** | Q4_K_M | ~120 t/s | ⬆ YES | Arena-Hard 82.7 surpasses 235B; MoE speed |
| Editing | Qwen3-32B | Q8_0 | ~40 t/s | ➡ Marginal | Q8_0 already available at 48GB |
| Email drafting | Qwen3-32B | Q4_K_M | ~50 t/s | ➡ No | 32B sufficient |
| **Document summarization** | **Qwen3-Next-80B-A3B** | Q4_K_M | ~120 t/s | ⬆ YES | 128K context for entire documents in one pass |
| Meeting notes | Qwen3-30B-A3B | Q8_0 | ~150 t/s | ➡ No | Already excellent at 48GB |
| Social media | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | Short-form, 14B sufficient |
| News aggregation | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | Classification + summary |
| Shopping/price comparison | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No | Structured extraction |
| Memory/knowledge mgmt | Qwen3-30B-A3B | Q8_0 | ~150 t/s | ➡ No | Already excellent at 48GB |
| **RAG/retrieval** | **Qwen3-Next-80B-A3B** | Q4_K_M | ~120 t/s | ⬆ YES | 128K+ context = massive retrieval windows |
| Data analysis | Nemotron-Super-49B | Q8_0 | ~32 t/s | ➡ Marginal | Q8_0 improves numerical precision |
| Website scraping | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No | Parsing, not reasoning |
| Image description | Gemma 3 27B | Q8_0 | ~40 t/s | ➡ No | Already Q8_0 at 48GB |
| Customer support | Qwen3-32B | Q4_K_M | ~50 t/s | ➡ No | 32B sufficient |
| Lead scoring | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | Classification task |
| Project summarization | Qwen3-32B | Q8_0 | ~40 t/s | ➡ No | Q8_0 already at 48GB |
| Transaction/approval | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No | Rule-heavy |
| Home automation | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No | Command parsing |
| Fitness tracking | Qwen3-8B | Q4_K_M | ~186 t/s | ➡ No | Data logging |
| Recipe/cooking | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | Knowledge retrieval |
| Personal finance | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | 14B handles well |
| SEO optimization | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | Content analysis |
| Landing page generation | Qwen3-32B | Q8_0 | ~40 t/s | ➡ No | Already good at 48GB |
| Travel planning | Qwen3-14B | Q4_K_M | ~124 t/s | ➡ No | 14B sufficient |

**Tier 2 summary:** 4 upgrades, all driven by Qwen3-Next-80B-A3B's combination of 128K+ context and MoE speed. The upgrades target document-heavy and research roles where context length is the binding constraint.

### 6.3 Tier 3 — Complex Roles (11 roles) — 7 Upgrades

| Role | 96GB Model | Quant | Speed | Upgrade? | Why |
|---|---|---|---|---|---|
| **Code generation** | **GPT-oss-120B** | MXFP4 | ~130 t/s | ⬆ YES | 120B MoE with tool calling, outperforms Llama 70B |
| **Code review** | **GPT-oss-120B** | MXFP4 | ~130 t/s | ⬆ YES | Broader code understanding at 120B |
| **QA/test writing** | **GPT-oss-120B** | MXFP4 | ~130 t/s | ⬆ YES | Better edge-case generation |
| **Task planning** | **GPT-oss-120B** | MXFP4 | ~130 t/s | ⬆ YES | Configurable reasoning depth for planning |
| **Fact-checking** | **Llama 3.3 70B** | Q8_0 | ~28 t/s | ⬆ YES | Q8_0 near-lossless reduces hallucination |
| **Critic/review** | **GPT-oss-120B** | MXFP4 | ~130 t/s | ⬆ YES | Nuanced evaluation benefits from 120B scale |
| **Market research** | **Qwen3-Next-80B-A3B** | Q4_K_M | ~120 t/s | ⬆ YES | 128K context for multi-source synthesis |
| Synthesizer/aggregator | Qwen3-30B-A3B | Q8_0 | ~150 t/s | ➡ No | 160K ctx + speed still optimal |
| Curriculum design | Qwen3-32B | Q8_0 | ~40 t/s | ➡ No | Already good at 48GB |
| Prototype generation | GPT-oss-120B | MXFP4 | ~130 t/s | ➡ Marginal | Coding already served by Llama 70B |
| DevOps | Qwen3-32B | Q8_0 | ~40 t/s | ➡ No | Config/IaC generation, 32B sufficient |

**Tier 3 summary:** 7 upgrades. GPT-oss-120B dominates coding and planning roles at 130 t/s — it's faster than any dense 70B model while delivering stronger results. Qwen3-Next-80B-A3B handles long-context synthesis. Llama 3.3 70B at Q8_0 provides near-lossless fact-checking.

### 6.4 Tier 4 — Reasoning Roles (3 roles) — ALL Upgraded

| Role | 96GB Model | Quant | Speed | Upgrade? | Why |
|---|---|---|---|---|---|
| **Math/logic reasoning** | **Qwen3-Next-80B-A3B-Thinking** | Q4_K_M | ~120 t/s | ⬆⬆ MAJOR | AIME 87.8% vs R1-Distill-70B's 70%. Game-changing. |
| **STEM analysis** | **Qwen3-Next-80B-A3B-Thinking** | Q4_K_M | ~120 t/s | ⬆⬆ MAJOR | GPQA 77.2% vs R1-Distill-70B's 65.2% |
| **Algorithm exploration** | **Qwen3-Next-80B-A3B-Thinking** | Q6_K | ~90 t/s | ⬆⬆ MAJOR | LiveCodeBench 68.7%, CFEval 2071 |

**Tier 4 represents the most dramatic upgrade at 96GB.** Qwen3-Next-80B-A3B-Thinking's AIME 87.8% demolishes every model available at 48GB or 64GB. The R1-Distill-70B that was the 48GB-tier reasoning champion (AIME 70%) is now decisively surpassed — and the new model runs at MoE speeds (100+ t/s) rather than dense 70B speeds (~25 t/s). This is a fundamental shift: frontier-class mathematical reasoning at interactive speeds on a single GPU.

**Alt strategy for maximum math quality:** Load R1-Distill-70B at Q8_0 (~60 GB) when reasoning chain fidelity at the 70B-class is preferred over raw benchmark scores. The Q8_0 quantization preserves chain-of-thought precision that Q4 noticeably degrades.

### 6.5 Tier 5 — Frontier Roles (10 roles) — 6 Upgrades

| Role | 96GB Model | Quant | Speed | Cloud still better? | Upgrade? |
|---|---|---|---|---|---|
| **Orchestrator/manager** | **GPT-oss-120B** | MXFP4 | ~130 t/s | Closing gap | ⬆ YES |
| **Software architect** | **GPT-oss-120B** | MXFP4 | ~130 t/s | Narrowing | ⬆ YES |
| **Complex debugger** | **GPT-oss-120B** | MXFP4 | ~130 t/s | Narrowing | ⬆ YES |
| **Legal document review** | **Llama 3.3 70B** | Q8_0 | ~28 t/s | Yes, still | ⬆ YES |
| Medical/health analysis | Nemotron-Super-49B | Q8_0 | ~32 t/s | Yes, always verify | ➡ Marginal |
| Financial analysis | Nemotron-Super-49B | Q8_0 | ~32 t/s | Yes, for complex | ➡ Marginal |
| **Security analyst** | **GPT-oss-120B** | MXFP4 | ~130 t/s | Narrowing | ⬆ YES |
| **SRE/incident response** | **GPT-oss-120B** | MXFP4 | ~130 t/s | Partially | ⬆ YES |
| Book writing | Qwen3-Next-80B-A3B | Q4_K_M | ~120 t/s | For style/coherence | ➡ Marginal |
| Compliance/regulatory | Llama 3.3 70B | Q8_0 | ~28 t/s | Yes, strongly | ➡ Marginal |

**The orchestrator role gets its most significant upgrade yet.** GPT-oss-120B's combination of native tool calling (Harmony 8 format), configurable reasoning intensity, and 90% MMLU knowledge breadth makes it the strongest local orchestrator available. The configurable reasoning is specifically valuable: dial to "low" for routine routing decisions (faster), "high" for complex multi-agent coordination (slower but more reliable). At 120+ t/s, even the high-reasoning mode is interactive.

### 6.6 Upgrade Summary — All 57 Roles

| Tier | Total Roles | Upgraded at 96GB | Unchanged | Key Driver |
|---|---|---|---|---|
| Tier 1 (simple) | 8 | 0 | 8 | 8–14B already sufficient |
| Tier 2 (moderate) | 25 | 4 | 21 | Qwen3-Next-80B 128K+ context |
| Tier 3 (complex) | 11 | 7 | 4 | GPT-oss-120B speed + quality |
| Tier 4 (reasoning) | 3 | 3 | 0 | Qwen3-Next-80B-Thinking AIME 87.8% |
| Tier 5 (frontier) | 10 | 6 | 4 | GPT-oss-120B orchestration + tool calling |
| **Total** | **57** | **20** | **37** | |

### 6.7 Model Usage Across All Roles

| Model | Roles Served | Tier Coverage | Key Advantage |
|---|---|---|---|
| **GPT-oss-120B** MXFP4 | 11 roles | T3–T5 | Frontier workhorse: 120+ t/s, 90% MMLU, configurable reasoning, native tool calling. Orchestrator, coding, debugging, security, SRE, planning, architecture |
| **Qwen3-Next-80B-A3B** Q4_K_M (Instruct) | 5 roles | T2–T3 | Context king: 128K+ at MoE speed. Research, content writing, document summary, RAG, market research |
| **Qwen3-Next-80B-A3B** Q4_K_M (Thinking) | 3 roles | T4 | Reasoning champion: AIME 87.8%, LiveCodeBench 68.7%. Math, STEM, algorithms |
| **Llama 3.3 70B** Q8_0 | 2 roles | T3–T5 | Near-lossless dense: fact-checking, legal review |
| **Nemotron-Super-49B** Q8_0 | 2 roles | T5 | Balanced quality: medical analysis, financial analysis |
| **Qwen3-30B-A3B** Q8_0 (MoE) | 2 roles | T2–T3 | Speed + context: synthesis, meeting notes |
| **Qwen3-32B** Q8_0 | 6 roles | T2–T3 | Quality general: editing, email, DevOps, curriculum, landing pages, customer support |
| **Qwen3-14B** Q4_K_M | 8 roles | T1–T2 | Mid-range: social media, news, finance, SEO, travel, recipes |
| **Qwen3-8B** Q4_K_M | 8 roles | T1 | Fast lightweight: router, validator, alerts, sentiment, scheduling, scraping |
| **Qwen3-0.6B** Q8_0 | 1 role | T1 | Heartbeat monitor |

---

## 7. Deployment Architectures at 96GB

### 7.1 Architecture A — Single Frontier Model

Load one large model and swap as needed.

**Default:** GPT-oss-120B MXFP4 (~65 GB) with ~31 GB for KV cache. Covers orchestrator, coding, planning, and all Tier 3–5 roles. Swap to Qwen3-Next-80B-A3B-Thinking for deep reasoning tasks.

**Swap time:** ~15–25 seconds for 65 GB models from NVMe SSD.

### 7.2 Architecture B — Frontier + Router (Recommended for OpenClaw)

Load two models simultaneously:
- **GPT-oss-120B** MXFP4 (~65 GB) — handles all complex tasks
- **Qwen3-8B** Q4_K_M (~5.5 GB) — handles routing, triage, notifications, heartbeat

Total: ~70.5 GB. Leaves ~25.5 GB for KV cache across both models.

**Zero model swap latency** for the vast majority of agent interactions. Only swap to specialized models (Qwen3-Next-80B Thinking, Llama 3.3 70B Q8_0) for infrequent specialized tasks.

### 7.3 Architecture C — Context-Optimized

Load Qwen3-Next-80B-A3B Q4_K_M (48.5 GB) with ~47.5 GB for KV cache. This configuration provides 128K+ context at MoE speed — ideal for document-heavy workflows, RAG pipelines, and research agent workloads that need to ingest entire documents or codebases.

Optionally co-load Qwen3-14B Q4_K_M (~9 GB) for mid-range tasks, totaling ~57.5 GB with ~38.5 GB for KV cache.

### 7.4 Architecture D — Maximum Quality

Load Llama 3.3 70B Q8_0 (~60 GB) for near-lossless dense model quality. Leaves ~36 GB for KV cache (32–48K context). Best for roles where quantization-induced quality loss matters: legal analysis, compliance, fact-checking, and any domain requiring maximum factual precision.

### 7.5 Recommended Architecture by Workload

| Workload | Best Architecture | Models | Why |
|---|---|---|---|
| OpenClaw multi-agent pipeline | **B — Frontier + Router** | GPT-oss-120B + Qwen3-8B | Zero-swap for 80%+ of tasks, 120+ t/s |
| Heavy coding sessions | A — Single frontier | GPT-oss-120B all day | Best tool calling + coding quality |
| Deep reasoning tasks | A — Swap to specialist | Qwen3-Next-80B-Thinking | AIME 87.8% at MoE speed |
| Document-heavy analysis | C — Context-optimized | Qwen3-Next-80B Q4_K_M | 128K+ context for full documents |
| Legal/compliance review | D — Maximum quality | Llama 3.3 70B Q8_0 | Near-lossless for precision-critical work |
| Mixed diverse roles | B + occasional swap | GPT-oss-120B + 8B, swap to specialists | Covers everything |

---

## 8. Models That Do NOT Fit at 96GB

**No CPU offloading. No partial fits. Minimum Q4 quantization.**

| Model | Params | Architecture | Smallest Viable Quant | Weight Size | Verdict |
|---|---|---|---|---|---|
| DeepSeek-R1 | 671B | MoE | Q2_K | ~250 GB | ❌ Datacenter only (8× H100) |
| DeepSeek V3.2 | 685B | MoE | Q4_K_M | ~386 GB | ❌ Datacenter only |
| GLM-5 | 744B | MoE | Q4_K_M | ~400+ GB | ❌ Datacenter only |
| Kimi K2.5 | 1T | MoE | Q4_K_M | ~621 GB | ❌ Datacenter only |
| MiniMax M2.5 | 230B | MoE | Q4_K_M | ~140 GB | ❌ 44 GB over limit |
| Qwen3-235B-A22B | 235B | MoE | Q4_K_M | ~140+ GB | ❌ Far too large |
| Llama 4 Maverick | 402B | MoE | Q4_K_M | ~240+ GB | ❌ Far too large |
| Mixtral 8x22B | 141B | MoE | Q4_K_M | ~85.6 GB | ❌ Fits weights but only ~10 GB KV = unusable |
| Qwen2.5-72B | 72.7B | Dense | Q8_0 | ~73+ GB | ⚠️ Tight — limited context. Llama 3.3 70B Q8_0 preferred |
| Llama 3.3 70B | 70B | Dense | BF16 | ~140 GB | ❌ Full precision doesn't fit |

The models that remain out of reach at 96GB are truly massive: 200B+ MoE models and full-precision 70B+ dense models. These require either datacenter GPUs (A100 80GB, H100, B200) or multi-card 96GB setups — a configuration reserved for the multi-GPU consumer tier report.

---

## 9. Diminishing Returns Assessment — Is 96GB Worth It?

### 9.1 The Honest Calculus

**From 48GB → 64GB** (covered in Part 6), the primary gains were quantization upgrades (70B at Q5_K_M, 49B at Q8_0) and multi-model serving. The jump was modest.

**From 64GB → 96GB**, the story changes because of two models that didn't exist at the 64GB tier:

1. **GPT-oss-120B** — a genuine 120B-class model running at 120+ t/s. No amount of quantization trickery brings this model into 64GB. It's a category jump.
2. **Qwen3-Next-80B-A3B** — while the Q4_K_M (48.5 GB) technically fits at 64GB, the KV cache room on a 64GB setup (multi-GPU pipeline split) is severely constrained and the speed penalty from splitting a 48.5 GB MoE model is wasteful. On the native 96GB card, it has 47.5 GB of KV headroom for 128K+ context at full single-card speed.

**Without these two models, 96GB would be a marginal upgrade over 64GB.** With them, it represents a genuine capability tier for agent deployment.

### 9.2 Cost-Benefit

| Configuration | Price | Best Model | Speed | Context |
|---|---|---|---|---|
| 2× RTX 5090 (64GB) | ~$4,000 | Llama 3.3 70B Q5_K_M | ~8–10 t/s (pipeline) | 16–32K |
| RTX PRO 6000 (96GB) | ~$8,000 | GPT-oss-120B MXFP4 | **120–163 t/s** | 64–131K |

The speed differential is staggering: 12–20× faster for a model that's also substantially stronger. The cost-per-useful-token-per-second strongly favors the native 96GB card over multi-GPU 64GB setups.

**Versus cloud APIs:** At ~$8,000 one-time cost, the RTX PRO 6000 running GPT-oss-120B or Qwen3-Next-80B-A3B pays for itself versus cloud API usage within 2–6 months for heavy agent workloads (assuming $100–300/month in API costs). The breakeven is faster for teams running 24/7 agent pipelines.

### 9.3 What 96GB Still Cannot Do

- **Cloud APIs still lead on the hardest tasks.** Claude Sonnet 4, GPT-5, Gemini 2.5 Pro, and o3 outperform any local 96GB model on the most complex multi-step reasoning, creative writing, and nuanced judgment calls.
- **The 200B+ MoE frontier is out of reach.** MiniMax M2.5 (230B, 80.2% SWE-bench), Qwen3-235B-A22B, and full DeepSeek-R1 require datacenter-class hardware.
- **Legal, medical, and compliance roles still benefit from cloud verification.** While 96GB models are substantially better than 48GB models for these domains, the liability risk on safety-critical decisions means human + cloud API review remains advisable.
- **Multimodal video understanding is limited.** Llama 4 Scout offers basic vision but no video processing. Production-quality multimodal remains a cloud API strength.

---

## 10. Conclusion & Recommended OpenClaw Model Stack at 96GB

### 10.1 Primary Recommendation

| Priority | Model | Roles Covered | Key Advantage |
|---|---|---|---|
| **Frontier workhorse** | GPT-oss-120B MXFP4 | 11 roles (T3–T5): orchestrator, coding, debugging, security, SRE, planning, architecture, critic, QA/test, task planning | 120+ t/s, 90% MMLU, configurable reasoning, native tool calling |
| **Context king** | Qwen3-Next-80B-A3B Q4_K_M (Instruct) | 5 roles (T2–T3): research, content writing, document summary, RAG, market research | 128K+ context at MoE speed, Arena-Hard 82.7 |
| **Reasoning champion** | Qwen3-Next-80B-A3B Q4_K_M (Thinking) | 3 roles (T4): math, STEM, algorithms | AIME 87.8%, GPQA 77.2%, LiveCodeBench 68.7% |
| **Near-lossless dense** | Llama 3.3 70B Q8_0 | 2 roles (T3–T5): fact-checking, legal review | Q8_0 = +0.001 perplexity, 32–48K context |
| **Analytical specialist** | Nemotron-Super-49B Q8_0 | 2 roles (T5): medical, financial | Reasoning toggle + tool calling at Q8_0 |
| **Speed + context** | Qwen3-30B-A3B Q8_0 (MoE) | 2 roles (T2–T3): synthesis, meetings | 150+ t/s, 160K+ context |
| **Quality general** | Qwen3-32B Q8_0 | 6 roles (T2–T3): editing, email, DevOps, curriculum, landing pages, support | Near-lossless quality |
| **Mid-range** | Qwen3-14B Q4_K_M | 8 roles (T1–T2): social, news, finance, SEO, travel, recipes | Fast single-GPU |
| **Fast lightweight** | Qwen3-8B Q4_K_M | 8 roles (T1): routing, validation, alerts | 186 t/s, co-loads with any model |
| **Heartbeat** | Qwen3-0.6B Q8_0 | 1 role (T1): health monitor | 500+ t/s |

### 10.2 Core Insight: MoE-First at Unprecedented Scale

The defining advantage of 96GB is running MoE models large enough to compete with frontier APIs. Both GPT-oss-120B (5.1B active of 117B) and Qwen3-Next-80B-A3B (3B active of 80B) deliver their quality through massive parameter pools with tiny activation footprints. This is why they're fast — token generation speed is primarily limited by active parameters, not total VRAM consumption.

The result is an unusual performance profile: **models that use 65–85 GB of VRAM but generate tokens at speeds comparable to 8B models.** This makes them practical as primary workhorse models for interactive agent pipelines in a way that dense 70B models (which generate at 25–30 t/s) are not.

### 10.3 Minimum Viable Stack

For the simplest effective OpenClaw deployment at 96GB:

1. **GPT-oss-120B MXFP4** (~65 GB) + **Qwen3-8B Q4_K_M** (~5.5 GB) simultaneously loaded — covers orchestrator, all coding, all Tier 1 routing, and most Tier 3–5 roles at zero swap latency
2. Swap to **Qwen3-Next-80B-A3B-Thinking Q4_K_M** (48.5 GB) for deep reasoning tasks (AIME 87.8%)
3. Swap to **Llama 3.3 70B Q8_0** (~60 GB) for precision-critical legal/compliance work

This three-model rotation covers all 57 roles. The GPT-oss-120B + Qwen3-8B dual-load handles 80%+ of tasks without any model swapping.

### 10.4 The 96GB Verdict

The RTX PRO 6000 Blackwell at 96GB is the first single-GPU configuration where local AI agent deployment stops being a compromise and becomes a genuine production-grade alternative to cloud APIs. The combination of GPT-oss-120B (frontier tool calling + reasoning at MoE speed) and Qwen3-Next-80B-A3B (frontier reasoning + ultra-long context at MoE speed) creates an agent stack that matches or approaches cloud API quality for the vast majority of agent roles — at 120+ tokens per second, with full data privacy, and zero per-token cost.

**20 of 57 roles upgrade at 96GB.** The remaining 37 were already well-served at lower tiers. The upgrades concentrate precisely where they matter most: orchestration, complex coding, deep reasoning, and long-context analysis. For teams building serious OpenClaw deployments where quality, privacy, and cost efficiency all matter, the 96GB tier is the sweet spot.
