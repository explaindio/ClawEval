#!/usr/bin/env python3
"""
OpenClaw Model Evaluation Framework
Tests AI models across phases for OpenClaw agent role fitness.
"""

import json
import time
import os
import sys
import argparse
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("Installing openai package...")
    os.system(f"{sys.executable} -m pip install openai -q")
    from openai import OpenAI

# ============================================================
# CONFIG
# ============================================================
DEFAULT_BASE_URL = "http://192.168.1.9:8080/v1"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "test_results")

def get_client(base_url=DEFAULT_BASE_URL):
    return OpenAI(base_url=base_url, api_key="not-needed")

def get_model_name(client):
    models = client.models.list()
    return models.data[0].id if models.data else "unknown"

def timed_completion(client, model, messages, max_tokens=512, temperature=0.7):
    """Send a chat completion and measure timing."""
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    elapsed = time.time() - start
    content = response.choices[0].message.content or ""
    usage = response.usage
    return {
        "content": content,
        "elapsed_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
        "tokens_per_second": round((usage.completion_tokens / elapsed), 1) if usage and elapsed > 0 else 0,
    }

def save_results(model_id, phase, data):
    """Save results to structured directory."""
    model_dir = os.path.join(RESULTS_DIR, model_id)
    phase_dir = os.path.join(model_dir, phase)
    os.makedirs(phase_dir, exist_ok=True)
    
    filepath = os.path.join(phase_dir, "results.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  → Saved to {filepath}")
    return filepath

