# ClawEval (OpenClaw) — AI Braindump

> This file exists so a new AI assistant can pick up this project with full context.
> Last updated: 2026-05-04

---

## 1. What Is This Project?

**ClawEval** (repo name `OpenClaw`) is a **benchmark framework for evaluating LLM agent capabilities**. It tests how well models follow structured instructions across 59 diverse agentic roles (coding, writing, analysis, planning, etc.) with dense constraint scoring.

- **GitHub**: `AIgenteur/ClawEval`
- **Branch**: `master` (all work happens here)
- **Owner**: Andrew (user)

---

## 2. Project Structure

```
OpenClaw/
├── README.md                    # Main README with 36-model leaderboard
├── .env                         # API keys (Ollama cloud, OpenRouter free tier, Alibaba)
├── eval/
│   ├── run_phase_h.py           # MAIN test runner — 59-test agentic suite
│   ├── run_phase_f.py           # Phase F (predecessor, reused for scorers)
│   ├── phase_h.py               # Test definitions (PHASE_H_TESTS array)
│   ├── openrouter_keys.py       # Multi-key rotation for OpenRouter free tier
│   └── test_results/            # All model results (one dir per model)
│       ├── <ModelName>/phase_h/
│       │   ├── H01_Router___Triage_Agent.txt   # Raw model output per test
│       │   ├── ...
│       │   └── phase_h_scores.json             # Aggregated scores
│       └── ...
├── docs/
│   ├── results-phase-h.md       # Full Phase H results & per-agent breakdown
│   ├── results-rtx3090-24gb.md  # RTX 3090 local leaderboard (17 models)
│   ├── results-turboquant.md    # TurboQuant KV-cache experiment
│   ├── results-local-tps.md     # Tokens/second benchmarks
│   └── ...                      # Various VRAM tier guides
└── BRAINDUMP.md                 # ← This file
```

---

## 3. How To Run Tests

### Basic command
```bash
cd eval/
python3 run_phase_h.py \
  --base-url "http://192.168.0.187:8080/v1" \
  --model "ModelDisplayName" \
  --api-model "actual/model-id" \
  --max-tokens 16000 \
  --timeout 300
```

### Key flags
| Flag | Purpose |
|------|---------|
| `--model` | Display name (used for directory + reports) |
| `--api-model` | Actual model ID sent to the API |
| `--test-ids 10 12 48` | Run ONLY specific test IDs (for retests) |
| `--api-key KEY` | API key for cloud endpoints |
| `--reasoning-budget-tokens N` | For thinking models (sets `reasoning_budget_tokens` in extra_body) |
| `--max-tokens N` | Max tokens per response (default 8000) |
| `--timeout N` | Seconds per test before giving up |

### For thinking models
```bash
python3 run_phase_h.py \
  --base-url "http://192.168.0.187:8080/v1" \
  --model "ModelName-Think" \
  --api-model "model/id" \
  --max-tokens 16000 \
  --timeout 600 \
  --reasoning-budget-tokens 4000
```

### For cloud models (Ollama)
```bash
python3 run_phase_h.py \
  --base-url "https://ollama.com/v1" \
  --model "ModelName" \
  --api-model "model-name:cloud" \
  --api-key "$(grep OLLAMA_API_KEY .env | cut -d= -f2)" \
  --max-tokens 16000
```

---

## 4. Scoring System

- **59 tests**, each with 7–60 checkpoints
- **Total max score: 1220 points**
- Tests cover: routing, validation, sentiment, coding, writing, DevOps, legal, medical, finance, etc.
- Scoring types: JSON field matching, keyword detection, code execution, constraint counting
- Results saved to `eval/test_results/<ModelName>/phase_h/`

---

## 5. Current Leaderboard (36 models, as of 2026-05-04)

| # | Model | Score | % |
|---|-------|-------|---|
| 1 | DeepSeek V4 Pro | 1060/1220 | 86.9% |
| 2 | DeepSeek V4 Flash | 1054/1220 | 86.4% |
| 3 | Kimi K2.5 Think | 1048/1220 | 85.9% |
| 4 | Qwen3.5-Plus | 1031/1220 | 84.5% |
| 5 | Qwen3.6-35B-A3B (local) | 1029/1220 | 84.3% |
| ... | | | |
| 36 | Qwen3.5-2B | 50/1220 | 4.1% |

Full leaderboard is in `README.md` lines 137-174.

---

## 6. Infrastructure

