"""
Phase G: Discriminator Tests
Harder tests designed to separate model quality for roles where
all tested models currently score identically (ceiling effect).
Each test uses graduated scoring (15-25 sub-checks) for smooth 0-10 scale.
"""

PHASE_G_TESTS = [
    # ================================================================
    # G-36: CODE GENERATION — Multi-Constraint Rate Limiter
    # Current Phase F: merge_intervals → all models 10/10
    # ================================================================
    {
        "id": 36, "role": "Code Generation Agent", "tier": 3,
        "phase": "G",
        "scoring_type": "code",
        "prompt": """Write a Python class `RateLimiter` that implements a hybrid token-bucket / sliding-window rate limiter.

Requirements (ALL must be implemented):
1. Constructor: `RateLimiter(max_requests: int, window_seconds: float, burst: int = 0)`
   - max_requests: max allowed in the window
   - window_seconds: sliding window duration
   - burst: extra requests allowed above max (temporary burst)

2. Method: `allow(user_id: str, endpoint: str = "default") -> dict`
   Returns: {"allowed": bool, "remaining": int, "retry_after": float or None}
   - Tracks limits per (user_id, endpoint) pair independently
   - If burst > 0, allow up to max_requests + burst, but burst tokens regenerate slower (2x window)

3. Method: `allow_priority(user_id: str, endpoint: str = "default") -> dict`
   - Always returns {"allowed": True, ...} — priority users skip limits

4. Method: `cleanup(max_age_seconds: float = None) -> int`
   - Remove entries older than max_age_seconds (default: 2 * window_seconds)
   - Returns count of removed entries

5. Method: `get_usage(user_id: str, endpoint: str = "default") -> dict`
   Returns: {"used": int, "limit": int, "window_seconds": float, "burst_remaining": int}

6. Method: `to_dict() -> dict` and class method `from_dict(data: dict) -> RateLimiter`
   - Serialize/deserialize full state

7. Must use `time.time()` for timestamps (no external deps)

Give ONLY the class code, no explanation. No imports except `time`, `threading`, `collections`.""",
        "scoring": {
            "type": "code_exec",
            "function_name": None,
            "class_name": "RateLimiter",
            "test_cases": [
                # Basic allow/deny (2 pts)
                {"test": "basic_allow", "code": """
rl = RateLimiter(3, 1.0)
r1 = rl.allow("user1")
assert r1["allowed"] == True
assert r1["remaining"] == 2
r2 = rl.allow("user1")
r3 = rl.allow("user1")
r4 = rl.allow("user1")
assert r4["allowed"] == False
assert r4["remaining"] == 0
assert r4["retry_after"] is not None and r4["retry_after"] > 0
"""},
                {"test": "basic_allow2", "code": """
rl = RateLimiter(2, 0.5)
rl.allow("u1")
rl.allow("u1")
r = rl.allow("u1")
assert r["allowed"] == False
import time; time.sleep(0.6)
r = rl.allow("u1")
assert r["allowed"] == True
"""},
                # Per-user isolation (1 pt)
                {"test": "per_user", "code": """
rl = RateLimiter(2, 1.0)
rl.allow("alice")
rl.allow("alice")
r_alice = rl.allow("alice")
r_bob = rl.allow("bob")
assert r_alice["allowed"] == False
assert r_bob["allowed"] == True
"""},
                # Per-endpoint isolation (1 pt)
                {"test": "per_endpoint", "code": """
rl = RateLimiter(2, 1.0)
rl.allow("user1", "/api/a")
rl.allow("user1", "/api/a")
r_a = rl.allow("user1", "/api/a")
r_b = rl.allow("user1", "/api/b")
assert r_a["allowed"] == False
assert r_b["allowed"] == True
"""},
                # Burst allowance (1 pt)
                {"test": "burst", "code": """
rl = RateLimiter(2, 1.0, burst=2)
r1 = rl.allow("u1")
r2 = rl.allow("u1")
r3 = rl.allow("u1")  # burst 1
r4 = rl.allow("u1")  # burst 2
r5 = rl.allow("u1")  # over burst
assert r3["allowed"] == True
assert r4["allowed"] == True
assert r5["allowed"] == False
"""},
                # Priority override (1 pt)
                {"test": "priority", "code": """
rl = RateLimiter(1, 1.0)
rl.allow("admin")
r = rl.allow("admin")
assert r["allowed"] == False
rp = rl.allow_priority("admin")
assert rp["allowed"] == True
"""},
                # Cleanup (1 pt)
                {"test": "cleanup", "code": """
import time
rl = RateLimiter(5, 0.3)
rl.allow("u1"); rl.allow("u2"); rl.allow("u3")
time.sleep(0.7)
removed = rl.cleanup()
assert removed >= 2
"""},
                # get_usage (1 pt)
                {"test": "get_usage", "code": """
rl = RateLimiter(5, 1.0, burst=3)
rl.allow("u1"); rl.allow("u1"); rl.allow("u1")
u = rl.get_usage("u1")
assert u["used"] == 3
assert u["limit"] == 5
assert u["window_seconds"] == 1.0
"""},
                # Serialization roundtrip (1 pt)
                {"test": "serialize", "code": """
rl = RateLimiter(5, 1.0, burst=2)
rl.allow("u1"); rl.allow("u1")
d = rl.to_dict()
rl2 = RateLimiter.from_dict(d)
u = rl2.get_usage("u1")
assert u["used"] == 2
assert u["limit"] == 5
"""},
                # Window sliding (1 pt)
                {"test": "window_slide", "code": """
import time
rl = RateLimiter(3, 0.5)
rl.allow("u1"); rl.allow("u1"); rl.allow("u1")
assert rl.allow("u1")["allowed"] == False
time.sleep(0.6)
assert rl.allow("u1")["allowed"] == True
assert rl.allow("u1")["allowed"] == True
assert rl.allow("u1")["allowed"] == True
assert rl.allow("u1")["allowed"] == False
"""},
            ]
        }
    },

    # ================================================================
    # G-2: INPUT VALIDATOR — Nested + Cross-Field Dependencies
    # Current Phase F: 10 obvious flat errors → all models 10/10
    # ================================================================
    {
        "id": 2, "role": "Input Validator / Sanitizer", "tier": 1,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Validate this complex nested API payload. Find ALL errors (there are exactly 15). Respond with ONLY JSON: {"errors": ["description1", ...], "error_count": 15}

Cross-field validation rules:
- If `same_as_shipping` is true, billing address must exactly match shipping address
- Each item's `subtotal` must equal `quantity * unit_price`
- `order_total` must equal sum of all subtotals minus `discount_amount`
- `delivery_date` must be after `order_date`
- `payment.card_expiry` must be after `order_date`
- `customer.email` domain must not be a disposable email (mailinator.com, tempmail.com, guerrillamail.com) 
- `shipping.zip` must be valid for `shipping.state` (NY zips start with 1, CA with 9, TX with 7)
- `items` array must have 1-50 items, each with quantity 1-999
- `payment.amount` must equal `order_total`
- `customer.phone` country code must match `shipping.country`

Payload:
```json
{
  "customer": {
    "name": "John Smith",
    "email": "john@mailinator.com",
    "phone": "+44-555-012-3456",
    "loyalty_tier": "platinum"
  },
  "shipping": {
    "address": {"street": "123 Main St", "city": "Los Angeles", "state": "CA", "zip": "10001", "country": "US"},
    "method": "express",
    "delivery_date": "2025-12-15"
  },
  "billing": {
    "same_as_shipping": true,
    "address": {"street": "456 Oak Ave", "city": "New York", "state": "NY", "zip": "90210", "country": "US"}
  },
  "items": [
    {"sku": "ITEM-001", "name": "Widget A", "quantity": 3, "unit_price": 29.99, "subtotal": 89.97},
    {"sku": "ITEM-002", "name": "Widget B", "quantity": 2, "unit_price": 49.99, "subtotal": 109.98},
    {"sku": "ITEM-003", "name": "Widget C", "quantity": 0, "unit_price": 15.00, "subtotal": 15.00},
    {"sku": "", "name": "Widget D", "quantity": 1, "unit_price": -5.00, "subtotal": -5.00}
  ],
  "order_date": "2026-01-15",
  "discount_code": "SAVE20",
  "discount_amount": 50.00,
  "order_total": 159.95,
  "payment": {
    "method": "credit_card",
    "card_last4": "12345",
    "card_expiry": "2025-06",
    "amount": 200.00,
    "currency": "GBP"
  },
  "notes": ""
}
```""",
        "scoring": {
            "type": "error_count_graduated",
            "expected_count": 15,
            "expected_errors": [
                "disposable email (mailinator.com)",
                "phone country code +44 doesn't match US shipping",
                "CA zip 10001 invalid (should start with 9)",
                "delivery_date 2025-12-15 is before order_date 2026-01-15",
                "billing address differs but same_as_shipping is true",
                "billing zip 90210 invalid for NY (should start with 1)",
                "item 2 subtotal wrong (2 * 49.99 = 99.98, not 109.98)",
                "item 3 quantity is 0 (must be 1-999)",
                "item 3 subtotal wrong (0 * 15 = 0, not 15)",
                "item 4 empty SKU",
                "item 4 negative unit_price",
                "item 4 subtotal wrong (1 * -5 = -5 but also negative price invalid)",
                "order_total incorrect (sum of subtotals minus discount doesn't match)",
                "card_expiry 2025-06 is before order_date 2026-01-15",
                "payment amount 200.00 doesn't match order_total 159.95",
            ]
        }
    },

    # ================================================================
    # G-5: SENTIMENT — Hard Cases, Nested Sarcasm, Domain-Specific
    # Current Phase F: 10 statements → all models 10/10
    # ================================================================
    {
        "id": 5, "role": "Sentiment Analysis Agent", "tier": 1,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Classify each statement's sentiment as exactly one of: positive, negative, neutral, mixed.

Watch for: nested sarcasm, domain-specific context, cultural references, understatement, and misdirection.

Respond with ONLY JSON: {"1": "sentiment", ..., "20": "sentiment"}

1. "The model achieved 0.3% improvement on the benchmark, which the authors describe as 'groundbreaking'."
2. "I've seen better error messages from a 404 page, but at least it didn't crash this time."
3. "The server has maintained 99.97% uptime, missing our 99.99% SLA by exactly 13 minutes."
4. "Oh wonderful, they deprecated the only API endpoint that actually worked. Progress!"
5. "Not the worst migration I've survived, which is genuinely the highest praise I can give."
6. "Revenue grew 2% while the market grew 15%."
7. "The intern's first PR had fewer bugs than our senior dev's last three combined."
8. "Sure, the UI redesign is 'modern' — if by modern you mean it takes 3 clicks to do what used to take 1."
9. "The battery lasts all day... if your day ends at 2 PM."
10. "I'm not saying the documentation is bad. I'm saying archaeologists would have an easier time with the Dead Sea Scrolls."
11. "Achieved $2M ARR in 18 months with zero paid marketing."
12. "The refactoring reduced code complexity by 40% and only introduced 2 new regressions."
13. "Their 'AI-powered' search still can't find an exact title match, but hey, it suggests related products really well."
14. "Lost only 3 customers this quarter, down from 47 last quarter."
15. "The team delivered on time and on budget for the first time in the company's history. Nobody believed it was possible."
16. "Stack Overflow copypasta with zero understanding, submitted as 'original implementation'."
17. "The framework has excellent documentation, an active community, and absolutely no backwards compatibility."
18. "Despite the layoffs, remaining employees report higher satisfaction — likely because the complainers were let go."
19. "Q3 results were flat, exactly matching analyst expectations."
20. "I wouldn't call it technical debt. It's more like technical bankruptcy with no restructuring plan." """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "negative", "2": "mixed", "3": "negative", "4": "negative",
                "5": "mixed", "6": "negative", "7": "mixed", "8": "negative",
                "9": "negative", "10": "negative", "11": "positive", "12": "mixed",
                "13": "negative", "14": "positive", "15": "positive", "16": "negative",
                "17": "mixed", "18": "mixed", "19": "neutral", "20": "negative"
            }
        }
    },

    # ================================================================
    # G-40: FACT-CHECKING — Plausible Falsehoods + Reasoning
    # Current Phase F: 10 well-known facts → all models 10/10
    # ================================================================
    {
        "id": 40, "role": "Fact-Checking Agent", "tier": 3,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Label each claim TRUE or FALSE. These are tricky — many are close to true but wrong in subtle ways. Respond as JSON: {"1": "TRUE" or "FALSE", ..., "20": "TRUE" or "FALSE"}

1. Python 3.0 was released in December 2008.
2. Git was initially released in 2004 by Linus Torvalds.
3. The first version of JavaScript was created in 10 days.
4. Redis is single-threaded for all operations including I/O.
5. Docker containers share the host OS kernel.
6. REST was defined by Roy Fielding in his 2000 doctoral dissertation.
7. SHA-256 has never had a collision found.
8. IPv6 addresses are 64 bits long.
9. The CAP theorem states you can only have 2 of: Consistency, Availability, Performance.
10. Kubernetes was originally developed at Google based on their Borg system.
11. The first commit to Linux kernel was in 1991.
12. TCP guarantees in-order delivery of packets.
13. UTF-8 can encode any Unicode character in at most 4 bytes.
14. MongoDB is ACID compliant for single-document operations.
15. The HTTP/2 protocol was standardized in 2015.
16. Rust was first released by Mozilla in 2010.
17. WebAssembly became a W3C recommendation in December 2019.
18. The maximum length of a URL is 2,048 characters per the HTTP spec.
19. Python's GIL prevents all multi-threaded execution.
20. gzip compression uses the DEFLATE algorithm.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "TRUE", "2": "FALSE", "3": "TRUE", "4": "FALSE",
                "5": "TRUE", "6": "TRUE", "7": "TRUE", "8": "FALSE",
                "9": "FALSE", "10": "TRUE", "11": "TRUE", "12": "TRUE",
                "13": "TRUE", "14": "TRUE", "15": "TRUE", "16": "FALSE",
                "17": "TRUE", "18": "FALSE", "19": "FALSE", "20": "TRUE"
            }
        }
    },

    # ================================================================
    # G-49: ALGORITHM — LRU Cache with TTL + Stats
    # Current Phase F: single algo → all models 10/10
    # ================================================================
    {
        "id": 49, "role": "Algorithm / Data Structure Explorer", "tier": 4,
        "phase": "G",
        "scoring_type": "code",
        "prompt": """Write a Python class `LRUCache` with time-based expiration.

Requirements:
1. `__init__(self, capacity: int)` — max items before LRU eviction
2. `get(self, key: str) -> any` — return value or None if missing/expired
3. `put(self, key: str, value: any, ttl: float = None)` — ttl in seconds, None = no expiry
4. `delete(self, key: str) -> bool` — return True if key existed
5. `size(self) -> int` — current number of non-expired entries
6. `get_stats(self) -> dict` — {"hits": N, "misses": N, "evictions": N, "expirations": N}
7. `keys(self) -> list` — return all non-expired keys in most-recently-used order
8. `clear(self) -> None` — remove all entries, reset stats

Constraints:
- get and put must be O(1) average time (use OrderedDict or dict + doubly linked list)
- Expired entries should be lazily removed on access
- Must use `time.time()` for timestamps
- No external dependencies

Give ONLY the class code. No explanation.""",
        "scoring": {
            "type": "code_exec",
            "function_name": None,
            "class_name": "LRUCache",
            "test_cases": [
                {"test": "basic_put_get", "code": """
c = LRUCache(3)
c.put("a", 1)
c.put("b", 2)
assert c.get("a") == 1
assert c.get("b") == 2
assert c.get("c") is None
"""},
                {"test": "capacity_eviction", "code": """
c = LRUCache(2)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
assert c.get("a") is None  # evicted (LRU)
assert c.get("b") == 2
assert c.get("c") == 3
"""},
                {"test": "lru_order", "code": """
c = LRUCache(3)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
c.get("a")  # a is now most recently used
c.put("d", 4)  # should evict b (least recently used)
assert c.get("b") is None
assert c.get("a") == 1
"""},
                {"test": "ttl_expiry", "code": """
import time
c = LRUCache(10)
c.put("x", 100, ttl=0.3)
assert c.get("x") == 100
time.sleep(0.4)
assert c.get("x") is None
"""},
                {"test": "ttl_no_expiry", "code": """
import time
c = LRUCache(10)
c.put("a", 1, ttl=None)
c.put("b", 2, ttl=0.2)
time.sleep(0.3)
assert c.get("a") == 1  # no TTL, still alive
assert c.get("b") is None  # expired
"""},
                {"test": "stats_hits_misses", "code": """
c = LRUCache(5)
c.put("a", 1); c.put("b", 2)
c.get("a")  # hit
c.get("b")  # hit
c.get("c")  # miss
s = c.get_stats()
assert s["hits"] == 2
assert s["misses"] == 1
"""},
                {"test": "stats_evictions", "code": """
c = LRUCache(2)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
s = c.get_stats()
assert s["evictions"] == 1
"""},
                {"test": "delete", "code": """
c = LRUCache(5)
c.put("a", 1)
assert c.delete("a") == True
assert c.delete("a") == False
assert c.get("a") is None
"""},
                {"test": "size", "code": """
c = LRUCache(10)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
assert c.size() == 3
c.delete("b")
assert c.size() == 2
"""},
                {"test": "keys_order", "code": """
c = LRUCache(5)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
c.get("a")  # move a to most recent
k = c.keys()
assert k[0] == "a"  # most recently used first
assert "b" in k and "c" in k
"""},
                {"test": "clear", "code": """
c = LRUCache(5)
c.put("a", 1); c.put("b", 2)
c.get("a")
c.clear()
assert c.size() == 0
assert c.get("a") is None
s = c.get_stats()
assert s["hits"] == 0
"""},
                {"test": "update_existing", "code": """
c = LRUCache(2)
c.put("a", 1)
c.put("a", 2)
assert c.get("a") == 2
assert c.size() == 1
"""},
                {"test": "evict_expired_first", "code": """
import time
c = LRUCache(3)
c.put("a", 1, ttl=0.2)
c.put("b", 2)
c.put("c", 3)
time.sleep(0.3)
c.put("d", 4)  # should evict expired "a" or LRU
assert c.get("b") is not None or c.get("c") is not None
"""},
                {"test": "stats_expirations", "code": """
import time
c = LRUCache(10)
c.put("x", 1, ttl=0.2)
time.sleep(0.3)
c.get("x")  # triggers lazy expiration
s = c.get_stats()
assert s["expirations"] >= 1
"""},
                {"test": "many_items", "code": """
c = LRUCache(100)
for i in range(200):
    c.put(f"k{i}", i)
assert c.size() == 100
s = c.get_stats()
assert s["evictions"] == 100
"""},
            ]
        }
    },

    # ================================================================
    # G-51: ARCHITECT — Trade-off Analysis with Measurable Constraints
    # Current Phase F: keyword presence → all models 10/10
    # ================================================================
    {
        "id": 51, "role": "System Architect", "tier": 5,
        "phase": "G",
        "scoring_type": "constraint",
        "prompt": """Design a URL shortener system. Respond as JSON with this exact structure.

Scale requirements:
- 10 million new short URLs created daily
- 1 billion redirect requests daily (100:1 read:write ratio)
- < 50ms p99 redirect latency
- 99.99% uptime target
- Must support custom aliases
- Must support link expiration
- Must comply with GDPR (data deletion on request)
- Budget: $5,000/month infrastructure
- Must handle 10x traffic spikes (Black Friday etc)

Output this exact JSON structure:
{
  "architecture": {
    "components": ["list of services/systems"],
    "database": {"primary": "...", "justification": "..."},
    "cache": {"type": "...", "strategy": "...", "invalidation": "..."},
    "hash_strategy": {"algorithm": "...", "length": N, "collision_handling": "..."}
  },
  "scaling": {
    "read_write_ratio": "...",
    "read_optimization": "...",
    "write_path": "...",
    "horizontal_scaling": "..."
  },
  "reliability": {
    "uptime_strategy": "...",
    "failover": "...",
    "data_replication": "..."
  },
  "compliance": {
    "gdpr_deletion": "...",
    "data_retention": "...",
    "analytics_separation": "..."
  },
  "cost_estimate": {
    "monthly_total": N,
    "breakdown": {"compute": N, "database": N, "cache": N, "cdn": N, "other": N},
    "fits_budget": true/false
  },
  "rate_limiting": {"strategy": "...", "limits": "..."},
  "monitoring": {"metrics": [...], "alerting": "..."}
}""",
        "scoring": {
            "type": "architecture_deep",
            "checks": [
                "mentions_read_write_ratio_100_1",
                "has_caching_with_invalidation_strategy",
                "database_has_justification_not_just_name",
                "hash_collision_handling_explicit",
                "cost_fits_5k_budget",
                "gdpr_deletion_mechanism",
                "custom_alias_support",
                "link_expiration_mechanism",
                "failover_multi_region",
                "rate_limiting_on_create",
                "analytics_separate_from_redirect",
                "handles_traffic_spikes",
                "monitoring_metrics_listed",
                "horizontal_scaling_described",
                "data_replication_described"
            ]
        }
    },

    # ================================================================
    # G-48: STEM ANALYSIS — Multi-Step Calculation with Unit Conversion
    # Current Phase F: straightforward → all models 10/10
    # ================================================================
    {
        "id": 48, "role": "STEM Research Analyst", "tier": 4,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Solve ALL 8 problems. Respond as JSON: {"q1": answer, ..., "q8": answer}

Answers must be numeric (round to 2 decimal places where needed).

Q1: A data center consumes 2.5 MW. PUE (Power Usage Effectiveness) is 1.4. If electricity costs $0.08/kWh, what is the monthly electricity bill for the ENTIRE facility (including cooling)? Answer in dollars.

Q2: An API processes requests at 50ms p50 latency with standard deviation of 15ms (normal distribution). What percentage of requests exceed 80ms? Answer as percentage (e.g., 2.28).

Q3: A distributed system has 5 nodes, each with 99.9% uptime independently. If the system requires 3 of 5 nodes to function (quorum), what is the system's effective uptime percentage? Answer as percentage with 6 decimal places.

Q4: A model with 70B parameters at FP16 (2 bytes per param) needs how many H100 GPUs (80GB each) just for model weights? Assume no overhead. Answer as integer.

Q5: If you compress a 1TB dataset with gzip achieving 3.2:1 ratio, then transfer it over a 10 Gbps link, how many minutes does the transfer take? Answer in minutes.

Q6: A hash function produces 64-bit hashes. After inserting N keys, the probability of at least one collision exceeds 50%. What is N? (Birthday problem — answer as integer, rounded to nearest thousand)

Q7: A Redis cluster processes 100,000 ops/sec with 64-byte average key and 256-byte average value. What is the minimum network bandwidth needed in Gbps? (Include both directions — request + response)

Q8: An ML training job uses 8 A100 GPUs at 70% utilization for 3 days. At $2.50/GPU-hour, what is the total cost? Answer in dollars.""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "q1": 252000,
                "q2": 2.28,
                "q3": 99.999,
                "q4": 2,
                "q5": 4.17,
                "q6": 5000000,
                "q7": 2.44,
                "q8": 1440
            },
            "tolerance": {
                "q1": 10000,
                "q2": 0.5,
                "q3": 0.002,
                "q4": 0,
                "q5": 0.5,
                "q6": 500000,
                "q7": 0.5,
                "q8": 50
            }
        }
    },

    # ================================================================
    # G-9: RESEARCH — Comparative Analysis with Contradictions
    # Current Phase F: keyword matching → all models 10/10
    # ================================================================
    {
        "id": 9, "role": "Research Agent", "tier": 2,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Analyze these 6 conflicting data sources about microservices vs monolith architecture and answer ALL questions. Respond as JSON.

Source A (2024 survey, 500 companies): "78% of companies with >100 developers use microservices. Average deployment frequency: 12x/day. Infrastructure cost: 3.2x higher than monolith."
Source B (performance study, 50 apps): "Microservices add 5-15ms latency per service hop. 90th percentile response time: 340ms vs 120ms for monolith equivalent."
Source C (failure analysis, 200 incidents): "67% of microservice outages caused by network issues. MTTR: 45 min for microservices vs 28 min for monolith."
Source D (developer survey, 2000 devs): "Developer satisfaction 15% higher with microservices. Onboarding time: 3 weeks vs 1 week for monolith."
Source E (cost study, 100 companies): "Total cost of ownership over 3 years: microservices 40% higher for <50 devs, 20% LOWER for >200 devs."
Source F (migration report, 30 companies): "Average migration time: 18 months. 40% reported net positive ROI within 2 years. 25% rolled back to monolith."

Questions:
{"q1": "At what team size does microservices become cost-effective? (number)",
 "q2": "What is the latency penalty range in ms? (e.g., '5-15')",
 "q3": "What percentage of microservice outages are network-related?",
 "q4": "MTTR difference in minutes (microservices minus monolith)?",
 "q5": "Onboarding time multiplier for microservices vs monolith? (e.g., 3.0)",
 "q6": "What fraction of companies that migrated rolled back?",
 "q7": "Infrastructure cost multiplier for microservices?",
 "q8": "Do Sources A and E contradict on cost? (yes/no and explain in 1 sentence)",
 "q9": "Developer satisfaction improvement percentage?",
 "q10": "What percentage achieved positive ROI within 2 years?"}""",
        "scoring": {
            "type": "json_values_mixed",
            "answers": {
                "q1": "200",
                "q2": "5-15",
                "q3": "67",
                "q4": "17",
                "q5": "3.0",
                "q6": "0.25",
                "q7": "3.2",
                "q8_contains": "yes",
                "q9": "15",
                "q10": "40"
            }
        }
    },

    # ================================================================
    # G-12: CONTENT PLANNER — Complex Calendar with Dependencies
    # Current Phase F: loose constraints → all models 10/10
    # ================================================================
    {
        "id": 12, "role": "Content Planner / Strategist", "tier": 2,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Create a 4-week content calendar for a B2B SaaS product launch. Respond as JSON.

Hard constraints (ALL must be met):
1. Exactly 20 content pieces total across 4 weeks
2. Each week: 5 pieces (Mon-Fri, one per day)
3. Content types: blog (B), social (S), email (E), video (V), webinar (W)
4. Distribution: exactly 6 blogs, 6 social posts, 4 emails, 3 videos, 1 webinar
5. No two consecutive days can have the same content type
6. The webinar must be on a Wednesday or Thursday in week 3 or 4
7. Videos cannot be on Mondays (production team unavailable)
8. Emails must be on Tuesday or Thursday only
9. Week 1 must start with a blog (launch announcement)
10. The last piece (week 4, Friday) must be a social post (recap)
11. Each blog must have a social post within 2 days after it (promotion)
12. No more than 2 content pieces of the same type per week

Format: {"weeks": [{"week": 1, "schedule": {"mon": "B/S/E/V/W", "tue": "...", "wed": "...", "thu": "...", "fri": "..."}}], "type_counts": {"B": N, "S": N, "E": N, "V": N, "W": N}, "constraint_violations": []}

The constraint_violations array should be empty if all constraints are met.""",
        "scoring": {
            "type": "content_calendar",
            "checks": [
                "has_20_pieces",
                "5_per_week",
                "correct_type_counts",
                "no_consecutive_same_type",
                "webinar_wed_or_thu_week_3_or_4",
                "no_monday_videos",
                "emails_tue_or_thu_only",
                "week1_starts_blog",
                "week4_ends_social",
                "blog_social_within_2_days",
                "max_2_per_type_per_week",
                "valid_types_only",
                "empty_violations",
                "all_days_filled",
                "correct_json_structure"
            ]
        }
    },

    # ================================================================
    # G-50: ORCHESTRATOR — Complex Multi-Agent Workflow
    # Current Phase F: basic orchestration → all models 8/10
    # ================================================================
    {
        "id": 50, "role": "Orchestrator / Meta-Agent", "tier": 5,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Design an agent orchestration workflow for this complex task. Respond as JSON.

Task: A customer reports a production outage. Design the automated response workflow.

Available agents:
- log_analyzer: Analyzes log files, returns error patterns
- metric_checker: Queries Prometheus/Grafana, returns metrics
- dependency_mapper: Maps service dependencies
- rollback_agent: Can rollback to previous deployment
- notification_agent: Sends alerts via Slack/PagerDuty/email
- db_checker: Checks database health, connections, locks
- incident_reporter: Creates and updates incident tickets
- customer_communicator: Sends status updates to affected customers
- capacity_planner: Checks resource utilization
- config_auditor: Checks recent config changes

Output:
{
  "phases": [
    {
      "phase": 1,
      "name": "...",
      "agents": [{"agent": "...", "input": "...", "timeout_seconds": N}],
      "parallel": true/false,
      "gate": "description of what must be true to proceed"
    }
  ],
  "decision_points": [
    {"after_phase": N, "condition": "...", "if_true": "go to phase N", "if_false": "go to phase N"}
  ],
  "escalation": {"trigger": "...", "action": "..."},
  "total_phases": N,
  "max_time_minutes": N,
  "rollback_conditions": ["..."]
}

Requirements:
1. Must have at least 5 phases
2. Phase 1 must run diagnostic agents in parallel
3. Must have at least 2 decision points with branching logic
4. Notification must happen within phase 1 or 2
5. Customer communication must happen before any rollback
6. Escalation trigger must include time-based condition
7. Rollback conditions must be specific (not just "if needed")
8. Must include a verification phase after any remediation
9. Max time must be reasonable (5-30 minutes)
10. Each agent must have a timeout""",
        "scoring": {
            "type": "orchestration_constraints",
            "checks": [
                "has_5_phases",
                "phase1_parallel_diagnostics",
                "has_2_decision_points",
                "early_notification",
                "customer_before_rollback",
                "time_based_escalation",
                "specific_rollback_conditions",
                "verification_after_remediation",
                "reasonable_max_time",
                "all_agents_have_timeouts",
                "uses_log_analyzer",
                "uses_metric_checker",
                "uses_incident_reporter",
                "branching_logic_valid",
                "no_circular_phases"
            ]
        }
    },

    # ================================================================
    # G-23: WEB SCRAPING — Complex Nested HTML Extraction
    # Current Phase F: format check only → all models 10/10
    # ================================================================
    {
        "id": 23, "role": "Web Scraping / Data Extraction", "tier": 2,
        "phase": "G",
        "scoring_type": "exact",
        "prompt": """Extract structured data from this messy HTML table. The table has inconsistencies, merged cells, missing values, and encoding issues. Respond as JSON.

```html
<table class="data" id="quarterly-results">
  <thead>
    <tr><th>Company</th><th>Q1 Rev ($M)</th><th>Q2 Rev ($M)</th><th>Q3 Rev</th><th>Q4 Rev ($M)</th><th>YoY Growth</th><th>Employees</th></tr>
  </thead>
  <tbody>
    <tr><td>Acme Corp</td><td>$125.3</td><td>$131.7</td><td>142.1M</td><td>$155.0</td><td>+18%</td><td>1,250</td></tr>
    <tr><td>Beta Inc</td><td>89.5</td><td>$92.1</td><td>$87.3</td><td>$95.8</td><td>-3.2%</td><td>890</td></tr>
    <tr><td>Gamma LLC</td><td>$210.0</td><td>N/A</td><td>$225.5</td><td>$240.1</td><td>14.5%</td><td>2100</td></tr>
    <tr><td>Delta &amp; Sons</td><td>$45.2</td><td>$44.8</td><td>$46.1</td><td>$47.5</td><td>+5.1%</td><td>~450</td></tr>
    <tr><td colspan="7" style="text-align:center"><em>* Gamma Q2 data pending audit</em></td></tr>
    <tr><td>Epsilon (acquired)</td><td>$78.0</td><td>$0</td><td>—</td><td>—</td><td>N/A</td><td>0 (dissolved)</td></tr>
  </tbody>
</table>
```

Extract and calculate. Respond with this exact JSON:
{
  "companies": [{"name": "...", "q1": N, "q2": N_or_null, "q3": N_or_null, "q4": N_or_null, "yoy_growth_pct": N_or_null, "employees": N_or_null, "annual_revenue": N_or_null, "notes": "..."}],
  "total_q1": N,
  "highest_revenue_company": "...",
  "company_with_negative_growth": "...",
  "companies_with_complete_data": N,
  "average_employee_count": N
}

Rules:
- Normalize all revenue to plain numbers in millions (no $, no M suffix)
- N/A, —, missing = null
- "~450" = 450 (approximate is fine)
- "0 (dissolved)" = 0 employees
- annual_revenue = sum of available quarters (not null ones)
- Handle HTML entities (&amp; → &)""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "total_q1": 548.0,
                "highest_revenue_company": "Gamma LLC",
                "company_with_negative_growth": "Beta Inc",
                "companies_with_complete_data": 2,
                "average_employee_count": 938
            },
            "tolerance": 5.0
        }
    },
]