# ============================================================
# PHASE 0: BASELINE
# ============================================================
def run_phase0(client, model):
    print("\n" + "="*60)
    print("PHASE 0: BASELINE — Speed & Connectivity")
    print("="*60)
    
    results = {
        "phase": "phase0_baseline",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Test 1: Simple response (warm-up)
    print("\n  [0.1] Warm-up request...")
    r = timed_completion(client, model, 
        [{"role": "user", "content": "Say 'hello' and nothing else."}],
        max_tokens=10, temperature=0)
    results["tests"].append({"name": "warmup", **r})
    print(f"       Response: {r['content'][:80]}  ({r['tokens_per_second']} t/s)")
    
    # Test 2: Short generation speed
    print("  [0.2] Short generation (50 tokens)...")
    r = timed_completion(client, model,
        [{"role": "user", "content": "Count from 1 to 50, one number per line."}],
        max_tokens=200, temperature=0)
    results["tests"].append({"name": "short_gen", **r})
    print(f"       {r['completion_tokens']} tokens in {r['elapsed_seconds']}s = {r['tokens_per_second']} t/s")
    
    # Test 3: Medium generation speed
    print("  [0.3] Medium generation (200 tokens)...")
    r = timed_completion(client, model,
        [{"role": "user", "content": "Write a detailed paragraph about the history of computing. Be thorough."}],
        max_tokens=300, temperature=0.7)
    results["tests"].append({"name": "medium_gen", **r})
    print(f"       {r['completion_tokens']} tokens in {r['elapsed_seconds']}s = {r['tokens_per_second']} t/s")
    
    # Test 4: Long generation speed
    print("  [0.4] Long generation (500 tokens)...")
    r = timed_completion(client, model,
        [{"role": "user", "content": "Write a comprehensive essay about artificial intelligence, covering its history, current state, and future implications. Include specific examples and dates."}],
        max_tokens=600, temperature=0.7)
    results["tests"].append({"name": "long_gen", **r})
    print(f"       {r['completion_tokens']} tokens in {r['elapsed_seconds']}s = {r['tokens_per_second']} t/s")
    
    # Summary
    speeds = [t["tokens_per_second"] for t in results["tests"] if t["tokens_per_second"] > 0]
    results["summary"] = {
        "avg_tps": round(sum(speeds)/len(speeds), 1) if speeds else 0,
        "max_tps": max(speeds) if speeds else 0,
        "min_tps": min(speeds) if speeds else 0,
    }
    print(f"\n  SUMMARY: avg {results['summary']['avg_tps']} t/s | "
          f"min {results['summary']['min_tps']} | max {results['summary']['max_tps']}")
    
    return results

# ============================================================
# PHASE 1: FORMAT COMPLIANCE
# ============================================================
PHASE1_TESTS = [
    {
        "name": "json_simple",
        "system": "You are a helpful assistant. Always respond in valid JSON format.",
        "user": "List 3 programming languages with their year of creation. Respond ONLY with a JSON array.",
        "check": "json",
    },
    {
        "name": "json_nested",
        "system": "Respond only in valid JSON. No markdown, no explanation.",
        "user": 'Create a JSON object with keys "name", "age", "skills" (array of strings), and "address" (nested object with "city" and "country").',
        "check": "json",
    },
    {
        "name": "json_from_text",
        "system": "You are a data extraction assistant. Extract information into valid JSON only. No other text.",
        "user": 'Extract structured data from this text: "John Smith, 34 years old, works at Google as a Senior Engineer in Mountain View, CA. His email is john@google.com." Return JSON with keys: name, age, company, title, location, email.',
        "check": "json",
    },
    {
        "name": "json_strict_schema",
        "system": "You must respond with ONLY valid JSON matching this exact schema: {\"action\": string, \"target\": string, \"confidence\": number between 0 and 1}. No explanation, no markdown fences.",
        "user": "The user says: 'Please schedule a meeting with Bob tomorrow at 3pm'",
        "check": "json",
    },
    {
        "name": "json_array_complex",
        "system": "Respond only with a valid JSON array. Each element must have: id (integer), task (string), priority (high/medium/low), done (boolean).",
        "user": "Generate a to-do list with 5 items for a software release.",
        "check": "json",
    },
    {
        "name": "system_prompt_adherence",
        "system": "You are a pirate. You MUST respond to every message in pirate speak. Never break character.",
        "user": "What is the capital of France?",
        "check": "contains_any",
        "expected_words": ["arr", "matey", "aye", "ye", "sail", "ship", "treasure", "seas", "cap'n", "ahoy", "plunder", "seafar"],
    },
    {
        "name": "one_word_constraint",
        "system": "You must respond with exactly ONE word. No punctuation, no explanation, just one single word.",
        "user": "What color is the sky on a clear day?",
        "check": "word_count",
        "expected_count": 1,
    },
    {
        "name": "numbered_list",
        "system": "Always respond with a numbered list. Each item must start with a number followed by a period.",
        "user": "What are the steps to make a peanut butter sandwich?",
        "check": "contains_pattern",
        "pattern": r"^\d+\.",
        "min_matches": 3,
    },
    {
        "name": "markdown_table",
        "system": "Respond only with a markdown table. No text before or after the table.",
        "user": "Show 4 planets with their distance from the sun and number of moons.",
        "check": "contains_all",
        "expected_words": ["|", "---"],
    },
    {
        "name": "refuse_and_redirect",
        "system": "You are a cooking assistant. If asked about anything not related to cooking or food, respond with exactly: 'I can only help with cooking-related questions.' Do not answer non-cooking questions.",
        "user": "What is the GDP of the United States?",
        "check": "contains_any",
        "expected_words": ["cooking", "food", "recipe", "can only help"],
    },
]

def check_json(content):
    """Try to parse as JSON, stripping markdown fences if present."""
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
    """Check if response passes the test criteria."""
    import re
    check_type = test["check"]
    
    if check_type == "json":
        return check_json(content)
    elif check_type == "contains_any":
        found = [w for w in test["expected_words"] if w.lower() in content.lower()]
        if found:
            return True, f"Contains: {', '.join(found)}"
        return False, f"Missing all expected words"
    elif check_type == "contains_all":
        missing = [w for w in test["expected_words"] if w not in content]
        if not missing:
            return True, "Contains all expected elements"
        return False, f"Missing: {', '.join(missing)}"
    elif check_type == "word_count":
        words = content.strip().split()
        expected = test["expected_count"]
        if len(words) <= expected + 1:  # Allow slight tolerance
            return True, f"Word count: {len(words)} (expected ~{expected})"
        return False, f"Word count: {len(words)} (expected ~{expected})"
    elif check_type == "contains_pattern":
        matches = re.findall(test["pattern"], content, re.MULTILINE)
        if len(matches) >= test["min_matches"]:
            return True, f"Pattern matches: {len(matches)} (min {test['min_matches']})"
        return False, f"Pattern matches: {len(matches)} (min {test['min_matches']})"
    return False, "Unknown check type"

def run_phase1(client, model):
    print("\n" + "="*60)
    print("PHASE 1: FORMAT COMPLIANCE")
    print("="*60)
    
    results = {
        "phase": "phase1_format_compliance",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "tests": [],
        "passed": 0,
        "failed": 0,
        "total": len(PHASE1_TESTS),
    }
    
    for i, test in enumerate(PHASE1_TESTS, 1):
        print(f"\n  [1.{i}] {test['name']}...")
        messages = []
        if test.get("system"):
            messages.append({"role": "system", "content": test["system"]})
        messages.append({"role": "user", "content": test["user"]})
        
        r = timed_completion(client, model, messages, max_tokens=512, temperature=0)
        passed, reason = check_result(test, r["content"])
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"       {status} — {reason}")
        if not passed:
            print(f"       Response: {r['content'][:120]}...")
        
        results["tests"].append({
            "name": test["name"],
            "passed": passed,
            "reason": reason,
            "response": r["content"],
            "elapsed": r["elapsed_seconds"],
            "tps": r["tokens_per_second"],
        })
        
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    score = round(results["passed"] / results["total"] * 100, 1)
    results["score_pct"] = score
    print(f"\n  SCORE: {results['passed']}/{results['total']} = {score}%")
    
    return results