### Local GPU (RTX 3090 24GB)
- **IP**: `192.168.0.187:8080` (LAN)
- **Backend**: llama.cpp (upstream or TurboQuant fork)
- **API**: OpenAI-compatible (`/v1/chat/completions`)
- **Auth**: none
- **User loads models manually** — always wait for user to confirm model is loaded before running tests

### Cloud APIs
- **Ollama Cloud**: `https://ollama.com/v1` + `OLLAMA_API_KEY` from `.env`
- **OpenRouter Free**: 13 keys in `.env` for rotation (for free-tier models)
- **Alibaba (Qwen)**: `ALIBABA_API_KEY` in `.env`, base URL `https://coding-intl.dashscope.aliyuncs.com/v1`

---

## 7. Critical Rules & Lessons Learned

### ⚠️ NEVER rate a model on infrastructure failures
- Always check for `500 Server Error`, `Connection refused`, `ERROR:`, `Response ended prematurely` in results
- If found, those tests MUST be rerun — they don't count as model failures
- Use `--test-ids` to rerun only the failed tests
- Audit command: `grep -rl "500 Server Error" eval/test_results/ModelName/phase_h/H*.txt`

### ⚠️ Thinking models underperform at small sizes
- Sub-30B thinking models waste tokens on CoT, leaving nothing for the actual answer
- Always compare Think vs NoThink/Instruct variants
- Pattern confirmed across Qwen3.5, Ministral-3 at 3B/8B/9B — thinking only helps at ≥30B MoE

### ⚠️ Token ceiling issues
- If many tests show exactly `16000tok` — the model hit the max_tokens ceiling
- For thinking models, increase `--max-tokens` and/or `--reasoning-budget-tokens`

### ⚠️ Quantization gap
- Larger models are more resilient to Q4 quantization
- 3B: ~7% gap (cloud vs local Q4), 8B: ~2% gap

---

## 8. TurboQuant Experiment

TurboQuant compresses KV cache from 8-bit to 3-bit. Model weights unchanged.
- Allows massive context expansion (32K → 262K) on same GPU
- Tested on 2 models:
  - **Gemma-4-31B (dense)**: baseline 76.0% → TQ3 83.1% (+7.1%, 4.9× ctx)
  - **Qwen3.6-35B-A3B (MoE)**: baseline 84.3% → TQ3 80.0% (-4.3%, 8× ctx, +22% speed)
- Full docs: `docs/results-turboquant.md`

---

## 9. Files To Edit When Adding a New Model

1. **Run the test** → results auto-save to `eval/test_results/<ModelName>/`
2. **README.md** → Add to leaderboard table (sorted by score, fix rank numbers)
3. **docs/results-rtx3090-24gb.md** → If local model, add to local leaderboard + TPS table
4. **docs/results-turboquant.md** → If TurboQuant experiment
5. **git add -A && git commit && git push**

### Leaderboard rank numbering
- Ranks must be sequential (1, 2, 3...) sorted by score descending
- Watch for duplicate rank numbers after insertions — common error

---

## 10. Pending / Incomplete Work

### Infra retest queue (COMPLETED as of 2026-05-04)
All infrastructure errors have been resolved. Every remaining zero in the leaderboard is a confirmed model failure.

### Models already fully tested (don't re-run)
- `nvidia/nemotron-3-super-120b-a12b` — tested both Think (83.3%) and NoThink (81.6%)
- All 36 models in the leaderboard have been run and pushed

---

## 11. .env Keys Reference

```
ALIBABA_API_KEY=sk-sp-...        # Qwen cloud
OLLAMA_API_KEY=ac2f77...         # Ollama cloud (MiniMax, Nemotron-Super, etc.)
FREE_OPENROUTER_API_KEY_1..13    # OpenRouter free tier rotation
```

---

## 12. Quick Audit Commands

```bash
# Check for infra errors across all models
for d in eval/test_results/*/phase_h; do
  model=$(dirname "$d" | xargs basename)
  count=$(grep -rl "500 Server Error\|Connection refused\|ERROR:" "$d"/H*.txt 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "$model: $count infra failures"
done

# Count total models
grep "^\|" README.md | grep -c "Local\|Ollama\|OpenRouter\|DeepSeek\|Alibaba"

# Check a model's zeros
grep "(0%)" eval/test_results/ModelName/phase_h/*.log

# Check if model hit token ceiling
grep "16000tok" /tmp/model_log.log | wc -l
```
