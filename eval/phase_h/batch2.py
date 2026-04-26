"""Phase H Dense Tests — Batch 2: Tests 1, 3, 4, 6, 7, 8, 11, 13, 14, 15, 16"""

PHASE_H_BATCH2 = [
    # H-1: ROUTER / TRIAGE — 30 tickets
    {
        "id": 1, "role": "Router / Triage Agent", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Route each of these 30 support tickets to the correct department. Options: billing, technical, sales, hr, legal, shipping, security, product, marketing, general.
Respond with ONLY JSON: {"1": "department", ...}

Tickets:
1. "I was charged twice for my subscription last month"
2. "The app crashes when I try to upload files larger than 50MB"
3. "I'd like to upgrade from the Pro to Enterprise plan"
4. "An employee filed a harassment complaint against their manager"
5. "We received a cease-and-desist letter regarding our logo design"
6. "My order #4521 hasn't arrived and it's been 3 weeks"
7. "Someone accessed my account from an IP address in Russia"
8. "Can you add dark mode to the mobile app?"
9. "We want to run a co-branded campaign with your company"
10. "Where can I find your office hours?"
11. "I need a refund for the overcharge on invoice #7892"
12. "SSL certificate expired on the production server"
13. "What volume discounts do you offer for 500+ seats?"
14. "We need to update our company's bank details for payroll"
15. "Is your software compliant with GDPR data residency requirements?"
16. "Package arrived damaged, need replacement shipped"
17. "I think my API key was leaked on GitHub"
18. "Your search algorithm returns irrelevant results for exact match queries"
19. "Can we get a case study for our investor presentation?"
20. "What's the dress code for the office?"
21. "My credit card on file expired and I can't update it"
22. "Database connection pool is exhausted during peak hours"
23. "We'd like to set up a reseller partnership"
24. "Employee needs FMLA leave for 12 weeks starting next month"
25. "A competitor is using our patented algorithm"
26. "Three packages sent to wrong addresses this week"
27. "Possible data breach — customer PII found on dark web"
28. "The new onboarding flow has a 60% drop-off rate at step 3"
29. "We need social media assets for the Q4 product launch"
30. "How do I reset my password?" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "billing", "2": "technical", "3": "sales",
                "4": "hr", "5": "legal", "6": "shipping",
                "7": "security", "8": "product", "9": "marketing",
                "10": "general", "11": "billing", "12": "technical",
                "13": "sales", "14": "hr", "15": "legal",
                "16": "shipping", "17": "security", "18": "product",
                "19": "marketing", "20": "hr", "21": "billing",
                "22": "technical", "23": "sales", "24": "hr",
                "25": "legal", "26": "shipping", "27": "security",
                "28": "product", "29": "marketing", "30": "technical"
            }
        }
    },

    # H-3: HEARTBEAT / HEALTH MONITOR — 15 services
    {
        "id": 3, "role": "Heartbeat / Health Monitor", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Analyze these 15 service health reports and provide status for each. Respond as JSON: {"s1": {"status": "healthy/degraded/down", "latency_ms": N, "error_rate_pct": N.N}, ...}

Reports:
s1: API Gateway — avg response 45ms, p99 120ms, error rate 0.01%, 99.99% uptime last 24h
s2: Auth Service — avg response 200ms, p99 1500ms, error rate 2.5%, 3 timeout errors in last hour
s3: Database Primary — avg response 5ms, p99 15ms, error rate 0%, replication lag 0ms
s4: Database Replica — avg response 5ms, p99 200ms, error rate 0.1%, replication lag 5200ms
s5: Cache (Redis) — avg response 1ms, p99 3ms, error rate 0%, memory usage 45%
s6: Search (Elasticsearch) — avg response 800ms, p99 5000ms, error rate 8%, cluster yellow status
s7: Email Service — avg response 150ms, p99 300ms, error rate 0.5%, queue depth 12
s8: Payment Processor — connection refused for last 30 minutes, all requests failing
s9: CDN — avg response 15ms, p99 50ms, error rate 0%, cache hit rate 94%
s10: Message Queue (Kafka) — avg response 10ms, consumer lag 50000 messages, error rate 0.2%
s11: ML Inference — avg response 2000ms, p99 8000ms, error rate 12%, GPU utilization 99%
s12: Storage (S3) — avg response 100ms, p99 500ms, error rate 0.02%, 99.99% availability
s13: DNS — avg response 2ms, p99 10ms, error rate 0%, all zones resolving
s14: Load Balancer — avg response 1ms, p99 5ms, error rate 0%, active connections 2500/10000
s15: Monitoring Service — avg response 50ms, all dashboards stale for 45 minutes, last data point 45min ago""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "s1_status": "healthy", "s2_status": "degraded", "s3_status": "healthy",
                "s4_status": "degraded", "s5_status": "healthy", "s6_status": "degraded",
                "s7_status": "healthy", "s8_status": "down", "s9_status": "healthy",
                "s10_status": "degraded", "s11_status": "degraded", "s12_status": "healthy",
                "s13_status": "healthy", "s14_status": "healthy", "s15_status": "down"
            }
        }
    },

    # H-4: NOTIFICATION / ALERT — 30 events
    {
        "id": 4, "role": "Notification / Alert Agent", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Classify each event by priority: critical, high, medium, low, info. Respond as JSON: {"1": "priority", ...}

Events:
1. Production database is unreachable — all write operations failing
2. CPU usage on web server hit 85% for 3 minutes
3. New user registered from marketing campaign
4. SSL certificate expires in 3 days
5. Disk usage on backup server reached 92%
6. Weekly automated backup completed successfully
7. Payment processing gateway returned 500 errors for 15 minutes
8. A/B test variant B showing 2% higher conversion
9. Memory leak detected — service consuming 300MB more than baseline per hour
10. Quarterly security scan completed — no new vulnerabilities
11. Master-slave database replication lag exceeded 30 seconds
12. New pull request opened by team member
13. DDoS attack detected — traffic spike 10x normal levels
14. API rate limit reached by one client
15. Automated test suite passed — all 847 tests green
16. Customer reported data inconsistency between dashboard and API
17. Third-party API (non-critical analytics) returning timeouts
18. Root SSH login detected from unknown IP address
19. Marketing email campaign sent to 50K recipients
20. Service deployment to staging completed
21. Primary load balancer failover triggered — secondary active
22. New employee onboarding workflow initiated
23. Database connection pool at 95% capacity
24. Monthly uptime report: 99.97% (below 99.99% SLA)
25. Container orchestrator auto-scaled from 3 to 8 pods
26. Git repository exceeded 10GB storage limit
27. Customer credit card charge declined — retry scheduled
28. Ransomware signature detected in uploaded file
29. Sprint retrospective meeting scheduled for Friday
30. Production API latency p99 increased from 200ms to 2000ms""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "critical", "2": "medium", "3": "info",
                "4": "high", "5": "high", "6": "info",
                "7": "critical", "8": "info", "9": "high",
                "10": "info", "11": "high", "12": "info",
                "13": "critical", "14": "medium", "15": "info",
                "16": "high", "17": "low", "18": "critical",
                "19": "info", "20": "info", "21": "high",
                "22": "info", "23": "high", "24": "medium",
                "25": "medium", "26": "low", "27": "medium",
                "28": "critical", "29": "info", "30": "critical"
            }
        }
    },

    # H-8: CALENDAR / SCHEDULING — 20 requests
    {
        "id": 8, "role": "Calendar / Scheduling Agent", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Given this calendar for Monday March 10, 2025:
- 09:00-10:00: Team standup
- 10:30-11:30: Client call with Acme Corp
- 12:00-13:00: Lunch
- 14:00-15:30: Sprint planning
- 16:00-16:30: 1-on-1 with manager

Answer each question. Respond as JSON: {"1": "answer", ...}

Questions:
1. Is there a free 30-min slot between 09:00 and 10:30?
2. Can a 1-hour meeting fit between 11:30 and 12:00?
3. What is the earliest available 45-minute slot after 10:00?
4. How many total minutes of meetings are scheduled?
5. What is the longest free gap in the day (in minutes)?
6. Can a 2-hour meeting fit anywhere between 09:00 and 17:00?
7. Is the slot 15:30-16:00 free?
8. How many meetings are scheduled before lunch?
9. What percentage of 09:00-17:00 is booked? (round to nearest integer)
10. If the client call is moved to 13:00-14:00, what is the new longest free gap?
11. Can two separate 30-min meetings fit between 13:00 and 14:00?
12. What time does the last meeting end?
13. If standup is cancelled, what is the earliest 90-min slot?
14. How many meetings are longer than 30 minutes?
15. Is there any overlap between existing meetings?
16. What is the total free time between 09:00-17:00 in minutes?
17. Can a 30-min meeting fit at 11:30?
18. If sprint planning ends 30 min early, is 15:00-16:00 free?
19. How many back-to-back meetings are there (no gap)?
20. What is the average meeting duration in minutes?""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "yes", "2": "no", "3": "11:30",
                "4": "270", "5": "90", "6": "no",
                "7": "yes", "8": "2", "9": "56",
                "10": "120", "11": "no", "12": "16:30",
                "13": "09:00", "14": "3", "15": "no",
                "16": "210", "17": "yes", "18": "yes",
                "19": "0", "20": "54"
            }
        }
    },

    # H-11: EDITOR AGENT — 30 errors to find
    {
        "id": 11, "role": "Editor Agent", "tier": 2,
        "scoring_type": "h_content_check",
        "prompt": """Find ALL errors in this business report. There are exactly 30 errors (spelling, grammar, punctuation, factual, formatting). List each with line reference and correction. Respond as JSON: {"errors": [{"line": N, "error": "...", "correction": "..."}, ...], "count": 30}

Report:
L1: Quartely Financial Reveiw — Q3 2024
L2:
L3: Executive Summery
L4: Revenue for Q3 reached $4.7M million, a 12% increase over Q2.
L5: Our gross margin improved too 68%, up from 62% in the pervious quarter.
L6: The company now employes 247 full-time staff accross 3 offices.
L7: Key achivements include launching 2 new features, aquiring 1,200 new customers
L8: and reducing chrun from 5.2% to 4.1%.
L9:
L10: Deparment Breakdown
L11: Engineering: 89 employees, $1.8M budget, on-track for Q4 relaese.
L12: Marketing: 34 employees, $620k budget,  ROI of 340%.
L13: Sales: 52 employees, $890K buget, hit 108% of there quarterly target.
L14: Customer Sucess: 28 employees. response time improved form 4hrs to 2hrs.
L15: Operations: 44 employees, $410K budget, 99.7% up-time achived.
L16:
L17: Financial Hightlights
L18: - Total revenue: $4,700000
L19: - Operating expences: $3,100,000
L20: - Net profit: $1,700,000 (this should be $1,600,000 based on above numbers)
L21: - Cash on-hand: $8.2M (down form $9.1M due to capaital expenditures)
L22: - Accounts recievable: $1.2M (45-day average collection priod)
L23:
L24: Looking Forward
L25: We anticapte Q4 revenue to reach $5.1M, driven by seasonal demand
L26: and the upcomming product launch, Management reccommends allocating
L27: an additonal $200K to marketing to capture holiday season demand.""",
        "scoring": {
            "checks": {
                "e1_quarterly": ["quarterly"],
                "e2_review": ["review"],
                "e3_summary": ["summary"],
                "e4_redundant_million": ["4.7m million", "redundant", "million"],
                "e5_too_to": ["too", "to"],
                "e6_previous": ["previous"],
                "e7_employs": ["employs"],
                "e8_across": ["across"],
                "e9_achievements": ["achievements"],
                "e10_acquiring": ["acquiring"],
                "e11_churn": ["churn"],
                "e12_department": ["department"],
                "e13_release": ["release"],
                "e14_double_space": ["double space", "extra space", "spacing"],
                "e15_budget": ["budget"],
                "e16_their": ["their"],
                "e17_success": ["success"],
                "e18_from_l14": ["from"],
                "e19_achieved": ["achieved"],
                "e20_highlights": ["highlights"],
                "e21_missing_comma": ["4,700,000", "missing comma", "formatting"],
                "e22_net_profit_math": ["1,600,000", "math", "calculation", "incorrect"],
                "e23_expenses": ["expenses"],
                "e24_from_l21": ["from"],
                "e25_capital": ["capital"],
                "e26_receivable": ["receivable"],
                "e27_period": ["period"],
                "e28_anticipate": ["anticipate"],
                "e29_recommends": ["recommends"],
                "e30_additional": ["additional"]
            }
        }
    },

    # H-13: EMAIL DRAFTING — 15 emails to classify/summarize
    {
        "id": 13, "role": "Email Drafting / Summarization", "tier": 2,
        "scoring_type": "json_values",
        "prompt": """Classify each email by: action_required (yes/no), priority (high/medium/low), category (meeting/task/fyi/approval/question). Respond as JSON: {"1": {"action": "yes/no", "priority": "...", "category": "..."}, ...}

Emails:
1. Subject: "URGENT: Production server down" — "The main API server crashed at 3am. All customer-facing services are offline. Need someone to restart and investigate root cause immediately."
2. Subject: "Q3 Report Draft" — "Attached is the draft Q3 report for your review. Please provide feedback by Friday."
3. Subject: "Team lunch next Thursday" — "Hey team, we're doing lunch at the Italian place next Thursday at noon. Let me know if you can make it!"
4. Subject: "Budget approval needed" — "I need your sign-off on the $15K marketing spend for the Q4 campaign. Contract deadline is tomorrow."
5. Subject: "FYI: New parking policy" — "Starting next month, visitor parking will require pre-registration. See attached policy document."
6. Subject: "Re: Client proposal" — "Quick question — should we include the custom integration pricing in the Acme proposal, or keep it as a separate line item?"
7. Subject: "Weekly standup cancelled" — "No standup this Monday due to the holiday. Async updates in Slack instead."
8. Subject: "SECURITY ALERT: Suspicious login" — "We detected 47 failed login attempts on the admin account from IP 185.x.x.x. Account has been temporarily locked. Please verify and reset credentials."
9. Subject: "Congratulations on the promotion!" — "Just wanted to say congrats on the well-deserved promotion. The team is lucky to have you leading."
10. Subject: "Invoice #4892 past due" — "This is a reminder that invoice #4892 ($23,450) is 15 days past due. Please process payment at your earliest convenience."
11. Subject: "Design review — new dashboard" — "The mockups for the new analytics dashboard are ready. Can we schedule a 30-min review this week?"
12. Subject: "Re: Re: Re: Meeting time" — "Tuesday 2pm works for me too. See you then."
13. Subject: "Vendor contract renewal" — "Our AWS contract expires in 30 days. Need decision on whether to renew at current terms ($45K/yr) or negotiate. Deadline: next Friday."
14. Subject: "Out of office" — "I'll be out Dec 23-Jan 2. Contact Sarah for urgent items."
15. Subject: "Data migration plan review" — "Please review the attached migration plan. We need sign-off from engineering and ops leads before proceeding. Migration window is Jan 15." """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1_action": "yes", "1_priority": "high", "1_category": "task",
                "2_action": "yes", "2_priority": "medium", "2_category": "task",
                "3_action": "yes", "3_priority": "low", "3_category": "meeting",
                "4_action": "yes", "4_priority": "high", "4_category": "approval",
                "5_action": "no", "5_priority": "low", "5_category": "fyi",
                "6_action": "yes", "6_priority": "medium", "6_category": "question",
                "7_action": "no", "7_priority": "low", "7_category": "fyi",
                "8_action": "yes", "8_priority": "high", "8_category": "task",
                "9_action": "no", "9_priority": "low", "9_category": "fyi",
                "10_action": "yes", "10_priority": "high", "10_category": "task",
                "11_action": "yes", "11_priority": "medium", "11_category": "meeting",
                "12_action": "no", "12_priority": "low", "12_category": "meeting",
                "13_action": "yes", "13_priority": "high", "13_category": "approval",
                "14_action": "no", "14_priority": "low", "14_category": "fyi",
                "15_action": "yes", "15_priority": "high", "15_category": "approval"
            }
        }
    },

    # H-14: DOCUMENT SUMMARIZATION — 15 metrics to extract
    {
        "id": 14, "role": "Document Summarization Agent", "tier": 2,
        "scoring_type": "json_numeric",
        "prompt": """Extract these 15 numeric metrics from the report below. Respond as JSON: {"m1": value, ...}

Report:
"TechCorp Annual Report 2024
Revenue reached $127.3M, up 23% year-over-year from $103.5M in 2023. Gross profit was $84.8M with a gross margin of 66.6%. Operating expenses totaled $61.2M, broken down as: R&D $28.4M (46.4% of opex), Sales & Marketing $22.1M (36.1%), G&A $10.7M (17.5%). Operating income was $23.6M, giving an operating margin of 18.5%.

Net income after tax was $18.9M (effective tax rate 19.9%). Earnings per share (diluted) were $2.37 on 7.98M shares outstanding. The company ended the year with $45.2M cash and $12.8M debt, for net cash of $32.4M.

Customer metrics: 8,420 total customers (up from 6,890), average revenue per customer $15,119. Annual churn rate decreased to 8.7% from 11.2%. Net revenue retention was 118%. Employee count grew to 612 from 489."

Questions:
m1: 2024 total revenue in millions
m2: YoY revenue growth percentage
m3: 2023 revenue in millions
m4: Gross profit in millions
m5: Gross margin percentage
m6: Total operating expenses in millions
m7: R&D spend in millions
m8: Operating income in millions
m9: Net income in millions
m10: Diluted EPS
m11: Cash on hand in millions
m12: Total customers in 2024
m13: Average revenue per customer
m14: Annual churn rate percentage
m15: Employee count in 2024""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "m1": 127.3, "m2": 23.0, "m3": 103.5,
                "m4": 84.8, "m5": 66.6, "m6": 61.2,
                "m7": 28.4, "m8": 23.6, "m9": 18.9,
                "m10": 2.37, "m11": 45.2, "m12": 8420,
                "m13": 15119, "m14": 8.7, "m15": 612
            },
            "tolerance": 0.05
        }
    },

    # H-16: SOCIAL MEDIA MONITORING — 20 posts
    {
        "id": 16, "role": "Social Media Scouting / Monitoring", "tier": 2,
        "scoring_type": "json_values",
        "prompt": """Analyze these 20 social media posts about our brand. For each, classify: sentiment (positive/negative/neutral), crisis_flag (yes/no), topic (product/service/price/competitor/general). Respond as JSON: {"1": {"sentiment": "...", "crisis": "...", "topic": "..."}, ...}

Posts:
1. "@TechCorp your new dashboard is amazing! Saved me 2 hours today 🎉"
2. "Just found out TechCorp raised prices 40% with ZERO notice. Moving to CompetitorX."
3. "Interesting comparison between TechCorp and CompetitorY features on ProductHunt"
4. "@TechCorp support has been ignoring my ticket for 2 WEEKS. Unacceptable."
5. "TechCorp quarterly earnings call is tomorrow at 4pm EST"
6. "WARNING: TechCorp had a data breach. My personal info was leaked. Contacting lawyer."
7. "The TechCorp API documentation is the best I've worked with"
8. "Switched from CompetitorZ to TechCorp. The migration tool worked flawlessly."
9. "TechCorp is hiring for 3 engineering positions in Austin"
10. "Am I the only one who thinks TechCorp's mobile app is a dumpster fire? 🔥"
11. "@TechCorp your pricing is actually quite fair compared to enterprise alternatives"
12. "TechCorp's server has been down for 6 hours. This is costing us thousands per hour."
13. "Just attended TechCorp's webinar on AI integration. Very informative!"
14. "My company switched to TechCorp and our customer complaints dropped 30%"
15. "Thread: Why TechCorp's architecture is fundamentally flawed (1/12)..."
16. "TechCorp customer support resolved my issue in under 10 minutes. Impressive."
17. "CEO of TechCorp caught making offensive remarks at industry conference"
18. "The new TechCorp release fixed all the bugs I reported. Great responsiveness!"
19. "Thinking about trying TechCorp. Anyone have experience with their free tier?"
20. "BREAKING: Former TechCorp employees allege systematic discrimination in lawsuit" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1_sentiment": "positive", "1_crisis": "no", "1_topic": "product",
                "2_sentiment": "negative", "2_crisis": "yes", "2_topic": "price",
                "3_sentiment": "neutral", "3_crisis": "no", "3_topic": "competitor",
                "4_sentiment": "negative", "4_crisis": "no", "4_topic": "service",
                "5_sentiment": "neutral", "5_crisis": "no", "5_topic": "general",
                "6_sentiment": "negative", "6_crisis": "yes", "6_topic": "service",
                "7_sentiment": "positive", "7_crisis": "no", "7_topic": "product",
                "8_sentiment": "positive", "8_crisis": "no", "8_topic": "competitor",
                "9_sentiment": "neutral", "9_crisis": "no", "9_topic": "general",
                "10_sentiment": "negative", "10_crisis": "no", "10_topic": "product",
                "11_sentiment": "positive", "11_crisis": "no", "11_topic": "price",
                "12_sentiment": "negative", "12_crisis": "yes", "12_topic": "service",
                "13_sentiment": "positive", "13_crisis": "no", "13_topic": "general",
                "14_sentiment": "positive", "14_crisis": "no", "14_topic": "product",
                "15_sentiment": "negative", "15_crisis": "no", "15_topic": "product",
                "16_sentiment": "positive", "16_crisis": "no", "16_topic": "service",
                "17_sentiment": "negative", "17_crisis": "yes", "17_topic": "general",
                "18_sentiment": "positive", "18_crisis": "no", "18_topic": "product",
                "19_sentiment": "neutral", "19_crisis": "no", "19_topic": "product",
                "20_sentiment": "negative", "20_crisis": "yes", "20_topic": "general"
            }
        }
    },
]
