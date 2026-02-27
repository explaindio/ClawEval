"""Tier 4: Expert-Level Roles (3 tests, IDs 47-49)"""

TIER4_TESTS = [
    {
        "id": 47, "role": "Math / Logic Reasoning", "tier": 4,
        "scoring_type": "exact",
        "prompt": """Solve these 5 problems. Give EXACT answers. Respond as JSON: {"p1": answer, "p2": answer, ...}

P1: A train leaves Station A at 9:00 AM traveling east at 85 mph. A second train leaves Station B (340 miles east of A) at 9:30 AM traveling west at 95 mph. At what time do they meet? (format: "H:MM AM/PM")

P2: In a room of 30 people, what is the probability that at least two share a birthday? (as percentage, round to 1 decimal)

P3: If you fold a piece of paper in half 42 times, how thick would it be in kilometers? (paper thickness = 0.1mm, round to nearest integer)

P4: A bat and ball cost $1.10 total. The bat costs $1.00 more than the ball. How much does the ball cost? (in dollars)

P5: Three people check into a hotel room that costs $30. They each pay $10. The manager realizes the room is $25 and gives $5 to the bellboy to return. The bellboy keeps $2 and returns $1 to each person. Each person paid $9 (total $27) plus $2 the bellboy kept = $29. Where is the missing $1? Answer with "no_missing_dollar" or the amount.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "p1": "10:53 AM",
                "p2": "70.6",
                "p3": 439805,
                "p4": "0.05",
                "p5": "no_missing_dollar"
            }
        }
    },
    {
        "id": 48, "role": "STEM Analysis", "tier": 4,
        "scoring_type": "exact",
        "prompt": """Solve these physics/engineering problems. Respond as JSON with numerical answers.

P1: A 5kg ball is dropped from 20m. What is its velocity just before hitting the ground? (g=9.8 m/s², ignore air resistance, answer in m/s, round to 2 decimal)

P2: A circuit has R1=100Ω and R2=200Ω in parallel, connected in series with R3=50Ω. Total voltage = 12V. What is the total current? (in amps, round to 4 decimal)

P3: How much energy (kWh) does it take to heat 50 liters of water from 20°C to 100°C? (specific heat = 4.186 J/g·°C, round to 2 decimal)

P4: A rocket burns fuel at 50 kg/s with exhaust velocity 3000 m/s. Initial mass 10,000 kg, fuel mass 6,000 kg. What is the burn time? (seconds)

P5: Sound travels at 343 m/s in air. If you see lightning and hear thunder 4.5 seconds later, how far away was the strike? (in km, round to 2 decimal)""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "p1": 19.80,
                "p2": 0.0873,
                "p3": 4.65,
                "p4": 120,
                "p5": 1.54
            },
            "tolerance": 0.1
        }
    },
    {
        "id": 49, "role": "Algorithm Exploration", "tier": 4,
        "scoring_type": "code",
        "prompt": """Implement a Python function `lru_cache(capacity)` that returns a cache object with `get(key)` and `put(key, value)` methods. Must be O(1) for both operations.

- get(key): returns value if exists, -1 if not
- put(key, value): inserts/updates. If at capacity, evict least recently used.
- Both get and put count as "use" for LRU purposes.

Give ONLY the code. Example:
```
cache = lru_cache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)       # returns 1
cache.put(3, 3)    # evicts key 2
cache.get(2)       # returns -1
cache.put(4, 4)    # evicts key 1
cache.get(1)       # returns -1
cache.get(3)       # returns 3
cache.get(4)       # returns 4
```""",
        "scoring": {
            "type": "code_exec",
            "function_name": "lru_cache",
            "test_cases": [
                {"ops": [("put",1,1),("put",2,2),("get",1,None)], "expected": [None,None,1], "capacity": 2},
                {"ops": [("put",1,1),("put",2,2),("put",3,3),("get",1,None)], "expected": [None,None,None,-1], "capacity": 2},
                {"ops": [("put",1,1),("put",2,2),("get",1,None),("put",3,3),("get",2,None)], "expected": [None,None,1,None,-1], "capacity": 2},
                {"ops": [("put",1,1),("get",1,None),("put",1,10),("get",1,None)], "expected": [None,1,None,10], "capacity": 1},
                {"ops": [("put",1,1),("put",2,2),("put",3,3)], "expected": [None,None,None], "capacity": 3},
                {"ops": [("get",1,None)], "expected": [-1], "capacity": 1},
                {"ops": [("put",1,1),("put",2,2),("put",1,10),("put",3,3),("get",2,None)], "expected": [None,None,None,None,-1], "capacity": 2},
                {"ops": [("put",1,1),("put",2,2),("get",1,None),("get",2,None),("put",3,3),("get",1,None)], "expected": [None,None,1,2,None,-1], "capacity": 2},
                {"ops": [("put",1,1)], "expected": [None], "capacity": 5},
                {"ops": [("put",1,1),("put",1,2),("put",1,3),("get",1,None)], "expected": [None,None,None,3], "capacity": 1}
            ]
        }
    },
]
