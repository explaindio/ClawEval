# 🦞 ClawEval — Handoff: Testing Small Qwen3.5 Models (8/12/16GB VRAM)

## Project Overview

**ClawEval** is a deterministic benchmark for evaluating LLMs as AI agents across 59 specialized roles. Located at `/Users/andrew/Documents/AAAPPS5/OpenClaw`. GitHub: `AIgenteur/ClawEval`.

The project tests models in two main phases:
- **Phase F** — 59 role-specific hard tests with automated scoring (exact JSON, code exec, keyword detection, constraints). ~590 max points.
- **Phase G** — 11 discriminator tests (harder versions of Phase F tests that separate model quality). ~110 max points.

Both phases use `run_phase_f.py` and `run_phase_g.py` which send prompts to an OpenAI-compatible API endpoint and score responses deterministically.

---

## What Has Been Done

### Cloud Models Tested (all via Alibaba Coding Plan API)
All use base URL: `https://coding-intl.dashscope.aliyuncs.com/v1`
API Key: `sk-sp-cba45834aa314899aa5b2a24b48cf367`

| Model | Phase F Score | Phase G Score | NoThink |
|-------|:---:|:---:|---|
| **Qwen3.5-Plus** (NT) 🥇 | **482/590 (82%)** | 86/110 (78%) | `enable_thinking: false` (root) |
| **Qwen3.5-Plus** (Think) | 465/590 (79%) | 86/110 (78%) | — |
| **Kimi K2.5** (Think) | 473/590 (80%) | **96/110 (87%)** 🥇 | `thinking: False` in `chat_template_kwargs` |
| **Kimi K2.5** (NoThink) | 469/590 (80%) | 91/110 (83%) | — |
| **GLM-5** (Think) | 465/590 (79%) | 76/110 (69%) | `enable_thinking: false` (root) |
| **GLM-5** (NoThink) | 461/590 (78%) | 80/110 (73%) | — |
| **MiniMax-M2.5** (Think only) | 465/590 (79%) | 78/110 (71%) | NOT SUPPORTED |

### Local Models Tested (24GB + 64-96GB VRAM)
- **Qwen3.5-27B Q4_K_M** — via llama.cpp
- **Qwen3.5-35B-A3B** — via SGLang (Think mode has overflow bug) and llama.cpp (NoThink)
- **Qwen3.5-122B-A10B** — via SGLang (NVFP4)
- **GPT-OSS-120B** — via llama.cpp (GGUF)

### Documentation Files
- `README.md` — Main page with "Best Model Per Role" tables for 24GB, 64-96GB, and Cloud tiers
- `docs/results-cloud.md` — All cloud model Phase F comparison (7 columns) + speed data + Phase G summary
- `docs/results-phase-g.md` — Phase G discriminator results for local (24GB, 64-96GB) and cloud
- `docs/results-24gb-vram.md` — 24GB local model comparison
- `docs/results-64-96gb-vram.md` — 64-96GB local model comparison
- `docs/results-phase-e.md` — Phase E (12 killer tests)
- `RESULTS.md` — Full detailed results with all configs

---

## What Is Next: Small Qwen3.5 Models

### Models to Test
These are newly released small Qwen3.5 models to test on local hardware (user will provide server IP):

1. **Qwen3.5-0.8B** — fits 8GB VRAM
2. **Qwen3.5-2B** — fits 8-12GB VRAM  
3. **Qwen3.5-4B** — fits 12GB VRAM
4. **Qwen3.5-9B** — fits 16GB VRAM

### Testing Protocol
For each model, run:
1. **Phase F** (59 role tests) — main scoring
2. **Phase G** (11 discriminator tests) — harder tests

For each, test both **Think** and **NoThink** modes if supported.

### New Documentation: `docs/results-small-vram.md`
Create a new results page for small VRAM tiers with a table like:

```markdown
# Small VRAM Models — Phase F (59-Role Evaluation)

| # | Agent Role | 0.8B | 2B | 4B | 9B |
|---|---|---|---|---|---|
| | | Qwen3.5-0.8B | Qwen3.5-2B | Qwen3.5-4B | Qwen3.5-9B |
| | **Tier 1 — Utility** | | | | |
| 1 | Router / Triage | ... | ... | ... | ... |
...
```

