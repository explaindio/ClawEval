"""Re-run empty quality responses for Qwen3-14B with max_tokens=16000."""
import json, sys, time, os, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from role_prompts import ROLE_TESTS
from openai import OpenAI
from datetime import datetime

BASE_URL = 'http://192.168.1.9:8080/v1'
client = OpenAI(base_url=BASE_URL, api_key='not-needed', timeout=900)
model = client.models.list().data[0].id
model_id = model.replace('/', '_').replace(' ', '_')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_results')
model_dir = os.path.join(RESULTS_DIR, model_id)

print(f'Model: {model}', flush=True)
print(f'Model ID: {model_id}', flush=True)

# IDs to re-run (empty or minimal responses)
RERUN_IDS = [8, 22, 45, 46, 47, 48]
MAX_TOKENS = 16000

# Load existing quality_responses.json
qr_path = os.path.join(model_dir, 'quality_responses.json')
with open(qr_path) as f:
    quality_data = json.load(f)

print(f'\nLoaded {len(quality_data["results"])} existing quality responses', flush=True)
print(f'Re-running IDs: {RERUN_IDS} with max_tokens={MAX_TOKENS}', flush=True)
print(f'{"="*70}', flush=True)

# Build lookup of tests by ID
tests_by_id = {t['id']: t for t in ROLE_TESTS}

for rid in RERUN_IDS:
    test = tests_by_id[rid]
    print(f'\n  [{rid}/59] T{test["tier"]} #{rid} {test["role"]}', flush=True)
    print(f'         Starting... (max_tokens={MAX_TOKENS}, timeout=900s)', flush=True)

    start = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': test['quality_prompt']}],
            max_tokens=MAX_TOKENS,
            temperature=0.7,
        )
        elapsed = round(time.time() - start, 2)
        content = r.choices[0].message.content or ''
        tps = round(r.usage.completion_tokens / elapsed, 1) if elapsed > 0 else 0
        words = len(content.split()) if content.strip() else 0
        tok = r.usage.completion_tokens

        status = '✅' if words > 0 else '⬜'
        preview = content[:120].replace('\n', ' ') if content.strip() else '(still empty)'
        print(f'         {status} {tok} tok, {words} words, {tps} t/s, {elapsed}s', flush=True)
        print(f'         {preview}...', flush=True)

        # Update the result in quality_data
        for i, result in enumerate(quality_data['results']):
            if result['id'] == rid:
                quality_data['results'][i] = {
                    'id': rid,
                    'role': test['role'],
                    'tier': test['tier'],
                    'prompt': test['quality_prompt'],
                    'response': content,
                    'tps': tps,
                    'elapsed': elapsed,
                    'completion_tokens': tok,
                    'manual_score': None,
                    'manual_notes': None,
                }
                break

    except Exception as e:
        elapsed = round(time.time() - start, 2)
        print(f'         ❌ ERROR after {elapsed}s: {e}', flush=True)
        traceback.print_exc()

# Save updated quality_responses.json
quality_data['rerun_note'] = f'IDs {RERUN_IDS} re-run at {datetime.now().isoformat()} with max_tokens={MAX_TOKENS}'
with open(qr_path, 'w') as f:
    json.dump(quality_data, f, indent=2, ensure_ascii=False)
print(f'\n→ Saved updated quality_responses.json', flush=True)

# Print summary
print(f'\n{"="*70}', flush=True)
print(f'  RE-RUN COMPLETE', flush=True)
print(f'{"="*70}', flush=True)
empty = sum(1 for r in quality_data['results'] if not r['response'].strip())
print(f'  Remaining empty: {empty}', flush=True)
for r in quality_data['results']:
    if r['id'] in RERUN_IDS:
        words = len(r['response'].split()) if r['response'].strip() else 0
        status = '✅' if words > 0 else '⬜'
        print(f'  {status} #{r["id"]} {r["role"]}: {words} words, {r["completion_tokens"]} tok', flush=True)
