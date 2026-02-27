"""Tier 3: Advanced/Specialized Roles (11 tests, IDs 36-46)"""

TIER3_TESTS = [
    {
        "id": 36, "role": "Code Generation Agent", "tier": 3,
        "scoring_type": "code",
        "prompt": """Write a Python function `merge_intervals(intervals)` that takes a list of [start, end] intervals and returns the merged result, sorted by start time. Overlapping or adjacent intervals should be merged.

Examples:
- merge_intervals([[1,3],[2,6],[8,10],[15,18]]) → [[1,6],[8,10],[15,18]]
- merge_intervals([[1,4],[4,5]]) → [[1,5]]

Give ONLY the function code, no explanation.""",
        "scoring": {
            "type": "code_exec",
            "function_name": "merge_intervals",
            "test_cases": [
                {"input": [[1,3],[2,6],[8,10],[15,18]], "expected": [[1,6],[8,10],[15,18]]},
                {"input": [[1,4],[4,5]], "expected": [[1,5]]},
                {"input": [[1,4],[0,4]], "expected": [[0,4]]},
                {"input": [[1,4],[2,3]], "expected": [[1,4]]},
                {"input": [], "expected": []},
                {"input": [[1,1]], "expected": [[1,1]]},
                {"input": [[1,10],[2,3],[4,5],[6,7]], "expected": [[1,10]]},
                {"input": [[1,2],[3,4],[5,6]], "expected": [[1,2],[3,4],[5,6]]},
                {"input": [[5,8],[1,3],[2,6],[10,12]], "expected": [[1,8],[10,12]]},
                {"input": [[1,100]], "expected": [[1,100]]}
            ]
        }
    },
    {
        "id": 37, "role": "Code Review Agent", "tier": 3,
        "scoring_type": "exact",
        "prompt": """Find ALL bugs in this Python code. Respond as JSON: {"bugs": [{"line": N, "issue": "...", "fix": "..."}], "count": N}

```python
def process_orders(orders):
    total = 0
    processed = []
    
    for order in orders:
        if order['status'] == 'pending':
            discount = order.get('discount', 0)
            price = order['price'] * order['quantity']
            price = price - (price * discount / 100)  # line 8
            
            if price < 0:  # line 10
                price = 0
            
            order['final_price'] = round(price, 2)
            order['status'] = 'processed'
            processed.append(order)
            total += price
    
    avg = total / len(processed)  # line 18
    
    return {
        'orders': processed,
        'total': total,
        'average': avg,
        'count': len(orders)  # line 23
    }
```

Test with: process_orders([]) and process_orders([{'status':'shipped','price':10,'quantity':1}])

Bugs to find:
- Line 18: ZeroDivisionError when no orders are pending
- Line 23: Returns len(orders) not len(processed)
- Line 8: discount could be > 100, no validation
- Mutates input orders dict (side effect)
- No type checking on price/quantity (could be None)""",
        "scoring": {
            "type": "bug_detection",
            "bugs": [
                {"keyword": "ZeroDivisionError", "line": 18},
                {"keyword": "len(orders)", "line": 23},
                {"keyword": "discount", "detail": "over 100"},
                {"keyword": "mutate", "detail": "input"},
                {"keyword": "None", "detail": "type"}
            ]
        }
    },
    {
        "id": 38, "role": "QA / Test Writing Agent", "tier": 3,
        "scoring_type": "code",
        "prompt": """Write Python unit tests for this function using pytest. Cover ALL edge cases.

```python
def calculate_tax(income, filing_status):
    \"\"\"Calculate US federal income tax (simplified 2024 brackets).
    filing_status: 'single' or 'married'
    Returns: (tax_amount, effective_rate)
    \"\"\"
    if not isinstance(income, (int, float)) or income < 0:
        raise ValueError("Income must be non-negative number")
    if filing_status not in ('single', 'married'):
        raise ValueError("Invalid filing status")
    
    brackets_single = [(11600, 0.10), (47150, 0.12), (100525, 0.22), (191950, 0.24), (243725, 0.32), (609350, 0.35), (float('inf'), 0.37)]
    brackets_married = [(23200, 0.10), (94300, 0.12), (201050, 0.22), (383900, 0.24), (487450, 0.32), (731200, 0.35), (float('inf'), 0.37)]
    
    brackets = brackets_single if filing_status == 'single' else brackets_married
    tax = 0
    prev = 0
    for limit, rate in brackets:
        if income <= prev:
            break
        taxable = min(income, limit) - prev
        tax += taxable * rate
        prev = limit
    
    effective_rate = round(tax / income * 100, 2) if income > 0 else 0
    return (round(tax, 2), effective_rate)
```

Write at least 8 test functions covering: zero income, typical income, high income, single vs married, invalid inputs, bracket boundaries. Give ONLY the test code.""",
        "scoring": {
            "type": "code_exec_tests",
            "function_code_above": True,
            "checks": [
                "tests_zero_income",
                "tests_negative_income",
                "tests_invalid_status",
                "tests_single_basic",
                "tests_married_basic",
                "tests_high_income",
                "tests_bracket_boundary",
                "tests_effective_rate",
                "has_8_tests",
                "all_tests_pass"
            ]
        }
    },
    {
        "id": 39, "role": "Task Planning / Decomposition", "tier": 3,
        "scoring_type": "constraint",
        "prompt": """Decompose this project into tasks with dependencies. Respond as JSON.

Project: Build a REST API for a todo app with user authentication.

Requirements:
1. User registration and login (JWT)
2. CRUD operations for todos
3. Todo categories/tags
4. Due date reminders
5. PostgreSQL database
6. Docker deployment
7. API documentation (OpenAPI)
8. Rate limiting
9. Unit tests (80%+ coverage)
10. CI/CD pipeline

Output: {"tasks": [{"id": "T1", "name": "...", "depends_on": ["T0"], "estimated_hours": N, "assignable_to": "backend/devops/fullstack"}], "critical_path": ["T1","T2",...], "total_hours": N, "parallel_tracks": N}

Rules:
- Database setup must come before any API work
- Auth must come before protected endpoints
- Tests depend on the features they test
- Docker depends on working application
- CI/CD depends on tests and Docker
- Docs can be done in parallel with tests""",
        "scoring": {
            "type": "task_decomposition",
            "checks": [
                "has_db_task_first", "auth_before_crud",
                "tests_after_features", "docker_after_app",
                "cicd_after_tests_docker", "docs_parallel_tests",
                "has_critical_path", "dependencies_valid",
                "reasonable_hours", "has_parallel_tracks"
            ]
        }
    },
    {
        "id": 40, "role": "Fact-Checking Agent", "tier": 3,
        "scoring_type": "exact",
        "prompt": """Label each claim TRUE or FALSE. Respond as JSON: {"1": "TRUE/FALSE", ...}

1. Python was created by Guido van Rossum and first released in 1991.
2. TCP/IP uses a 4-layer model: Application, Transport, Internet, Network Access.
3. The first iPhone was released in 2008.
4. Git was created by Linus Torvalds for Linux kernel development.
5. HTTP status code 404 means "Internal Server Error".
6. JavaScript was originally called LiveScript before Netscape renamed it.
7. The first computer bug was a literal moth found in the Mark II computer.
8. SQL stands for "Simple Query Language".
9. The Internet was invented by Tim Berners-Lee in 1989.
10. Moore's Law states that transistor count doubles approximately every 2 years.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "TRUE", "2": "TRUE", "3": "FALSE", "4": "TRUE",
                "5": "FALSE", "6": "TRUE", "7": "TRUE", "8": "FALSE",
                "9": "FALSE", "10": "TRUE"
            }
        }
    },
    {
        "id": 41, "role": "Critic / Review Agent", "tier": 3,
        "scoring_type": "manual",
        "prompt": """Write a critical review of this code architecture proposal. Identify strengths, weaknesses, and suggest improvements.

Proposal: "We'll build our e-commerce platform as a monolithic Django application. The database will be a single MySQL instance. All static files served from the same server. User sessions stored in local memory. Payments processed synchronously in the main request thread. No caching layer. Background jobs run as cron scripts. Deployment via FTP to a single production server. No staging environment. Logs written to local files."

Evaluate on: scalability, reliability, security, maintainability, performance, deployment practices, data management, monitoring, cost efficiency, and industry best practices.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "identifies_scaling_issues", "identifies_spof",
                "identifies_security_gaps", "identifies_session_problem",
                "identifies_payment_risk", "identifies_caching_need",
                "identifies_deployment_issues", "identifies_monitoring_gap",
                "suggests_improvements", "balanced_tone"
            ]
        }
    },
    {
        "id": 42, "role": "Market Research Agent", "tier": 3,
        "scoring_type": "exact",
        "prompt": """Calculate market metrics from this data. Respond as JSON.

Company data in the CRM/Project Management market:
- Asana: Revenue $547M, Growth 18%, Customers 139K, Employees 1,800
- Monday.com: Revenue $729M, Growth 24%, Customers 186K, Employees 1,900
- ClickUp: Revenue $180M, Growth 45%, Customers 800K, Employees 1,000
- Notion: Revenue $340M, Growth 35%, Customers 30M (including free), Employees 500
- Smartsheet: Revenue $830M, Growth 15%, Customers 113K, Employees 3,200

Total addressable market: $15B

{"total_revenue": N, "avg_growth": N, "market_leader_by_revenue": "...", "fastest_growing": "...", "highest_revenue_per_employee": "...", "combined_market_share": N, "avg_revenue_per_customer": N, "largest_customer_base": "...", "smallest_company": "...", "revenue_range": N}""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "total_revenue": 2626,
                "avg_growth": 27.4,
                "market_leader_by_revenue": "Smartsheet",
                "fastest_growing": "ClickUp",
                "highest_revenue_per_employee": "Notion",
                "combined_market_share": 17.51,
                "avg_revenue_per_customer": "varies",
                "largest_customer_base": "Notion",
                "smallest_company": "Notion",
                "revenue_range": 650
            },
            "tolerance": 5.0
        }
    },
    {
        "id": 43, "role": "Synthesizer / Aggregator", "tier": 3,
        "scoring_type": "exact",
        "prompt": """These 5 sources discuss remote work productivity. Identify where they AGREE and DISAGREE. Respond as JSON: {"agreements": [...], "disagreements": [...], "agreement_count": N, "disagreement_count": N}

Source A: "Remote workers are 13% more productive. Communication suffers. Best for focused work."
Source B: "Productivity gains are a myth — they only measure output, not innovation. Communication tools solve the gap. Best for all work types."
Source C: "Remote workers are 5-20% more productive for individual tasks. Team collaboration is harder. Best for experienced workers."
Source D: "No significant productivity difference. Communication is the same with modern tools. Works equally for all experience levels."
Source E: "Remote workers are more productive. Communication quality drops but quantity increases. Best for senior employees."

Find exactly 3 agreements and 4 disagreements.""",
        "scoring": {
            "type": "synthesis",
            "expected_agreements": 3,
            "expected_disagreements": 4,
            "key_agreements": ["productivity", "remote", "work"],
            "key_disagreements": ["communication", "experience", "innovation", "all types"]
        }
    },
    {
        "id": 44, "role": "Curriculum / Course Designer", "tier": 3,
        "scoring_type": "constraint",
        "prompt": """Design a 6-week Python course. Respond as JSON.

Constraints:
1. 6 weeks × 3 sessions/week = 18 sessions total
2. Each session: 90 minutes (45min lecture + 45min hands-on)
3. Prerequisites must be taught before dependent topics
4. Week 1-2: Fundamentals, Week 3-4: Intermediate, Week 5-6: Advanced
5. Must cover: variables, functions, classes, file I/O, APIs, testing, data structures, error handling, decorators, generators
6. Each week has 1 quiz + 1 assignment
7. Final project in week 6 that integrates at least 5 concepts
8. Difficulty must increase monotonically
9. Each session has clear learning objectives (2-3 per session)
10. Total lecture hours ≤ 13.5, total hands-on ≥ 13.5

Format: {"weeks": [{"week": N, "theme": "...", "sessions": [{"day": N, "topic": "...", "objectives": [...], "lecture_min": N, "handson_min": N}], "quiz": "...", "assignment": "..."}], "final_project": "..."}""",
        "scoring": {
            "type": "curriculum_constraints",
            "checks": [
                "has_18_sessions", "session_duration_90",
                "prerequisites_ordered", "correct_week_themes",
                "covers_all_topics", "has_quizzes_assignments",
                "has_final_project", "monotonic_difficulty",
                "has_objectives", "time_balance"
            ]
        }
    },
    {
        "id": 45, "role": "Prototype Generator", "tier": 3,
        "scoring_type": "code",
        "prompt": """Generate a Python Flask REST API skeleton for a bookstore. Include these endpoints:

1. GET /books — list all books (with pagination: ?page=1&per_page=10)
2. GET /books/<id> — get single book
3. POST /books — create book (title, author, isbn, price required)
4. PUT /books/<id> — update book
5. DELETE /books/<id> — delete book

Requirements:
- Input validation on POST/PUT
- Proper HTTP status codes (200, 201, 404, 400, 422)
- JSON error responses with "error" key
- Use an in-memory list as "database"
- Include a Book dataclass or dict structure

Give ONLY the code, no explanation.""",
        "scoring": {
            "type": "code_structure",
            "checks": [
                "has_get_list", "has_get_single", "has_post",
                "has_put", "has_delete", "has_validation",
                "has_404_handling", "has_pagination",
                "has_error_responses", "runs_without_error"
            ]
        }
    },
    {
        "id": 46, "role": "DevOps Agent", "tier": 3,
        "scoring_type": "exact",
        "prompt": """Find ALL issues in this Docker Compose file. Respond as JSON: {"issues": [{"line": "...", "problem": "...", "fix": "..."}], "count": N}

```yaml
version: '2'
services:
  web:
    image: node:latest
    ports:
      - "80:3000"
    environment:
      DB_PASSWORD: supersecret123
      NODE_ENV: development
    volumes:
      - .:/app
    restart: no
    
  db:
    image: mysql:5.6
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: supersecret123
    volumes:
      - /tmp/mysql-data:/var/lib/mysql
      
  redis:
    image: redis
    ports:
      - "6379:6379"
```

Issues to find:
1. version '2' is outdated
2. 'latest' tag is non-deterministic
3. DB password in plaintext (should use secrets)
4. NODE_ENV should be 'production'  
5. Source volume mount (.:/app) in production
6. restart: no — should be 'unless-stopped' or 'always'
7. MySQL 5.6 is EOL
8. DB port 3306 exposed publicly
9. /tmp for persistent data (will be lost)
10. Redis port exposed publicly + no auth""",
        "scoring": {
            "type": "issue_detection",
            "issues": [
                "version", "latest", "password plaintext",
                "development", "volume mount", "restart",
                "mysql 5.6", "3306 exposed", "/tmp",
                "redis exposed"
            ]
        }
    },
]
