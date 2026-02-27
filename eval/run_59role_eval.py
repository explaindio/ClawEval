#!/usr/bin/env python3
"""
OpenClaw 59-Role Model Evaluation Runner
Tests the active model against all 59 OpenClaw agent roles.
Saves automated scores + raw outputs for manual quality review.
"""

import json
import time
import os
import re
import sys
import argparse
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("Run: eval/.venv/bin/pip install openai")
    sys.exit(1)

# Ensure we can import role_prompts regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from role_prompts import ROLE_TESTS

DEFAULT_BASE_URL = "http://192.168.1.9:8080/v1"
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")
NOTHINK = False  # Global flag for /nothink mode
MAX_TOKENS_OVERRIDE = 0  # Global override for max_tokens (0 = no override)


def get_client(base_url):
    return OpenAI(base_url=base_url, api_key="not-needed", timeout=600)


def get_model_name(client):
    models = client.models.list()
    return models.data[0].id if models.data else "unknown"


def timed_completion(client, model, messages, max_tokens=512, temperature=0):
    # Note: nothink mode is handled server-side via --chat-template-kwargs
    # The --nothink flag only affects output directory naming
    # Apply global token override
    if MAX_TOKENS_OVERRIDE > 0:
        max_tokens = max(max_tokens, MAX_TOKENS_OVERRIDE)
    start = time.time()
    response = client.chat.completions.create(
        model=model, messages=messages,
        max_tokens=max_tokens, temperature=temperature,
    )
    elapsed = time.time() - start
    content = response.choices[0].message.content or ""
    usage = response.usage
    return {
        "content": content,
        "elapsed_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "tokens_per_second": round((usage.completion_tokens / elapsed), 1) if usage and elapsed > 0 else 0,
    }


def extract_python_code(content):
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0]
    elif "```" in content:
        code = content.split("```")[1].split("```")[0]
    else:
        code = content
    return code.strip()


def check_json(content):
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    try:
        json.loads(cleaned)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_result(test, content):
    check_type = test.get("check", "none")
    
    if check_type == "json":
        return check_json(content)
    
    elif check_type == "contains":
        expected = test["expected"]
        if expected.lower() in content.lower():
            return True, f"Contains '{expected}'"
        return False, f"Missing '{expected}' in: {content[:80]}"
    
    elif check_type == "contains_any":
        found = [w for w in test["expected"] if w.lower() in content.lower()]
        if found:
            return True, f"Contains: {', '.join(found)}"
        return False, "Missing all expected words"
    
    elif check_type == "contains_all":
        missing = [w for w in test["expected"] if w.lower() not in content.lower()]
        if not missing:
            return True, "Contains all expected elements"
        return False, f"Missing: {', '.join(missing)}"
    
    elif check_type == "contains_pattern":
        matches = re.findall(test["pattern"], content, re.MULTILINE)
        if len(matches) >= test["min_matches"]:
            return True, f"Pattern matches: {len(matches)}"
        return False, f"Pattern matches: {len(matches)} (need {test['min_matches']})"
    
    elif check_type == "length_min":
        words = len(content.split())
        if words >= test["expected"]:
            return True, f"Length OK: {words} words"
        return False, f"Too short: {words} words (need {test['expected']})"
    
    elif check_type == "length_max":
        if len(content) <= test["expected"]:
            return True, f"Length OK: {len(content)} chars"
        return False, f"Too long: {len(content)} chars (max {test['expected']})"
    
    elif check_type == "code":
        code = extract_python_code(content)
        try:
            exec_globals = {}
            exec(code, exec_globals)
            exec(test["test_code"], exec_globals)
            result = exec_globals["test"]()
            if result:
                return True, "All tests pass"
            return False, "Tests returned False"
        except Exception as e:
            return False, f"Code error: {e}"
    
    return True, "No automated check"


