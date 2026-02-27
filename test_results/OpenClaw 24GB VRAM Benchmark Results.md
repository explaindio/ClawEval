# OpenClaw 24GB VRAM Benchmark Results

**Hardware**: NVIDIA RTX 3090 24GB | 32GB System RAM  
**Backend**: llama.cpp b8128 (Vulkan)  
**Date**: 2026-02-22  
**Context testing**: All models tested with 2K-step granularity

---

## Results Summary

### Sorted by Token Generation TPS (Short Context)

| ID | Model | Quant | VRAM (GB) | PP TPS | TG TPS | Max Ctx | Architecture |
|----|-------|-------|-----------|--------|--------|---------|-------------|
| A3 | GPT-oss-20B | MXFP4 | 11.27 | 3,747 | **155.0** | 32K | MoE |
| B2 | Qwen3-Coder-30B-A3B | Q4_K_M | 17.28 | 3,563 | **151.5** | 24K | MoE |
| B1 | Qwen3-30B-A3B | Q4_K_M | 17.35 | 3,531 | **149.2** | 24K | MoE |
| B8 | Nemotron 3 Nano 30B | Q4_K_M | 22.88 | 2,832 | **148.2** | 4K | MoE |
| A0 | Qwen3-14B | Q4_K_M | 8.99 | 2,384 | **66.7** | 43K | Dense |
| A1 | Qwen3-14B | Q6_K | 11.28 | 2,187 | **57.0** | 35K | Dense |
| A2 | Qwen3-14B | Q8_0 | 14.61 | 2,382 | **49.4** | 27K | Dense |
| A4 | Gemma 3 27B IT QAT | Q4_0 | 14.54 | 713 | **40.0** | 45K | Dense |
| B6Q4 | Gemma 3 27B IT | Q4_K_M | ~15.0 | ~983 | **~32.5** | 41K | Dense |
| B5 | EXAONE 4.0.1 32B | Q4_K_M | 18.01 | 1,121 | **31.6** | 24K | Dense |
| B3 | Qwen3-32B | Q4_K_M | 18.40 | 1,099 | **31.6** | 8K | Dense |
| B4 | DeepSeek-R1-32B | Q4_K_M | 18.48 | 1,150 | **31.4** | 12K | Dense |
| B6 | Gemma 3 27B IT | Q6_K | 20.64 | 983 | **28.0** | 12K | Dense |
| B7 | Seed-OSS-36B | Q4_K_M | 20.26 | 1,002 | **27.9** | 6K | Dense |

### TPS at Maximum Stable Context

| ID | Model | Max Ctx | PP TPS @Max | TG TPS @Max |
|----|-------|---------|-------------|-------------|
| A0 | Qwen3-14B Q4_K_M | 43K | 521 | 65.2 |
| A1 | Qwen3-14B Q6_K | 35K | 513 | 56.2 |
| A2 | Qwen3-14B Q8_0 | 27K | 1,031 | 49.0 |
| A3 | GPT-oss-20B | 32K | 460 | 150.4 |
| A4 | Gemma 3 27B QAT | 45K | 713 | 40.0 |
| B1 | Qwen3-30B-A3B | 24K | 1,231 | 146.2 |
| B2 | Qwen3-Coder-30B-A3B | 24K | 1,224 | 150.1 |
| B3 | Qwen3-32B | 8K | 662 | 31.1 |
| B4 | DeepSeek-R1-32B | 12K | 798 | 30.9 |
| B5 | EXAONE 4.0.1 32B | 24K | 709 | 31.1 |
| B6 | Gemma 3 27B IT Q6_K | 12K | 875 | 27.8 |
| B6Q4 | Gemma 3 27B IT Q4_K_M | 41K | ~750 | ~32.5 |
| B7 | Seed-OSS-36B | 6K | 749 | 27.6 |
| B8 | Nemotron 3 Nano 30B | 4K | 2,701 | 145.8 |

---

## Context Window: Native vs VRAM-Limited

All models were tested starting from their full native context, stepping down in 2K increments until stable. Only A3 reaches its full native window — all others are VRAM-constrained:

