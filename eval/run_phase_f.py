#!/usr/bin/env python3
"""
Phase F: 59-Role Deterministic Hard Evaluation Runner
Runs all 59 tests with automated + manual scoring.
Usage: python3 run_phase_f.py --base-url URL --model MODEL [--max-tokens N] [--timeout N] [--test-ids 1 2 3]
"""

import argparse
import json
import math
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from phase_f import PHASE_F_TESTS


def call_llm(messages, base_url, model, max_tokens=4000, timeout=120, extra_body=None, api_key=None):
    """Send messages and return response content."""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key or 'not-needed'}"}
    body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.1}
    if extra_body:
        body.update(extra_body)
    start = time.time()
    try:
        r = requests.post(f"{base_url}/chat/completions", headers=headers, json=body, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        # Strip SGLang thinking content — model may output </think> with no opening tag
        if "</think>" in content:
            content = content.split("</think>")[-1].strip()
        elif "<think>" in content:
            content = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()
        elapsed = time.time() - start
        tokens = data.get("usage", {}).get("completion_tokens", 0)
        tps = tokens / elapsed if elapsed > 0 else 0
        return content, tokens, round(tps, 1), round(elapsed, 1)
    except Exception as e:
        elapsed = time.time() - start
        return f"ERROR: {e}", 0, 0, round(elapsed, 1)


def extract_json(text):
    """Extract JSON from response text, handling markdown code fences."""
    text = text.strip()
    if "```" in text:
        m = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if m:
            text = m.group(1).strip()
    try:
        return json.loads(text)
    except:
        pass
    for pattern in [r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', r'\[.*\]']:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except:
                pass
    # Try finding deeply nested JSON
    try:
        start = text.index('{')
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{': depth += 1
            elif text[i] == '}': depth -= 1
            if depth == 0:
                return json.loads(text[start:i+1])
    except:
        pass
    return None


# ============================================================
# GENERIC SCORERS
# ============================================================

def _find_value_in_json(data, key):
    """Flexibly find a value in JSON — handles case-insensitive keys, nested dicts, composite keys."""
    if not isinstance(data, dict):
        return None
    key_lower = key.lower()
    # Direct match (case-insensitive)
    for k, v in data.items():
        if k.lower() == key_lower:
            return v
    # Try underscore-split: "1_category" → look for "1" then "category" in nested dicts
    if "_" in key:
        parts = key.split("_", 1)
        # Try data[parts[0]][parts[1]]
        for k, v in data.items():
            if k.lower() == parts[0].lower() and isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2.lower() == parts[1].lower():
                        return v2
        # Try data[any_container][parts[0]][parts[1]] (e.g. tickets.1.category)
        for k, v in data.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2.lower() == parts[0].lower() and isinstance(v2, dict):
                        for k3, v3 in v2.items():
                            if k3.lower() == parts[1].lower():
                                return v3
    # Try nested: look inside all sub-dicts
    for k, v in data.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                if k2.lower() == key_lower:
                    return v2
                # One more level: data["scores"]["1"]["value"]
                if isinstance(v2, dict):
                    for k3, v3 in v2.items():
                        if k3.lower() == key_lower:
                            return v3
    return None

def score_json_values(content, scoring):
    """Score exact JSON value matches with flexible key lookup."""
    data = extract_json(content)
    answers = scoring["answers"]
    if data is None:
        return 0, len(answers), "Could not parse JSON"

    correct = 0
    details = []
    for key, expected in answers.items():
        actual = _find_value_in_json(data, key)

        if actual is not None:
            # Flexible comparison
            if str(actual).lower().strip() == str(expected).lower().strip():
                correct += 1
            elif isinstance(expected, bool) and actual == expected:
                correct += 1
            else:
                details.append(f"{key}: expected {expected}, got {actual}")
        else:
            details.append(f"{key}: not found")

    total = len(answers)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_json_numeric(content, scoring):
    """Score numeric JSON values with tolerance and flexible key lookup."""
    data = extract_json(content)
    answers = scoring["answers"]
    tolerance = scoring.get("tolerance", 0.01)
    if data is None:
        return 0, len(answers), "Could not parse JSON"

    correct = 0
    details = []
    for key, expected in answers.items():
        actual = _find_value_in_json(data, key)
        if actual is not None:
            # Handle string values in numeric context
            if isinstance(expected, str):
                if str(actual).lower().strip() == expected.lower().strip():
                    correct += 1
                else:
                    details.append(f"{key}: expected {expected}, got {actual}")
            elif isinstance(expected, bool):
                if actual == expected:
                    correct += 1
                else:
                    details.append(f"{key}: expected {expected}, got {actual}")
            else:
                try:
                    act_val = float(str(actual).replace(",", "").replace("$", "").replace("%", ""))
                    if abs(act_val - float(expected)) <= tolerance:
                        correct += 1
                    else:
                        details.append(f"{key}: expected {expected}, got {actual}")
                except (ValueError, TypeError):
                    details.append(f"{key}: not numeric: {actual}")
        else:
            details.append(f"{key}: missing")

    total = len(answers)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_error_count(content, scoring):
    """Score error detection by checking if the right number and types of errors found."""
    data = extract_json(content)
    expected_errors = scoring["expected_errors"]

    if data is None:
        # Fallback: count keyword matches in text
        found = sum(1 for err in expected_errors if err.lower() in content.lower())
        score = round(found / len(expected_errors) * 10)
        return score, 10, f"Fallback: {found}/{len(expected_errors)} error keywords found"

    # Check error count
    errors = data.get("errors", [])
    if isinstance(errors, list):
        found = 0
        for exp in expected_errors:
            for err in errors:
                err_text = str(err).lower() if isinstance(err, str) else json.dumps(err).lower()
                if exp.lower() in err_text:
                    found += 1
                    break
        score = round(found / len(expected_errors) * 10)
        return score, 10, f"{found}/{len(expected_errors)} errors found"

    return 0, 10, "No errors array found"


def score_keyword_detection(content, scoring, field_name="issues"):
    """Generic scorer: checks if keywords appear in the full response text.
    Each keyword can match if any significant word from it appears in the content."""
    keywords = scoring.get(field_name, scoring.get("issues", scoring.get("bugs", scoring.get("vulns", scoring.get("findings", [])))))
    content_lower = content.lower()

    found = 0
    details = []
    for kw in keywords:
        if isinstance(kw, dict):
            kw_text = kw.get("keyword", kw.get("text", ""))
        else:
            kw_text = kw
        kw_lower = kw_text.lower()
        # Try exact substring first
        if kw_lower in content_lower:
            found += 1
        else:
            # Flexible: check if all significant words (>3 chars) from the keyword appear
            words = [w for w in kw_lower.split() if len(w) > 3]
            if words and all(w in content_lower for w in words):
                found += 1
            # Even more flexible: check individual core words
            elif any(w in content_lower for w in words if len(w) > 4):
                found += 1
            else:
                details.append(f"missed: {kw_text}")

    total = len(keywords)
    score = round(found / total * 10) if total > 0 else 0
    msg = f"{found}/{total} found"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_code_exec(content, scoring):
    """Score by executing code and running test cases."""
    # Extract code
    code = content.strip()
    if "```" in code:
        m = re.search(r'```(?:python)?\s*\n?(.*?)\n?```', code, re.DOTALL)
        if m:
            code = m.group(1)

    func_name = scoring["function_name"]
    ns = {}
    try:
        exec(code, ns)
    except Exception as e:
        return 0, 10, f"Code exec error: {e}"

    if func_name not in ns:
        return 0, 10, f"Function '{func_name}' not defined"

    func = ns[func_name]
    test_cases = scoring["test_cases"]
    passed = 0
    details = []

    for i, tc in enumerate(test_cases):
        try:
            if "ops" in tc:
                # LRU cache style tests
                cache = func(tc["capacity"])
                results = []
                for op in tc["ops"]:
                    if op[0] == "put":
                        results.append(cache.put(op[1], op[2]))
                    elif op[0] == "get":
                        results.append(cache.get(op[1]))
                if results == tc["expected"]:
                    passed += 1
                else:
                    details.append(f"tc{i+1}: expected {tc['expected']}, got {results}")
            else:
                result = func(tc["input"])
                if result == tc["expected"]:
                    passed += 1
                else:
                    details.append(f"tc{i+1}: expected {tc['expected']}, got {result}")
        except Exception as e:
            details.append(f"tc{i+1}: error: {e}")

    total = len(test_cases)
    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} test cases passed"
    if details:
        msg += " | " + "; ".join(details[:3])
    return score, 10, msg


def score_generic_constraints(content, scoring):
    """Generic constraint checker — counts how many check keywords appear."""
    checks = scoring["checks"]
    content_lower = content.lower()
    data = extract_json(content)

    passed = 0
    details = []
    for check in checks:
        # Simple presence check — the check name describes what to look for
        words = check.replace("_", " ").split()
        if any(w in content_lower for w in words if len(w) > 3):
            passed += 1
        else:
            details.append(check)

    total = len(checks)
    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} constraints"
    if details:
        msg += " | Missing: " + ", ".join(details[:5])
    return score, 10, msg


def score_manual(content, scoring):
    """Manual scoring — save for later review. Give 5/10 as placeholder."""
    criteria = scoring.get("criteria", [])
    return 5, 10, f"MANUAL — {len(criteria)} criteria to review"


def score_action_items(content, scoring):
    """Score action item extraction."""
    expected = scoring["expected"]
    content_lower = content.lower()

    found = 0
    details = []
    for item in expected:
        owner = item["owner"].lower()
        task_kw = item["task"].lower().split()[0]  # First word of task
        if owner in content_lower and task_kw in content_lower:
            found += 1
        else:
            details.append(f"missed: {item['owner']} - {item['task']}")

    total = len(expected)
    score = round(found / total * 10) if total > 0 else 0
    msg = f"{found}/{total} action items"
    if details:
        msg += " | " + "; ".join(details[:3])
    return score, 10, msg


def score_social_monitoring(content, scoring):
    """Score social media monitoring (sentiment + crisis detection)."""
    data = extract_json(content)
    answers = scoring["answers"]

    if data is None:
        return 0, 10, "Could not parse JSON"

    posts = data.get("posts", data)
    correct = 0
    total = 10  # 10 posts to classify
    details = []

    for post_id, expected in answers.items():
        post_data = None
        if isinstance(posts, dict):
            post_data = posts.get(post_id) or posts.get(str(post_id))

        if post_data and isinstance(post_data, dict):
            # Check sentiment (half point)
            exp_sent = expected["sentiment"]
            act_sent = post_data.get("sentiment", "").lower()[:3]
            if act_sent == exp_sent[:3]:
                correct += 0.5

            # Check crisis flag (half point)
            exp_crisis = expected["crisis"]
            act_crisis = post_data.get("crisis", False)
            if act_crisis == exp_crisis:
                correct += 0.5

    score = round(correct / (total / 2) * 10) if total > 0 else 0
    msg = f"{correct}/{total/2} checks correct"
    return score, 10, msg


# Map scoring types to scorer functions
SCORERS = {
    "json_values": score_json_values,
    "json_numeric": score_json_numeric,
    "error_count": score_error_count,
    "manual": score_manual,
    "action_items": score_action_items,
    "social_monitoring": score_social_monitoring,
    "code_exec": score_code_exec,
    # These all use keyword detection
    "error_detection": lambda c, s: score_keyword_detection(c, s, "errors"),
    "bug_detection": lambda c, s: score_keyword_detection(c, s, "bugs"),
    "security_vulns": lambda c, s: score_keyword_detection(c, s, "vulns"),
    "legal_issues": lambda c, s: score_keyword_detection(c, s, "issues"),
    "medical_findings": lambda c, s: score_keyword_detection(c, s, "findings"),
    "compliance_issues": lambda c, s: score_keyword_detection(c, s, "issues"),
    "issue_detection": lambda c, s: score_keyword_detection(c, s, "issues"),
    "news_dedup": lambda c, s: score_keyword_detection(c, {"issues": s.get("error_reasons", [])}),
    # These use generic constraint checking
    "faq_constraints": score_generic_constraints,
    "translation_constraints": score_generic_constraints,
    "content_calendar_constraints": score_generic_constraints,
    "seo_constraints": score_generic_constraints,
    "travel_constraints": score_generic_constraints,
    "home_automation": score_generic_constraints,
    "task_decomposition": score_generic_constraints,
    "curriculum_constraints": score_generic_constraints,
    "orchestration_constraints": score_generic_constraints,
    "architecture_constraints": score_generic_constraints,
    "code_structure": score_generic_constraints,
    "code_exec_tests": score_generic_constraints,
    "synthesis": lambda c, s: score_keyword_detection(c, {"issues": s.get("key_agreements", []) + s.get("key_disagreements", [])}),
    "recipe_scaling": lambda c, s: score_recipe(c, s),
}

# Map expected keys to possible descriptive keys the model might use
_RECIPE_KEY_ALIASES = {
    "flour_cups": ["flour", "all-purpose flour", "all purpose flour", "ap flour"],
    "baking_powder_tsp": ["baking powder", "baking_powder"],
    "salt_tsp": ["salt"],
    "butter_cups": ["butter", "unsalted butter"],
    "sugar_cups": ["sugar", "granulated sugar"],
    "eggs": ["eggs", "large eggs", "egg"],
    "milk_cups": ["milk", "whole milk"],
    "vanilla_tsp": ["vanilla", "vanilla extract"],
    "cocoa_cups": ["cocoa", "cocoa powder", "unsweetened cocoa"],
}

def score_recipe(content, scoring):
    """Score recipe scaling with flexible key matching and numeric extraction."""
    data = extract_json(content)
    answers = scoring["answers"]
    tolerance = scoring.get("tolerance", 0.5)
    if data is None:
        return 0, len(answers), "Could not parse JSON"

    correct = 0
    details = []
    for key, expected in answers.items():
        actual_val = None
        # Try direct key first
        actual_val_raw = _find_value_in_json(data, key)
        if actual_val_raw is None:
            # Try aliases
            aliases = _RECIPE_KEY_ALIASES.get(key, [])
            for alias in aliases:
                actual_val_raw = _find_value_in_json(data, alias)
                if actual_val_raw is not None:
                    break
        if actual_val_raw is not None:
            # Extract numeric value from strings like "3.5 cups" or "2.75 tsp"
            try:
                val_str = str(actual_val_raw).replace(",", "")
                # Extract first number from string
                import re as _re
                nums = _re.findall(r'[\d.]+', val_str)
                if nums:
                    actual_val = float(nums[0])
            except:
                pass
        if actual_val is not None:
            try:
                if abs(actual_val - float(expected)) <= tolerance:
                    correct += 1
                else:
                    details.append(f"{key}: expected {expected}, got {actual_val}")
            except:
                details.append(f"{key}: not numeric: {actual_val_raw}")
        else:
            details.append(f"{key}: missing")

    total = len(answers)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def run_test(test, base_url, model, max_tokens, timeout, extra_body=None, reasoning_prefix=None, api_key=None):
    """Run a single test and score it."""
    messages = []
    if reasoning_prefix:
        messages.append({"role": "system", "content": reasoning_prefix})
    messages.append({"role": "user", "content": test["prompt"]})
    content, tokens, tps, elapsed = call_llm(messages, base_url, model, max_tokens, timeout=timeout, extra_body=extra_body, api_key=api_key)

    scoring = test["scoring"]
    stype = scoring["type"]
    scorer = SCORERS.get(stype)

    if scorer:
        score, max_score, detail = scorer(content, scoring)
    else:
        score, max_score, detail = 0, 10, f"Unknown scoring type: {stype}"

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
    parser = argparse.ArgumentParser(description="Phase F: 59-Role Deterministic Hard Evaluation")
    parser.add_argument("--base-url", required=True, help="LLM server base URL")
    parser.add_argument("--model", required=True, help="Model name for output directory")
    parser.add_argument("--api-model", help="Model name to send in API requests (defaults to --model)")
    parser.add_argument("--api-key", help="API key for cloud endpoints (sent as Bearer token)")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max tokens per response")
    parser.add_argument("--timeout", type=int, default=300, help="Request timeout in seconds")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds between tests (for rate-limited APIs)")
    parser.add_argument("--thinking-budget", type=int, help="SGLang thinking token budget")
    parser.add_argument("--nothink", action="store_true", help="Disable thinking (Kimi: chat_template_kwargs.thinking=False)")
    parser.add_argument("--nothink-root", action="store_true", help="Disable thinking (GLM-5: enable_thinking=false at root level)")
    parser.add_argument("--reasoning", choices=["low", "medium", "high"], help="Reasoning level for system message (GPT-OSS-120B)")
    parser.add_argument("--test-ids", type=int, nargs="*", help="Run only these test IDs")
    parser.add_argument("--tier", type=int, help="Run only this tier")
    args = parser.parse_args()

    api_model = args.api_model or args.model
    reasoning_prefix = f"Reasoning: {args.reasoning}" if args.reasoning else None
    extra_body = None
    if args.nothink:
        extra_body = {"chat_template_kwargs": {"thinking": False}}
    elif args.nothink_root:
        extra_body = {"enable_thinking": False}
    elif args.thinking_budget:
        extra_body = {"chat_template_kwargs": {"enable_thinking": True, "thinking_budget": args.thinking_budget}}

    out_dir = Path(f"test_results/{args.model}/phase_f")
    out_dir.mkdir(parents=True, exist_ok=True)

    tests = PHASE_F_TESTS
    if args.test_ids:
        tests = [t for t in tests if t["id"] in args.test_ids]
    if args.tier:
        tests = [t for t in tests if t["tier"] == args.tier]

    think_label = f", thinking_budget={args.thinking_budget}" if args.thinking_budget else ""
    print(f"=== Phase F: 59-Role Deterministic Hard Evaluation ===")
    print(f"Model: {args.model}")
    print(f"API Model: {api_model}")
    print(f"Base URL: {args.base_url}")
    print(f"Max Tokens: {args.max_tokens}{think_label}")
    print(f"Timeout: {args.timeout}s")
    print(f"Tests: {len(tests)}")
    print(f"{'='*60}\n")

    results = []
    total_score = 0
    total_max = 0
    manual_tests = []

    for i, test in enumerate(tests):
        tid = test["id"]
        role = test["role"]
        tier = test["tier"]
        is_manual = test["scoring_type"] == "manual"
        manual_tag = " [MANUAL]" if is_manual else ""

        # Delay between tests (for rate-limited cloud APIs)
        if i > 0 and args.delay:
            import random
            jitter = random.randint(0, max(3, args.delay // 4))
            wait = args.delay + jitter
            print(f"  \u23f3 Waiting {wait}s...", flush=True)
            time.sleep(wait)

        print(f"[{i+1}/{len(tests)}] #{tid} T{tier}: {role}{manual_tag}")

        result = run_test(test, args.base_url, api_model, args.max_tokens, args.timeout, extra_body=extra_body, reasoning_prefix=reasoning_prefix, api_key=args.api_key)

        score = result["score"]
        max_score = result["max_score"]
        total_score += score
        total_max += max_score

        emoji = "✅" if score >= 8 else "⚠️" if score >= 5 else "❌"
        if is_manual:
            emoji = "📝"
            manual_tests.append({"id": tid, "role": role})

        print(f"  {emoji} {score}/{max_score} — {result['detail']}")
        print(f"     {result['tokens']}tok, {result['tps']}t/s, {result['elapsed']}s")

        result["test_id"] = tid
        result["role"] = role
        result["tier"] = tier
        result["scoring_type"] = test["scoring_type"]
        results.append(result)

        # Save individual response
        safe_role = role.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        resp_file = out_dir / f"{tid:02d}_{safe_role}.txt"
        with open(resp_file, "w") as f:
            f.write(result.get("response", ""))

    # Summary
    print(f"\n{'='*60}")
    print(f"PHASE F RESULTS — {args.model}")
    pct = total_score / total_max * 100 if total_max > 0 else 0
    print(f"Overall: {total_score}/{total_max} ({pct:.1f}%)")

    # Tier breakdown
    tiers = {}
    for r in results:
        t = r["tier"]
        if t not in tiers:
            tiers[t] = {"score": 0, "max": 0, "count": 0}
        tiers[t]["score"] += r["score"]
        tiers[t]["max"] += r["max_score"]
        tiers[t]["count"] += 1

    print("\nTier Breakdown:")
    for t in sorted(tiers):
        data = tiers[t]
        tp = data["score"] / data["max"] * 100 if data["max"] > 0 else 0
        print(f"  Tier {t}: {data['score']}/{data['max']} ({tp:.0f}%) [{data['count']} tests]")

    # Scoring type breakdown
    stypes = {}
    for r in results:
        st = r["scoring_type"]
        if st not in stypes:
            stypes[st] = {"score": 0, "max": 0, "count": 0}
        stypes[st]["score"] += r["score"]
        stypes[st]["max"] += r["max_score"]
        stypes[st]["count"] += 1

    print("\nScoring Type Breakdown:")
    for st, data in sorted(stypes.items()):
        sp = data["score"] / data["max"] * 100 if data["max"] > 0 else 0
        print(f"  {st}: {data['score']}/{data['max']} ({sp:.0f}%) [{data['count']} tests]")

    if manual_tests:
        print(f"\n📝 Manual review needed for {len(manual_tests)} tests:")
        for mt in manual_tests:
            print(f"   #{mt['id']} {mt['role']}")

    # Save scores
    scores_data = {
        "model": args.model,
        "timestamp": datetime.now().isoformat(),
        "total_score": total_score,
        "total_max": total_max,
        "percentage": round(pct, 1),
        "manual_tests": len(manual_tests),
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

    scores_file = out_dir / "phase_f_scores.json"
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)

    print(f"\nResults saved to: {scores_file}")


if __name__ == "__main__":
    main()
