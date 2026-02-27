#!/usr/bin/env python3
"""
Phase D: Hard Evaluation Runner
Runs adversarial, verifiable prompts against a model and scores responses.
Usage: python3 run_phase_d.py --base-url URL --model MODEL [--max-tokens N] [--thinking]
"""

import argparse
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import requests

from hard_prompts import HARD_TESTS


def call_llm(prompt, base_url, model, max_tokens=4000, timeout=600, nothink=False):
    """Call the model and return response content."""
    headers = {"Content-Type": "application/json", "Authorization": "Bearer not-needed"}
    messages = []
    # Note: nothink mode is handled server-side via --chat-template-kwargs
    # The --nothink flag only affects output directory naming
    messages.append({"role": "user", "content": prompt})
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    start = time.time()
    try:
        r = requests.post(f"{base_url}/chat/completions", headers=headers, json=body, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        elapsed = time.time() - start
        tokens = data.get("usage", {}).get("completion_tokens", 0)
        tps = tokens / elapsed if elapsed > 0 else 0
        return content, tokens, round(tps, 1), round(elapsed, 1)
    except Exception as e:
        elapsed = time.time() - start
        return f"ERROR: {e}", 0, 0, round(elapsed, 1)


def auto_score_exact(content, scoring_data):
    """Score exact-answer tests. Returns (score, max_score, details)."""
    answers = scoring_data.get("answers", {})
    if not answers:
        # Single answer check
        answer = str(scoring_data.get("answer", ""))
        alts = scoring_data.get("answer_alt", [])
        found = answer.lower() in content.lower() or any(a.lower() in content.lower() for a in alts)
        return (10, 10, "Correct answer found") if found else (0, 10, f"Expected '{answer}' not found")

    # Multi-answer check (e.g., classification)
    correct = 0
    total = len(answers)
    details = []
    for num, expected in answers.items():
        # Look for patterns like "1": "category" or 1: category or 1. category
        patterns = [
            rf'"{num}"\s*:\s*"{expected}"',
            rf'"{num}"\s*:\s*"{expected.replace("_", " ")}"',
            rf'{num}[.:)\s]+\s*{expected}',
            rf'{num}[.:)\s]+\s*{expected.replace("_", " ")}',
        ]
        found = any(re.search(p, content, re.IGNORECASE) for p in patterns)
        if found:
            correct += 1
        else:
            details.append(f"#{num}: expected '{expected}'")
    score = round(correct / total * 10)
    return score, 10, f"{correct}/{total} correct" + (f" | Missing: {'; '.join(details)}" if details else "")


def auto_score_constraint(content, scoring_data):
    """Score constraint-based tests. Returns (score, max_score, details)."""
    checks = 0
    passed = 0
    details = []

    content_lower = content.lower()

    # Check for required identifications
    for key in ["must_identify", "contradictions", "must_find_all", "conflicts", "red_flags",
                 "critical_issues", "fraud_transactions"]:
        items = scoring_data.get(key, [])
        if isinstance(items, list) and items:
            for item in items:
                checks += 1
                # Check if the concept is mentioned (fuzzy match)
                # Split on underscores since constraint items use snake_case
                keywords = item.lower().replace("_", " ").split()
                # At least half the words should appear
                found = sum(1 for w in keywords if w in content_lower)
                if found >= max(1, len(keywords) // 2):
                    passed += 1
                else:
                    details.append(f"Missing: {item}")

    # Check boolean flags
    for key in ["must_flag_contradictions", "must_deduplicate", "must_identify_false_positive",
                 "must_say_not_in_context", "must_not_hallucinate", "must_identify_bot_pattern",
                 "must_identify_overtraining", "must_spot_fraud", "must_identify_keyword_cannibalization",
                 "must_catch_seo_spam", "must_handle_conflicts", "must_catch_data_inconsistency",
                 "must_detect_circular", "must_catch_survivorship_bias", "must_identify_unrealistic_assumption",
                 "must_identify_contradiction_between_agents", "must_catch_impossible_schedule",
                 "must_find_hidden_clause", "must_catch_drug_interaction", "must_flag_inconsistency",
                 "must_catch_red_flag", "must_find_subtle", "must_identify_cascade",
                 "must_identify_race_condition", "must_identify_contradictory_requirements",
                 "must_catch_jurisdiction_conflict", "must_identify_data_flow_violation",
                 "must_identify_confound", "must_catch_bug"]:
        if scoring_data.get(key):
            checks += 1
            # These are hard to automatically verify — give credit if response is substantial
            if len(content) > 200:
                passed += 1
            else:
                details.append(f"Response too short for {key}")

    # Check for traps
    trap = scoring_data.get("trap")
    if trap:
        checks += 1
        trap_words = trap.lower().replace("_", " ").split()
        found = sum(1 for w in trap_words if w in content_lower)
        if found >= max(1, len(trap_words) // 3):
            passed += 1
        else:
            details.append(f"Trap not identified: {trap}")

    if checks == 0:
        return 5, 10, "No automated constraints to check"

    score = round(passed / checks * 10)
    return score, 10, f"{passed}/{checks} constraints met" + (f" | {'; '.join(details[:3])}" if details else "")


def auto_score_code(content, scoring_data):
    """Score code tests by actually executing them. Returns (score, max_score, details)."""
    test_code = scoring_data.get("test_code", "")
    if not test_code:
        return 5, 10, "No test code provided"

    # Extract function from response
    code_match = re.search(r'(?:```python\s*)?((?:def \w+.*?)(?:```|\Z))', content, re.DOTALL)
    if not code_match:
        # Try without code block
        code_match = re.search(r'(def \w+\(.*?\n(?:[ \t]+.*\n)*)', content, re.DOTALL)

    if not code_match:
        return 0, 10, "No function found in response"

    func_code = code_match.group(1).replace('```', '').strip()

    try:
        ns = {}
        exec(func_code, ns)
        exec(test_code, ns)
        if ns.get('test') and ns['test']():
            return 10, 10, "All tests passed"
        else:
            return 3, 10, "Test function returned False"
    except AssertionError as e:
        return 3, 10, f"Assertion failed: {e}"
    except Exception as e:
        return 1, 10, f"Execution error: {e}"


def score_response(test, content):
    """Auto-score a response based on scoring_type."""
    scoring_type = test.get("scoring_type", "manual")
    scoring_data = test.get("scoring_data", {})

    if scoring_type == "exact":
        return auto_score_exact(content, scoring_data)
    elif scoring_type == "constraint":
        return auto_score_constraint(content, scoring_data)
    elif scoring_type == "code":
        return auto_score_code(content, scoring_data)
    else:
        # Manual scoring — just check if response is substantial
        word_count = len(content.split())
        if word_count < 50:
            return 2, 10, f"Very short response ({word_count} words)"
        elif word_count < 200:
            return 5, 10, f"Brief response ({word_count} words)"
        else:
            return 7, 10, f"Substantial response ({word_count} words) — needs manual review"


def main():
    parser = argparse.ArgumentParser(description="Phase D Hard Evaluation")
    parser.add_argument("--base-url", required=True, help="LLM API base URL")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max tokens (default 4000, use 16000 for thinking models)")
    parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds")
    parser.add_argument("--nothink", action="store_true", help="Disable thinking with /nothink system message")
    parser.add_argument("--start-id", type=int, default=1, help="Start from this test ID")
    parser.add_argument("--end-id", type=int, default=59, help="End at this test ID")
    args = parser.parse_args()

    # Create output directory
    model_slug = args.model.replace("/", "_")
    if args.nothink:
        model_slug += "-nothink"
    results_dir = Path(f"test_results/{model_slug}")
    results_dir.mkdir(parents=True, exist_ok=True)

    hard_dir = results_dir / "phase_d_hard"
    hard_dir.mkdir(exist_ok=True)

    print(f"=== Phase D Hard Evaluation ===")
    print(f"Model: {args.model}")
    print(f"Base URL: {args.base_url}")
    print(f"Max Tokens: {args.max_tokens}")
    print(f"Output: {hard_dir}")
    print(f"Tests: {args.start_id}-{args.end_id}")
    print("=" * 40)

    results = []
    total_score = 0
    total_max = 0

    for test in HARD_TESTS:
        tid = test["id"]
        if tid < args.start_id or tid > args.end_id:
            continue

        role = test["role"]
        tier = test["tier"]
        prompt = test["hard_prompt"]

        print(f"\n[{tid}/59] T{tier} — {role}", flush=True)
        print(f"  Sending prompt ({len(prompt)} chars)...", flush=True)

        content, tokens, tps, elapsed = call_llm(
            prompt, args.base_url, args.model, args.max_tokens, args.timeout, nothink=args.nothink
        )

        if content.startswith("ERROR:"):
            print(f"  ❌ {content}", flush=True)
            score, max_score, detail = 0, 10, content
        else:
            word_count = len(content.split())
            print(f"  ✓ {word_count} words, {tokens} tokens, {tps} t/s, {elapsed}s", flush=True)
            score, max_score, detail = score_response(test, content)
            print(f"  Score: {score}/{max_score} — {detail}", flush=True)

        total_score += score
        total_max += max_score

        result = {
            "id": tid,
            "role": role,
            "tier": tier,
            "scoring_type": test["scoring_type"],
            "auto_score": score,
            "max_score": max_score,
            "detail": detail,
            "word_count": len(content.split()) if not content.startswith("ERROR:") else 0,
            "tokens": tokens,
            "tps": tps,
            "elapsed": elapsed,
        }
        results.append(result)

        # Save individual response
        resp_file = hard_dir / f"{tid:02d}_{role.replace(' / ', '_').replace(' ', '_')}.txt"
        with open(resp_file, "w") as f:
            f.write(f"# Phase D Hard Test — #{tid} {role}\n")
            f.write(f"# Tier: {tier} | Score: {score}/{max_score} | {detail}\n")
            f.write(f"# Tokens: {tokens} | Speed: {tps} t/s | Time: {elapsed}s\n\n")
            f.write(f"## PROMPT:\n{prompt}\n\n")
            f.write(f"## RESPONSE:\n{content}\n")

    # Save summary
    summary = {
        "model": args.model,
        "timestamp": datetime.now().isoformat(),
        "max_tokens": args.max_tokens,
        "total_score": total_score,
        "total_max": total_max,
        "percentage": round(total_score / total_max * 100, 1) if total_max > 0 else 0,
        "results": results,
    }

    # Tier breakdown
    tier_scores = {}
    for r in results:
        t = r["tier"]
        if t not in tier_scores:
            tier_scores[t] = {"score": 0, "max": 0, "count": 0}
        tier_scores[t]["score"] += r["auto_score"]
        tier_scores[t]["max"] += r["max_score"]
        tier_scores[t]["count"] += 1

    summary["tier_breakdown"] = {}
    for t in sorted(tier_scores):
        ts = tier_scores[t]
        summary["tier_breakdown"][f"T{t}"] = {
            "score": ts["score"],
            "max": ts["max"],
            "percentage": round(ts["score"] / ts["max"] * 100, 1) if ts["max"] > 0 else 0,
            "count": ts["count"],
        }

    with open(hard_dir / "hard_scores.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 50)
    print(f"PHASE D RESULTS — {args.model}")
    print(f"Overall: {total_score}/{total_max} ({summary['percentage']}%)")
    print("\nTier Breakdown:")
    for t, ts in summary["tier_breakdown"].items():
        print(f"  {t}: {ts['score']}/{ts['max']} ({ts['percentage']}%) [{ts['count']} tests]")
    print(f"\nResults saved to: {hard_dir}")


if __name__ == "__main__":
    main()
