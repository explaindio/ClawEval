"""Phase H Dense Tests — Batch 6: Tests 29, 31, 33, 35, 43, 44, 45, 50, 51, 52 (final batch)"""

PHASE_H_BATCH6 = [
    # H-29: HOME AUTOMATION — 20 rules
    {
        "id": 29, "role": "Home Automation Agent", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Given these 20 smart home scenarios, determine the correct action for each. Respond as JSON: {"1": "action", ...}

House config: Thermostat (heating/cooling), lights (on/off/dim), doors (lock/unlock), alarm (arm/disarm), blinds (open/close), music (play/pause/stop), cameras (on/off).

Rules:
- When nobody is home, lock all doors, arm alarm, turn off lights, set thermostat to eco (62°F)
- When someone arrives home, disarm alarm, unlock front door, turn on hall lights
- After 11pm, dim all lights to 20%, lock all doors
- When temperature > 78°F, turn on cooling
- When temperature < 65°F, turn on heating
- When motion detected at night + nobody home = trigger alarm
- When doorbell rings, show camera feed, unlock door only if recognized face
- Morning routine (7am): open blinds, turn on kitchen lights, play morning playlist

Scenarios:
1. It's 7:00 AM, occupant's alarm just went off
2. Last person left house, door closed
3. Temperature sensor reads 82°F, someone is home
4. It's 11:30 PM, family is home
5. Motion detected in backyard, 2 AM, nobody home
6. Front doorbell rings, camera recognizes regular visitor
7. Front doorbell rings, camera shows unknown person
8. First person arrives home at 6 PM
9. Temperature sensor reads 61°F, nobody home
10. It's 7 AM but it's a detected holiday
11. Smoke detector triggered
12. Water leak sensor activated in basement
13. Baby room noise level exceeds threshold at night
14. Guest WiFi device count exceeds 10
15. Power outage detected, UPS active
16. All windows closed, indoor CO2 > 1000 ppm
17. Sunlight sensor reads very bright, living room occupied
18. It's 3 AM, toddler's room door opened
19. Garage door has been open for 30 minutes, nobody in garage
20. Outdoor temperature dropped below freezing overnight""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "open blinds, kitchen lights on, play morning playlist",
                "2": "lock doors, arm alarm, lights off, eco thermostat",
                "3": "turn on cooling",
                "4": "dim lights to 20%, lock doors",
                "5": "trigger alarm",
                "6": "show camera, unlock door",
                "7": "show camera, keep door locked",
                "8": "disarm alarm, unlock front door, hall lights on",
                "9": "turn on heating",
                "10": "open blinds, kitchen lights on, play morning playlist",
                "11": "trigger alarm, notify emergency, unlock doors",
                "12": "send alert, shut water valve if available",
                "13": "send alert to parents, turn on nightlight",
                "14": "send notification, no action needed",
                "15": "switch to essential devices, send notification",
                "16": "activate ventilation or open windows",
                "17": "close blinds or dim shading",
                "18": "send alert, turn on hallway nightlight",
                "19": "close garage door, send notification",
                "20": "ensure heating is on, notify about pipes"
            }
        }
    },

    # H-31: RECIPE SCALING — 15 calculations
    {
        "id": 31, "role": "Recipe / Cooking Agent", "tier": 2,
        "scoring_type": "json_numeric",
        "prompt": """Scale this recipe from 4 servings to 14 servings. Calculate all 15 ingredient amounts. Respond as JSON: {"i1": value, ...}. Round to 2 decimal places. Give amounts in the original unit.

Original recipe (4 servings):
i1: All-purpose flour: 2 cups
i2: Sugar: 3/4 cup
i3: Butter: 1/2 cup (1 stick)
i4: Eggs: 2 large
i5: Milk: 1 1/3 cups
i6: Baking powder: 2 1/4 teaspoons
i7: Salt: 1/2 teaspoon
i8: Vanilla extract: 1 1/2 teaspoons
i9: Cocoa powder: 1/3 cup
i10: Heavy cream: 3/4 cup
i11: Chocolate chips: 1 cup
i12: Cinnamon: 1/4 teaspoon
i13: Nutmeg: 1/8 teaspoon
i14: Lemon juice: 2 tablespoons
i15: Cornstarch: 1 1/2 tablespoons

Scale factor: 14/4 = 3.5""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "i1": 7.0, "i2": 2.63, "i3": 1.75,
                "i4": 7.0, "i5": 4.67, "i6": 7.88,
                "i7": 1.75, "i8": 5.25, "i9": 1.17,
                "i10": 2.63, "i11": 3.5, "i12": 0.88,
                "i13": 0.44, "i14": 7.0, "i15": 5.25
            },
            "tolerance": 0.1
        }
    },

    # H-33: SEO OPTIMIZATION — 15 checks
    {
        "id": 33, "role": "SEO Optimization Agent", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Audit this webpage for SEO issues. Find ALL 15 problems. Respond as JSON: {"issues": [{"id": 1, "issue": "...", "severity": "critical/major/minor", "fix": "..."}, ...], "count": 15}

Page HTML:
```html
<html>
<head>
<title>Home</title>
</head>
<body>
<h2>Welcome to Our Store</h2>
<h1>Best Products</h1>
<h1>Shop Now</h1>
<img src="product1.jpg">
<img src="product2.jpg">
<img src="banner.jpg">
<p>Buy our stuff. Click here for more. Click here to order.</p>
<a href="https://example.com/products">Click here</a>
<a href="https://example.com/about">Click here</a>
<div style="display:none">cheap shoes buy online discount sale best price</div>
<p>Lorem ipsum dolor sit amet...</p>
<meta name="keywords" content="buy,cheap,best,discount,shoes,bags,clothes">
</body>
</html>
```
URL: example.com/page-1234?ref=123&utm=abc""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "i1": "generic title tag (just 'Home')",
                "i2": "no meta description",
                "i3": "multiple h1 tags (2 h1s)",
                "i4": "h2 appears before h1 - wrong hierarchy",
                "i5": "images missing alt attributes",
                "i6": "non-descriptive anchor text ('click here')",
                "i7": "hidden text (display:none with keywords) - black hat",
                "i8": "keyword stuffing in meta keywords",
                "i9": "thin/low-quality content",
                "i10": "non-semantic URL with query parameters",
                "i11": "no canonical tag",
                "i12": "no structured data / schema markup",
                "i13": "no viewport meta tag (mobile)",
                "i14": "lorem ipsum placeholder content",
                "i15": "duplicate anchor text for different URLs"
            }
        }
    },

    # H-35: TRAVEL PLANNING — 15 constraints
    {
        "id": 35, "role": "Travel Planning Agent", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Plan a 5-day trip to Tokyo, Japan. Budget: $2000 total. Respond as JSON: {"days": [{"day": 1, "morning": "...", "afternoon": "...", "evening": "...", "hotel": "...", "meals_budget": N, "transport_budget": N, "activity_budget": N}], "total_budget": N}

ALL 15 constraints must be met:
1. Exactly 5 days
2. Total budget does not exceed $2000
3. At least 1 temple/shrine visit
4. At least 1 technology/electronics district visit (Akihabara)
5. At least 1 traditional Japanese meal experience
6. At least 1 day trip outside central Tokyo (e.g., Kamakura, Nikko)
7. No more than $150/night on hotel
8. Include at least 2 free activities
9. Mix of cultural and modern attractions
10. All 5 days must have morning, afternoon, and evening activities
11. Include public transport (train/subway) usage
12. At least 1 food market visit (Tsukiji/Toyosu)
13. Budget breakdown per day must be provided
14. Include at least 1 nature activity (park, garden, mountain)
15. Evening activities should include at least 2 different areas (e.g., Shibuya, Shinjuku, Roppongi)""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "total_days": "5",
                "within_budget": "yes",
                "has_temple": "yes",
                "has_akihabara": "yes",
                "has_japanese_meal": "yes",
                "has_daytrip": "yes",
                "hotel_under_150": "yes",
                "free_activities_min_2": "yes",
                "has_cultural": "yes",
                "has_modern": "yes",
                "all_3_slots": "yes",
                "has_train": "yes",
                "has_food_market": "yes",
                "has_budget_breakdown": "yes",
                "has_nature": "yes"
            }
        }
    },

    # H-43: SYNTHESIZER — 15 claims to verify
    {
        "id": 43, "role": "Synthesizer / Aggregator", "tier": 3,
        "scoring_type": "json_values",
        "prompt": """Given these 5 conflicting reports about a product launch, synthesize and verify 15 claims as CONFIRMED, CONTRADICTED, or UNVERIFIED. Respond as JSON: {"1": "CONFIRMED/CONTRADICTED/UNVERIFIED", ...}

Report A (Press Release): "TechCo launched ProductX on March 1 at $49.99. Supports Windows, Mac, and Linux. Free trial: 14 days. Over 1,000 beta testers. CEO John Smith said 'revolutionary.'"
Report B (Tech Blog): "ProductX launched February 28 (early access). Price: $49.99 (introductory, normally $79.99). Windows and Mac only at launch, Linux coming Q2. 30-day free trial."
Report C (User Forum): "Got ProductX on March 1. Paid $49.99. Linux version doesn't work. Free trial was only 14 days for me. About 500 beta testers according to community manager."
Report D (Competitor Analysis): "ProductX launched at $49.99, undercutting our $69.99. Supports Windows and Mac. No Linux support observed. They claim 1,000+ beta testers but we estimate 600-800."
Report E (Internal Leak): "Launch date was March 1. Pricing: $49.99 introductory for 6 months, then $79.99. Linux support delayed to Q3. Beta program had 847 participants."

Claims:
1. ProductX price is $49.99
2. ProductX supports Linux at launch
3. Free trial is 14 days
4. Over 1,000 beta testers participated
5. CEO's name is John Smith
6. Launch date was March 1
7. Normal price is $79.99
8. Free trial is 30 days
9. ProductX supports Windows
10. ProductX supports Mac
11. Linux coming in Q2
12. The $49.99 price is introductory/temporary
13. Beta tester count was approximately 847
14. ProductX launched on February 28
15. The product is described as 'revolutionary'""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "CONFIRMED", "2": "CONTRADICTED", "3": "CONTRADICTED",
                "4": "CONTRADICTED", "5": "UNVERIFIED", "6": "CONFIRMED",
                "7": "CONFIRMED", "8": "CONTRADICTED", "9": "CONFIRMED",
                "10": "CONFIRMED", "11": "CONTRADICTED", "12": "CONFIRMED",
                "13": "UNVERIFIED", "14": "CONTRADICTED", "15": "UNVERIFIED"
            }
        }
    },

    # H-44: CURRICULUM DESIGN — 15 constraints
    {
        "id": 44, "role": "Curriculum / Course Designer", "tier": 3,
        "scoring_type": "h_keywords",
        "prompt": """Design a 6-week Python programming course. Respond as JSON: {"weeks": [{"week": 1, "topic": "...", "objectives": [...], "assignment": "...", "prerequisites": [...]}]}

ALL 15 constraints:
1. Exactly 6 weeks
2. Start with fundamentals (variables, types) in week 1
3. Include OOP (classes, inheritance) by week 4
4. Include error handling (try/except) before week 5
5. Include file I/O before the final project
6. Week 6 must be a capstone project
7. Each week must have 2-4 learning objectives
8. Each week must have 1 assignment
9. Prerequisites must reference earlier weeks only
10. Week 1 must have no prerequisites
11. Include at least 1 week on data structures (lists, dicts)
12. Include testing concepts (unittest/pytest) before capstone
13. Assignments must increase in complexity
14. Include at least 1 practical project (not just exercises)
15. Total learning objectives across all weeks: between 15-20""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "total_weeks": "6",
                "w1_fundamentals": "yes",
                "oop_by_w4": "yes",
                "error_handling_before_w5": "yes",
                "file_io_before_w6": "yes",
                "w6_capstone": "yes",
                "objectives_2_4": "yes",
                "each_has_assignment": "yes",
                "valid_prerequisites": "yes",
                "w1_no_prereqs": "yes",
                "has_data_structures": "yes",
                "has_testing": "yes",
                "increasing_complexity": "yes",
                "has_practical_project": "yes",
                "objectives_15_20": "yes"
            }
        }
    },

    # H-45: PROTOTYPE GENERATOR — 15 test cases
    {
        "id": 45, "role": "Prototype Generator", "tier": 3,
        "scoring_type": "code_exec",
        "prompt": """Write a Python class `JSONValidator` that validates JSON-like data against a schema. NO imports needed.

Schema format: {"field_name": {"type": "str/int/float/bool/list/dict", "required": true/false, "min": N, "max": N, "min_length": N, "max_length": N}}

Method: `validate(data, schema)` → returns {"valid": True/False, "errors": [list of error strings]}

Rules:
- Check type matches (str, int, float, bool, list, dict)
- If required=true and field is missing, error
- For numbers: check min/max if specified
- For strings: check min_length/max_length if specified
- For lists: check min_length/max_length for list length
- Extra fields not in schema are allowed (no error)
- Return all errors, not just first one""",
        "scoring": {
            "type": "code_exec",
            "test_cases": [
                {"call": "v = JSONValidator(); r = v.validate({'name': 'Alice', 'age': 30}, {'name': {'type': 'str', 'required': True}, 'age': {'type': 'int', 'required': True}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({}, {'name': {'type': 'str', 'required': True}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'age': 'thirty'}, {'age': {'type': 'int', 'required': True}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'score': 150}, {'score': {'type': 'int', 'required': True, 'min': 0, 'max': 100}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'score': 50}, {'score': {'type': 'int', 'required': True, 'min': 0, 'max': 100}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'name': 'AB'}, {'name': {'type': 'str', 'required': True, 'min_length': 3}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'tags': [1,2,3]}, {'tags': {'type': 'list', 'required': True, 'min_length': 2}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'tags': [1]}, {'tags': {'type': 'list', 'required': True, 'min_length': 2}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'active': True}, {'active': {'type': 'bool', 'required': True}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'extra': 'field', 'name': 'test'}, {'name': {'type': 'str', 'required': True}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({}, {'opt': {'type': 'str', 'required': False}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'x': -5}, {'x': {'type': 'int', 'required': True, 'min': 0}}); r['valid']", "expected": "False"},
                {"call": "v = JSONValidator(); r = v.validate({'x': 3.14}, {'x': {'type': 'float', 'required': True}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'d': {'a': 1}}, {'d': {'type': 'dict', 'required': True}}); r['valid']", "expected": "True"},
                {"call": "v = JSONValidator(); r = v.validate({'name': 'ABCDEF'}, {'name': {'type': 'str', 'required': True, 'max_length': 5}}); r['valid']", "expected": "False"},
            ]
        }
    },

    # H-50: ORCHESTRATOR — 15 constraints
    {
        "id": 50, "role": "Orchestrator / Manager Agent", "tier": 5,
        "scoring_type": "h_keywords",
        "prompt": """Design a multi-agent workflow for processing a customer refund request. Respond as JSON: {"agents": [{"name": "...", "input": "...", "output": "...", "next": "...", "fallback": "..."}], "constraints": {...}}

15 constraints:
1. Minimum 6 agents in the pipeline
2. Must include: validation, fraud-check, approval, payment, notification agents
3. Each agent must have defined input, output, and next step
4. Must have at least 1 conditional branch (if/else routing)
5. Must have a fallback/error handler for each agent
6. First agent must be a validation/triage agent
7. Last agent must be a notification agent
8. Fraud check must happen before approval
9. Payment processing must happen after approval
10. Total expected processing time must be under 60 seconds
11. Must handle both approved and rejected outcomes
12. Must include logging/audit at each step
13. No circular dependencies
14. Must include human escalation path for edge cases
15. Each agent must have a timeout value""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "min_6_agents": "yes",
                "has_validation": "yes",
                "has_fraud_check": "yes",
                "has_approval": "yes",
                "has_payment": "yes",
                "has_notification": "yes",
                "has_io_defined": "yes",
                "has_conditional": "yes",
                "has_fallback": "yes",
                "starts_validation": "yes",
                "ends_notification": "yes",
                "fraud_before_approval": "yes",
                "payment_after_approval": "yes",
                "handles_rejection": "yes",
                "has_escalation": "yes"
            }
        }
    },

    # H-51: SOFTWARE ARCHITECT — 15 design decisions
    {
        "id": 51, "role": "Software Architect Agent", "tier": 5,
        "scoring_type": "h_keywords",
        "prompt": """Design a system architecture for a real-time collaborative document editor (like Google Docs). Answer 15 architecture questions. Respond as JSON: {"q1": "answer", ...}

q1: What conflict resolution strategy? (OT/CRDT/locking)
q2: WebSocket or SSE for real-time sync?
q3: What database for document storage? (single best choice)
q4: How to handle offline editing?
q5: What message broker for real-time events?
q6: Horizontal scaling strategy for WebSocket servers?
q7: How to handle cursor position sharing?
q8: Authentication protocol?
q9: How to implement version history?
q10: CDN strategy for static assets?
q11: How to handle large documents (1000+ pages)?
q12: Rate limiting approach?
q13: Data backup strategy?
q14: How to handle concurrent image uploads?
q15: Monitoring and observability stack?""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "q1_valid": "OT or CRDT",
                "q2_valid": "WebSocket",
                "q3_valid": "database mentioned",
                "q4_valid": "local storage or sync queue",
                "q5_valid": "message broker mentioned",
                "q6_valid": "sticky sessions or shared state",
                "q7_valid": "broadcast or presence channel",
                "q8_valid": "OAuth or JWT",
                "q9_valid": "snapshots or event log",
                "q10_valid": "CDN mentioned",
                "q11_valid": "chunking or pagination",
                "q12_valid": "token bucket or similar",
                "q13_valid": "regular backups mentioned",
                "q14_valid": "object storage or async",
                "q15_valid": "logging and metrics mentioned"
            }
        }
    },

    # H-52: COMPLEX DEBUGGER — 15 bugs
    {
        "id": 52, "role": "Complex Debugger Agent", "tier": 5,
        "scoring_type": "h_content_check",
        "prompt": """Find ALL 15 bugs in this async Python code. Respond as JSON: {"bugs": [{"line": "...", "bug": "...", "fix": "..."}, ...], "count": 15}

```python
import asyncio
import aiohttp

class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = []  # Line 8: Bug

    async def acquire(self):
        now = asyncio.get_event_loop().time()  # Line 11: Bug
        self.requests = [r for r in self.requests if now - r < self.period]
        if len(self.requests) >= self.max_requests:
            wait = self.requests[0] + self.period - now
            await asyncio.sleep(wait)
        self.requests.append(now)

async def fetch_all(urls, max_concurrent=10):
    results = {}
    semaphore = asyncio.Semaphore(max_concurrent)
    limiter = RateLimiter(100, 60)

    async def fetch_one(url):
        async with semaphore:
            await limiter.acquire()
            async with aiohttp.ClientSession() as session:  # Line 25: Bug
                try:
                    response = await session.get(url, timeout=30)  # Line 27: Bug
                    data = await response.json()
                    results[url] = data  # Line 29: Bug
                except Exception:
                    results[url] = None  # Line 31: Bug
                    pass  # Line 32: Bug

    tasks = [fetch_one(url) for url in urls]
    await asyncio.gather(*tasks)  # Line 35: Bug
    return results

async def process_batch(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        tasks = []
        for item in batch:
            task = process_item(item)  # Line 42: Bug - missing await
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for r in results:
            yield r  # Line 45: Bug

async def process_item(item):
    await asyncio.sleep(0.1)
    return item * 2

class ConnectionPool:
    def __init__(self, size=10):
        self.pool = []  # Line 52: Bug
        self.size = size

    async def get_connection(self):
        if self.pool:
            return self.pool.pop()
        return await self.create_connection()

    async def release(self, conn):
        self.pool.append(conn)  # Line 60: Bug

    async def create_connection(self):
        return object()  # Line 63: Bug

async def main():
    urls = ["http://example.com"] * 100
    results = await fetch_all(urls)
    print(f"Got {len(results)} results")  # Line 68: Bug
```""",
        "scoring": {
            "checks": {
                "b1_list_not_safe": ["thread-safe", "race condition", "lock", "concurrent", "shared"],
                "b2_get_event_loop": ["get_event_loop", "deprecated", "get_running_loop"],
                "b3_session_per_request": ["session", "per request", "new session", "clientsession"],
                "b4_timeout_type": ["timeout", "clienttimeout", "aiohttp"],
                "b5_dict_mutation": ["dict", "concurrent", "mutation", "results"],
                "b6_swallow_errors": ["swallow", "silent", "log", "error"],
                "b7_bare_pass": ["pass", "bare", "retry", "exception"],
                "b8_gather_exceptions": ["gather", "return_exceptions", "crash"],
                "b9_missing_await": ["await", "coroutine", "not awaited"],
                "b10_yield_async": ["yield", "async generator", "async for", "async iter"],
                "b11_unbounded_pool": ["unbounded", "pool", "queue", "asyncio.queue"],
                "b12_pool_size": ["size", "pool", "grow", "limit", "beyond"],
                "b13_dummy_connection": ["dummy", "object", "real connection", "placeholder"],
                "b14_same_url": ["same url", "duplicate", "1 key", "one key", "overwrite"],
                "b15_session_cleanup": ["cleanup", "close", "session", "leak"]
            }
        }
    },
]