| ID | Model | Quant | VRAM (GB) | Native Ctx | Achieved on 24GB | Limited by |
|----|-------|-------|-----------|-----------|------------------|------------|
| A0 | Qwen3-14B | Q4_K_M | 8.99 | 128K | **43K** | VRAM |
| A1 | Qwen3-14B | Q6_K | 11.28 | 128K | **35K** | VRAM |
| A2 | Qwen3-14B | Q8_0 | 14.61 | 128K | **27K** | VRAM |
| A3 | GPT-oss-20B | MXFP4 | 11.27 | 32K | **32K** | ✅ Full |
| A4 | Gemma 3 27B QAT | Q4_0 | 14.54 | 128K | **45K** | VRAM |
| B1 | Qwen3-30B-A3B | Q4_K_M | 17.35 | 128K | **24K** | VRAM |
| B2 | Qwen3-Coder-30B-A3B | Q4_K_M | 17.28 | 128K | **24K** | VRAM |
| B3 | Qwen3-32B | Q4_K_M | 18.40 | 128K | **8K** | VRAM |
| B4 | DeepSeek-R1-32B | Q4_K_M | 18.48 | 128K | **12K** | VRAM |
| B5 | EXAONE 4.0.1 32B | Q4_K_M | 18.01 | 32K | **24K** | VRAM |
| B6 | Gemma 3 27B IT | Q6_K | 20.64 | 128K | **12K** | VRAM |
| B6Q4 | Gemma 3 27B IT | Q4_K_M | ~15.0 | 128K | **41K** | VRAM |
| B7 | Seed-OSS-36B | Q4_K_M | 20.26 | 128K | **6K** | VRAM |
| B8 | Nemotron 3 Nano 30B | Q4_K_M | 22.88 | 128K | **4K** | VRAM |

---

## Key Findings

### MoE Models Dominate Performance
The Mixture-of-Experts (MoE) models deliver **4-5x faster token generation** than dense models of similar size:
- **MoE average**: ~150 TG TPS  
- **Dense average**: ~35 TG TPS

### Best Overall: A3 (GPT-oss-20B MXFP4)
- Fastest TG TPS (155 t/s) with only 11.27 GB VRAM
- Full 32K context window (native max)
- Best combination of speed, context, and VRAM efficiency

### Best Coding Model: B2 (Qwen3-Coder-30B-A3B)
- 151.5 TG TPS with 24K context
- MoE architecture keeps it fast despite 30B parameters
- Code-specialized training

### Best Context Window: A4 (Gemma 3 27B IT QAT)
- 45K context — highest of any model tested
- 40 TG TPS is usable for interactive work
- QAT (Quantization-Aware Training) preserves quality at Q4_0

### Best Dense Model: A0 (Qwen3-14B Q4_K_M)
- 66.7 TG TPS with 43K context
- Only 8.99 GB VRAM — leaves plenty of headroom
- Best speed + context balance for a dense model

### Quantization Impact: B6 vs B6Q4
Same model (Gemma 3 27B IT), different quants:
- **Q6_K**: 20.64 GB VRAM, 12K context, 28 TPS
- **Q4_K_M**: ~15 GB VRAM, 41K context, ~32 TPS
- Q4_K_M delivers **3.4x more context** with similar TPS — always prefer Q4_K_M on 24GB

### Dense 32B Models: Tight Fit
All dense 32B models (B3, B4, B5) use 18+ GB VRAM for weights alone, leaving very little for KV cache. They are limited to 8-24K context and run at ~31 TG TPS.

### Diminishing Returns on Quantization (Qwen3-14B)
| Quant | VRAM | TG TPS | Max Context |
|-------|------|--------|-------------|
| Q4_K_M | 8.99 GB | 66.7 | 43K |
| Q6_K | 11.28 GB | 57.0 | 35K |
| Q8_0 | 14.61 GB | 49.4 | 27K |

Higher quantization trades speed AND context for marginal quality gains on 24GB.

---

## Recommendations

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| **General chat** | A3 GPT-oss-20B | Fastest + full 32K native context |
| **Coding** | B2 Qwen3-Coder-30B-A3B | Code-tuned MoE + 151 TPS + 24K ctx |
| **Long documents** | A4 Gemma 3 27B QAT | 45K context, highest of all models |
| **Reasoning** | B4 DeepSeek-R1-32B | R1-distilled reasoning, 12K ctx |
| **Best value** | A0 Qwen3-14B Q4_K_M | 66.7 TPS + 43K ctx, only 9GB |
| **Large + long ctx** | B6Q4 Gemma 3 27B Q4_K_M | 27B dense + 41K context |