# ============================================================
# PHASE 2: TOOL CALLING
# ============================================================
AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Temperature units"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a calendar event",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Event title"},
                    "date": {"type": "string", "description": "Event date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Event time in HH:MM format"},
                    "duration_minutes": {"type": "integer", "description": "Duration in minutes"},
                },
                "required": ["title", "date", "time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"},
                },
                "required": ["path"],
            },
        },
    },
]

PHASE2_TESTS = [
    {
        "name": "simple_search",
        "user": "Search the web for the latest news about artificial intelligence.",
        "expected_tool": "search_web",
        "expected_params": ["query"],
    },
    {
        "name": "weather_query",
        "user": "What's the weather like in Tokyo right now?",
        "expected_tool": "get_weather",
        "expected_params": ["city"],
    },
    {
        "name": "calendar_create",
        "user": "Schedule a team meeting for March 15, 2026 at 2:30 PM, 60 minutes long.",
        "expected_tool": "create_calendar_event",
        "expected_params": ["title", "date", "time"],
    },
    {
        "name": "email_send",
        "user": "Send an email to alice@company.com with subject 'Q4 Report' saying the quarterly report is attached.",
        "expected_tool": "send_email",
        "expected_params": ["to", "subject", "body"],
    },
    {
        "name": "file_read",
        "user": "Read the file at /home/user/documents/notes.txt",
        "expected_tool": "read_file",
        "expected_params": ["path"],
    },
    {
        "name": "weather_with_units",
        "user": "Tell me the temperature in London in fahrenheit.",
        "expected_tool": "get_weather",
        "expected_params": ["city"],
    },
    {
        "name": "no_tool_needed",
        "user": "What is 2 + 2?",
        "expected_tool": None,
        "expected_params": [],
    },
    {
        "name": "ambiguous_search",
        "user": "Find information about how photosynthesis works.",
        "expected_tool": "search_web",
        "expected_params": ["query"],
    },
    {
        "name": "calendar_implicit",
        "user": "Remind me about the dentist appointment tomorrow at 9 AM.",
        "expected_tool": "create_calendar_event",
        "expected_params": ["title", "date", "time"],
    },
    {
        "name": "multi_step_intent",
        "user": "Look up the population of Canada and then email the answer to bob@example.com.",
        "expected_tool": "search_web",  # Should at least call search first
        "expected_params": ["query"],
    },
]

