"""Phase H Dense Tests — Batch 4: Tests 23, 27, 31, 37, 38, 42, 43, 45, 46, 47"""

PHASE_H_BATCH4 = [
    # H-23: WEBSITE SCRAPING — 15 data points
    {
        "id": 23, "role": "Website Scraping / Understanding", "tier": 2,
        "scoring_type": "json_values",
        "prompt": """Extract 15 structured data points from this raw HTML snippet. Respond as JSON: {"d1": value, ...}

```html
<div class="product-page" data-sku="WDG-2847">
  <h1 class="product-title">ProMax Wireless Headphones X500</h1>
  <div class="pricing">
    <span class="original-price">$199.99</span>
    <span class="sale-price">$149.99</span>
    <span class="discount-badge">25% OFF</span>
  </div>
  <div class="ratings">
    <span class="stars" data-rating="4.3">★★★★☆</span>
    <span class="review-count">(2,847 reviews)</span>
  </div>
  <ul class="specs">
    <li>Battery Life: <strong>35 hours</strong></li>
    <li>Weight: <strong>248g</strong></li>
    <li>Bluetooth: <strong>5.3</strong></li>
    <li>Driver Size: <strong>40mm</strong></li>
    <li>Noise Cancelling: <strong>Active (ANC)</strong></li>
  </ul>
  <div class="availability">
    <span class="stock-status in-stock">In Stock</span>
    <span class="shipping">Free shipping on orders over $50</span>
    <span class="delivery-est">Arrives: Mar 15-18</span>
  </div>
  <div class="brand-info">
    <a href="/brands/audiotech">AudioTech International</a>
    <span class="model-year">2024 Model</span>
  </div>
</div>
```

Questions:
d1: Product name
d2: SKU
d3: Original price (number only)
d4: Sale price (number only)
d5: Discount percentage (number only)
d6: Star rating (number)
d7: Number of reviews (number only)
d8: Battery life in hours (number)
d9: Weight in grams (number)
d10: Bluetooth version
d11: Driver size in mm (number)
d12: Has active noise cancelling? (yes/no)
d13: In stock? (yes/no)
d14: Brand name
d15: Model year""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "d1": "ProMax Wireless Headphones X500",
                "d2": "WDG-2847", "d3": "199.99", "d4": "149.99",
                "d5": "25", "d6": "4.3", "d7": "2847",
                "d8": "35", "d9": "248", "d10": "5.3",
                "d11": "40", "d12": "yes", "d13": "yes",
                "d14": "AudioTech International", "d15": "2024"
            }
        }
    },

    # H-27: SPRINT / PROJECT SUMMARIZER — 15 metrics
    {
        "id": 27, "role": "Sprint / Project Summarizer", "tier": 2,
        "scoring_type": "json_numeric",
        "prompt": """Calculate 15 sprint metrics from this data. Respond as JSON: {"s1": value, ...}. Round to 1 decimal place.

Sprint 14 (2 weeks):
Stories: 24 planned, 19 completed, 3 carried over, 2 descoped
Story points: 89 planned, 72 completed
Bugs: 8 opened, 11 closed (3 from previous sprints)
Team: 6 developers, 1 QA, 1 PM = 8 people
Capacity: 6 devs × 10 days × 6 hrs = 360 dev-hours available
Time tracking: 312 dev-hours logged on sprint work, 48 on unplanned work
Deployments: 4 releases, 1 rollback
PRs: 47 opened, 42 merged, 3 rejected, 2 still open
Code reviews: avg 2.3 hours from PR open to first review
Incidents: 2 P2 incidents, total downtime 45 minutes

Questions:
s1: Completion rate (completed/planned stories * 100)
s2: Points completion rate (completed/planned * 100)
s3: Velocity (completed story points)
s4: Average points per completed story
s5: Bug fix rate (closed/opened * 100)
s6: Capacity utilization (logged sprint hours / available * 100)
s7: Unplanned work percentage (unplanned / total logged * 100)
s8: PR merge rate (merged/opened * 100)
s9: Average points per developer per sprint
s10: Deployment frequency (releases per week)
s11: Rollback rate (rollbacks/releases * 100)
s12: Net bug count change (opened - closed)
s13: Team size
s14: Dev hours per completed story point
s15: Downtime in minutes""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "s1": 79.2, "s2": 80.9, "s3": 72,
                "s4": 3.8, "s5": 137.5, "s6": 86.7,
                "s7": 13.3, "s8": 89.4, "s9": 12.0,
                "s10": 2.0, "s11": 25.0, "s12": -3,
                "s13": 8, "s14": 4.3, "s15": 45
            },
            "tolerance": 0.05
        }
    },

    # H-37: CODE REVIEW — 15 bugs
    {
        "id": 37, "role": "Code Review Agent", "tier": 3,
        "scoring_type": "h_content_check",
        "prompt": """Find ALL 15 bugs in this Python code. For each, identify the line and describe the bug. Respond as JSON: {"bugs": [{"line": N, "bug": "description", "severity": "critical/major/minor"}, ...], "count": 15}

```python
def process_orders(orders, tax_rate=0.08):
    results = []
    total_revenue = 0

    for order in orders:
        # Calculate subtotal
        subtotal = 0
        for item in order['items']:
            subtotal += item['price'] * item['qty']

        # Apply discount
        if order.get('discount_code') == 'SAVE20':
            subtotal = subtotal * 0.20  # Line 12: Bug
        elif order.get('discount_code') == 'SAVE10':
            subtotal -= subtotal * 10  # Line 14: Bug

        # Calculate tax
        tax = subtotal * tax_rate
        total = subtotal + tax

        # Update inventory
        for item in order['items']:
            item['stock'] = item['stock'] - item['qty']
            if item['stock'] < 0:
                pass  # Line 22: Bug - should raise error or skip

        # Build result
        result = {
            'order_id': order['id'],
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'status': 'completed'
        }
        results.append(result)
        total_revenue =+ total  # Line 31: Bug

    # Calculate analytics
    avg_order = total_revenue / len(orders)  # Line 34: Bug
    max_order = max(r['total'] for r in results)  # Line 35: Bug

    return {
        'orders': results,
        'total_revenue': total_revenue,
        'average_order': avg_order,
        'max_order': max_order,
        'order_count': len(results),
        'tax_collected': sum(r['tax'] for r in results)
    }

def validate_email(email):
    if '@' in email:
        return True  # Line 46: Bug - insufficient validation
    return False

def calculate_shipping(weight, distance, express=False):
    base_rate = 5.99
    per_kg = 2.50
    per_km = 0.01

    cost = base_rate + weight * per_kg + distance + per_km  # Line 53: Bug
    if express:
        cost = cost * 1.5
    if weight > 30:
        cost += 15.00
    elif weight > 50:  # Line 57: Bug - unreachable
        cost += 25.00

    return round(cost)  # Line 60: Bug - loses decimal precision

def merge_user_profiles(profile_a, profile_b):
    merged = profile_a  # Line 63: Bug
    for key, value in profile_b.items():
        if key not in merged:
            merged[key] = value
    merged['updated_at'] = '2024-01-01'  # Line 67: Bug - hardcoded date
    return merged

def parse_csv_line(line):
    return line.split(',')  # Line 71: Bug

def find_duplicates(items):
    seen = []
    duplicates = []
    for item in items:
        if item in seen:
            duplicates.append(item)
        seen.append(item)  # Line 78: Bug
    return duplicates
```""",
        "scoring": {
            "checks": {
                "b1_save20": ["0.20", "80%", "20%", "discount"],
                "b2_save10": ["* 10", "multiply", "0.10", "1000%"],
                "b3_negative_stock": ["negative stock", "negative", "silently"],
                "b4_equals_plus": ["=+", "+=", "assignment"],
                "b5_division_zero": ["division by zero", "empty", "len(orders)"],
                "b6_empty_results": ["empty", "max", "valueerror"],
                "b7_email_validation": ["email", "validation", "insufficient"],
                "b8_distance_perkm": ["distance", "per_km", "addition"],
                "b9_unreachable": ["unreachable", "elif", "50"],
                "b10_round_precision": ["round", "precision", "decimal"],
                "b11_shallow_copy": ["shallow copy", "mutate", "reference", "profile_a"],
                "b12_hardcoded_date": ["hardcoded", "date", "timestamp", "2024"],
                "b13_csv_quoted": ["csv", "comma", "quoted", "split"],
                "b14_seen_append": ["seen", "append", "duplicate"],
                "b15_stock_side_effect": ["side effect", "in-place", "mutate", "stock"]
            }
        }
    },

    # H-38: QA / TEST WRITING — 15 test cases
    {
        "id": 38, "role": "QA / Test Writing Agent", "tier": 3,
        "scoring_type": "code_exec",
        "prompt": """Write a Python function `is_valid_password(password)` that checks all these rules, then write 15 test cases.

Rules:
- At least 8 characters long
- At most 64 characters
- Contains at least 1 uppercase letter
- Contains at least 1 lowercase letter
- Contains at least 1 digit
- Contains at least 1 special character from: !@#$%^&*()-_+=
- No spaces allowed
- Cannot start with a digit
- Cannot contain more than 3 consecutive identical characters
- Cannot contain the word "password" (case-insensitive)

Provide ONLY the function definition followed by a function `run_tests()` that returns a list of tuples [(input, expected, actual), ...] for all 15 tests. No imports needed.""",
        "scoring": {
            "type": "code_exec",
            "test_cases": [
                {"call": "is_valid_password('Str0ng!Pass')", "expected": "True"},
                {"call": "is_valid_password('Ab1!')", "expected": "False"},
                {"call": "is_valid_password('alllowercase1!')", "expected": "False"},
                {"call": "is_valid_password('ALLUPPERCASE1!')", "expected": "False"},
                {"call": "is_valid_password('NoDigits!Here')", "expected": "False"},
                {"call": "is_valid_password('NoSpecial1Here')", "expected": "False"},
                {"call": "is_valid_password('Has Space1!')", "expected": "False"},
                {"call": "is_valid_password('1StartsDigit!aA')", "expected": "False"},
                {"call": "is_valid_password('Aaaa1234!')", "expected": "False"},
                {"call": "is_valid_password('MyPassword1!')", "expected": "False"},
                {"call": "is_valid_password('X1!aaaaa')", "expected": "True"},
                {"call": "is_valid_password('Aa1!Bb2@Cc3#')", "expected": "True"},
                {"call": "is_valid_password('')", "expected": "False"},
                {"call": "is_valid_password('A' * 65 + '1!')", "expected": "False"},
                {"call": "is_valid_password('Valid-Pass_1')", "expected": "True"},
            ]
        }
    },

    # H-42: MARKET RESEARCH — 15 metrics
    {
        "id": 42, "role": "Market Research Agent", "tier": 3,
        "scoring_type": "json_numeric",
        "prompt": """Analyze this market data and calculate 15 metrics. Respond as JSON: {"m1": value, ...}. Round to 1 decimal place.

SaaS Market Data (2024):
| Company | Revenue ($M) | Growth % | Customers | Employees | Market Share % |
|---------|-------------|----------|-----------|-----------|---------------|
| AlphaCo | 450 | 28 | 12000 | 1200 | 18.0 |
| BetaCo | 380 | 15 | 9500 | 950 | 15.2 |
| GammaCo | 310 | 42 | 7200 | 680 | 12.4 |
| DeltaCo | 280 | 8 | 11000 | 720 | 11.2 |
| EpsilCo | 220 | 35 | 5800 | 520 | 8.8 |
| Others | 860 | 12 | 45000 | 4200 | 34.4 |

Questions:
m1: Total addressable market size ($M)
m2: Top 5 companies combined market share (%)
m3: Revenue-weighted average growth rate for top 5 (%)
m4: AlphaCo revenue per customer ($)
m5: Average revenue per employee for top 5 ($K)
m6: GammaCo projected revenue next year ($M) based on growth rate
m7: Market HHI (Herfindahl–Hirschman Index, sum of squared market shares)
m8: BetaCo revenue per employee ($K)
m9: Highest growth company's market share (%)
m10: Customers per employee ratio for DeltaCo
m11: If GammaCo maintains growth for 2 years, projected revenue ($M)
m12: Top 3 market share combined (%)
m13: Average customers per company (top 5 only)
m14: Revenue needed for 20% market share ($M)
m15: EpsilCo revenue per customer ($)""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "m1": 2500, "m2": 65.6, "m3": 24.4,
                "m4": 37500, "m5": 403.0, "m6": 440.2,
                "m7": 1904.0, "m8": 400.0, "m9": 12.4,
                "m10": 15.3, "m11": 625.1, "m12": 45.6,
                "m13": 9100, "m14": 500, "m15": 37931.0
            },
            "tolerance": 0.05
        }
    },

    # H-47: MATH / LOGIC — 15 problems
    {
        "id": 47, "role": "Math / Logic Reasoning", "tier": 4,
        "scoring_type": "json_numeric",
        "prompt": """Solve these 15 math and logic problems. Respond as JSON: {"p1": answer, ...}. Give exact answers (integers or decimals to 2 places).

p1: A train leaves station A at 80 km/h. Another leaves station B (300 km away) at 120 km/h toward A at the same time. How many minutes until they meet?
p2: If 5 machines make 5 widgets in 5 minutes, how many minutes do 100 machines take to make 100 widgets?
p3: A bat and ball cost $1.10 total. The bat costs $1.00 more than the ball. How much does the ball cost in cents?
p4: What is the sum of the first 100 positive integers?
p5: In a room of 23 people, what's the probability (%) that at least two share a birthday? (Round to 1 decimal)
p6: A lily pad doubles in size every day. It takes 48 days to cover a lake. On what day does it cover half the lake?
p7: Three cards: one red on both sides, one blue on both sides, one red/blue. You pick a card and see red. What's the probability the other side is also red? (Express as a fraction: N/M)
p8: If you have 12 coins, one is counterfeit (lighter), and a balance scale, what's the minimum weighings needed to find it?
p9: What is 2^10 × 5^10?
p10: A snail climbs 3 feet each day and slides back 2 feet each night. How many days to reach the top of a 30-foot wall?
p11: In base 8, what is 77 + 1?
p12: How many trailing zeros does 100! have?
p13: What is the next number: 1, 1, 2, 3, 5, 8, 13, ?
p14: You flip a fair coin 10 times. What's the probability of getting exactly 5 heads? (Express as percentage to 2 decimal places)
p15: A clock shows 3:15. What is the angle between the hour and minute hands in degrees?""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "p1": "90", "p2": "5", "p3": "5",
                "p4": "5050", "p5": "50.7", "p6": "47",
                "p7": "2/3", "p8": "3", "p9": "10000000000",
                "p10": "28", "p11": "100", "p12": "24",
                "p13": "21", "p14": "24.61", "p15": "7.5"
            }
        }
    },
]
