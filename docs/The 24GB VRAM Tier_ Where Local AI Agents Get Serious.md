# The 24GB VRAM tier: where local AI agents get serious

Upgrading from 16GB to 24GB VRAM doesn't just unlock a few more models — it fundamentally changes what's possible for local AI agent deployment. **Qwen3-32B at Q4 quantization matches the prior generation's 72B-class models in base capability**, and a new generation of 30B MoE models delivers efficient inference with genuine tool-calling and agentic reasoning. The two GPUs that define this tier, the RTX 3090 (~$800 used) and RTX 4090 (~$1,800 used), share the same 24GB VRAM ceiling and run identical model sizes. Their architectural differences in quantization support matter less than expected at this tier — but the performance gap and price-to-performance ratio create a genuinely interesting choice for builders.

---

## Hardware-level quantization: what each GPU actually computes natively

The RTX 3090 (Ampere, GA102) and RTX 4090 (Ada Lovelace, AD102) both carry 24GB of GDDR6X, but their tensor cores speak different languages at the hardware level. Understanding this split is critical for choosing quantization formats, even though — as we'll see — the practical impact at the 24GB model tier is narrower than the spec sheets suggest.

**RTX 3090's 3rd-generation tensor cores** (CUDA compute capability 8.6) natively accelerate **INT8, INT4, FP16, BF16, and TF32** matrix operations. They also support 2:4 structured sparsity for doubled effective throughput on compatible workloads. What Ampere does *not* have: any form of FP8, FP6, FP4, NVFP4, or MXFP4. These formats simply don't exist in the hardware. The 3090 has 328 tensor cores, **936 GB/s** memory bandwidth, a modest 6MB L2 cache, and draws 350W TDP.

**RTX 4090's 4th-generation tensor cores** (compute capability 8.9) retain everything Ampere offers and add one major capability: **native FP8 (E4M3 and E5M2) tensor core acceleration** via NVIDIA's Transformer Engine, first introduced in the data-center Hopper architecture. This enables W8A8 (weight-8-bit, activation-8-bit) inference at hardware speed — roughly doubling throughput versus FP16 for memory-bound operations. The 4090 does *not* support FP4, NVFP4, MXFP4, or FP6; those are Blackwell-exclusive (compute capability 10.0+). The 4090 packs 512 tensor cores (56% more than the 3090), **1,008 GB/s** bandwidth (7.7% more), and a transformative **96MB L2 cache** — 16× the 3090's 6MB. It draws 450W.

| Capability | RTX 3090 (Ampere) | RTX 4090 (Ada Lovelace) |
|---|---|---|
| Tensor core generation | 3rd | 4th |
| Compute capability | 8.6 | 8.9 |
| **FP8 (E4M3, E5M2)** | ❌ No | ✅ Yes |
| FP4 / NVFP4 / MXFP4 | ❌ No | ❌ No (Blackwell only) |
| INT8 / INT4 | ✅ Yes | ✅ Yes |
| BF16 / FP16 / TF32 | ✅ Yes | ✅ Yes |
| 2:4 structured sparsity | ✅ Yes | ✅ Yes |
| Memory bandwidth | 936 GB/s | 1,008 GB/s |
| L2 cache | 6 MB | 96 MB |
| TDP | 350W | 450W |
| Used price (Feb 2026) | ~$700–900 | ~$1,500–2,200 |

At the software quantization level, both GPUs run every major format identically. **GGUF** (Q2_K through Q8_0), **BitsAndBytes** (NF4, INT4, INT8), **GPTQ**, **AWQ**, **EXL2**, and **Marlin INT4 kernels** all work on both architectures through custom CUDA kernels that dequantize to FP16/BF16 before hitting the tensor cores. The only meaningful software-level divergence is FP8: vLLM and TensorRT-LLM support W8A8 FP8 on compute ≥8.9 (4090), while on the 3090, FP8 falls back to W8A16 weight-only mode via the Marlin kernel — functional but without the full throughput advantage.

## The FP8 paradox at 24GB: architecture advantage meets VRAM reality

