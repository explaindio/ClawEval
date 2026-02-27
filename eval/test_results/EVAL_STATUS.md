# ClawEval — Evaluation Status

## Phase E & F Coverage

| Model | Server | Phase E | Phase F | Notes |
|---|---|---|---|---|
| **Qwen3.5-122B-A10B NVFP4** (think 16K) | SGLang | ✅ 108/120 (90%) | ✅ ~443/590 (75.1%) | Best overall |
| **Qwen3.5-122B-A10B NVFP4** (nothink) | SGLang | ✅ 79/120 (66%) | ❌ TODO re-run | Was split run + old scorers, needs clean single run |
| **Qwen3.5-35B-A3B Q4_K_M** (think) | llama.cpp | ✅ 102/120 (85%) | ✅ 405/582 (70%) | 10 tests 32K overflow — needs re-run on vLLM/SGLang |
| **Qwen3.5-35B-A3B Q4_K_M** (nothink) | llama.cpp | ✅ 76/120 (63%) | ❌ TODO | |
| **Qwen3.5-27B Q4_K_M** (nothink) | llama.cpp | ✅ 83/120 (69%) | ❌ TODO | |
| **Qwen3.5-27B Q4_K_M** (think) | llama.cpp | ❌ TODO | ❌ TODO | Blocked: no think cap on llama.cpp |

## Skipped Models (older Qwen3, replaced by Qwen3.5)

| Model | Phases Completed | Reason Skipped |
|---|---|---|
| Gemma-3-27B QAT Q4 | A–C | Different architecture, not Qwen family |
| GPT-OSS-20B MXFP4 | A–C | Smaller model, superseded |
| Qwen3-14B Q4_K_M | A–C | Replaced by Qwen3.5 series |
| Qwen3-30B-A3B Q4_K_M | A–C | Replaced by Qwen3.5-35B-A3B |

## Pending: 35B-A3B Think Overflow Re-runs

The following 10 tests hit 32K max_tokens overflow on llama.cpp (unlimited thinking, no `thinking_budget` support). Re-run on vLLM or SGLang when the model is supported with `thinking_budget: 16384`:

| # | Role | Reason |
|---|---|---|
| 3 | Heartbeat / Health Monitor | 32K overflow |
| 9 | Research / Web Search Agent | 32K overflow |
| 13 | Email Drafting / Summarization | 32K overflow |
| 22 | Data Analysis Agent | 32K overflow |
| 27 | Sprint / Project Summarizer | 32K overflow |
| 28 | Transaction / Approval Agent | 32K overflow |
| 31 | Recipe / Cooking Agent | 32K overflow |
| 32 | Personal Finance Tracking | 32K overflow |
| 42 | Market Research Agent | 32K overflow |
| 57 | SRE / Incident Response | 32K overflow |
