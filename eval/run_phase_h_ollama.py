#!/usr/bin/env python3
"""
Phase H runner for Ollama Cloud API (api.ollama.com/api/chat).
Same scoring as run_phase_h.py but adapted for Ollama's native API format.

Usage:
  python3 run_phase_h_ollama.py --model kimi-k2.6 --output-name "Kimi-K2.6" [--test-ids 1 2 3]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# Reuse Phase H infrastructure
sys.path.insert(0, os.path.dirname(__file__))
from run_phase_f import extract_json, _find_value_in_json
from run_phase_h import H_SCORERS, PHASE_H_TESTS


def load_env(path=".env"):
    """Load .env file into os.environ."""
    for candidate in [path, os.path.join(os.path.dirname(__file__), '..', '.env')]:
        if os.path.exists(candidate):
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())
            return


def call_ollama(messages, model, max_tokens=8000, timeout=600):
    """Call Ollama Cloud /api/chat with streaming to avoid Cloudflare 524 timeouts."""
    key = os.environ.get('OLLAMA_API_KEY', '')
    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }
    body = {
        'model': model,
        'messages': messages,
        'stream': True,
        'options': {
            'num_predict': max_tokens,
            'temperature': 0.1,
        }
    }

    start = time.time()
    try:
        r = requests.post(
            'https://api.ollama.com/api/chat',
            headers=headers, json=body, timeout=timeout, stream=True
        )
        r.raise_for_status()

        content = ''
        tokens = 0
        for line in r.iter_lines():
            if line:
                d = json.loads(line)
                chunk = d.get('message', {}).get('content', '')
                content += chunk
                if d.get('done'):
                    tokens = d.get('eval_count', 0)
                    break

        # Strip think tags
        if '</think>' in content:
            content = content.split('</think>')[-1].strip()
        elif '<think>' in content:
            content = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

        elapsed = time.time() - start
        tps = tokens / elapsed if elapsed > 0 else 0
        return content, tokens, round(tps, 1), round(elapsed, 1)
    except Exception as e:
        elapsed = time.time() - start
        return f"ERROR: {e}", 0, 0, round(elapsed, 1)


def run_test(test, model, max_tokens, timeout):
    """Run a single Phase H test via Ollama Cloud and score it."""
    messages = [{"role": "user", "content": test["prompt"]}]
    content, tokens, tps, elapsed = call_ollama(messages, model, max_tokens, timeout)

    scoring = test["scoring"]
    stype = test.get("scoring_type", scoring.get("type"))
    scorer = H_SCORERS.get(stype)

    if scorer:
        score, max_score, detail = scorer(content, scoring)
    else:
        score, max_score, detail = 0, 0, f"Unknown scoring type: {stype}"

    return {
        "score": score,
        "max_score": max_score,
        "detail": detail,
        "tokens": tokens,
        "tps": tps,
        "elapsed": elapsed,
        "response": content,
    }


def main():
    parser = argparse.ArgumentParser(description="Phase H via Ollama Cloud")
    parser.add_argument("--model", required=True, help="Ollama Cloud model name (e.g. kimi-k2.6)")
    parser.add_argument("--output-name", required=True, help="Output directory name (e.g. Kimi-K2.6)")
    parser.add_argument("--max-tokens", type=int, default=8000)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--test-ids", type=int, nargs="*", help="Run only these test IDs")
    args = parser.parse_args()

    load_env()

    tests = PHASE_H_TESTS
    if args.test_ids:
        tests = [t for t in tests if t["id"] in args.test_ids]

    out_dir = Path(f"test_results/{args.output_name}/phase_h")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Phase H: Ollama Cloud — {args.output_name} ===")
    print(f"Model: {args.model}")
    print(f"Tests: {len(tests)}")
    print(f"Max Tokens: {args.max_tokens}")
    print(f"{'='*60}\n")

    results = []
    total_score = 0
    total_max = 0

    for i, test in enumerate(tests):
        tid = test["id"]
        role = test["role"]
        tier = test["tier"]

        print(f"[{i+1}/{len(tests)}] H-{tid} T{tier}: {role}")

        result = run_test(test, args.model, args.max_tokens, args.timeout)

        score = result["score"]
        max_score = result["max_score"]
        total_score += score
        total_max += max_score
        pct = score / max_score * 100 if max_score > 0 else 0

        emoji = "✅" if pct >= 80 else "⚠️" if pct >= 50 else "❌"
        print(f"  {emoji} {score}/{max_score} ({pct:.0f}%) — {result['detail'][:120]}")
        print(f"     {result['tokens']}tok, {result['tps']}t/s, {result['elapsed']}s")

        result["test_id"] = tid
        result["role"] = role
        result["tier"] = tier
        result["scoring_type"] = test.get("scoring_type", test["scoring"]["type"])
        results.append(result)

        # Save individual response
        safe_role = role.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        resp_file = out_dir / f"H{tid:02d}_{safe_role}.txt"
        with open(resp_file, "w") as f:
            f.write(result.get("response", ""))

    # Summary
    print(f"\n{'='*60}")
    print(f"PHASE H RESULTS — {args.output_name}")
    pct = total_score / total_max * 100 if total_max > 0 else 0
    print(f"Overall: {total_score}/{total_max} ({pct:.1f}%)")

    print(f"\nPer-Test Scores:")
    for r in results:
        rpct = r["score"] / r["max_score"] * 100 if r["max_score"] > 0 else 0
        emoji = "✅" if rpct >= 80 else "⚠️" if rpct >= 50 else "❌"
        print(f"  {emoji} H-{r['test_id']:>2d} {r['role']:<40s} {r['score']}/{r['max_score']} ({rpct:.0f}%)")

    # Save scores
    scores_data = {
        "model": args.output_name,
        "phase": "H",
        "timestamp": datetime.now().isoformat(),
        "total_score": total_score,
        "total_max": total_max,
        "percentage": round(pct, 1),
        "results": [
            {
                "id": r["test_id"], "role": r["role"], "tier": r["tier"],
                "scoring_type": r["scoring_type"],
                "score": r["score"], "max": r["max_score"],
                "detail": r["detail"], "tokens": r["tokens"],
            }
            for r in results
        ]
    }

    scores_file = out_dir / "phase_h_scores.json"
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)

    print(f"\nResults saved to: {scores_file}")


if __name__ == "__main__":
    main()