Here's the counterintuitive finding: **the RTX 4090's headline FP8 capability provides almost no practical advantage for the models that define the 24GB tier**. The reason is simple arithmetic. FP8 stores one byte per parameter. A 27B model at FP8 requires ~27GB for weights alone — already exceeding 24GB VRAM before any KV cache allocation. A 32B model at FP8 needs ~32GB. The models that *unlock* at 24GB (27B–32B parameter range) are simply too large for FP8 quantization on a 24GB card.

For these models, both GPUs converge on the same practical format: **Q4_K_M** (GGUF, ~4.8 bits per parameter) or equivalent INT4 schemes (GPTQ, AWQ, EXL2). The 4090's FP8 advantage is real but only applies to smaller models (8B–14B) that already fit comfortably at 16GB — models covered in the existing report section.

The 4090's *actual* advantages at this tier are more nuanced and entirely about speed:

- **Token generation**: 20–30% faster than the 3090 (e.g., Qwen3-32B at 16K context: **37.7 t/s on 4090** vs **30.3 t/s on 3090**), driven by slightly higher bandwidth and the massive L2 cache keeping more KV-cache data near compute units
- **Prompt processing (prefill)**: 2.5–3.5× faster, because prefill is compute-bound and the 4090 has 56% more tensor cores at higher clocks
- **L2 cache effect**: The 96MB L2 cache provides outsized benefit for LLM inference specifically, reducing main memory round-trips for KV cache access

For agentic workloads involving repeated tool calls and context reprocessing, the 4090's prefill speed advantage compounds. But for single-stream token generation — the bottleneck in most agent conversations — the 3090 delivers roughly 80% of the 4090's performance at less than half the price.

## Models that unlock: the 24GB roster

The jump from 16GB to 24GB opens access to two distinct model classes: 30B-class MoE models that were 1–2GB over the 16GB limit, and 27B–32B dense models that bring substantially stronger reasoning. Here's every model that crosses the 24GB threshold with practical VRAM headroom, listed from most comfortable fit to tightest.

### 30B MoE models: the efficiency sweet spot

These models load all 30B parameters into VRAM (required for expert routing) but activate only ~3B per token, yielding dramatically faster inference than dense alternatives at similar total VRAM.

**Qwen3-30B-A3B** (30.5B total, 3.3B active, 128 experts, 8 active per token) is the standout general-purpose model at this tier. At Q4_K_M, it occupies ~18.6GB and fits **32K context** comfortably within 24GB. Inference speeds are remarkable: **87–114 t/s on the 3090** and **105–140 t/s on the 4090** at 16K context — 3–4× faster than dense 32B models. It features native tool calling, hybrid thinking/non-thinking modes, 119 language support, and Apache 2.0 licensing. On ArenaHard, it scores **91.0** in thinking mode — surpassing both Qwen3-32B (89.5) and QwQ-32B. The remarkable efficiency claim: 10× fewer active parameters than QwQ-32B while matching or exceeding it.

**Qwen3-Coder-30B-A3.3B** (July 2025) shares the same MoE architecture but is purpose-built for agentic coding. It achieves **~50% on SWE-bench Verified** with 256K native context for repository-scale understanding. At Q4_K_M on the Aider Polyglot benchmark, quality loss is minimal: 60.9% versus 61.8% at full BF16. Tool calling was initially buggy in llama.cpp/Ollama but has been fixed by Unsloth. Same ~18.6GB at Q4_K_M, same 32K+ practical context on 24GB.

**NVIDIA Nemotron 3 Nano** (December 2025, 30B total, ~3.2–3.5B active) is architecturally unique: a hybrid of 23 Mamba-2 layers, 23 MoE layers, and 6 GQA attention layers, with 128 routed experts per MoE layer. NVIDIA claims 3.3× higher throughput than Qwen3-30B-A3B on H200. However, there's a practical VRAM catch: the Q4_K_M GGUF weighs **~24.5GB** — essentially filling all 24GB with no room for KV cache. Deployment requires the Unsloth UD-Q4_K_XL variant (~22.8GB) or Q4_K_S (~22GB) to leave context headroom. Native tool calling, hybrid reasoning on/off, and theoretical 1M token context are supported. Language support is limited to six languages (EN, DE, ES, FR, IT, JA).