### Update README.md
Add a new VRAM tier section to the main "Best Model Per Role" table. The README currently has columns for `🟢 Best 24GB` and `🔵 Best 64–96GB`. Add columns for `🟡 8GB`, `🟡 12GB`, `🟡 16GB` or combine into a single `🟡 Best Small` column showing the best small model per role.

The VRAM tier table at top of README (lines 21-25) should be updated to include the small models:

```markdown
| 🔴 8GB VRAM | 🟡 12GB VRAM | 🟡 16GB VRAM | 🟢 24GB VRAM | 🔵 64–96GB VRAM |
|---|---|---|---|---|
| Qwen3.5-0.8B, Qwen3.5-2B | Qwen3.5-4B | Qwen3.5-9B | Qwen3.5-35B-A3B ... | Qwen3.5-122B-A10B ... |
```

---

## How to Run Tests

### Phase F (59-Role Tests) — Local Server
```bash
cd /Users/andrew/Documents/AAAPPS5/OpenClaw/eval

# Think mode (default)
python3 -u run_phase_f.py \
  --base-url http://<SERVER_IP>:<PORT>/v1 \
  --model qwen3.5-0.8b-think \
  --max-tokens 4000 \
  --timeout 120 2>&1

# NoThink mode (for models that support it)
python3 -u run_phase_f.py \
  --base-url http://<SERVER_IP>:<PORT>/v1 \
  --model qwen3.5-0.8b-nothink \
  --nothink \
  --max-tokens 4000 \
  --timeout 120 2>&1
```

Key flags:
- `--model` = output directory name (e.g., `qwen3.5-0.8b-think`)
- `--api-model` = model name in API (only needed if different from `--model`)
- `--nothink` = Kimi-style (`chat_template_kwargs.thinking=False`)
- `--nothink-root` = GLM/Qwen-style (`enable_thinking: false` at root)
- `--api-key` = for cloud APIs only
- `--delay` = seconds between tests (for rate-limited APIs)
- `--test-ids 1 2 3` = run specific tests only
- `--timeout` = per-request timeout in seconds

Results saved to: `eval/test_results/<model>/phase_f/phase_f_scores.json`

### Phase G (11 Discriminator Tests) — Local Server
```bash
cd /Users/andrew/Documents/AAAPPS5/OpenClaw/eval

python3 -u run_phase_g.py \
  --base-url http://<SERVER_IP>:<PORT>/v1 \
  --model qwen3.5-0.8b-think \
  --max-tokens 8000 \
  --timeout 300 2>&1
```

Or use inline script for better error handling (recommended, especially for small models that may timeout):

```python
cd /Users/andrew/Documents/AAAPPS5/OpenClaw/eval && python3 -u -c "
import json, time, random, traceback
from pathlib import Path
from run_phase_g import run_test, PHASE_G_TESTS

base_url = 'http://<SERVER_IP>:<PORT>/v1'
model = '<MODEL_NAME>'
out_dir = Path('test_results/<OUTPUT_DIR>/phase_g')
out_dir.mkdir(parents=True, exist_ok=True)

results = []
total_s = total_m = 0

for i, test in enumerate(PHASE_G_TESTS):
    tid = test['id']
    role = test['role']
    if i > 0:
        wait = 5 + random.randint(0, 3)
        print(f'  Waiting {wait}s...', flush=True)
        time.sleep(wait)
    
    print(f'[{i+1}/11] G-{tid}: {role}', flush=True)
    try:
        r = run_test(test, base_url, model, 8000, 300)
        s, m = r['score'], r['max_score']
        total_s += s; total_m += m
        e = 'OK' if s >= 8 else 'WARN' if s >= 5 else 'FAIL'
        print(f'  {e} {s}/{m}', flush=True)
        
        safe = role.replace(' ','_').replace('/','_')
        with open(out_dir / f'G{tid:02d}_{safe}.txt', 'w') as f:
            f.write(r.get('response',''))
        results.append({'id':tid,'role':role,'tier':test['tier'],'scoring_type':test['scoring']['type'],'score':s,'max':m,'detail':r['detail'],'tokens':r['tokens']})
    except Exception as e:
        traceback.print_exc()
        results.append({'id':tid,'role':role,'tier':test['tier'],'scoring_type':test['scoring']['type'],'score':0,'max':10,'detail':f'ERROR: {e}','tokens':0})
        total_m += 10

with open(out_dir / 'phase_g_scores.json', 'w') as f:
    json.dump({'model':'<OUTPUT_DIR>','total_score':total_s,'total_max':total_m,'results':results}, f, indent=2)
print(f'\nTOTAL: {total_s}/{total_m} ({total_s/total_m*100:.1f}%)', flush=True)
" 2>&1
```

