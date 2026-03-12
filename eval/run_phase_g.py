#!/usr/bin/env python3
"""
Phase G: Discriminator Tests — Harder tests that separate model quality.
Targets roles where all models currently score identically (ceiling effect).

Usage:
  python3 run_phase_g.py --base-url URL --model MODEL [--max-tokens N] [--test-ids 36 2 5]
"""

import argparse
import json
import math
import os
import re
import sys
import time
import textwrap
import traceback
from datetime import datetime
from pathlib import Path

import requests

from phase_g import PHASE_G_TESTS


# ============================================================
# LLM CALL (same as Phase F)
# ============================================================

def call_llm(messages, base_url, model, max_tokens=4000, timeout=300, extra_body=None, api_key=None):
    """Send messages and return response content."""
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0,
    }
    if extra_body:
        payload.update(extra_body)

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    t0 = time.time()
    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    elapsed = round(time.time() - t0, 1)
    resp.raise_for_status()
    data = resp.json()
    choice = data["choices"][0]

    content = choice["message"].get("content", "")

    # Strip thinking content — multiple formats:
    # 1. <think>...</think> tags (llama.cpp / vLLM)
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    # 2. SGLang "Thinking Process:" block — strip everything before the actual answer
    #    The answer typically starts with JSON ({), code (```), or a clear section break
    if content.startswith("Thinking Process"):
        # Find the first JSON object, code fence, or final answer
        json_match = re.search(r'(?:^|\n)(\{[\s\S]*)', content)
        code_match = re.search(r'(?:^|\n)(```[\s\S]*)', content)
        # Use whichever comes first
        positions = []
        if json_match:
            positions.append((json_match.start(1), json_match.group(1)))
        if code_match:
            positions.append((code_match.start(1), code_match.group(1)))
        if positions:
            positions.sort(key=lambda x: x[0])
            content = positions[0][1].strip()

    tokens = data.get("usage", {}).get("completion_tokens", 0)
    tps = round(tokens / elapsed, 1) if elapsed > 0 else 0
    return content, tokens, tps, elapsed


def _clean_json_text(text):
    """Clean common JSON issues from LLM output before parsing."""
    # Strip JS-style comments: // ... and /* ... */
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'(\d+(?:\.\d+)?)\s*[MBKmbk]\b', r'\1', text)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    # Fix stray trailing quotes on numeric values: "key": 40" → "key": 40
    # Only match when preceded by ': ' (JSON value context) to avoid breaking strings
    text = re.sub(r'(:\s*\d+)"(\s*[,}\n])', r'\1\2', text, flags=re.DOTALL)
    return text

def _try_parse_json(text):
    """Try to parse JSON, returning parsed result or None."""
    try:
        result = json.loads(text)
        if isinstance(result, list) and len(result) == 1 and isinstance(result[0], dict):
            return result[0]
        return result
    except:
        return None

