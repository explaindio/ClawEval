#!/usr/bin/env python3
"""
Phase E: Killer Evaluation Runner
Runs 12 hard tests with 100% automated scoring.
Supports single-turn and multi-turn (agentic) tests.
Usage: python3 run_phase_e.py --base-url URL --model MODEL [--max-tokens N]
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

from phase_e_prompts import PHASE_E_TESTS


def call_llm(messages, base_url, model, max_tokens=4000, timeout=120, extra_body=None):
    """Send messages and return response content."""
    headers = {"Content-Type": "application/json", "Authorization": "Bearer not-needed"}
    body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.1}
    if extra_body:
        body.update(extra_body)
    start = time.time()
    try:
        r = requests.post(f"{base_url}/chat/completions", headers=headers, json=body, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        # Strip SGLang thinking content — model may use <think>...</think> or output
        # "Thinking Process:..." followed by </think> before the actual answer
        if "</think>" in content:
            # Take everything after the last </think>
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
    # Strip markdown code fences
    if "```" in text:
        m = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if m:
            text = m.group(1).strip()
    # Try parsing directly
    try:
        return json.loads(text)
    except:
        pass
    # Try finding JSON object or array
    for pattern in [r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', r'\[.*\]']:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except:
                pass
    return None


# ============================================================
# SCORERS — one per scoring type
# ============================================================

def score_json_values(content, scoring):
    """Score exact JSON value matches."""
    data = extract_json(content)
    answers = scoring["answers"]
    if data is None:
        return 0, len(answers), "Could not parse JSON"

    correct = 0
    details = []
    for key, expected in answers.items():
        # Handle nested keys like "Alice_car"
        if "_" in key and isinstance(expected, str):
            parts = key.split("_", 1)
            actual = None
            if isinstance(data, dict):
                person = data.get(parts[0], {})
                if isinstance(person, dict):
                    actual = person.get(parts[1])
            if actual is not None and str(actual).lower() == str(expected).lower():
                correct += 1
            else:
                details.append(f"{key}: expected {expected}, got {actual}")
        else:
            actual = data.get(key) if isinstance(data, dict) else None
            if actual is not None and (actual == expected or str(actual) == str(expected)):
                correct += 1
            else:
                details.append(f"{key}: expected {expected}, got {actual}")

    total = len(answers)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_json_numeric(content, scoring):
    """Score numeric JSON values with tolerance."""
    data = extract_json(content)
    answers = scoring["answers"]
    tolerance = scoring.get("tolerance", 0.01)
    if data is None:
        return 0, len(answers), "Could not parse JSON"

    correct = 0
    details = []
    for key, expected in answers.items():
        actual = data.get(key) if isinstance(data, dict) else None
        if actual is not None:
            try:
                if abs(float(actual) - float(expected)) <= tolerance:
                    correct += 1
                else:
                    details.append(f"{key}: expected {expected}, got {actual}")
            except (ValueError, TypeError):
                details.append(f"{key}: not a number: {actual}")
        else:
            details.append(f"{key}: missing")

    total = len(answers)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_json_constraints(content, scoring):
    """Score constrained JSON generation."""
    data = extract_json(content)
    if data is None:
        return 0, 10, "Could not parse JSON"

    checks = scoring["checks"]
    passed = 0
    details = []

    for check in checks:
        ok = False
        try:
            if check == "has_exact_keys":
                ok = isinstance(data, dict) and set(data.keys()) == {"order_id", "customer", "items", "payment", "metadata"}
            elif check == "order_id_format":
                ok = isinstance(data.get("order_id"), str) and bool(re.match(r'^ORD-\d{6}$', data["order_id"]))
            elif check == "customer_name_len":
                name = data.get("customer", {}).get("name", "")
                ok = isinstance(name, str) and 2 <= len(name) <= 50
            elif check == "customer_email":
                email = data.get("customer", {}).get("email", "")
                ok = isinstance(email, str) and "@" in email and "." in email.split("@")[-1]
            elif check == "items_count_3":
                ok = isinstance(data.get("items"), list) and len(data["items"]) == 3
            elif check == "items_structure":
                items = data.get("items", [])
                if isinstance(items, list) and len(items) == 3:
                    ok = all(
                        isinstance(it, dict) and
                        isinstance(it.get("name"), str) and
                        isinstance(it.get("price"), (int, float)) and it["price"] > 0 and
                        isinstance(it.get("quantity"), int) and it["quantity"] >= 1
                        for it in items
                    )
            elif check == "total_range":
                items = data.get("items", [])
                if isinstance(items, list):
                    total = sum(it.get("price", 0) * it.get("quantity", 0) for it in items)
                    ok = 25.0 <= total <= 100.0
            elif check == "payment_method":
                ok = data.get("payment", {}).get("method") in ("credit_card", "debit_card", "cash")
            elif check == "payment_matches":
                items = data.get("items", [])
                if isinstance(items, list):
                    total = round(sum(it.get("price", 0) * it.get("quantity", 0) for it in items), 2)
                    amount = data.get("payment", {}).get("amount")
                    ok = amount is not None and abs(float(amount) - total) < 0.01
            elif check == "valid_timestamp":
                ts = data.get("metadata", {}).get("timestamp", "")
                ok = bool(re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(ts)))
        except Exception:
            ok = False

        if ok:
            passed += 1
        else:
            details.append(check)

    score = round(passed / len(checks) * 10)
    msg = f"{passed}/{len(checks)} constraints"
    if details:
        msg += " | Failed: " + ", ".join(details[:5])
    return score, 10, msg


def score_output_lines(content, scoring):
    """Score code output prediction line by line."""
    expected = scoring["expected"]
    lines = [l.strip() for l in content.strip().split("\n") if l.strip() and not l.strip().startswith(("#", "//", "```"))]

    correct = 0
    details = []
    for i, exp in enumerate(expected):
        if i < len(lines) and lines[i] == exp:
            correct += 1
        else:
            got = lines[i] if i < len(lines) else "(missing)"
            details.append(f"Line {i+1}: expected '{exp}', got '{got}'")

    total = len(expected)
    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} lines correct"
    if details:
        msg += " | " + "; ".join(details[:3])
    return score, 10, msg


def score_contradictions(content, scoring):
    """Score contradiction detection."""
    true_ids = scoring["true_contradictions"]
    all_contras = {c["id"]: c for c in true_ids} if isinstance(true_ids[0], dict) else None

    # For the simplified version, use keyword matching
    if all_contras is None:
        # true_contradictions is a list of IDs, look up from parent
        contras = scoring.get("true_contradictions", [])
        found = 0
        details = []

        content_lower = content.lower()

        # Check for department total contradiction (110+120≠195)
        if any(k in content_lower for k in ["230", "110", "195"]) and "120" in content_lower:
            found += 1
        else:
            details.append("missed: dept_total (110+120≠195)")

        # Check for churn rate contradiction (2.63% not 3.2%)
        if any(k in content_lower for k in ["2.6", "2.63", "50/1900"]):
            found += 1
        else:
            details.append("missed: churn_rate")

        # Check for R&D percentage contradiction (22.1% vs actual 19.4%)
        if "22.1" in content_lower and any(k in content_lower for k in ["8.2", "42.3", "19.4", "19.3"]):
            found += 1
        else:
            details.append("missed: rd_pct (8.2/42.3=19.4% not 22.1%)")

        score = round(found / 3 * 10)
        msg = f"{found}/3 contradictions found"
        if details:
            msg += " | " + "; ".join(details[:3])
        return score, 10, msg

    return 5, 10, "Fallback scoring"


def score_json_array_exact(content, scoring):
    """Score exact array match — order matters."""
    data = extract_json(content)
    expected = scoring["expected"]

    if not isinstance(data, list):
        return 0, 10, "Response is not a JSON array"

    correct = 0
    total = len(expected)
    details = []
    for i, exp in enumerate(expected):
        if i < len(data) and data[i] == exp:
            correct += 1
        else:
            got = data[i] if i < len(data) else "(missing)"
            details.append(f"pos {i}: expected {exp}, got {got}")

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} positions correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_regex_test(content, scoring):
    """Score regex by actually testing it."""
    # Extract regex pattern
    pattern = content.strip()
    pattern = pattern.strip("`'\"")
    if pattern.startswith("r\"") or pattern.startswith("r'"):
        pattern = pattern[2:-1]
    # Remove any newlines
    pattern = pattern.split("\n")[0].strip()

    correct = 0
    total = len(scoring["should_match"]) + len(scoring["should_not_match"])
    details = []

    try:
        regex = re.compile(pattern)

        for s in scoring["should_match"]:
            if regex.fullmatch(s) or regex.search(s):
                correct += 1
            else:
                details.append(f"should match '{s}' but didn't")

        for s in scoring["should_not_match"]:
            if not (regex.fullmatch(s) or regex.search(s)):
                correct += 1
            else:
                details.append(f"should NOT match '{s}' but did")

    except re.error as e:
        return 0, 10, f"Invalid regex: {e}"

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} test cases"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_data_transform(content, scoring):
    """Score data transformation pipeline."""
    data = extract_json(content)
    expected = scoring["expected"]

    if data is None:
        return 0, 10, "Could not parse JSON"

    correct = 0
    total = 0
    details = []

    for dept, exp_items in expected.items():
        total += 1
        if dept not in data:
            details.append(f"missing dept {dept}")
            continue

        actual_items = data[dept]
        if not isinstance(actual_items, list):
            details.append(f"{dept}: not a list")
            continue

        # Check items match
        dept_ok = True
        for i, exp_item in enumerate(exp_items):
            if i >= len(actual_items):
                dept_ok = False
                details.append(f"{dept}[{i}] missing")
                break
            act = actual_items[i]
            if act.get("name") != exp_item["name"]:
                dept_ok = False
                details.append(f"{dept}[{i}] name: expected {exp_item['name']}, got {act.get('name')}")
                break
            # Allow small tolerance on bonus
            if abs(act.get("bonus", 0) - exp_item["bonus"]) > 5:
                dept_ok = False
                details.append(f"{dept}[{i}] bonus: expected {exp_item['bonus']}, got {act.get('bonus')}")
                break

        if dept_ok and len(actual_items) == len(exp_items):
            correct += 1

    # Also check no extra departments
    total += 1
    if set(data.keys()) == set(expected.keys()):
        correct += 1
    else:
        extra = set(data.keys()) - set(expected.keys())
        if extra:
            details.append(f"extra depts: {extra}")

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} department groups correct"
    if details:
        msg += " | " + "; ".join(details[:5])
    return score, 10, msg


def score_instruction_chain(content, scoring):
    """Score instruction-following chain where each step builds on the last."""
    expected = scoring["expected"]
    actual = content.strip().strip('"\'')

    # Check exact match first
    if actual == expected:
        return 10, 10, "Exact match"

    # Partial scoring
    correct = 0
    total = 5
    details = []

    # Check 1: Words are reversed
    if "D*g" in actual or "dog" in actual.lower().split()[0:1]:
        correct += 1
    else:
        details.append("words not reversed")

    # Check 2: First word capitalized
    words = actual.split()
    if words and words[0][0].isupper():
        correct += 1
    else:
        details.append("first word not capitalized")

    # Check 3: Vowels replaced with *
    if "*" in actual and not any(v in actual.lower().replace("(", "").replace(")", "").replace(" ", "") for v in "aeiou"):
        correct += 1
    else:
        details.append("vowels not replaced")

    # Check 4: Has word count in parens
    if "(9)" in actual:
        correct += 1
    else:
        details.append("missing (9)")

    # Check 5: Right number of words (9 before the count)
    main_part = actual.split("(")[0].strip() if "(" in actual else actual
    if len(main_part.split()) == 9:
        correct += 1
    else:
        details.append(f"word count should be 9, got {len(main_part.split())}")

    score = round(correct / total * 10) if total > 0 else 0
    msg = f"{correct}/{total} criteria"
    if details:
        msg += " | " + "; ".join(details)
    return score, 10, msg


def score_multi_turn_code(responses, scoring):
    """Score multi-turn code refinement test."""
    checks = scoring["checks"]
    passed = 0
    total = len(checks)
    details = []

    if len(responses) < 3:
        return 0, 10, f"Only {len(responses)} turns completed, need 3"

    turn1 = responses[0]  # Initial function
    turn2 = responses[1]  # Fixed function
    turn3 = responses[2]  # Test assertions

    # Extract function code from turn2 (the fixed version)
    func_code = turn2
    if "```" in func_code:
        m = re.search(r'```(?:python)?\s*\n?(.*?)\n?```', func_code, re.DOTALL)
        if m:
            func_code = m.group(1)

    # Try to execute the function
    ns = {}
    func_defined = False
    try:
        exec(func_code, ns)
        func_defined = "parse_duration" in ns
    except Exception as e:
        details.append(f"exec error: {e}")

    for check in checks:
        ok = False
        try:
            if check == "function_defined":
                ok = func_defined
            elif check == "handles_compound" and func_defined:
                ok = ns["parse_duration"]("2h30m15s") == 9015
            elif check == "handles_simple" and func_defined:
                ok = ns["parse_duration"]("45m") == 2700
            elif check == "handles_duplicates" and func_defined:
                ok = ns["parse_duration"]("1h1h") == -1
            elif check == "handles_empty" and func_defined:
                ok = ns["parse_duration"]("") == -1
            elif check == "handles_zero" and func_defined:
                ok = ns["parse_duration"]("0s") == 0
            elif check == "handles_any_order" and func_defined:
                ok = ns["parse_duration"]("30m2h") == 9000
            elif check == "handles_invalid" and func_defined:
                ok = ns["parse_duration"]("abc") == -1
            elif check == "turn3_has_6_asserts":
                assert_lines = [l for l in turn3.strip().split("\n") if l.strip().startswith("assert")]
                ok = len(assert_lines) == 6
            elif check == "turn3_asserts_pass":
                # Run turn3's assertions with the fixed function
                try:
                    assert_code = turn3
                    if "```" in assert_code:
                        m = re.search(r'```(?:python)?\s*\n?(.*?)\n?```', assert_code, re.DOTALL)
                        if m:
                            assert_code = m.group(1)
                    exec(assert_code, ns)
                    ok = True
                except AssertionError:
                    details.append("turn3 assertion failed")
                except Exception:
                    pass
        except Exception:
            pass

        if ok:
            passed += 1
        elif check not in [c for c in details]:
            details.append(check)

    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} checks"
    if details:
        msg += " | Failed: " + ", ".join([d for d in details if not d.startswith("exec")][:5])
    return score, 10, msg


def score_multi_turn_state(responses, scoring):
    """Score multi-turn state tracking test."""
    expected_states = scoring["expected_states"]
    checks = scoring["checks"]
    passed = 0
    total = len(checks)
    details = []

    if len(responses) < 4:
        return 0, 10, f"Only {len(responses)} turns, need 4"

    # Parse each turn's JSON response
    parsed = {}
    for i, resp in enumerate(responses):
        parsed[f"turn_{i+1}"] = extract_json(resp)

    for check in checks:
        ok = False
        try:
            if check == "turn1_correct_board":
                t1 = parsed.get("turn_1")
                if t1 and "todo" in t1:
                    todo_ids = [t.get("id") for t in t1.get("todo", []) if isinstance(t, dict)]
                    ok = set(todo_ids) == {1, 2, 3} and len(t1.get("in_progress", [])) == 0

            elif check == "turn2_moves_correct":
                t2 = parsed.get("turn_2")
                if t2:
                    ip_ids = [t.get("id") for t in t2.get("in_progress", []) if isinstance(t, dict)]
                    ok = set(ip_ids) == {1, 2} and any(t.get("id") == 4 for t in t2.get("todo", []) if isinstance(t, dict))

            elif check == "turn3_done_correct":
                t3 = parsed.get("turn_3")
                if t3:
                    done_ids = [t.get("id") for t in t3.get("done", []) if isinstance(t, dict)]
                    ok = set(done_ids) == {1, 2}

            elif check == "turn3_reassign":
                t3 = parsed.get("turn_3")
                if t3:
                    for t in t3.get("todo", []):
                        if isinstance(t, dict) and t.get("id") == 4:
                            ok = t.get("assignee") == "Dave"

            elif check == "turn3_in_progress":
                t3 = parsed.get("turn_3")
                if t3:
                    ip_ids = [t.get("id") for t in t3.get("in_progress", []) if isinstance(t, dict)]
                    ok = ip_ids == [3]

            elif check == "turn4_total":
                t4 = parsed.get("turn_4")
                if t4:
                    ok = t4.get("total_tasks") == 4

            elif check == "turn4_done_count":
                t4 = parsed.get("turn_4")
                if t4:
                    ok = t4.get("done_count") == 2

            elif check == "turn4_bobs_tasks":
                t4 = parsed.get("turn_4")
                if t4:
                    bobs = t4.get("bobs_tasks", [])
                    ok = sorted(bobs) == [2]

            elif check == "turn4_in_progress_titles":
                t4 = parsed.get("turn_4")
                if t4:
                    titles = t4.get("in_progress_titles", [])
                    ok = titles == ["Design DB"]

            elif check == "state_consistency":
                # Check no tasks lost across turns
                t3 = parsed.get("turn_3")
                if t3:
                    all_ids = set()
                    for col in ["todo", "in_progress", "done"]:
                        for t in t3.get(col, []):
                            if isinstance(t, dict):
                                all_ids.add(t.get("id"))
                    ok = all_ids == {1, 2, 3, 4}

        except Exception:
            pass

        if ok:
            passed += 1
        else:
            details.append(check)

    score = round(passed / total * 10) if total > 0 else 0
    msg = f"{passed}/{total} state checks"
    if details:
        msg += " | Failed: " + ", ".join(details[:5])
    return score, 10, msg


SCORERS = {
    "json_values": score_json_values,
    "json_numeric": score_json_numeric,
    "json_constraints": score_json_constraints,
    "output_lines": score_output_lines,
    "contradictions": score_contradictions,
    "json_array_exact": score_json_array_exact,
    "regex_test": score_regex_test,
    "data_transform": score_data_transform,
    "instruction_chain": score_instruction_chain,
}


def run_single_turn(test, base_url, model, max_tokens, timeout=120, extra_body=None):
    """Run a single-turn test."""
    messages = [{"role": "user", "content": test["prompt"]}]
    content, tokens, tps, elapsed = call_llm(messages, base_url, model, max_tokens, timeout=timeout, extra_body=extra_body)

    scoring = test["scoring"]
    scorer = SCORERS.get(scoring["type"])
    if scorer:
        score, max_score, detail = scorer(content, scoring)
    else:
        score, max_score, detail = 0, 10, f"Unknown scoring type: {scoring['type']}"

    return {
        "score": score,
        "max_score": max_score,
        "detail": detail,
        "tokens": tokens,
        "tps": tps,
        "elapsed": elapsed,
        "response": content,
    }


def run_multi_turn(test, base_url, model, max_tokens, timeout=120, extra_body=None):
    """Run a multi-turn test, accumulating conversation history."""
    turns = test["turns"]
    messages = []
    responses = []
    total_tokens = 0
    total_elapsed = 0

    for turn in turns:
        messages.append({"role": turn["role"], "content": turn["content"]})
        content, tokens, tps, elapsed = call_llm(messages, base_url, model, max_tokens, timeout=timeout, extra_body=extra_body)
        messages.append({"role": "assistant", "content": content})
        responses.append(content)
        total_tokens += tokens
        total_elapsed += elapsed

    # Score based on type
    scoring = test["scoring"]
    stype = scoring["type"]

    if stype == "multi_turn_code":
        score, max_score, detail = score_multi_turn_code(responses, scoring)
    elif stype == "multi_turn_state":
        score, max_score, detail = score_multi_turn_state(responses, scoring)
    else:
        score, max_score, detail = 0, 10, f"Unknown multi-turn scoring: {stype}"

    avg_tps = total_tokens / total_elapsed if total_elapsed > 0 else 0

    return {
        "score": score,
        "max_score": max_score,
        "detail": detail,
        "tokens": total_tokens,
        "tps": round(avg_tps, 1),
        "elapsed": round(total_elapsed, 1),
        "responses": responses,
        "turns": len(turns),
    }


def main():
    parser = argparse.ArgumentParser(description="Phase E: Killer Evaluation Runner")
    parser.add_argument("--base-url", required=True, help="LLM server base URL (e.g., http://host:8080/v1)")
    parser.add_argument("--model", required=True, help="Model name for output directory")
    parser.add_argument("--api-model", help="Model name to send in API requests (defaults to --model)")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max tokens per response")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout in seconds")
    parser.add_argument("--thinking-budget", type=int, help="SGLang thinking token budget (enables thinking with limit)")
    parser.add_argument("--nothink", action="store_true", help="SGLang: disable thinking (enable_thinking=false)")
    parser.add_argument("--test-ids", type=int, nargs="*", help="Run only these test IDs")
    args = parser.parse_args()

    api_model = args.api_model or args.model
    extra_body = None
    if args.nothink:
        extra_body = {"chat_template_kwargs": {"enable_thinking": False}}
    elif args.thinking_budget:
        extra_body = {"chat_template_kwargs": {"enable_thinking": True, "thinking_budget": args.thinking_budget}}

    out_dir = Path(f"test_results/{args.model}/phase_e")
    out_dir.mkdir(parents=True, exist_ok=True)

    tests = PHASE_E_TESTS
    if args.test_ids:
        tests = [t for t in tests if t["id"] in args.test_ids]

    think_label = f", thinking_budget={args.thinking_budget}" if args.thinking_budget else ""
    print(f"=== Phase E Killer Evaluation ===")
    print(f"Model: {args.model}")
    print(f"API Model: {api_model}")
    print(f"Base URL: {args.base_url}")
    print(f"Max Tokens: {args.max_tokens}{think_label}")
    print(f"Tests: {len(tests)}")
    print(f"{'='*50}\n")

    results = []
    total_score = 0
    total_max = 0

    for i, test in enumerate(tests):
        tid = test["id"]
        name = test["name"]
        is_multi = test.get("multi_turn", False)
        turns_label = f" ({len(test.get('turns', []))} turns)" if is_multi else ""
        print(f"[{i+1}/{len(tests)}] Test {tid}: {name}{turns_label}")

        if is_multi:
            result = run_multi_turn(test, args.base_url, api_model, args.max_tokens, timeout=args.timeout, extra_body=extra_body)
        else:
            result = run_single_turn(test, args.base_url, api_model, args.max_tokens, timeout=args.timeout, extra_body=extra_body)

        score = result["score"]
        max_score = result["max_score"]
        total_score += score
        total_max += max_score

        emoji = "✅" if score >= 8 else "⚠️" if score >= 5 else "❌"
        print(f"  {emoji} {score}/{max_score} — {result['detail']}")
        print(f"     {result['tokens']}tok, {result['tps']}t/s, {result['elapsed']}s")

        result["test_id"] = tid
        result["test_name"] = name
        result["category"] = test["category"]
        results.append(result)

        # Save individual response
        resp_file = out_dir / f"{tid:02d}_{name.replace(' ', '_').replace('/', '_')}.txt"
        if is_multi:
            with open(resp_file, "w") as f:
                for j, resp in enumerate(result["responses"]):
                    f.write(f"=== TURN {j+1} ===\n{resp}\n\n")
        else:
            with open(resp_file, "w") as f:
                f.write(result.get("response", ""))

    # Summary
    print(f"\n{'='*50}")
    print(f"PHASE E RESULTS — {args.model}")
    print(f"Overall: {total_score}/{total_max} ({total_score/total_max*100:.1f}%)")
    print()

    # Category breakdown
    cats = {}
    for r in results:
        cat = r["category"]
        if cat not in cats:
            cats[cat] = {"score": 0, "max": 0, "count": 0}
        cats[cat]["score"] += r["score"]
        cats[cat]["max"] += r["max_score"]
        cats[cat]["count"] += 1

    print("Category Breakdown:")
    for cat, data in sorted(cats.items()):
        pct = data["score"] / data["max"] * 100 if data["max"] > 0 else 0
        print(f"  {cat}: {data['score']}/{data['max']} ({pct:.0f}%) [{data['count']} tests]")

    # Save scores
    scores_data = {
        "model": args.model,
        "timestamp": datetime.now().isoformat(),
        "total_score": total_score,
        "total_max": total_max,
        "percentage": round(total_score / total_max * 100, 1) if total_max > 0 else 0,
        "results": [
            {
                "id": r["test_id"],
                "name": r["test_name"],
                "category": r["category"],
                "score": r["score"],
                "max": r["max_score"],
                "detail": r["detail"],
                "tokens": r["tokens"],
                "tps": r["tps"],
            }
            for r in results
        ],
    }

    scores_file = out_dir / "phase_e_scores.json"
    with open(scores_file, "w") as f:
        json.dump(scores_data, f, indent=2)
    print(f"\nResults saved to: {scores_file}")


if __name__ == "__main__":
    main()