**GLM-4.7-Flash** (January 2026, ~30B total, ~3B active MoE) from Zhipu AI rounds out the MoE tier. MIT-licensed with tool calling, CoT "thinking" support, and 128K–200K context. At Q4 quantization it runs comfortably on 24GB at **120–220 t/s on the 4090**. Community testing is still limited given its recent release, but early signals are positive for coding and agentic tasks.

### Dense 27B–32B models: maximum quality per parameter

Dense models activate every parameter on every token. They're slower than MoE alternatives but can deliver stronger reasoning precision since no routing mechanism introduces selection noise.

**Gemma 3 27B** offers the most headroom. Google's QAT (Quantization-Aware Training) Q4_0 variant fits in ~15.6GB, leaving room for **16–20K context** on 24GB. Key strengths include multimodal vision+text input, 140+ language support, and 128K native context architecture. The catch: Gemma 3 has unusually high KV cache overhead due to its hybrid sliding-window/full-attention design. One community report found 22.5GB total at 20K context (19.1GB weights + 4.7GB KV cache). **Tool calling is limited** — functional but not best-in-class. Google's QAT variants preserve ~54% more quality than naive Q4_0 at the same size, making them the recommended quantization choice.

**Qwen3-32B** (dense, 32B) is the tier's reasoning powerhouse. At Q4_K_M (~19.8GB), it fits on 24GB with approximately **16K usable context** (verified by Hardware Corner benchmarks: 23GB VRAM = 16K context for this model). Inference runs at **30.3 t/s on the 3090** and **37.7 t/s on the 4090**. The headline claim: Qwen3-32B-Base matches Qwen2.5-72B-Base in overall performance — a generational leap. It scores 89.5 on ArenaHard, 68.2 on BFCL v3 (strong tool calling), and 85% human preference in blind creative writing evaluations. Native MCP support and hybrid thinking modes make it the most versatile dense model at this tier. The tradeoff versus MoE models is clear: stronger reasoning and broader capability, but 3–4× slower inference and roughly half the context window.

**DeepSeek-R1-Distill-Qwen-32B** (dense, 32B, distilled from DeepSeek-R1) is a reasoning specialist. At Q4_K_M (~20GB), it fits similarly to Qwen3-32B with **8–16K practical context**. Its benchmarks are extraordinary for math and logic: **72.6% on AIME 2024** (outperforming OpenAI o1-mini), **94.3% on MATH-500**, and 57.2% on LiveCodeBench. Inference speed: ~20 t/s on the 3090, ~34–38 t/s on the 4090. The critical limitation for agent use: **it lacks tool calling, system prompt support, and general instruction-following**. It's a pure reasoning engine, not a general-purpose agent model. Use it as a specialized subagent for mathematical and logical verification — not as an orchestrator.

### Models that still don't fit at 24GB

| Model | Total params | Smallest viable GGUF | Why it fails |
|---|---|---|---|
| Llama 4 Scout | 109B MoE (17B active) | ~29GB at TQ1_0 | All 109B must load for router; only fits at ~1.78-bit Unsloth Dynamic with severe quality loss |
| Llama 3.3 70B | 70B dense | ~21GB at IQ2_XS | Only 2-bit fits; substantial quality degradation makes it worse than a good 32B at Q4 |
| Mistral Large 3 | 675B MoE (41B active) | ~73GB at Q4 | Far too large at any quantization |
| Command R+ | 104B dense | ~39.5GB at Q2_K | Dense 104B exceeds 24GB even at Q2 |

The community consensus on r/LocalLLaMA is clear: a high-quality 32B model at Q4 consistently outperforms a 70B model at IQ2_XS or a 109B MoE at sub-2-bit quantization. **Don't chase parameter counts at the cost of quantization quality.**

## Mapping 24GB models to upgraded subagent roles

The 24GB tier transforms the agent capability picture. Roles that were quality-limited or infeasible at 16GB become production-viable. Here's how each upgrade maps, with clear 3090 vs 4090 guidance.