def extract_json(text):
    """Extract JSON from response text, handling markdown code fences and preamble."""
    text = text.strip()
    # Strip any residual </think> tags (e.g. Nemotron inline thinking)
    if "</think>" in text:
        text = text.split("</think>")[-1].strip()
    # Extract from code fences first
    if "```" in text:
        m = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if m:
            text = m.group(1).strip()
    # Try raw parse
    result = _try_parse_json(text)
    if result is not None:
        return result
    # Try after cleaning
    result = _try_parse_json(_clean_json_text(text))
    if result is not None:
        return result
    # Try regex extraction — try ALL matches, last first (answer is usually at end)
    for pattern in [r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', r'\[.*\]']:
        matches = list(re.finditer(pattern, text, re.DOTALL))
        for m in reversed(matches):
            result = _try_parse_json(m.group())
            if result is not None:
                return result
            result = _try_parse_json(_clean_json_text(m.group()))
            if result is not None:
                return result
    # Try finding deeply nested JSON — scan from last } backwards
    try:
        last_close = text.rfind('}')
        if last_close >= 0:
            depth = 0
            for i in range(last_close, -1, -1):
                if text[i] == '}': depth += 1
                elif text[i] == '{': depth -= 1
                if depth == 0:
                    candidate = text[i:last_close+1]
                    result = _try_parse_json(candidate)
                    if result is not None:
                        return result
                    result = _try_parse_json(_clean_json_text(candidate))
                    if result is not None:
                        return result
                    break
    except:
        pass
    # Fallback: scan from first { forward
    try:
        start = text.index('{')
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{': depth += 1
            elif text[i] == '}': depth -= 1
            if depth == 0:
                candidate = text[start:i+1]
                result = _try_parse_json(candidate)
                if result is not None:
                    return result
                result = _try_parse_json(_clean_json_text(candidate))
                if result is not None:
                    return result
                break
    except:
        pass
    return None



# ============================================================
# SCORERS
# ============================================================

def _find_value_in_json(data, key):
    """Flexibly find a value in JSON — handles case-insensitive keys, nested dicts, and lists."""
    if isinstance(data, list):
        # If key is numeric, use as 1-based index into list
        try:
            idx = int(key) - 1
            if 0 <= idx < len(data):
                return data[idx]
        except (ValueError, TypeError):
            pass
        return None
    if not isinstance(data, dict):
        return None
    # Exact match
    if key in data:
        return data[key]
    # Case-insensitive
    for k, v in data.items():
        if k.lower().replace(" ", "_").replace("-", "_") == key.lower().replace(" ", "_").replace("-", "_"):
            return v
    # Search nested
    for k, v in data.items():
        if isinstance(v, dict):
            result = _find_value_in_json(v, key)
            if result is not None:
                return result
    return None


def score_json_values(content, scoring):
    """Score exact JSON value matches."""
    data = extract_json(content)
    if not data:
        return 0, 10, "Could not parse JSON"

    answers = scoring["answers"]
    correct = 0
    total = len(answers)
    details = []

    for key, expected in answers.items():
        # Skip explanatory keys
        if key.endswith("_contains"):
            actual = str(_find_value_in_json(data, key.replace("_contains", "")) or "")
            if expected.lower() in actual.lower():
                correct += 1
            else:
                details.append(f"{key}: expected contains '{expected}', got '{actual}'")
            continue

        actual = _find_value_in_json(data, key)
        if actual is None:
            details.append(f"{key}: missing")
            continue

        actual_str = str(actual).strip().upper()
        expected_str = str(expected).strip().upper()

        if actual_str == expected_str:
            correct += 1
        else:
            details.append(f"{key}: expected '{expected}', got '{actual}'")

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_json_numeric(content, scoring):
    """Score numeric JSON values with tolerance."""
    data = extract_json(content)
    if not data:
        return 0, 10, "Could not parse JSON"

    answers = scoring["answers"]
    tolerance = scoring.get("tolerance", 5.0)
    correct = 0
    total = 0
    details = []

    for key, expected in answers.items():
        if isinstance(expected, str):
            # String comparison for non-numeric answers
            actual = _find_value_in_json(data, key)
            if actual and str(actual).strip().lower() == expected.lower():
                correct += 1
            else:
                details.append(f"{key}: expected '{expected}', got '{actual}'")
            total += 1
            continue

        actual = _find_value_in_json(data, key)
        if actual is None:
            details.append(f"{key}: missing")
            total += 1
            continue

        try:
            actual_num = float(str(actual).replace(",", "").replace("%", "").replace("$", ""))
        except (ValueError, TypeError):
            details.append(f"{key}: cannot parse '{actual}' as number")
            total += 1
            continue

        # Use per-key tolerance if provided
        tol = tolerance
        if isinstance(tolerance, dict):
            tol = tolerance.get(key, 5.0)

        if abs(actual_num - expected) <= tol:
            correct += 1
        else:
            details.append(f"{key}: expected {expected}±{tol}, got {actual_num}")
        total += 1

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_error_count_graduated(content, scoring):
    """Score error detection with graduated scoring — 1 point per N errors found."""
    data = extract_json(content)
    content_lower = content.lower()
    expected_errors = scoring.get("expected_errors", [])
    expected_count = scoring.get("expected_count", len(expected_errors))

    found = 0
    missed = []
    for err in expected_errors:
        # Check for key phrases from the error description
        keywords = [w.lower() for w in err.split() if len(w) > 3]
        if any(kw in content_lower for kw in keywords):
            found += 1
        else:
            missed.append(err[:40])

    # Graduated: each error is worth proportional points
    score = round(found / expected_count * 10) if expected_count > 0 else 0
    score = min(score, 10)

    msg = f"Found {found}/{expected_count} errors"
    if missed:
        msg += f" | Missed: {'; '.join(missed[:3])}"
    return score, 10, msg


def score_code_exec_class(content, scoring):
    """Score by executing code that defines a class and running test cases."""
    # Extract code from response
    code_match = re.search(r"```(?:python)?\s*(.*?)```", content, re.DOTALL)
    code = code_match.group(1) if code_match else content

    # Clean up code
    lines = []
    for line in code.split("\n"):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            lines.append(line)
        elif stripped and not stripped.startswith("#"):
            lines.append(line)
        elif not stripped:
            lines.append(line)
    code = "\n".join(lines)

    test_cases = scoring["test_cases"]
    passed = 0
    total = len(test_cases)
    details = []

    for tc in test_cases:
        test_name = tc["test"]
        test_code = tc["code"]
        full_code = f"import time\nimport threading\nfrom collections import OrderedDict, defaultdict\n\n{code}\n\n{test_code}"

        try:
            exec(full_code, {})
            passed += 1
        except Exception as e:
            details.append(f"{test_name}: {str(e)[:50]}")

    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} tests passed"
    if details:
        msg += " | " + "; ".join(details[:3])
    return score, 10, msg


def score_generic_constraints(content, scoring):
    """Score by checking constraint keywords in the response text."""
    checks = scoring.get("checks", [])
    content_lower = content.lower().replace("_", " ").replace("-", " ")

    passed = 0
    details = []

    for check in checks:
        # Convert check name to search terms
        terms = check.replace("_", " ").lower().split()
        significant = [t for t in terms if len(t) > 2 and t not in {"has", "the", "and", "for", "with", "not"}]

        if len(significant) >= 2:
            found = sum(1 for t in significant if t in content_lower)
            if found >= len(significant) * 0.6:
                passed += 1
            else:
                details.append(check)
        elif significant:
            if significant[0] in content_lower:
                passed += 1
            else:
                details.append(check)
        else:
            passed += 1  # No meaningful check

    total = len(checks)
    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} constraints met"
    if details:
        msg += " | Missing: " + "; ".join(details[:3])
    return score, 10, msg