def run_automated_tests(client, model, role_ids=None):
    """Run the automated-scoring prompt for each role."""
    print(f"\n{'='*70}")
    print(f"  PHASE A: AUTOMATED ROLE TESTS — {model}")
    print(f"{'='*70}")
    
    results = []
    
    tests = ROLE_TESTS
    if role_ids:
        tests = [t for t in tests if t["id"] in role_ids]
    
    total = len(tests)
    passed = 0
    
    for i, test in enumerate(tests, 1):
        role_name = test["role"]
        tier = test["tier"]
        print(f"\n  [{i:2d}/{total}] T{tier} #{test['id']:2d} {role_name}")
        
        try:
            r = timed_completion(
                client, model,
                [{"role": "user", "content": test["prompt"]}],
                max_tokens=4000, temperature=0,
            )
            
            ok, reason = check_result(test, r["content"])
            status = "✅" if ok else "❌"
            if ok:
                passed += 1
            
            print(f"         {status} {reason}  ({r['tokens_per_second']} t/s, {r['elapsed_seconds']}s)")
            
            results.append({
                "id": test["id"],
                "role": role_name,
                "tier": tier,
                "passed": ok,
                "reason": reason,
                "response": r["content"],
                "tps": r["tokens_per_second"],
                "elapsed": r["elapsed_seconds"],
                "completion_tokens": r["completion_tokens"],
            })
            
        except Exception as e:
            print(f"         ❌ ERROR: {e}")
            results.append({
                "id": test["id"], "role": role_name, "tier": tier,
                "passed": False, "reason": f"Error: {e}",
                "response": "", "tps": 0, "elapsed": 0,
            })
    
    score = round(passed / total * 100, 1)
    print(f"\n  {'='*50}")
    print(f"  AUTOMATED SCORE: {passed}/{total} = {score}%")
    
    # Per-tier breakdown
    for tier in range(1, 6):
        tier_results = [r for r in results if r["tier"] == tier]
        if tier_results:
            tier_passed = sum(1 for r in tier_results if r["passed"])
            tier_total = len(tier_results)
            print(f"    Tier {tier}: {tier_passed}/{tier_total} = {round(tier_passed/tier_total*100, 1)}%")
    
    return {
        "phase": "automated_role_tests",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "score_pct": score,
        "results": results,
    }


def run_quality_tests(client, model, role_ids=None):
    """Run the quality-review prompt for each role (saved for manual evaluation)."""
    print(f"\n{'='*70}")
    print(f"  PHASE B: QUALITY PROMPTS (for manual review) — {model}")
    print(f"{'='*70}")
    
    results = []
    
    tests = ROLE_TESTS
    if role_ids:
        tests = [t for t in tests if t["id"] in role_ids]
    
    total = len(tests)
    
    for i, test in enumerate(tests, 1):
        role_name = test["role"]
        tier = test["tier"]
        print(f"\n  [{i:2d}/{total}] T{tier} #{test['id']:2d} {role_name}")
        
        try:
            r = timed_completion(
                client, model,
                [{"role": "user", "content": test["quality_prompt"]}],
                max_tokens=4000, temperature=0.7,
            )
            
            preview = r["content"][:120].replace("\n", " ")
            print(f"         {r['completion_tokens']} tok, {r['tokens_per_second']} t/s → {preview}...")
            
            results.append({
                "id": test["id"],
                "role": role_name,
                "tier": tier,
                "prompt": test["quality_prompt"],
                "response": r["content"],
                "tps": r["tokens_per_second"],
                "elapsed": r["elapsed_seconds"],
                "completion_tokens": r["completion_tokens"],
                "manual_score": None,  # To be filled in during manual review
                "manual_notes": None,
            })
            
        except Exception as e:
            print(f"         ❌ ERROR: {e}")
            results.append({
                "id": test["id"], "role": role_name, "tier": tier,
                "prompt": test.get("quality_prompt", ""), "response": f"ERROR: {e}",
                "tps": 0, "elapsed": 0, "completion_tokens": 0,
                "manual_score": None, "manual_notes": None,
            })
    
    return {
        "phase": "quality_review_prompts",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "results": results,
    }


def save_results(model_id, phase_name, data):
    model_dir = os.path.join(RESULTS_DIR, model_id)
    os.makedirs(model_dir, exist_ok=True)
    filepath = os.path.join(model_dir, f"{phase_name}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  → Saved: {filepath}")
    return filepath