**Orchestrator / Manager Agent** — *was Tier 4–5 (partially feasible to infeasible), now Tier 2 (strong)*. **Recommended: Qwen3-32B at Q4_K_M.** Its BFCL v3 score of 68.2 (leading among open 32B-class models), native MCP support, and hybrid thinking modes make it the first local model that can genuinely handle multi-step orchestration with tool routing. On both 3090 and 4090 via Q4_K_M GGUF. The 4090 adds ~24% faster generation and substantially faster context reprocessing when re-reading agent outputs. Versus the 14B recommendation at 16GB: this represents roughly a doubling of effective orchestration capability — the gap between "works with simple routing" and "handles complex multi-step plans."

**Complex Code Generation** — *was Tier 3 (feasible, quality-limited), now Tier 1–2*. **Recommended: Qwen3-Coder-30B-A3.3B at Q4_K_M.** Purpose-built for agentic coding with 50% SWE-bench Verified, 256K context for full-repository understanding, and fast MoE inference (~87–140 t/s). For algorithmic problem-solving specifically, swap in DeepSeek-R1-Distill-32B (57.2% LiveCodeBench, 1691 CodeForces rating). Both work on 3090 and 4090 at Q4_K_M. The coding agent role sees perhaps the largest improvement at 24GB: Qwen3-Coder was designed for exactly this use case and dramatically outperforms any 14B coding model.

**Research / Analysis Agent** — *was Tier 3, now Tier 2*. **Recommended: Qwen3-32B in thinking mode at Q4_K_M.** The configurable thinking depth (0–38K tokens) enables deep multi-step analysis when needed and fast responses when not. Strong instruction-following and multi-turn coherence make it suitable for iterative research workflows. The 16K context limit at 24GB constrains very long document analysis — for those cases, Qwen3-30B-A3B at Q4 offers 32K context with somewhat less reasoning depth.

**Math / Science Reasoning** — *was Tier 5 (not feasible), now Tier 1*. **Recommended: DeepSeek-R1-Distill-Qwen-32B at Q4_K_M.** This is a transformative unlock. The 16GB tier had no model that could reliably handle competition-level math or complex scientific reasoning. R1-Distill-32B outperforms OpenAI o1-mini on AIME benchmarks. Runs on both 3090 (~20 t/s) and 4090 (~34 t/s); the 4090's speed advantage matters here since reasoning traces can be long.

**Multi-step Planning** — *was Tier 3–4, now Tier 2*. **Recommended: Qwen3-30B-A3B at Q4_K_M** for frequent planning calls (fast MoE inference, ArenaHard 91.0), or **Qwen3-32B** when planning complexity demands maximum reasoning depth. The MoE model's 3–4× speed advantage makes it the better default for planning agents that fire frequently in agent loops.

**Document Summarization (complex docs)** — *was Tier 3, now Tier 2*. **Recommended: Gemma 3 27B QAT Q4_0 for multimodal documents** (scanned PDFs, images embedded in text, 140+ languages), or **Qwen3-32B for reasoning-heavy synthesis** of text-only documents. Gemma 3's vision capability is unique at this tier and genuinely useful for mixed-format document processing.

**Creative Writing** — *was Tier 3, now Tier 2*. **Recommended: Qwen3-32B in non-thinking mode.** 85% human preference in blind evaluations, specifically trained for creative writing and role-playing in post-training stages. No other 24GB model approaches this quality for long-form narrative generation.

**Multilingual Tasks** — *was Tier 3–4, now Tier 2*. **Recommended: Gemma 3 27B for broadest coverage** (140+ languages with multimodal OCR for non-Latin scripts), or **Qwen3-32B for highest quality** (119 languages, MultiIF score 73.0). Both work on 3090 and 4090 at Q4_K_M.

### Quick reference: the 3090 vs 4090 decision for each role