def run_phase2(client, model):
    print("\n" + "="*60)
    print("PHASE 2: TOOL CALLING")
    print("="*60)
    
    results = {
        "phase": "phase2_tool_calling",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "tests": [],
        "passed": 0,
        "failed": 0,
        "total": len(PHASE2_TESTS),
    }
    
    for i, test in enumerate(PHASE2_TESTS, 1):
        print(f"\n  [2.{i}] {test['name']}...")
        
        try:
            start = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with access to tools. Use the appropriate tool when the user's request requires it. If no tool is needed, respond normally."},
                    {"role": "user", "content": test["user"]},
                ],
                tools=AVAILABLE_TOOLS,
                tool_choice="auto",
                max_tokens=512,
                temperature=0,
            )
            elapsed = time.time() - start
            
            msg = response.choices[0].message
            tool_calls = msg.tool_calls
            text_content = msg.content or ""
            
            passed = False
            reason = ""
            tool_name_used = None
            tool_args = {}
            
            if test["expected_tool"] is None:
                # Should NOT call a tool
                if not tool_calls:
                    passed = True
                    reason = "Correctly did not call a tool"
                else:
                    reason = f"Incorrectly called: {tool_calls[0].function.name}"
            else:
                # Should call the expected tool
                if tool_calls:
                    tc = tool_calls[0]
                    tool_name_used = tc.function.name
                    try:
                        tool_args = json.loads(tc.function.arguments)
                    except:
                        tool_args = {}
                    
                    if tool_name_used == test["expected_tool"]:
                        # Check required params
                        missing = [p for p in test["expected_params"] if p not in tool_args]
                        if not missing:
                            passed = True
                            reason = f"Correct tool + params: {tool_args}"
                        else:
                            reason = f"Correct tool but missing params: {missing}"
                    else:
                        reason = f"Wrong tool: {tool_name_used} (expected {test['expected_tool']})"
                else:
                    reason = f"No tool called (expected {test['expected_tool']}). Text: {text_content[:80]}"
            
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"       {status} — {reason}")
            
            results["tests"].append({
                "name": test["name"],
                "passed": passed,
                "reason": reason,
                "tool_called": tool_name_used,
                "tool_args": tool_args,
                "text_response": text_content[:200] if text_content else None,
                "elapsed": round(elapsed, 2),
            })
            
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
                
        except Exception as e:
            print(f"       ❌ ERROR: {e}")
            results["tests"].append({
                "name": test["name"],
                "passed": False,
                "reason": f"Error: {str(e)}",
            })
            results["failed"] += 1
    
    score = round(results["passed"] / results["total"] * 100, 1)
    results["score_pct"] = score
    print(f"\n  SCORE: {results['passed']}/{results['total']} = {score}%")
    
    return results

# ============================================================
# PHASE 3: ROLE-SPECIFIC FUNCTIONAL TESTS
# ============================================================
PHASE3_ROUTER_TESTS = [
    {"input": "Can you write a Python function to sort a list?", "expected": "code_generation"},
    {"input": "Review this pull request for security issues", "expected": "code_review"},
    {"input": "What's the weather going to be like this weekend?", "expected": "weather"},
    {"input": "Summarize this 20-page document for me", "expected": "summarization"},
    {"input": "Schedule a call with the design team for Friday at 3pm", "expected": "calendar"},
    {"input": "Translate this paragraph into French", "expected": "translation"},
    {"input": "Analyze the sentiment of these customer reviews", "expected": "sentiment_analysis"},
    {"input": "Draft an email to the client about the project delay", "expected": "email"},
    {"input": "Search for the latest research on CRISPR gene editing", "expected": "research"},
    {"input": "Check if this claim is true: The Great Wall is visible from space", "expected": "fact_checking"},
    {"input": "Create unit tests for this authentication module", "expected": "qa_testing"},
    {"input": "What's 2+2?", "expected": "general"},
    {"input": "Help me plan a trip to Japan for 2 weeks", "expected": "travel_planning"},
    {"input": "Generate a landing page for a SaaS product", "expected": "landing_page"},
    {"input": "Debug why this API returns a 500 error", "expected": "debugging"},
    {"input": "Analyze this company's quarterly earnings report", "expected": "financial_analysis"},
    {"input": "Write a blog post about sustainable energy trends", "expected": "content_writing"},
    {"input": "Track my calories for today: I had oatmeal for breakfast and a sandwich for lunch", "expected": "fitness_tracking"},
    {"input": "Compare prices for iPhone 16 Pro across different retailers", "expected": "shopping"},
    {"input": "Optimize this article for SEO targeting 'best running shoes 2026'", "expected": "seo"},
]

