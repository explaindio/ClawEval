"""Tier 1: Simple/Utility Roles (8 tests, IDs 1-8)"""

TIER1_TESTS = [
    {
        "id": 1, "role": "Router / Triage Agent", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Classify each message into EXACTLY ONE category. Respond with ONLY a JSON object: {"1": "category", "2": "category", ...}

Categories: code_help, scheduling, research, support, billing, creative, data_analysis, devops

Messages:
1. "Can you refactor this function to use async/await instead of callbacks?"
2. "What time works for a standup with the Tokyo and London teams?"
3. "Find me the top 5 papers on transformer architectures from 2024"
4. "My account was charged twice for the same subscription"
5. "The Docker container keeps crashing with OOM errors on pod restart"
6. "Write a limerick about our company's new product launch"
7. "Move my Thursday 3pm to Friday and invite the design team"
8. "What's the average response time trend over the last 30 days from our API logs?"
9. "I can't log in — it says my password is expired but I just changed it"
10. "Generate a SQL query to find customers who churned in Q3 but returned in Q4" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "code_help", "2": "scheduling", "3": "research",
                "4": "billing", "5": "devops", "6": "creative",
                "7": "scheduling", "8": "data_analysis", "9": "support",
                "10": "data_analysis"
            }
        }
    },
    {
        "id": 2, "role": "Input Validator / Sanitizer", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Validate this API request payload. Find ALL errors. Respond with ONLY a JSON object: {"errors": ["error1", "error2", ...], "error_count": N}

Rules:
- email must be valid format (user@domain.tld)
- age must be integer 0-150
- phone must be 10 digits (US)
- zip must be 5 digits
- state must be valid 2-letter US state abbreviation
- password must be >= 8 chars with at least 1 uppercase, 1 number
- dates must be valid ISO format (YYYY-MM-DD) and in the future
- amount must be positive number <= 10000
- currency must be USD, EUR, or GBP
- items array must have 1-10 items

Payload:
```json
{
  "email": "john@.com",
  "age": 200,
  "phone": "555-123-45",
  "zip": "9021",
  "state": "XX",
  "password": "short",
  "date": "2020-13-45",
  "amount": -50,
  "currency": "BTC",
  "items": []
}
```""",
        "scoring": {
            "type": "error_count",
            "expected_count": 10,
            "expected_errors": [
                "email", "age", "phone", "zip", "state",
                "password", "date", "amount", "currency", "items"
            ]
        }
    },
    {
        "id": 3, "role": "Heartbeat / Health Monitor", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Analyze this server health timeline. Answer ALL 5 questions with exact numbers. Respond as JSON: {"q1": answer, "q2": answer, ...}

Timeline (readings every 5 minutes):
00:00 - CPU: 45%, Mem: 62%, Disk: 78%, Conns: 120, Errors: 2
00:05 - CPU: 47%, Mem: 63%, Disk: 78%, Conns: 125, Errors: 1
00:10 - CPU: 92%, Mem: 64%, Disk: 79%, Conns: 890, Errors: 45
00:15 - CPU: 95%, Mem: 65%, Disk: 79%, Conns: 920, Errors: 52
00:20 - CPU: 48%, Mem: 66%, Disk: 80%, Conns: 130, Errors: 3
00:25 - CPU: 46%, Mem: 67%, Disk: 80%, Conns: 128, Errors: 2
00:30 - CPU: 44%, Mem: 68%, Disk: 81%, Conns: 122, Errors: 1
00:35 - CPU: 45%, Mem: 69%, Disk: 81%, Conns: 125, Errors: 2
00:40 - CPU: 93%, Mem: 70%, Disk: 82%, Conns: 905, Errors: 48
00:45 - CPU: 46%, Mem: 71%, Disk: 82%, Conns: 124, Errors: 1

Questions (exact answers):
q1: How many CPU spike events occurred (CPU > 90%)?
q2: What is the average error count during CPU spikes vs normal?
q3: Memory increases by how many percentage points per 5-min interval (trend)?
q4: At this memory growth rate, in how many minutes from 00:45 will memory reach 95%?
q5: What is disk growth rate in percentage points per hour?""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "q1": 3,
                "q2_spike": 48.33,
                "q2_normal": 1.71,
                "q3": 1.0,
                "q4": 120,
                "q5": 4.0
            },
            "tolerance": 1.0
        }
    },
    {
        "id": 4, "role": "Notification / Alert Agent", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Prioritize these 10 alerts. Respond with ONLY a JSON object mapping alert number to priority: {"1": "P1/P2/P3/P4", "2": "...", ...}

Priority rules:
- P1: Data loss risk, security breach, or complete service outage
- P2: Degraded performance, partial outage, or approaching capacity limits
- P3: Warnings, non-critical errors, scheduled maintenance
- P4: Informational, successful deployments, routine metrics

Alerts:
1. "Database replication lag exceeded 30 seconds — risk of data inconsistency"
2. "SSL certificate expires in 3 days for api.example.com"
3. "Deployment v2.5.1 completed successfully on production"
4. "Unauthorized SSH login attempt from IP 203.0.113.42 — 50 failed attempts in 1 minute"
5. "Disk usage on /data reached 94% — estimated 6 hours until full"
6. "Weekly backup completed — all 12 databases backed up successfully"
7. "API response time p99 increased from 200ms to 1.2s in last 15 minutes"
8. "Memory usage on worker-3 at 87% — GC running frequently"
9. "Primary database server unreachable — all write operations failing"
10. "New user signup rate up 15% compared to last week" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "P1", "2": "P2", "3": "P4", "4": "P1", "5": "P2",
                "6": "P4", "7": "P2", "8": "P3", "9": "P1", "10": "P4"
            }
        }
    },
    {
        "id": 5, "role": "Sentiment Analysis Agent", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Classify each statement's sentiment as exactly one of: positive, negative, neutral. Watch for sarcasm, double negatives, and irony. Respond with ONLY JSON: {"1": "sentiment", ...}

Statements:
1. "I can't believe how not terrible this product turned out to be."
2. "The service is about as useful as a screen door on a submarine."
3. "Revenue increased 2% year-over-year, in line with projections."
4. "Oh great, another update that breaks everything. Just what I needed."
5. "I wouldn't say I'm unhappy with the results."
6. "The food was fine. Nothing special but nothing wrong either."
7. "If you enjoy watching paint dry, you'll LOVE their customer support."
8. "Not gonna lie, I was skeptical, but this thing actually slaps."
9. "The quarterly results exceeded analyst expectations by 12%."
10. "Sure, their 'AI' is really impressive — if you're comparing it to a calculator from 1995." """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "positive", "2": "negative", "3": "neutral",
                "4": "negative", "5": "positive", "6": "neutral",
                "7": "negative", "8": "positive", "9": "positive",
                "10": "negative"
            }
        }
    },
    {
        "id": 6, "role": "FAQ Generation Agent", "tier": 1,
        "scoring_type": "constraint",
        "prompt": """Generate exactly 8 FAQ entries from this product documentation. The documentation contains 3 deliberate contradictions — your FAQ must address and resolve ALL 3.

Documentation:
CloudSync Pro is available in three tiers: Free, Pro ($9.99/mo), and Enterprise ($29.99/mo). All tiers include unlimited storage. The Free tier is limited to 5GB of storage. Files are encrypted with AES-256 at rest and in transit. Maximum file size is 2GB for Free users and 10GB for paid users. The service supports Windows, Mac, and Linux. Mobile apps are available for iOS only. Android support is coming in Q2 2025. Deleted files are recoverable for 30 days. Enterprise users can recover files for up to 90 days. Our uptime SLA is 99.9% for all tiers. Free tier users are not covered by the SLA.

Format each FAQ as: Q: ... A: ...
After the FAQs, list the 3 contradictions you found.""",
        "scoring": {
            "type": "faq_constraints",
            "checks": [
                "has_8_faqs",
                "mentions_storage_contradiction",
                "mentions_mobile_contradiction",
                "mentions_sla_contradiction",
                "q_a_format",
                "covers_pricing",
                "covers_security",
                "covers_file_limits",
                "covers_platforms",
                "lists_3_contradictions"
            ]
        }
    },
    {
        "id": 7, "role": "Translation Agent", "tier": 1,
        "scoring_type": "constraint",
        "prompt": """Translate this English text to Spanish AND Japanese. For EACH language, add [NOTE] markers for every cultural adaptation you make.

Text:
"Our new Cloud9 platform is a real home run — it's like having your cake and eating it too. We've gone the whole nine yards to make it user-friendly. Even your grandmother could use it! It's available 24/7, rain or shine. We think it's the bee's knees, and we're not just whistling Dixie. Sign up before Black Friday for early-bird pricing."

Requirements:
1. Translate to both languages
2. Mark EVERY idiom/cultural reference with [NOTE: explanation]
3. The idioms to handle: "home run", "having your cake and eating it too", "gone the whole nine yards", "your grandmother could use it", "rain or shine", "bee's knees", "whistling Dixie", "Black Friday", "early-bird", "Cloud9/cloud nine"
4. Explain whether you preserved, adapted, or replaced each idiom""",
        "scoring": {
            "type": "translation_constraints",
            "checks": [
                "has_spanish", "has_japanese", "has_notes",
                "handles_home_run", "handles_cake_idiom",
                "handles_nine_yards", "handles_grandmother",
                "handles_bees_knees", "handles_whistling_dixie",
                "handles_black_friday"
            ]
        }
    },
    {
        "id": 8, "role": "Calendar / Scheduling Agent", "tier": 1,
        "scoring_type": "exact",
        "prompt": """Find the 30-minute meeting window that works for ALL 4 people. Respond with ONLY JSON: {"utc_start": "HH:MM", "utc_end": "HH:MM", "local_times": {"Alice": "HH:MM TZ", "Bob": "HH:MM TZ", "Carol": "HH:MM TZ", "Dave": "HH:MM TZ"}}

Constraint: The meeting must be during reasonable hours (8:00 AM - 8:00 PM local time) for everyone.

Alice (UTC-5, New York):
- 9:00-10:30 AM: Team standup
- 11:00-12:00 PM: Lunch
- 1:00-2:00 PM: Client call
- 3:00-5:00 PM: Deep work (blocked)
- Available: 10:30-11:00, 12:00-1:00, 2:00-3:00

Bob (UTC+0, London):
- 9:00-10:00 AM: Planning
- 11:00-12:30 PM: Workshop
- 2:00-3:00 PM: 1:1 with manager
- Available: 10:00-11:00, 12:30-2:00, 3:00-6:00

Carol (UTC+8, Singapore):
- 9:00-11:00 AM: Sprint review
- 12:00-1:00 PM: Lunch
- 2:00-4:00 PM: Coding
- 7:00-8:00 PM: Dinner
- Available: 11:00-12:00, 1:00-2:00, 4:00-7:00, 8:00+

Dave (UTC+5:30, Mumbai):
- 9:00-11:00 AM: Client workshops
- 12:00-1:00 PM: Lunch
- 2:00-4:00 PM: Code review
- Available: 11:00-12:00, 1:00-2:00, 4:00-8:00

Convert ALL times to UTC, find overlapping 30-min slot, state answer in UTC.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "utc_start": "17:00",
                "utc_end": "17:30"
            }
        }
    },
]