| Role | Model | 3090 speed | 4090 speed | 4090 worth it? |
|---|---|---|---|---|
| Orchestrator | Qwen3-32B Q4 | ~30 t/s | ~38 t/s | Marginal; 3090 is fine |
| Coding agent | Qwen3-Coder 30B Q4 | ~87 t/s | ~140 t/s | Yes — faster tool-call loops |
| Research | Qwen3-32B Q4 | ~30 t/s | ~38 t/s | Marginal |
| Math/science | R1-Distill-32B Q4 | ~20 t/s | ~34 t/s | Yes — long reasoning chains |
| Planning | Qwen3-30B-A3B Q4 | ~87 t/s | ~140 t/s | Nice but not necessary |
| Summarization | Gemma 3 27B Q4 | ~25 t/s | ~35 t/s | Marginal |
| Creative writing | Qwen3-32B Q4 | ~30 t/s | ~38 t/s | No — generation speed is fine |
| Multilingual | Gemma 3 27B Q4 | ~25 t/s | ~35 t/s | No |

The 3090 is sufficient for every role. The 4090 provides meaningful improvement primarily for high-frequency agent loops (coding, planning) and long reasoning chains (math/science), where accumulated latency savings add up.

## What 24GB still can't do: honest limitations

Even with the substantial upgrade this tier represents, several categories remain firmly out of reach. Being honest about these boundaries prevents wasting time forcing models into roles they can't fill.

**Parallel multi-agent execution on a single GPU is not practical.** A 32B model at Q4 occupies ~20GB. Running an orchestrator plus even one subagent simultaneously requires model swapping (high latency, 5–10 seconds per swap) or multiple GPUs. Single-GPU agent systems must run agents sequentially, with one model loaded at a time.

**Context windows are constrained for dense 32B models.** Qwen3-32B at Q4_K_M on 24GB caps at ~16K tokens of context. For agent tasks requiring long conversation histories or large document ingestion, this is a hard ceiling. MoE models (Qwen3-30B-A3B) achieve ~32K context, which helps, but at the cost of somewhat less reasoning depth per token.

**Frontier-level agentic coding remains out of reach.** The best 24GB models achieve ~50% on SWE-bench Verified. Frontier models (Claude Sonnet 4, Gemini 2.5 Pro) reach 60–70%+. For production-critical autonomous code generation — complex multi-file refactors, novel architectural decisions — the quality gap is real and meaningful.

**Production-quality multimodal understanding is limited.** Gemma 3 27B handles vision adequately for document processing and basic image understanding, but it substantially lags behind Qwen2.5-VL-72B and proprietary models like GPT-4o for complex visual reasoning, fine-grained chart interpretation, or video understanding.

**Long-tail factual knowledge has gaps.** 32B models carry narrower world knowledge than 70B+ models. Obscure domain queries, rare entity lookups, and highly specialized technical knowledge will show higher hallucination rates. For agent roles requiring authoritative factual recall, consider pairing the local model with RAG retrieval.

**Quantization tax is real but manageable.** Q4 quantization introduces ~2–5% benchmark degradation versus full precision across tasks. For most agent roles this is acceptable. MoE models suffer less since the active 3.3B parameters maintain proportionally higher precision. Dense 32B models at Q4 show the degradation more clearly on the most demanding reasoning tasks — this is where the 16K context limit and quantization loss compound.

## Conclusion

The 24GB VRAM tier represents the threshold where local AI agent deployment transitions from "impressive demo" to "useful tool." The key insight isn't the hardware quantization split between 3090 and 4090 — both GPUs run the same Q4_K_M formats for the models that matter here, since FP8 is too large for 27–32B models at 24GB. The real story is that **Qwen3-generation 32B models have reached the capability level of previous-generation 72B models**, and 30B MoE architectures deliver this capability at inference speeds exceeding 100 t/s.

For budget-conscious builders, the RTX 3090 at ~$800 used is the clear value play — 80% of the 4090's generation speed at under half the price, with identical model compatibility. The 4090 justifies its premium primarily through faster prompt processing (2.5–3.5×) and meaningful speedups for latency-sensitive agent loops. Both GPUs unlock roles that were genuinely infeasible at 16GB: math/science reasoning (R1-Distill-32B), production-quality coding agents (Qwen3-Coder-30B), and viable orchestration (Qwen3-32B). The 24GB tier doesn't solve everything — parallel multi-agent execution still needs multiple GPUs, and frontier-level autonomous coding remains a 70B+ capability — but it's the first point where a single consumer GPU can run agent systems that produce genuinely useful work.