PHASE3_CODE_TESTS = [
    {
        "name": "fizzbuzz",
        "prompt": "Write a Python function called fizzbuzz(n) that returns a list of strings from 1 to n where: multiples of 3 are 'Fizz', multiples of 5 are 'Buzz', multiples of both are 'FizzBuzz', and other numbers are the number as a string. Return ONLY the function code, no explanation.",
        "test_code": """
def test():
    result = fizzbuzz(15)
    assert result[0] == '1'
    assert result[2] == 'Fizz'
    assert result[4] == 'Buzz'
    assert result[14] == 'FizzBuzz'
    assert len(result) == 15
    return True
""",
    },
    {
        "name": "reverse_string",
        "prompt": "Write a Python function called reverse_words(s) that reverses the order of words in a string while keeping each word intact. Example: 'hello world' → 'world hello'. Return ONLY the function code.",
        "test_code": """
def test():
    assert reverse_words('hello world') == 'world hello'
    assert reverse_words('the sky is blue') == 'blue is sky the'
    assert reverse_words('a') == 'a'
    assert reverse_words('') == ''
    return True
""",
    },
    {
        "name": "fibonacci",
        "prompt": "Write a Python function called fib(n) that returns the nth Fibonacci number (0-indexed, so fib(0)=0, fib(1)=1, fib(2)=1, fib(6)=8). Return ONLY the function code.",
        "test_code": """
def test():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(10) == 55
    return True
""",
    },
    {
        "name": "palindrome",
        "prompt": "Write a Python function called is_palindrome(s) that returns True if the input string is a palindrome (ignoring case and non-alphanumeric characters). Return ONLY the function code.",
        "test_code": """
def test():
    assert is_palindrome('racecar') == True
    assert is_palindrome('A man, a plan, a canal: Panama') == True
    assert is_palindrome('hello') == False
    assert is_palindrome('') == True
    return True
""",
    },
    {
        "name": "flatten_list",
        "prompt": "Write a Python function called flatten(lst) that flattens a nested list of integers into a single flat list. Example: flatten([1, [2, 3], [4, [5, 6]]]) → [1, 2, 3, 4, 5, 6]. Return ONLY the function code.",
        "test_code": """
def test():
    assert flatten([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
    assert flatten([]) == []
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([[1], [[2]], [[[3]]]]) == [1, 2, 3]
    return True
""",
    },
]

def extract_python_code(content):
    """Extract Python code from a response, handling markdown fences."""
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0]
    elif "```" in content:
        code = content.split("```")[1].split("```")[0]
    else:
        code = content
    return code.strip()

def run_phase3(client, model):
    print("\n" + "="*60)
    print("PHASE 3: ROLE-SPECIFIC FUNCTIONAL TESTS")
    print("="*60)
    
    results = {
        "phase": "phase3_functional",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "clusters": {},
    }
    
    # --- 3A: ROUTING ---
    print("\n  --- 3A: ROUTING (20 scenarios) ---")
    router_results = {"passed": 0, "total": len(PHASE3_ROUTER_TESTS), "tests": []}
    
    for i, test in enumerate(PHASE3_ROUTER_TESTS, 1):
        r = timed_completion(client, model, [
            {"role": "system", "content": 'You are a message router. Classify the user\'s message into exactly ONE category. Respond with ONLY the category name, nothing else. Categories: code_generation, code_review, weather, summarization, calendar, translation, sentiment_analysis, email, research, fact_checking, qa_testing, general, travel_planning, landing_page, debugging, financial_analysis, content_writing, fitness_tracking, shopping, seo'},
            {"role": "user", "content": test["input"]},
        ], max_tokens=20, temperature=0)
        
        response_cat = r["content"].strip().lower().replace(" ", "_").replace("-", "_")
        # Flexible matching
        passed = test["expected"] in response_cat or response_cat in test["expected"]
        status = "✅" if passed else "❌"
        print(f"    [{i:2d}] {status} '{test['input'][:50]}...' → {r['content'].strip()} (expected: {test['expected']})")
        
        router_results["tests"].append({
            "input": test["input"],
            "expected": test["expected"],
            "got": r["content"].strip(),
            "passed": passed,
        })
        if passed:
            router_results["passed"] += 1
    
    router_results["score_pct"] = round(router_results["passed"] / router_results["total"] * 100, 1)
    print(f"    ROUTING SCORE: {router_results['passed']}/{router_results['total']} = {router_results['score_pct']}%")
    results["clusters"]["routing"] = router_results
    
    # --- 3B: CODE GENERATION ---
    print("\n  --- 3B: CODE GENERATION (5 problems) ---")
    code_results = {"passed": 0, "total": len(PHASE3_CODE_TESTS), "tests": []}
    
    for i, test in enumerate(PHASE3_CODE_TESTS, 1):
        r = timed_completion(client, model, [
            {"role": "system", "content": "You are a Python coding assistant. Write clean, correct Python code. Return ONLY the function implementation, no explanation or examples."},
            {"role": "user", "content": test["prompt"]},
        ], max_tokens=500, temperature=0)
        
        code = extract_python_code(r["content"])
        passed = False
        error_msg = ""
        
        try:
            exec_globals = {}
            exec(code, exec_globals)
            exec(test["test_code"], exec_globals)
            passed = exec_globals["test"]()
        except Exception as e:
            error_msg = str(e)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"    [{i}] {status} {test['name']}" + (f" — {error_msg}" if error_msg else ""))
        
        code_results["tests"].append({
            "name": test["name"],
            "passed": passed,
            "code": code,
            "error": error_msg,
            "tps": r["tokens_per_second"],
        })
        if passed:
            code_results["passed"] += 1
    
    code_results["score_pct"] = round(code_results["passed"] / code_results["total"] * 100, 1)
    print(f"    CODE SCORE: {code_results['passed']}/{code_results['total']} = {code_results['score_pct']}%")
    results["clusters"]["code_generation"] = code_results
    
    return results

