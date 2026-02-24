"""59-role evaluation for Gemma 3 27B IT QAT (Q4_0).
Gemma 3 is NOT a thinking model — standard max_tokens should work fine.
Phase A: max_tokens=2000, temperature=0
Phase B: max_tokens=4000, temperature=0.7
"""
import json, sys, time, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from role_prompts import ROLE_TESTS
from openai import OpenAI
from datetime import datetime

BASE_URL = 'http://192.168.1.9:8080/v1'
client = OpenAI(base_url=BASE_URL, api_key='not-needed', timeout=600)
model = client.models.list().data[0].id
model_id = model.replace('/', '_').replace(' ', '_')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_results')

print(f'Model: {model}', flush=True)
print(f'Model ID: {model_id}', flush=True)

def timed_completion(msgs, max_tokens=2000, temperature=0):
    start = time.time()
    r = client.chat.completions.create(
        model=model, messages=msgs,
        max_tokens=max_tokens, temperature=temperature,
    )
    elapsed = time.time() - start
    content = r.choices[0].message.content or ''
    tps = round(r.usage.completion_tokens / elapsed, 1) if elapsed > 0 else 0
    return {
        'content': content, 'elapsed': round(elapsed, 2),
        'completion_tokens': r.usage.completion_tokens,
        'tokens_per_second': tps,
    }

def check_result(test, content):
    check = test.get('check', 'contains')
    if not content.strip():
        return False, 'Empty response'
    if check == 'json':
        try:
            json.loads(content)
            return True, 'Valid JSON'
        except Exception:
            m = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', content, re.DOTALL)
            if m:
                try:
                    json.loads(m.group(1))
                    return True, 'Valid JSON (extracted from code block)'
                except Exception:
                    pass
            return False, 'Invalid JSON'
    elif check == 'table':
        if '|' in content and '---' in content:
            return True, 'Contains markdown table'
        return False, 'No table found'
    elif check == 'code':
        test_code = test.get('test_code', '')
        if test_code:
            code_match = re.search(r'(?:```python\s*)?(def \w+.*?)(?:```|\Z)', content, re.DOTALL)
            if code_match:
                func_code = code_match.group(1)
                try:
                    ns = {}
                    exec(func_code, ns)
                    exec(test_code, ns)
                    if ns.get('test') and ns['test']():
                        return True, 'Code passes all tests'
                except Exception as e:
                    return False, f'Code error: {e}'
            return False, 'No function found'
        has_code = ('```' in content or 'def ' in content)
        return has_code, 'Contains code' if has_code else 'No code block'
    elif check == 'contains':
        expected = test.get('expected', [])
        if isinstance(expected, str):
            expected = [expected]
        found = sum(1 for e in expected if e.lower() in content.lower())
        if not expected:
            has_content = bool(content.strip())
            return has_content, 'Has content' if has_content else 'Empty'
        return found == len(expected), f'Found {found}/{len(expected)} keywords'
    has_content = bool(content.strip())
    return has_content, 'Has content' if has_content else 'Empty'

# Phase A: Automated tests
print(f"\n{'='*70}", flush=True)
print(f'  PHASE A: AUTOMATED ROLE TESTS — {model}', flush=True)
print(f"{'='*70}", flush=True)

results_a = []
total = len(ROLE_TESTS)
passed = 0

for i, test in enumerate(ROLE_TESTS, 1):
    role_name = test['role']
    tier = test['tier']
    print(f'\n  [{i:2d}/{total}] T{tier} #{test["id"]:2d} {role_name}', flush=True)
    try:
        r = timed_completion(
            [{'role': 'user', 'content': test['prompt']}],
            max_tokens=2000, temperature=0,
        )
        ok, reason = check_result(test, r['content'])
        status = '✅' if ok else '❌'
        if ok:
            passed += 1
        print(f'         {status} {reason}  ({r["tokens_per_second"]} t/s, {r["elapsed"]}s)', flush=True)
        results_a.append({
            'id': test['id'], 'role': role_name, 'tier': tier,
            'passed': ok, 'reason': reason,
            'response': r['content'], 'tps': r['tokens_per_second'],
            'elapsed': r['elapsed'], 'completion_tokens': r['completion_tokens'],
        })
    except Exception as e:
        print(f'         ❌ ERROR: {e}', flush=True)
        results_a.append({
            'id': test['id'], 'role': role_name, 'tier': tier,
            'passed': False, 'reason': f'Error: {e}',
            'response': '', 'tps': 0, 'elapsed': 0, 'completion_tokens': 0,
        })