---

## Scoring System

- Scores are out of 10 per role (59 roles × 10 = 590 max for Phase F)
- Phase G has 11 tests × 10 = 110 max
- Emojis: 🟢 = 8-10, 🟡 = 5-7, 🔴 = 0-4, 📝 = Manual review (defaults to 5/10)
- 6 tests require manual review (#10, #17, #24, #34, #41, #58) — always show as 📝 5
- `†` suffix means Phase G discriminator score is used

## Table Formatting Conventions

### Best Model Per Role Tables (README.md)
```markdown
| # | Agent Role | 🟡 Best Small | | 🟢 Best 24GB | | 🔵 Best 64–96GB | |
|---|---|---|---|---|---|---|---|
| | | **Model** | **Score** | **Model** | **Score** | **Model** | **Score** |
| 1 | Router / Triage | Qwen3.5-9B | 🟢 8 | 27B / 35B NT | 🟢 10 | 122B Think | 🟢 10 |
```

### Detailed Comparison Tables (docs/*.md)
```markdown
| # | Role | 0.8B | 2B | 4B | 9B |
|---|---|---|---|---|---|
| 1 | Router / Triage | 🔴 2 | 🟡 5 | 🟡 7 | 🟢 9 |
```

### Speed & Efficiency Table
```markdown
| Model | Score | Total Tokens | Avg Tok/Test | Speed |
|-------|-------|:---:|:---:|:---:|
| **0.8B** | X/590 (X%) | XK | X | ~X t/s |
```

---

## Known Issues & Quirks

1. **Scoring Bug:** Social Media Scouting (#16) can report 20/10 — cap at 10 using `min(score, 10)`
2. **Calendar (#8):** All models score 0/10 — the test is extremely hard
3. **Recipe (#31):** Most models score 0-2/10 — Qwen3.5+ NT uniquely scored 9/10
4. **SGLang thinking bug:** `thinking_budget` not enforced for some models — causes think overflow (⏱️)
5. **GLM-5 Financial:** Returns decimals (0.40) instead of percentages (40.0) — model behavior, not parser fault
6. **STEM without thinking:** Models that rely on reasoning score 0/10 on STEM (#48) in NoThink mode

## Git Workflow
```bash
cd /Users/andrew/Documents/AAAPPS5/OpenClaw
git add -A && git commit -m 'descriptive message' && git push
```

## File Locations
- Project root: `/Users/andrew/Documents/AAAPPS5/OpenClaw`
- Eval scripts: `eval/run_phase_f.py`, `eval/run_phase_g.py`
- Test definitions: `eval/phase_f/` (59 tests), `eval/phase_g/` (11 tests)
- Test results: `eval/test_results/<model>/phase_f/phase_f_scores.json`
- Documentation: `docs/results-cloud.md`, `docs/results-phase-g.md`, `docs/results-24gb-vram.md`, etc.
- README: `README.md` (main page with summary tables)

## SmokeDisk Test Before Running
Always verify the local server works before starting a full run:
```bash
python3 -c "
import requests
resp = requests.post('http://<SERVER_IP>:<PORT>/v1/chat/completions',
    headers={'Content-Type': 'application/json'},
    json={'model': '<MODEL>', 'messages': [{'role': 'user', 'content': 'Reply only: hello'}], 'max_tokens': 50},
    timeout=10)
print(f'Status: {resp.status_code}')
print(f'Body: {resp.text[:300]}')
"
```

---

## Summary of Next Steps

1. **User will provide:** Server IP, port, and model names for the 4 small Qwen3.5 models
2. **For each model** (0.8B, 2B, 4B, 9B):
   a. Smoke test the endpoint
   b. Run Phase F Think mode
   c. Run Phase F NoThink mode (if supported)
   d. Run Phase G Think mode
   e. Run Phase G NoThink mode (if supported)
3. **Create** `docs/results-small-vram.md` with comparison tables
4. **Update** `README.md` with new VRAM tier columns (8GB, 12GB, 16GB)
5. **Update** `docs/results-phase-g.md` with small model Phase G scores
6. **Commit and push** after each model or batch of results
