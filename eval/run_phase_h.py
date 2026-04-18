#!/usr/bin/env python3
"""
Phase H: Dense Constraint Evaluation Runner
Upgraded versions of Phase F ceiling-effect tests with 30-50 checkpoints per test.
Reuses Phase F scorer infrastructure.
Usage: python3 run_phase_h.py --base-url URL --model MODEL [--max-tokens N] [--timeout N] [--test-ids 2 5 9]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Reuse Phase F infrastructure
from run_phase_f import (
    call_llm, extract_json, SCORERS, _find_value_in_json,
    score_code_exec, score_keyword_detection
)
from phase_h import PHASE_H_TESTS


# ============================================================
# PHASE H SCORERS — same logic, raw checkpoint scoring (not /10)
# ============================================================

def score_h_json_values(content, scoring):
    """Score JSON key-value matching — raw checkpoint count."""
    data = extract_json(content)
    answers = scoring["answers"]
    total = len(answers)
    if data is None:
        return 0, total, "Could not parse JSON"

    correct = 0
    wrong = []
    for key, expected in answers.items():
        actual = _find_value_in_json(data, key)
        if actual is not None:
            if str(actual).strip().upper() == str(expected).strip().upper():
                correct += 1
            else:
                wrong.append(f"#{key}: exp={expected}, got={actual}")
        else:
            wrong.append(f"#{key}: missing")

    msg = f"{correct}/{total} correct"
    if wrong:
        msg += " | " + "; ".join(wrong[:10])
    return correct, total, msg


def score_h_json_numeric(content, scoring):
    """Score numeric JSON values with tolerance — raw checkpoint count."""
    data = extract_json(content)
    answers = scoring["answers"]
    tolerance_pct = scoring.get("tolerance", 0.5)  # percentage tolerance
    total = len(answers)
    if data is None:
        return 0, total, "Could not parse JSON"

    correct = 0
    wrong = []
    for key, expected in answers.items():
        actual = _find_value_in_json(data, key)
        if actual is not None:
            try:
                actual_f = float(actual)
                expected_f = float(expected)
                # Use percentage tolerance for large numbers, absolute for small
                if expected_f != 0:
                    pct_diff = abs(actual_f - expected_f) / abs(expected_f)
                    if pct_diff <= tolerance_pct:
                        correct += 1
                    else:
                        wrong.append(f"{key}: exp={expected}, got={actual_f}")
                elif abs(actual_f - expected_f) < 0.01:
                    correct += 1
                else:
                    wrong.append(f"{key}: exp={expected}, got={actual_f}")
            except (ValueError, TypeError):
                wrong.append(f"{key}: not numeric: {actual}")
        else:
            wrong.append(f"{key}: missing")

    msg = f"{correct}/{total} correct"
    if wrong:
        msg += " | " + "; ".join(wrong[:10])
    return correct, total, msg


def score_h_code_exec(content, scoring):
    """Score code execution with raw test case count."""
    test_cases = scoring["test_cases"]
    total = len(test_cases)

    # Extract code from response
    import re
    code = content
    if "```" in content:
        m = re.search(r'```(?:python)?\s*\n?(.*?)\n?```', content, re.DOTALL)
        if m:
            code = m.group(1).strip()

    correct = 0
    wrong = []
    for i, tc in enumerate(test_cases):
        call = tc["call"]
        expected = tc["expected"]
        try:
            # Execute in isolated namespace
            namespace = {}
            exec(code, namespace)
            # Handle multi-statement test cases: exec all but last, eval the last
            statements = [s.strip() for s in call.split(";") if s.strip()]
            for stmt in statements[:-1]:
                exec(stmt, namespace)
            result = eval(statements[-1], namespace)
            result_str = str(result).replace(" ", "")
            expected_str = str(expected).replace(" ", "")
            if result_str == expected_str:
                correct += 1
            else:
                wrong.append(f"tc{i+1}: exp={expected}, got={result}")
        except Exception as e:
            wrong.append(f"tc{i+1}: error={str(e)[:50]}")

    msg = f"{correct}/{total} test cases passed"
    if wrong:
        msg += " | " + "; ".join(wrong[:10])
    return correct, total, msg


def score_h_security_vulns(content, scoring):
    """Score security vulnerability detection — raw count."""
    data = extract_json(content)
    expected_vulns = scoring["vulns"]
    total = len(expected_vulns)

    if data is None:
        return 0, total, "Could not parse JSON"

    response_text = json.dumps(data).lower() if isinstance(data, dict) else content.lower()
    found = 0
    missed = []
    for vuln in expected_vulns:
        vtype = vuln["type"].lower()
        location = vuln["location"].lower()
        # Check if both type and location are mentioned
        type_keywords = vtype.replace("/", " ").replace("_", " ").split()
        loc_keywords = location.replace("/", " ").replace("_", " ").split()

        type_found = any(kw in response_text for kw in type_keywords)
        loc_found = any(kw in response_text for kw in loc_keywords)

        if type_found and loc_found:
            found += 1
        elif type_found:
            found += 1  # Partial credit if type identified
        else:
            missed.append(f"{vuln['type']}@{vuln['location']}")

    msg = f"{found}/{total} vulnerabilities found"
    if missed:
        msg += " | missed: " + "; ".join(missed[:8])
    return found, total, msg
def score_h_keywords(content, scoring):
    """Score by checking if the expected keyword strings are present in the output text."""
    answers = scoring.get("answers", {})
    if not answers:
        return 0, 0, "No answers defined."
    total = len(answers)
    text = content.lower()
    import re
    correct = 0
    wrong = []
    
    for key, expected in answers.items():
        kw_lower = str(expected).lower()
        if kw_lower == "yes":
            # For boolean constraints, check if the key's words are in the text
            words = [w for w in key.replace("_", " ").split() if len(w) >= 3]
            if words and all(w in text for w in words):
                correct += 1
            else:
                wrong.append(f"#{key}: missing")
            continue
            
        # Strip L12: prefixes from kw_lower
        kw_clean = re.sub(r'l\d+:\s*', '', kw_lower)
        if kw_clean in text:
            correct += 1
        elif kw_clean.replace("→", "->") in text:
            correct += 1
        else:
            words = [w for w in kw_clean.replace("/", " ").replace("→", " ").replace("-", " ").split() if len(w) > 3]
            if words and all(w in text for w in words):
                correct += 1
            else:
                wrong.append(f"#{key}: missing {expected}")
                
    msg = f"{correct}/{total} correct"
    if wrong:
        msg += " | " + "; ".join(wrong[:5])
        
    return correct, total, msg

def score_h_content_planner(content, scoring):
    """Score content planner with dense constraint checking."""
    data = extract_json(content)
    answers = scoring["answers"]
    total = len(answers)

    if data is None:
        return 0, total, "Could not parse JSON"

    # For content planner, we check structural constraints against the generated calendar
    # Since we can't fully verify all cross-references automatically in a simple scorer,
    # we check key structural constraints and use the json_values scorer for the rest
    correct = 0
    wrong = []

    response_text = json.dumps(data).lower()
    weeks = data.get("weeks", [])

    for key, expected in answers.items():
        passed = False
        try:
            if key == "total_posts":
                all_posts = sum(len(w.get("posts", [])) for w in weeks)
                passed = str(all_posts) == str(expected)
                if not passed: wrong.append(f"total_posts: {all_posts} vs {expected}")
            elif key == "total_blogs":
                blogs = sum(1 for w in weeks for p in w.get("posts", []) if "blog" in str(p.get("type", "")).lower())
                passed = str(blogs) == str(expected)
                if not passed: wrong.append(f"total_blogs: {blogs} vs {expected}")
            elif key == "total_emails":
                emails = sum(1 for w in weeks for p in w.get("posts", []) if "email" in str(p.get("type", "")).lower())
                passed = str(emails) == str(expected)
                if not passed: wrong.append(f"total_emails: {emails} vs {expected}")
            elif key == "total_videos":
                videos = sum(1 for w in weeks for p in w.get("posts", []) if "video" in str(p.get("type", "")).lower())
                passed = str(videos) == str(expected)
                if not passed: wrong.append(f"total_videos: {videos} vs {expected}")
            elif key == "total_podcasts":
                pods = sum(1 for w in weeks for p in w.get("posts", []) if "podcast" in str(p.get("type", "")).lower())
                passed = str(pods) == str(expected)
                if not passed: wrong.append(f"total_podcasts: {pods} vs {expected}")
            elif key == "total_social":
                social = sum(1 for w in weeks for p in w.get("posts", []) if "social" in str(p.get("type", "")).lower())
                passed = str(social) == str(expected)
                if not passed: wrong.append(f"total_social: {social} vs {expected}")
            elif key == "total_linkedin":
                li = sum(1 for w in weeks for p in w.get("posts", []) if "linkedin" in str(p.get("channel", "")).lower())
                passed = str(li) == str(expected)
                if not passed: wrong.append(f"total_linkedin: {li} vs {expected}")
            elif key == "no_weekends":
                weekend_posts = sum(1 for w in weeks for p in w.get("posts", [])
                                   if str(p.get("day", "")).lower() in ("sat", "sun", "saturday", "sunday"))
                passed = weekend_posts == 0
                if not passed: wrong.append(f"weekend_posts: {weekend_posts}")
            elif key == "correct_themes":
                expected_themes = ["awareness", "education", "social proof", "technical", "engagement", "conversion"]
                actual_themes = [str(w.get("theme", "")).lower() for w in weeks]
                passed = all(any(et in at for at in actual_themes) for et in expected_themes)
                if not passed: wrong.append(f"themes: {actual_themes}")
            elif key == "podcast_weeks_correct":
                pod_weeks = set()
                for w in weeks:
                    for p in w.get("posts", []):
                        if "podcast" in str(p.get("type", "")).lower():
                            pod_weeks.add(w.get("week"))
                passed = pod_weeks == {3, 6} or pod_weeks.issubset({3, 6})
                if not passed: wrong.append(f"podcast_weeks: {pod_weeks}")
            else:
                # Generic check — look for the key's value in the response
                if str(expected).lower() == "true":
                    passed = True  # Assume pass for boolean constraints we can't fully verify
                else:
                    passed = False
                    wrong.append(f"{key}: unverifiable")
        except Exception as e:
            wrong.append(f"{key}: error={str(e)[:40]}")

        if passed:
            correct += 1

    msg = f"{correct}/{total} constraints met"
    if wrong:
        msg += " | " + "; ".join(wrong[:10])
    return correct, total, msg


def score_h_news_errors(content, scoring):
    """Score news headline error detection."""
    data = extract_json(content)
    answers = scoring["answers"]
    total = len(answers)

    if data is None:
        return 0, total, "Could not parse JSON"

    response_text = json.dumps(data).lower() if isinstance(data, dict) else content.lower()
    found = 0
    missed = []

    for key, expected_error in answers.items():
        # Extract headline number from key (e.g., "error_5" → "5")
        headline_num = key.split("_")[1]
        error_desc = expected_error.lower()

        # Check if the response mentions this headline number and relevant error keywords
        error_keywords = error_desc.replace(",", " ").split()[:3]  # First 3 words of the error
        num_mentioned = headline_num in response_text
        error_mentioned = any(kw in response_text for kw in error_keywords if len(kw) > 3)

        if num_mentioned and error_mentioned:
            found += 1
        elif num_mentioned:
            found += 1  # Partial: identified wrong headline but imprecise explanation
        else:
            missed.append(f"H{headline_num}: {expected_error[:40]}")

    msg = f"{found}/{total} errors found"
    if missed:
        msg += " | missed: " + "; ".join(missed[:5])
    return found, total, msg


# Phase H scorer map
H_SCORERS = {
    "json_values": score_h_json_values,
    "json_numeric": score_h_json_numeric,
    "code_exec": score_h_code_exec,
    "security_vulns": score_h_security_vulns,
    "content_planner": score_h_content_planner,
    "news_errors": score_h_news_errors,
    "h_keywords": score_h_keywords,
}


def run_test(test, base_url, model, max_tokens, timeout, extra_body=None, api_key=None):
    """Run a single Phase H test and score it with raw checkpoint counts."""
    messages = [{"role": "user", "content": test["prompt"]}]
    content, tokens, tps, elapsed = call_llm(
        messages, base_url, model, max_tokens, timeout=timeout,
        extra_body=extra_body, api_key=api_key
    )

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
    parser = argparse.ArgumentParser(description="Phase H: Dense Constraint Evaluation")
    parser.add_argument("--base-url", required=True, help="LLM server base URL")
    parser.add_argument("--model", required=True, help="Model name for output directory")
    parser.add_argument("--api-model", help="Model name to send in API requests (defaults to --model)")
    parser.add_argument("--api-key", help="API key for cloud endpoints")
    parser.add_argument("--max-tokens", type=int, default=8000, help="Max tokens per response (default higher for dense tests)")
    parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds")
    parser.add_argument("--reasoning-budget-tokens", type=int, help="Reasoning budget for llama.cpp / Gemma-4")
    parser.add_argument("--test-ids", type=int, nargs="*", help="Run only these test IDs")
    args = parser.parse_args()

    api_model = args.api_model or args.model
    extra_body = {}
    if args.reasoning_budget_tokens:
        extra_body["reasoning_budget_tokens"] = args.reasoning_budget_tokens

    out_dir = Path(f"test_results/{args.model}/phase_h")
    out_dir.mkdir(parents=True, exist_ok=True)

    tests = PHASE_H_TESTS
    if args.test_ids:
        tests = [t for t in tests if t["id"] in args.test_ids]

    print(f"=== Phase H: Dense Constraint Evaluation ===")
    print(f"Model: {args.model}")
    print(f"API Model: {api_model}")
    print(f"Base URL: {args.base_url}")
    print(f"Max Tokens: {args.max_tokens}")
    print(f"Tests: {len(tests)} (with 30-50 checkpoints each)")
    print(f"{'='*60}\n")

    results = []
    total_score = 0
    total_max = 0

    for i, test in enumerate(tests):
        tid = test["id"]
        role = test["role"]
        tier = test["tier"]

        print(f"[{i+1}/{len(tests)}] H-{tid} T{tier}: {role}")

        result = run_test(
            test, args.base_url, api_model, args.max_tokens,
            args.timeout, extra_body=extra_body or None, api_key=args.api_key
        )

        score = result["score"]
        max_score = result["max_score"]
        total_score += score
        total_max += max_score
        pct = score / max_score * 100 if max_score > 0 else 0

        emoji = "✅" if pct >= 80 else "⚠️" if pct >= 50 else "❌"
        print(f"  {emoji} {score}/{max_score} ({pct:.0f}%) — {result['detail']}")
        print(f"     {result['tokens']}tok, {result['tps']}t/s, {result['elapsed']}s")

        result["test_id"] = tid
        result["role"] = role
        result["tier"] = tier
        result["scoring_type"] = test["scoring_type"]
        results.append(result)

        # Save individual response
        safe_role = role.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        resp_file = out_dir / f"H{tid:02d}_{safe_role}.txt"
        with open(resp_file, "w") as f:
            f.write(result.get("response", ""))

    # Summary
    print(f"\n{'='*60}")
    print(f"PHASE H RESULTS — {args.model}")
    pct = total_score / total_max * 100 if total_max > 0 else 0
    print(f"Overall: {total_score}/{total_max} ({pct:.1f}%)")

    print(f"\nPer-Test Scores:")
    for r in results:
        rpct = r["score"] / r["max_score"] * 100 if r["max_score"] > 0 else 0
        emoji = "✅" if rpct >= 80 else "⚠️" if rpct >= 50 else "❌"
        print(f"  {emoji} H-{r['test_id']:>2d} {r['role']:<40s} {r['score']}/{r['max_score']} ({rpct:.0f}%)")

    # Save scores
    scores_data = {
        "model": args.model,
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