score = round(passed / total * 100, 1)
print(f"\n  {'='*50}", flush=True)
print(f'  AUTOMATED SCORE: {passed}/{total} = {score}%', flush=True)
for tier in range(1, 6):
    tr = [r for r in results_a if r['tier'] == tier]
    if tr:
        tp = sum(1 for r in tr if r['passed'])
        print(f'    Tier {tier}: {tp}/{len(tr)} = {round(tp/len(tr)*100, 1)}%', flush=True)

auto_data = {
    'phase': 'automated_role_tests', 'model': model,
    'timestamp': datetime.now().isoformat(),
    'total': total, 'passed': passed, 'score_pct': score,
    'results': results_a,
}

model_dir = os.path.join(RESULTS_DIR, model_id)
os.makedirs(model_dir, exist_ok=True)
with open(os.path.join(model_dir, 'automated_scores.json'), 'w') as f:
    json.dump(auto_data, f, indent=2, ensure_ascii=False)
print(f'\n  → Saved automated_scores.json', flush=True)

# Phase B: Quality tests
print(f"\n{'='*70}", flush=True)
print(f'  PHASE B: QUALITY PROMPTS (for review) — {model}', flush=True)
print(f"{'='*70}", flush=True)

results_b = []
for i, test in enumerate(ROLE_TESTS, 1):
    role_name = test['role']
    tier = test['tier']
    print(f'\n  [{i:2d}/{total}] T{tier} #{test["id"]:2d} {role_name}', flush=True)
    try:
        r = timed_completion(
            [{'role': 'user', 'content': test['quality_prompt']}],
            max_tokens=4000, temperature=0.7,
        )
        words = len(r['content'].split())
        preview = r['content'][:120].replace('\n', ' ')
        print(f'         {r["completion_tokens"]} tok, {words} words, {r["tokens_per_second"]} t/s', flush=True)
        print(f'         {preview}...', flush=True)
        results_b.append({
            'id': test['id'], 'role': role_name, 'tier': tier,
            'prompt': test['quality_prompt'], 'response': r['content'],
            'tps': r['tokens_per_second'], 'elapsed': r['elapsed'],
            'completion_tokens': r['completion_tokens'],
            'manual_score': None, 'manual_notes': None,
        })
    except Exception as e:
        print(f'         ❌ ERROR: {e}', flush=True)
        results_b.append({
            'id': test['id'], 'role': role_name, 'tier': tier,
            'prompt': test.get('quality_prompt', ''), 'response': f'ERROR: {e}',
            'tps': 0, 'elapsed': 0, 'completion_tokens': 0,
            'manual_score': None, 'manual_notes': None,
        })

quality_data = {
    'phase': 'quality_review_prompts', 'model': model,
    'timestamp': datetime.now().isoformat(),
    'total': total, 'results': results_b,
}
with open(os.path.join(model_dir, 'quality_responses.json'), 'w') as f:
    json.dump(quality_data, f, indent=2, ensure_ascii=False)
print(f'\n  → Saved quality_responses.json', flush=True)

# Final summary
print(f"\n{'='*70}", flush=True)
print(f'  EVALUATION COMPLETE: {model}', flush=True)
print(f"{'='*70}", flush=True)
print(f'  Automated: {score}% ({passed}/{total})', flush=True)
avg_tps_a = round(sum(r["tps"] for r in results_a) / len(results_a), 1) if results_a else 0
print(f'  Avg speed (auto): {avg_tps_a} t/s', flush=True)
empty_b = sum(1 for r in results_b if not r['response'].strip())
short_b = sum(1 for r in results_b if r['response'].strip() and len(r['response'].split()) < 50)
print(f'  Quality responses saved: {len(results_b)} ({empty_b} empty, {short_b} short <50w)', flush=True)
print(f'  Results: {model_dir}/', flush=True)