# ============================================================
# PHASE 4: OPEN-ENDED QUALITY EVAL
# ============================================================
PHASE4_PROMPTS = [
    {
        "cluster": "writing",
        "name": "blog_post",
        "system": "You are a professional content writer.",
        "user": "Write a compelling 300-word blog post about why remote work is changing the future of cities. Include a catchy title.",
    },
    {
        "cluster": "writing",
        "name": "email_professional",
        "system": "You are a professional email writer.",
        "user": "Draft an email to a client explaining that their project will be delayed by 2 weeks due to unexpected technical challenges. Be professional but honest. The client is 'Acme Corp' and the project is a website redesign.",
    },
    {
        "cluster": "analysis",
        "name": "data_interpretation",
        "system": "You are a data analyst.",
        "user": "A company's quarterly revenue data (in millions): Q1: $45, Q2: $52, Q3: $48, Q4: $61. Analyze the trend, identify anomalies, and provide 3 actionable recommendations for the next quarter.",
    },
    {
        "cluster": "analysis",
        "name": "summarization",
        "system": "You are an expert summarizer.",
        "user": "Summarize the key points of this text in exactly 3 bullet points:\n\nArtificial intelligence has evolved dramatically over the past decade. Machine learning models have grown from millions to trillions of parameters. The cost of training frontier models has increased from thousands to hundreds of millions of dollars. However, inference costs have dropped significantly thanks to hardware improvements and quantization techniques. Open-weight models have democratized access, allowing individuals and small companies to run powerful AI locally. The debate around AI safety has intensified, with governments worldwide introducing regulatory frameworks. Despite concerns about job displacement, new roles in AI engineering, prompt design, and AI ethics have emerged. The technology is increasingly being integrated into everyday tools, from code editors to email clients, fundamentally changing how knowledge workers operate.",
    },
    {
        "cluster": "reasoning",
        "name": "logic_puzzle",
        "system": "You are a logical reasoning expert. Show your step-by-step reasoning.",
        "user": "Five people (Alice, Bob, Carol, Dave, Eve) sit in a row. Alice is not next to Bob. Carol is in the middle. Dave is next to Eve. Bob is at one of the ends. Where is everyone sitting? List from left to right.",
    },
    {
        "cluster": "reasoning",
        "name": "math_word_problem",
        "system": "You are a math tutor. Show your work step by step.",
        "user": "A store has a 30% off sale. If you also have a coupon for 15% off the sale price, and the original price of a jacket is $120, what is the final price? Also calculate the total percentage saved from the original price.",
    },
    {
        "cluster": "planning",
        "name": "project_plan",
        "system": "You are a project manager.",
        "user": "Create a high-level project plan for building a mobile app for a local restaurant. Include phases, key milestones, estimated timelines, and team roles needed. The budget is $50,000.",
    },
    {
        "cluster": "planning",
        "name": "task_decomposition",
        "system": "You are a task planning specialist.",
        "user": "Break down this task into subtasks with dependencies: 'Deploy a new microservice that reads from a Kafka topic, processes messages, stores results in PostgreSQL, and exposes a REST API for querying results.'",
    },
]