# ============================================================
# SCORER REGISTRY
# ============================================================

SCORERS = {
    "json_values": score_json_values,
    "json_values_mixed": score_json_values,
    "json_numeric": score_json_numeric,
    "error_count_graduated": score_error_count_graduated,
    "code_exec": score_code_exec_class,
    "architecture_deep": score_generic_constraints,
    "content_calendar": score_generic_constraints,
    "orchestration_constraints": score_generic_constraints,
}


# ============================================================
# TEST RUNNER
# ============================================================

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
        try:
            score, max_score, detail = scorer(content, scoring)
        except Exception as e:
            score, max_score, detail = 0, 10, f"Scorer error: {str(e)[:80]}"
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
    parser = argparse.ArgumentParser(description="Phase G: Discriminator Tests — Harder tests for ceiling-effect roles")
    parser.add_argument("--base-url", required=True, help="LLM server base URL")
    parser.add_argument("--model", required=True, help="Model name for output directory")
    parser.add_argument("--api-model", help="Model name to send in API requests (defaults to --model)")
    parser.add_argument("--api-key", help="API key for cloud endpoints (sent as Bearer token)")
    parser.add_argument("--max-tokens", type=int, default=8000, help="Max tokens per response (default: 8000)")
    parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds (default: 600)")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds between tests (for rate-limited APIs)")
    parser.add_argument("--thinking-budget", type=int, help="SGLang thinking token budget")
    parser.add_argument("--nothink", action="store_true", help="Disable thinking (Kimi: chat_template_kwargs.thinking=False)")
    parser.add_argument("--nothink-root", action="store_true", help="Disable thinking (GLM-5: enable_thinking=false at root level)")
    parser.add_argument("--reasoning", choices=["low", "medium", "high"], help="Reasoning level (GPT-OSS-120B)")
    parser.add_argument("--test-ids", type=int, nargs="*", help="Run only these test IDs")
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

    out_dir = Path(f"test_results/{args.model}/phase_g")
    out_dir.mkdir(parents=True, exist_ok=True)

    tests = PHASE_G_TESTS
    if args.test_ids:
        tests = [t for t in tests if t["id"] in args.test_ids]

    print(f"=== Phase G: Discriminator Tests ===")
    print(f"Model: {args.model}")
    print(f"API Model: {api_model}")
    print(f"Base URL: {args.base_url}")
    print(f"Max Tokens: {args.max_tokens}")
    print(f"Timeout: {args.timeout}s")
    if args.api_key:
        print(f"API Key: ...{args.api_key[-6:]}")
    if args.delay:
        print(f"Delay: {args.delay}s between tests")
    if reasoning_prefix:
        print(f"Reasoning: {args.reasoning}")
    print(f"Tests: {len(tests)}")
    print(f"{'='*60}\n")

    results = []
    total_score = 0
    total_max = 0

    for i, test in enumerate(tests):
        tid = test["id"]
        role = test["role"]

        # Delay between tests (for rate-limited cloud APIs)
        if i > 0 and args.delay:
            import random
            jitter = random.randint(0, max(5, args.delay // 3))
            wait = args.delay + jitter
            print(f"  ⏳ Waiting {wait}s before next test...", flush=True)
            time.sleep(wait)

        print(f"[{i+1}/{len(tests)}] G-{tid}: {role}")

        result = run_test(test, args.base_url, api_model, args.max_tokens, args.timeout,
                         extra_body=extra_body, reasoning_prefix=reasoning_prefix, api_key=args.api_key)

        score = result["score"]
        max_score = result["max_score"]
        total_score += score
        total_max += max_score

        emoji = "✅" if score >= 8 else "⚠️" if score >= 5 else "❌"
        print(f"  {emoji} {score}/{max_score} — {result['detail']}")
        print(f"     {result['tokens']}tok, {result['tps']}t/s, {result['elapsed']}s")

        result["test_id"] = tid
        result["role"] = role
        result["tier"] = test.get("tier", 0)
        result["scoring_type"] = test["scoring_type"]
        results.append(result)

        # Save individual response
        safe_role = role.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        resp_file = out_dir / f"G{tid:02d}_{safe_role}.txt"
        with open(resp_file, "w") as f:
            f.write(result.get("response", ""))

    # Summary
    print(f"\n{'='*60}")
    print(f"PHASE G RESULTS — {args.model}")
    pct = total_score / total_max * 100 if total_max > 0 else 0
    print(f"Overall: {total_score}/{total_max} ({pct:.1f}%)")

    # Per-test breakdown
    print("\nPer-Test Scores:")
    for r in results:
        emoji = "✅" if r["score"] >= 8 else "⚠️" if r["score"] >= 5 else "❌"
        print(f"  {emoji} G-{r['test_id']:2d} {r['role']:<35s} {r['score']}/{r['max_score']}")

    # Compare with Phase F if available
    pf_scores = Path(f"test_results/{args.model}/phase_f/phase_f_scores.json")
    if pf_scores.exists():
        with open(pf_scores) as f:
            pf = json.load(f)
        print(f"\n📊 Phase F vs Phase G comparison:")
        pf_by_id = {r["id"]: r for r in pf["results"]}
        for r in results:
            if r["test_id"] in pf_by_id:
                pf_r = pf_by_id[r["test_id"]]
                arrow = "↓" if r["score"] < pf_r["score"] else "↑" if r["score"] > pf_r["score"] else "="
                print(f"  #{r['test_id']:2d} {r['role']:<35s} F:{pf_r['score']}/10 → G:{r['score']}/10 {arrow}")

    # Save scores
    scores_data = {
        "model": args.model,
        "phase": "G",
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

    scores_file = out_dir / "phase_g_scores.json"
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)

    print(f"\nResults saved to: {scores_file}")


if __name__ == "__main__":
    main()