def generate_report(model_id, auto_results, quality_results):
    """Generate a human-readable markdown report."""
    model_dir = os.path.join(RESULTS_DIR, model_id)
    report_path = os.path.join(model_dir, "REPORT.md")
    
    lines = [
        f"# OpenClaw 59-Role Evaluation Report",
        f"",
        f"**Model:** {auto_results['model']}",
        f"**Date:** {auto_results['timestamp'][:10]}",
        f"**Automated Score:** {auto_results['passed']}/{auto_results['total']} = {auto_results['score_pct']}%",
        f"",
        f"---",
        f"",
        f"## Automated Test Results",
        f"",
        f"| # | Role | Tier | Pass | Speed | Notes |",
        f"|---|------|------|------|-------|-------|",
    ]
    
    for r in auto_results["results"]:
        status = "✅" if r["passed"] else "❌"
        reason = r["reason"][:50]
        lines.append(f"| {r['id']} | {r['role']} | T{r['tier']} | {status} | {r['tps']} t/s | {reason} |")
    
    lines.extend([
        f"",
        f"## Tier Breakdown",
        f"",
        f"| Tier | Passed | Total | Score |",
        f"|------|--------|-------|-------|",
    ])
    
    for tier in range(1, 6):
        tier_results = [r for r in auto_results["results"] if r["tier"] == tier]
        if tier_results:
            tp = sum(1 for r in tier_results if r["passed"])
            tt = len(tier_results)
            lines.append(f"| Tier {tier} | {tp} | {tt} | {round(tp/tt*100, 1)}% |")
    
    lines.extend([
        f"",
        f"## Quality Responses (Manual Review Needed)",
        f"",
    ])
    
    for r in quality_results["results"]:
        lines.extend([
            f"### #{r['id']} — {r['role']} (T{r['tier']})",
            f"",
            f"**Prompt:** {r['prompt'][:200]}...",
            f"",
            f"**Response ({r['completion_tokens']} tok, {r['tps']} t/s):**",
            f"",
            f"<details><summary>Click to expand</summary>",
            f"",
            f"{r['response']}",
            f"",
            f"</details>",
            f"",
            f"**Manual Score:** ___/10  **Notes:** ___",
            f"",
            f"---",
            f"",
        ])
    
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  → Report: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 59-Role Evaluation")
    parser.add_argument("--url", default=DEFAULT_BASE_URL)
    parser.add_argument("--auto-only", action="store_true", help="Run only automated tests")
    parser.add_argument("--quality-only", action="store_true", help="Run only quality prompts")
    parser.add_argument("--roles", nargs="+", type=int, help="Test specific role IDs only")
    parser.add_argument("--tier", type=int, help="Test only roles from this tier (1-5)")
    parser.add_argument("--nothink", action="store_true", help="Disable thinking with /nothink system message")
    parser.add_argument("--max-tokens", type=int, default=0, help="Override min max_tokens (e.g. 16000 for thinking models)")
    args = parser.parse_args()

    global NOTHINK, MAX_TOKENS_OVERRIDE
    NOTHINK = args.nothink
    MAX_TOKENS_OVERRIDE = args.max_tokens

    client = get_client(args.url)
    model = get_model_name(client)
    model_id = model.replace("/", "_").replace("\\", "_").replace(" ", "_")
    if args.nothink:
        model_id += "-nothink"
    
    role_ids = args.roles
    if args.tier:
        role_ids = [t["id"] for t in ROLE_TESTS if t["tier"] == args.tier]
    
    print(f"\n{'#'*70}")
    print(f"#  OpenClaw 59-Role Model Evaluation")
    print(f"#  Model: {model}")
    print(f"#  Server: {args.url}")
    print(f"#  Roles: {len(role_ids) if role_ids else 59}")
    print(f"#  Time: {datetime.now().isoformat()}")
    print(f"{'#'*70}")
    
    auto_results = None
    quality_results = None
    
    if not args.quality_only:
        auto_results = run_automated_tests(client, model, role_ids)
        save_results(model_id, "automated_scores", auto_results)
    
    if not args.auto_only:
        quality_results = run_quality_tests(client, model, role_ids)
        save_results(model_id, "quality_responses", quality_results)
    
    if auto_results and quality_results:
        generate_report(model_id, auto_results, quality_results)
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"  EVALUATION COMPLETE: {model}")
    print(f"{'='*70}")
    if auto_results:
        print(f"  Automated: {auto_results['score_pct']}% ({auto_results['passed']}/{auto_results['total']})")
        avg_tps = round(sum(r["tps"] for r in auto_results["results"]) / len(auto_results["results"]), 1)
        print(f"  Avg speed: {avg_tps} t/s")
    if quality_results:
        print(f"  Quality responses: {len(quality_results['results'])} saved for review")
    print(f"  Results: {os.path.join(RESULTS_DIR, model_id)}/")


if __name__ == "__main__":
    main()