def run_phase4(client, model):
    print("\n" + "="*60)
    print("PHASE 4: OPEN-ENDED QUALITY EVAL")
    print("="*60)
    print("  (Outputs saved for offline comparison)")
    
    results = {
        "phase": "phase4_quality_eval",
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "responses": [],
    }
    
    for i, prompt in enumerate(PHASE4_PROMPTS, 1):
        print(f"\n  [4.{i}] {prompt['cluster']}/{prompt['name']}...")
        r = timed_completion(client, model, [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ], max_tokens=800, temperature=0.7)
        
        print(f"       {r['completion_tokens']} tokens in {r['elapsed_seconds']}s = {r['tokens_per_second']} t/s")
        print(f"       Preview: {r['content'][:100]}...")
        
        results["responses"].append({
            "cluster": prompt["cluster"],
            "name": prompt["name"],
            "prompt": prompt["user"],
            "response": r["content"],
            "tokens": r["completion_tokens"],
            "elapsed": r["elapsed_seconds"],
            "tps": r["tokens_per_second"],
        })
    
    print(f"\n  Saved {len(results['responses'])} responses for offline comparison.")
    return results

# ============================================================
# MAIN
# ============================================================
def run_all(base_url=DEFAULT_BASE_URL, phases=None):
    client = get_client(base_url)
    model = get_model_name(client)
    
    # Sanitize model name for directory
    model_id = model.replace("/", "_").replace("\\", "_").replace(" ", "_")
    
    print(f"\n{'#'*60}")
    print(f"# OpenClaw Model Evaluation")
    print(f"# Model: {model}")
    print(f"# Server: {base_url}")
    print(f"# Time: {datetime.now().isoformat()}")
    print(f"{'#'*60}")
    
    all_results = {"model": model, "model_id": model_id, "base_url": base_url}
    
    if phases is None or 0 in phases:
        r = run_phase0(client, model)
        save_results(model_id, "phase0_baseline", r)
        all_results["phase0"] = r
    
    if phases is None or 1 in phases:
        r = run_phase1(client, model)
        save_results(model_id, "phase1_format", r)
        all_results["phase1"] = r
    
    if phases is None or 2 in phases:
        r = run_phase2(client, model)
        save_results(model_id, "phase2_toolcall", r)
        all_results["phase2"] = r
    
    if phases is None or 3 in phases:
        r = run_phase3(client, model)
        save_results(model_id, "phase3_functional", r)
        all_results["phase3"] = r
    
    if phases is None or 4 in phases:
        r = run_phase4(client, model)
        save_results(model_id, "phase4_quality", r)
        all_results["phase4"] = r
    
    # Save combined results
    save_results(model_id, ".", {"all_phases": all_results, "timestamp": datetime.now().isoformat()})
    
    # Print summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"  Model: {model}")
    if "phase0" in all_results:
        print(f"  Speed: avg {all_results['phase0']['summary']['avg_tps']} t/s")
    if "phase1" in all_results:
        print(f"  Format Compliance: {all_results['phase1']['score_pct']}%")
    if "phase2" in all_results:
        print(f"  Tool Calling: {all_results['phase2']['score_pct']}%")
    if "phase3" in all_results:
        p3 = all_results["phase3"]
        for cluster_name, cluster_data in p3.get("clusters", {}).items():
            print(f"  {cluster_name.title()}: {cluster_data['score_pct']}%")
    if "phase4" in all_results:
        print(f"  Quality Responses: {len(all_results['phase4']['responses'])} saved for review")
    
    return all_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenClaw Model Evaluation")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--phases", nargs="+", type=int, help="Specific phases to run (0-4)")
    args = parser.parse_args()
    
    run_all(base_url=args.url, phases=args.phases)
