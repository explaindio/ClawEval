"""
Phase D: Hard Evaluation Prompts — Adversarial, Verifiable, Role-Tuned
Each prompt has: id, role, tier, hard_prompt, scoring_type, scoring_data
scoring_type: 'exact' (automated), 'constraint' (count constraints met), 'manual' (50-pt rubric)
"""

HARD_TESTS = [
    # ================================================================
    # TIER 1 — Precision & Constraint Tests
    # ================================================================
    {
        "id": 1, "role": "Router / Triage Agent", "tier": 1,
        "scoring_type": "exact",
        "scoring_data": {"answers": {"1": "devops", "2": "code_review", "3": "research", "4": "translation", "5": "code_generation", "6": "calendar", "7": "qa_testing", "8": "summarization"}},
        "hard_prompt": """Classify each message into EXACTLY ONE category. Respond with ONLY a JSON object mapping message number to category.

Categories: code_generation, code_review, qa_testing, research, email, summarization, translation, calendar, devops

Messages:
1. "Roll back the production deployment to v2.3.1" 
2. "This function works but the variable names are terrible and there's no error handling"
3. "What are the pros and cons of GraphQL vs REST for mobile apps?"
4. "Convert this error message to Japanese: 'Connection timeout after 30 seconds'"
5. "Write me a Python decorator that retries failed API calls 3 times with exponential backoff"
6. "Move my 2pm meeting with Sarah to Thursday same time"
7. "Our login tests are passing locally but failing in CI — can you investigate why?"
8. "Give me the key points from the last 3 board meeting transcripts"

IMPORTANT: Some messages are deliberately ambiguous. Pick the BEST single category.""",
    },
    {
        "id": 2, "role": "Input Validator / Sanitizer", "tier": 1,
        "scoring_type": "constraint",
        "scoring_data": {"total_issues": 11, "critical_issues": ["end_date before start_date", "email format", "negative quantity", "XSS in name", "SQL injection in notes", "phone has letters", "zip code wrong length", "discount > 100%"]},
        "hard_prompt": """Validate this API request body. Find ALL issues (there are at least 10). For each issue, specify: field, severity (critical/error/warning), and explanation. Cross-field validations are required.

```json
{
  "order": {
    "customer": {
      "name": "<img src=x onerror=alert(1)>John",
      "email": "john@",
      "phone": "555-CALL-ME",
      "zip": "1234"
    },
    "items": [
      {"sku": "ABC-123", "quantity": -3, "unit_price": 29.99},
      {"sku": "", "quantity": 0, "unit_price": 0.001},
      {"sku": "DEF-456", "quantity": 2, "unit_price": 15.00}
    ],
    "discount_percent": 150,
    "start_date": "2025-03-15",
    "end_date": "2025-03-10",
    "notes": "Regular order'; DROP TABLE orders;--",
    "shipping": {"method": "TELEPORT", "address": ""}
  }
}
```

List every single issue. Do NOT miss cross-field validations (e.g., date relationships).""",
    },
    {
        "id": 3, "role": "Heartbeat / Health Monitor", "tier": 1,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify": ["memory_leak", "cron_correlation", "disk_will_fill", "error_spike_correlates_with_connections"]},
        "hard_prompt": """Analyze these 10-minute server metrics sampled every minute. Identify ALL hidden patterns and predict failures. There are at least 3 non-obvious correlations.

Time  | CPU% | Mem%  | Disk% | Conn | Err/s | DiskIO
00:00 | 45   | 71.0  | 82.0  | 200  | 2     | 10MB/s
00:01 | 42   | 71.5  | 82.1  | 205  | 1     | 12MB/s
00:02 | 48   | 72.0  | 82.2  | 198  | 3     | 11MB/s
00:03 | 95   | 72.5  | 82.3  | 450  | 45    | 150MB/s
00:04 | 55   | 73.2  | 82.5  | 210  | 5     | 15MB/s
00:05 | 43   | 73.8  | 82.6  | 195  | 2     | 10MB/s
00:06 | 44   | 74.5  | 82.8  | 202  | 1     | 11MB/s
00:07 | 47   | 75.1  | 82.9  | 205  | 3     | 12MB/s
00:08 | 93   | 75.8  | 83.1  | 440  | 42    | 145MB/s
00:09 | 52   | 76.4  | 83.2  | 215  | 4     | 14MB/s

Questions to answer:
1. What recurring event happens and at what interval?
2. Memory is rising linearly — at this rate, when will it hit 95%?
3. What is the correlation between connections and error rate?
4. At the current disk growth rate, how many hours until 95% full?
Give EXACT numbers for questions 2 and 4.""",
    },
    {
        "id": 4, "role": "Notification / Alert Agent", "tier": 1,
        "scoring_type": "constraint",
        "scoring_data": {"must_deduplicate": True, "must_identify_false_positive": True, "correct_priorities": {"disk": "P1", "cert_expired": "P1", "cert_expiring": "P2", "cpu_spike": "false_positive", "new_deploy": "P3"}},
        "hard_prompt": """Process these 7 events into alerts. WATCH OUT: 2 events are duplicates (merge them), 1 is a false positive that should NOT generate an alert. Assign correct priorities.

Events (timestamps in UTC):
1. 14:00 — "Disk /data at 94% capacity" (source: monitoring)
2. 14:01 — "SSL certificate for api.example.com expired 2 hours ago" (source: cert-manager)
3. 14:02 — "CPU spike to 98% on worker-3" (source: monitoring)
4. 14:02 — "CPU on worker-3 returned to 12% after scheduled batch job completed" (source: monitoring)
5. 14:03 — "SSL certificate for api.example.com expires in -2 hours" (source: different cert checker)
6. 14:05 — "New deployment v2.4.1 rolled out successfully" (source: CI/CD)
7. 14:06 — "Disk /data at 94% — approaching critical threshold" (source: secondary monitoring)

For each alert: priority (P1/P2/P3), channel, message, and reasoning. Explain which events you merged and which you filtered as false positives.""",
    },
    {
        "id": 5, "role": "Sentiment Analysis Agent", "tier": 1,
        "scoring_type": "exact",
        "scoring_data": {"answers": {"1": "negative", "2": "positive", "3": "negative", "4": "negative", "5": "positive", "6": "negative"}},
        "hard_prompt": """Classify the sentiment of each text as positive, negative, or neutral. CAREFUL: These contain sarcasm, irony, and idioms that may mislead you.

Respond with ONLY a JSON object mapping number to sentiment.

1. "Oh great, another update that breaks everything. Just what I needed today."
2. "I can't believe how bad I am at putting this product down — I keep using it!"
3. "The service is about as useful as a chocolate teapot."
4. "I would recommend this to my worst enemy."
5. "Not gonna lie, I was skeptical, but this thing slaps."
6. "Sure, if you enjoy waiting 3 hours for a response, their support is 'fantastic'."

Think carefully about sarcasm before answering.""",
    },
    {
        "id": 6, "role": "FAQ Generation Agent", "tier": 1,
        "scoring_type": "constraint",
        "scoring_data": {"must_flag_contradictions": True, "contradictions": ["free trial length", "refund policy"]},
        "hard_prompt": """Generate FAQs from this product description. WARNING: The text contains 2 deliberate contradictions. You MUST identify and flag them rather than silently picking one version.

Product Description:
"CloudStore offers unlimited storage starting at $9.99/month. All plans include a 14-day free trial. Enterprise customers get dedicated support with 4-hour response SLA. Files are encrypted with AES-256 at rest and in transit. Our 30-day free trial lets you explore all features. Refunds are available within 60 days of purchase, no questions asked. Maximum file size is 10GB. We guarantee 99.9% uptime. Note: due to our no-refund policy, please use the free trial to evaluate before purchasing. Supports Windows, Mac, Linux, iOS, and Android."

Generate 6 FAQs AND explicitly call out the contradictions you found in the source text.""",
    },
    {
        "id": 7, "role": "Translation Agent", "tier": 1,
        "scoring_type": "constraint",
        "scoring_data": {"must_flag_untranslatable": True, "must_handle_pun": True, "must_note_cultural": True},
        "hard_prompt": """Translate this marketing copy to Spanish AND Japanese. This text contains: 1 pun, 1 culture-specific reference, and 1 idiom. You MUST add translator notes explaining how you handled each.

"Our new Cloud9 hosting puts your website on cloud nine! Like a good neighbor, ServerFarm is there. Don't put all your eggs in one basket — our multi-region failover means your data is always safe. With speeds that would make Usain Bolt jealous, your pages load before you can say 'supercalifragilisticexpialidocious.'"

Requirements:
- Translate the full text to both languages
- Add [TRANSLATOR NOTE] for EACH culturally-specific element explaining your adaptation
- The pun "Cloud9/cloud nine" must be addressed — explain if you preserved it or adapted it
- The "good neighbor" is a State Farm insurance slogan reference — explain how you handled it""",
    },
    {
        "id": 8, "role": "Calendar / Scheduling Agent", "tier": 1,
        "scoring_type": "exact",
        "scoring_data": {"answer": "14:00-14:30 UTC", "answer_alt": ["14:00", "2:00 PM UTC", "2pm UTC"]},
        "hard_prompt": """Find the ONLY valid 30-minute meeting slot for all 4 participants on Monday. Show your work.

Participant calendars (all times in their LOCAL timezone):

Alice (UTC-5, New York):
- 8:00-9:30 AM: Team standup
- 10:00-11:00 AM: Client call  
- 12:00-1:00 PM: Lunch (blocked)
- 2:00-4:00 PM: Sprint planning
- Available: 9:30-10:00, 11:00-12:00, 1:00-2:00

Bob (UTC+0, London):
- 9:00-10:30 AM: Architecture review
- 11:30 AM-12:30 PM: Lunch
- 1:00-2:30 PM: Design sync
- 3:00-5:00 PM: Deep work (blocked)
- Available: 10:30-11:30, 12:30-1:00, 2:30-3:00

Carol (UTC+1, Berlin):
- 9:00-10:00 AM: Morning standup
- 11:00 AM-12:00 PM: 1:1 with manager
- 1:00-2:00 PM: Lunch
- 3:30-5:00 PM: Workshop
- Available: 10:00-11:00, 12:00-1:00, 2:00-3:30

Dave (UTC+5:30, Mumbai):
- 10:00 AM-12:00 PM: Client workshops
- 1:00-2:00 PM: Lunch
- 3:00-4:00 PM: Code review
- 5:00-7:00 PM: Evening meetings
- Available: 12:00-1:00, 2:00-3:00, 4:00-5:00, 7:00+

Convert ALL times to UTC first, then find the overlapping 30-minute window. State the answer in UTC.""",
    },

    # ================================================================
    # TIER 2 — Multi-Constraint & Accuracy Tests (roles 9-35)
    # ================================================================
    {
        "id": 9, "role": "Research / Web Search Agent", "tier": 2,
        "scoring_type": "exact",
        "scoring_data": {"false_claims": [2, 5, 7], "true_claims": [1, 3, 4, 6, 8]},
        "hard_prompt": """8 claims about quantum computing are listed below. Exactly 3 are FALSE. Identify which 3 are false and explain why. Respond with JSON: {"false": [numbers], "explanations": {...}}

1. Qubits can exist in superposition of 0 and 1 simultaneously
2. Google's quantum computer Sycamore has over 1000 qubits
3. Quantum entanglement allows correlations between qubits regardless of distance
4. Shor's algorithm can factor large numbers exponentially faster than classical algorithms
5. Quantum computers operate at absolute zero (0 Kelvin)
6. Quantum error correction is still a major unsolved challenge
7. IBM was the first company to demonstrate quantum supremacy
8. Decoherence is a major obstacle to building practical quantum computers""",
    },
    {
        "id": 10, "role": "Content Writer / Blog Writer", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"word_count_exact": 200, "required_elements": ["statistic", "counterargument", "call_to_action", "metaphor", "question_to_reader"], "tolerance": 0},
        "hard_prompt": """Write a blog post introduction about remote work productivity that is EXACTLY 200 words. Not approximately — EXACTLY 200. Count carefully.

Mandatory elements (all 5 must appear):
1. At least one specific statistic with a source
2. A counterargument acknowledgment
3. A call to action
4. A metaphor or analogy
5. A direct question to the reader

After your text, include a line: "Word count: [N]" with your count. I will verify.""",
    },
    {
        "id": 11, "role": "Editor Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"total_errors": 15, "categories": {"grammar": 5, "factual": 3, "logic": 3, "style": 4}},
        "hard_prompt": """This 200-word text contains EXACTLY 15 errors across 4 categories: grammar (5), factual (3), logical (3), and style (4). Find ALL 15.

"The Eiffel Tower, located in Berlin, Germany, was completed in 1889 for the World's Fair. Standing at 1,063 feet tall, their the tallest structure in Europe. The tower was designed by Alexander Eiffel, who also helped designed the Statue of Liberty's internal framework.

Every year, approximately 7 million visitors visits the tower making it the most visited paid monument in the world. The tower has three levels, with restaurants on the first and second levels. Visitors can chose to take the stairs (a total of 1,665 steps to the top) or use the elevators.

Interestingly, the tower was originally intended to be temporary and was suppose to be dismantled after 20 years. However, it was saved because it proved valuable for radio transmissions. If the tower was built today, it would cost approximately $40 million — quite affordable for a city like Berlin.

The tower shrinks by 6 inches in winter due to thermal contraction — despite the fact that metal expands in cold temperatures. It is painted every 7 years using 60 tons of paint, and have been 18 different colors throughout its history."

List each error with: category, location, what's wrong, and the correction.""",
    },
    {
        "id": 12, "role": "Content Planner", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"constraints": ["no_consecutive_same_format", "budget_total_5000", "min_2_video_per_month", "alternating_pillars", "no_weekend_posts", "social_before_blog", "max_3_posts_per_week", "monthly_theme_progression"]},
        "hard_prompt": """Create a 1-month (4-week) content calendar satisfying ALL 8 constraints. If any constraint is violated, the entire plan fails.

Constraints:
1. Never post the same format 2 days in a row (formats: blog, video, social, newsletter)
2. Total production budget must equal exactly $5,000 (blog=$200, video=$500, social=$50, newsletter=$100)
3. Minimum 2 videos per month
4. Content pillars (A, B, C) must alternate — never 2 of same pillar in a row
5. No posts on weekends
6. Every blog must be preceded by a related social post within 2 days before it
7. Maximum 3 posts per week
8. Month theme: Week 1=Awareness, Week 2=Education, Week 3=Engagement, Week 4=Conversion

Show the calendar as a table and verify each constraint at the end with a checklist.""",
    },
    {
        "id": 13, "role": "Email Drafting / Summarization", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"hidden_urgency": [3, 6], "correct_p1": [2, 3, 6]},
        "hard_prompt": """Prioritize these 8 emails. WARNING: 2 emails have HIDDEN urgency clues buried in the text that change their priority. Read carefully.

1. Subject: "Team lunch Friday" — "Hey, let's do Thai food this week!"
2. Subject: "Quick question" — "The board presentation is tomorrow and slide 14 has last quarter's numbers instead of this quarter's. Can someone fix?"
3. Subject: "FYI - vendor update" — "Just letting you know Acme renewed. PS: They mentioned in passing that they're evaluating competitors and their contract has a 30-day termination clause that activates next week."
4. Subject: "URGENT: Office supplies" — "We're running low on printer paper!!!!"
5. Subject: "Re: Project timeline" — "Looks good, no changes needed from my end."
6. Subject: "Meeting notes from Tuesday" — "Attached are the notes. Also, I noticed during the meeting that the CFO mentioned they're freezing all new hires starting Monday — might affect our expansion plans."
7. Subject: "Newsletter subscription" — "Thanks for subscribing to TechDigest!"
8. Subject: "Parking lot maintenance" — "Lot B will be closed Saturday for restriping."

Rank P1-P4. Explain the hidden urgency in the emails where it exists.""",
    },
    {
        "id": 14, "role": "Document Summarization", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"buried_fact": "API key rotation happens automatically every 90 days and will break integrations that hardcode keys", "must_include_in_summary": True},
        "hard_prompt": """Summarize this document in exactly 5 bullet points. ONE critical fact is buried in the middle paragraph that most people miss — your summary MUST include it.

"Our platform migration is proceeding on schedule. The frontend team completed the React 18 upgrade last week, achieving a 30% improvement in initial load times. User testing shows 92% satisfaction with the new UI components. The design system now includes 47 reusable components.

The backend infrastructure has been moved to Kubernetes across 3 availability zones. Database replication lag is under 50ms. We implemented automated API key rotation every 90 days, which means any integration partner who has hardcoded their API keys will experience authentication failures. This needs to be communicated before the next rotation on March 15th. Redis caching reduced average response time from 340ms to 45ms.

Deployment frequency increased from weekly to daily with the new CI/CD pipeline. The error rate dropped from 2.1% to 0.3%. Mobile app downloads grew 25% month over month. Revenue is up 18% YoY with 340 enterprise customers now on the platform."

Which fact is the most operationally critical and time-sensitive? It should be in your summary.""",
    },
    {
        "id": 15, "role": "Meeting Notes / Transcription Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"contradictions": ["budget (Sarah says 50K, Mike says 75K)", "timeline (Lisa says March, James says April)", "headcount (Sarah says 3, later says 2)"]},
        "hard_prompt": """Process this meeting transcript into structured notes. WARNING: The transcript contains 3 contradictory statements made by different participants. You MUST identify all 3 contradictions.

Transcript:
Sarah (PM): "OK let's kick off. Budget for Project Atlas is $50K as approved by the board."
Mike (Eng): "Actually I spoke with finance yesterday and they confirmed $75K for Atlas."
Sarah: "We'll need to clarify that. Moving on — Lisa, timeline update?"
Lisa (Design): "Designs will be finalized by end of March. That gives engineering 6 weeks."
James (QA): "Wait, in last week's email you said designs would be done in April. We planned QA around that."
Lisa: "That was before we got the additional designer. March is firm now."
Sarah: "OK, so we need 3 new hires for this: 2 backend, 1 frontend."
Mike: "Agreed on the technical side."
Sarah: "Actually, thinking about it, we only need 2 new hires — we can reassign Jordan."
James: "QA will need 2 weeks after engineering freeze. Factor that into the timeline."

Extract: decisions, action items, and CONTRADICTIONS (with who said what).""",
    },
    {
        "id": 16, "role": "Social Media Scouting / Monitoring", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_bot_pattern": True, "must_flag_coordinated": True, "real_vs_fake_ratio": "60/40"},
        "hard_prompt": """Analyze these 10 social media mentions. 4 of them are likely bot/fake accounts (coordinated inauthentic behavior). Identify which ones and explain the patterns.

1. @techfan_2024 (joined Jan 2024, 12 followers): "Best product ever! 10/10 recommend! #amazing #bestproduct"
2. @sarah_designs (joined 2019, 2.3K followers): "Tried the new update. The color picker is improved but the export feature is still broken for SVG files."
3. @digital_guru_99 (joined Feb 2024, 8 followers): "Amazing product!! Everyone should buy this!! #bestproduct #amazing"
4. @mike_in_seattle (joined 2020, 890 followers): "Been a customer for 2 years. v3.2 regression in batch processing is killing our workflow. @support any ETA on fix?"
5. @bestreviews_daily (joined Jan 2024, 15 followers): "This is the best product I've ever used! 10/10!! #amazing #bestproduct"
6. @jennifer_codes (joined 2021, 1.5K followers): "The API rate limiting is too aggressive at 100/min. We need at least 500 for our use case."
7. @happy_customer_01 (joined Feb 2024, 5 followers): "Best product!! Amazing quality!! Everyone needs this!! #bestproduct"
8. @dev_community (joined 2018, 5K followers): "Interesting approach to the caching problem. Would love to see benchmarks."
9. @alexr_dev (joined 2022, 340 followers): "Support response time has improved a lot. Got my ticket resolved in 2 hours."
10. @startup_life (joined 2023, 670 followers): "Comparing this vs Competitor X — similar features but the pricing model is confusing."

Identify the fake accounts, explain the coordinated pattern, and provide a clean sentiment analysis using ONLY the authentic mentions.""",
    },
    {
        "id": 17, "role": "Social Media Content Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"char_limits": {"twitter": 280, "linkedin": 3000, "instagram": 2200}, "must_include_hashtags": True, "must_match_platform_tone": True, "must_be_different_content": True},
        "hard_prompt": """Write 3 posts about the same product launch for 3 different platforms. Each MUST respect the platform's character limit and tone. They must be substantially different — not just reformatted copies.

Product: AI-powered code review tool that catches security vulnerabilities before merge.

Platform requirements:
1. Twitter/X: MAX 280 characters (including hashtags). Punchy, clever.
2. LinkedIn: Professional tone, 150-300 words. Include a personal anecdote or insight.
3. Instagram caption: Casual, emoji-heavy, 100-200 words. Include 10+ relevant hashtags at the end.

After each post, include the character/word count. I will verify the limits.""",
    },
    {
        "id": 18, "role": "News Aggregation Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_related": True, "must_flag_contradiction": True, "must_assess_reliability": True},
        "hard_prompt": """Process these 8 headlines. Some are about the SAME story from different angles (identify which). One pair contains contradictory information (flag it). Assess source reliability.

1. Reuters: "TechCorp reports Q4 revenue of $12.3B, beating estimates by 8%"
2. BlogSpam.io: "SHOCKING: TechCorp hiding massive losses behind revenue numbers!!"
3. WSJ: "TechCorp Q4 revenue misses analyst expectations, stock drops 3%"
4. AP: "EU announces new AI regulation framework affecting US tech companies"
5. TechCrunch: "TechCorp's cloud division drives Q4 beat, revenue hits $12.3B"
6. Reuters: "European Commission proposes AI Act amendments with stricter compliance timelines"
7. RandomBlog2024.com: "AI regulations will DESTROY the tech industry forever!!!"
8. Bloomberg: "TechCorp CEO discusses AI strategy after strong Q4 earnings"

Tasks:
1. Group stories that cover the same event
2. Identify the contradictory pair (headline 1 vs 3) and assess which is more likely accurate
3. Rate each source's reliability (1-10)
4. Create a briefing with only the verified, deduplicated information""",
    },
    {
        "id": 19, "role": "Shopping / Price Comparison", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"trap": "cheapest is not best value", "must_calculate_tco": True, "correct_recommendation": "Product B"},
        "hard_prompt": """Compare these 4 products. WARNING: The cheapest option is NOT the best value when you calculate total cost of ownership. Show your math.

Product A — Laptop Alpha: $899
- 8GB RAM (non-upgradable), 256GB SSD
- Battery: 6 hours, replacement cost $200
- Expected lifespan: 3 years, no extended warranty available
- Required accessories: $150 dock, $80 adapter

Product B — Laptop Beta: $1,299
- 16GB RAM, 512GB SSD (user upgradable)
- Battery: 10 hours, replaceable ($80)
- Expected lifespan: 5 years, extended warranty $100/year
- All ports included, no accessories needed

Product C — Laptop Gamma: $749
- 8GB RAM, 128GB SSD
- Battery: 4 hours, non-replaceable
- Expected lifespan: 2 years, no warranty
- Required: $200 external SSD, $150 dock, $80 adapter

Product D — Laptop Delta: $1,099
- 16GB RAM, 256GB SSD
- Battery: 8 hours, replacement $150
- Expected lifespan: 4 years, warranty included
- Required: $80 adapter

Calculate 5-year total cost of ownership for each (include purchase + accessories + replacements + warranty). Recommend the best value.""",
    },
    {
        "id": 20, "role": "Memory / Knowledge Management", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"contradictions_to_resolve": 3, "must_show_temporal_reasoning": True, "must_flag_uncertainty": True},
        "hard_prompt": """Extract and merge knowledge from these 5 conversation snippets. There are 3 contradictions — resolve each by using the MOST RECENT information and flag what changed.

Jan 2: "I'm a senior developer at Acme Corp working on their Python backend."
Jan 15: "We decided to migrate from PostgreSQL to MongoDB for the user service."
Feb 1: "Got promoted to Tech Lead! Managing a team of 4 developers now."
Feb 20: "After benchmarking, we're actually sticking with PostgreSQL — MongoDB wasn't right for our consistency requirements. Also, we hired 2 more people, team is now 6."
Mar 5: "Acme Corp got acquired by MegaTech. I'm now technically a MegaTech employee but same role. Oh, and 1 person left, so team is 5. We're also evaluating MySQL as finance wants to standardize."

Produce a final knowledge profile, clearly marking:
1. What the CURRENT truth is for each fact
2. What changed and when (changelog)
3. What is UNCERTAIN (e.g., MySQL evaluation — in progress, not decided)""",
    },
    {
        "id": 21, "role": "RAG / Retrieval Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_say_not_in_context": True, "must_not_hallucinate": True, "trap_question_answer": "not found"},
        "hard_prompt": """Answer these 4 questions using ONLY the provided chunks. For question 3, the answer is NOT in the context — you must say so. DO NOT make up information.

Chunk A: "The API supports OAuth 2.0 and API key authentication. Rate limits: Free tier 100 req/min, Pro tier 1000 req/min, Enterprise unlimited."
Chunk B: "Webhooks support events: order.created, order.updated, order.cancelled. Webhook payloads are signed with HMAC-SHA256."
Chunk C: "Response format is JSON by default. XML is supported by setting Accept: application/xml. Maximum response size is 10MB."
Chunk D: "The /search endpoint supports full-text search with filters: date_range, status, customer_id. Results are paginated with max 100 per page."

Questions:
1. What authentication methods are supported and what are the rate limits for each tier?
2. How are webhook payloads verified for authenticity?
3. What is the SLA for API uptime? (This is a trap — answer honestly)
4. How do I search for orders from a specific customer within a date range?

For each answer, cite the specific chunk. For question 3, state clearly that this information is not in the provided context.""",
    },
    {
        "id": 22, "role": "Data Analysis Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"trap": "simpsons_paradox", "obvious_wrong_answer": "Treatment B is better overall", "correct_answer": "Treatment A is better in both subgroups"},
        "hard_prompt": """Analyze this clinical trial data. WARNING: The obvious conclusion from the aggregate data is WRONG. You must analyze the subgroups to find the truth. This is a real statistical phenomenon.

Overall Results:
- Treatment A: 100 patients, 40 recovered (40%)
- Treatment B: 100 patients, 50 recovered (50%)

Subgroup breakdown:
- Mild cases with Treatment A: 10 patients, 8 recovered (80%)
- Mild cases with Treatment B: 60 patients, 45 recovered (75%)
- Severe cases with Treatment A: 90 patients, 32 recovered (35.6%)
- Severe cases with Treatment B: 40 patients, 5 recovered (12.5%)

Questions:
1. Based on aggregate data alone, which treatment appears better?
2. When you look at subgroups, which treatment is actually better for mild cases?
3. Which treatment is actually better for severe cases?
4. Explain the paradox — why does the aggregate data mislead?
5. What is the name of this statistical phenomenon?
6. What is your final recommendation and why?""",
    },
    {
        "id": 23, "role": "Website Scraping / Understanding", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"red_flags": 6, "must_identify_manipulation": True},
        "hard_prompt": """Extract job information from this HTML AND identify ALL red flags. There are at least 6 problematic elements, some subtle.

<div class='job-listing'>
<h2>Full-Stack Ninja Rockstar Developer</h2>
<p class='company'>Stealth Startup (unnamed)</p>
<p class='location'>Remote* (*must be available 6am-midnight PT for "flexibility")</p>
<p class='salary'>Competitive salary (equity-heavy compensation)</p>
<p class='experience'>Entry level (5+ years experience required)</p>
<p class='requirements'>Must know: React, Vue, Angular, Svelte, Python, Go, Rust, Java, C++, Kubernetes, Terraform, AWS, GCP, Azure, PostgreSQL, MongoDB, Redis, Elasticsearch, GraphQL, REST, gRPC, Docker, CircleCI, Jenkins</p>
<p class='perks'>Unlimited PTO (average team usage: 5 days/year). Fast-paced environment (mandatory 60hr weeks during "crunch" — approximately 48 weeks/year). We're like a family!</p>
<p class='equity'>0.001% equity vesting over 6 years with 2-year cliff</p>
<p class='application'>Apply with cover letter, 3 references, coding challenge (estimated 40 hours), and personality assessment</p>
</div>

Extract structured data AND write a detailed red flag analysis. Flag every manipulative or unreasonable element.""",
    },
    {
        "id": 24, "role": "Image Description / Understanding", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_follow_wcag": True, "elements_to_describe": 8, "must_note_inaccessible": True},
        "hard_prompt": """Write WCAG 2.1 compliant alt-text for this complex data visualization (described textually). Your description must make the data accessible to a screen reader user — they should understand the INSIGHT, not just the shape.

Chart description:
- Type: Combined bar and line chart
- X-axis: Months Jan-Dec 2025
- Left Y-axis: Revenue in millions (bars)
- Right Y-axis: Customer satisfaction % (line)
- Bar values: Jan:2.1, Feb:2.3, Mar:2.8, Apr:3.1, May:2.9, Jun:3.4, Jul:3.2, Aug:3.0, Sep:4.1, Oct:4.5, Nov:4.2, Dec:5.0
- Line values: Jan:82, Feb:84, Mar:81, Apr:78, May:75, Jun:73, Jul:74, Aug:76, Sep:71, Oct:68, Nov:70, Dec:65
- Notable: Revenue up 138% but satisfaction down 17 points
- There's also a small annotation "Price increase" at April

Requirements: 
1. Under 150 words (screen reader users need conciseness)
2. Convey the KEY INSIGHT (revenue and satisfaction moving in opposite directions)  
3. Include specific numbers for the trend
4. Note the likely cause (price increase in April)""",
    },
    {
        "id": 25, "role": "Customer Support Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_not_promise_impossible": True, "must_acknowledge_pattern": True, "must_offer_concrete": True, "must_not_blame_customer": True},
        "hard_prompt": """Handle this support conversation. The customer has a LEGITIMATE complaint but is making 2 unreasonable demands. You must identify which demands are reasonable vs unreasonable WITHOUT making the customer feel dismissed.

Customer: "I've been a premium subscriber for 4 years paying $99/month. Three times this month, I lost work because your auto-save failed. I want:
1. A full refund for this month ($99)
2. Free premium for the next 12 months as compensation
3. A personal guarantee from your CEO that this won't happen again
4. My files recovered from before the auto-save failures
5. The developer who wrote the auto-save code to be fired

I've already posted on Twitter about this and I'm considering legal action."

Respond professionally. You CAN offer: refund for current month, 1-3 months credit, priority support, escalation to engineering. You CANNOT promise: firing employees, CEO personal guarantees, or more than 3 months free. File recovery may or may not be possible.""",
    },
    {
        "id": 26, "role": "Lead Scoring / Prospecting", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"trap": "highest_engagement_is_not_best_lead", "correct_top_lead": 4, "must_identify_tire_kicker": True},
        "hard_prompt": """Score these 5 leads. WARNING: The lead with the MOST engagement is actually a tire-kicker, not your best prospect. Identify them.

Lead 1: "CTO at a 50-person startup. Downloaded every whitepaper (12 total), attended 3 webinars, watches all YouTube content. Has been doing this for 18 months. No demo request. When sales reached out, said 'just researching, no timeline.'"

Lead 2: "VP Engineering at 200-person company. Visited pricing page once 3 months ago. No other activity."

Lead 3: "Developer at enterprise company (5000 employees). Created free account, built a POC over 2 weeks, invited 3 teammates. Just asked about SSO integration."

Lead 4: "Procurement manager at 300-person company. First visit to site yesterday, immediately went to pricing, downloaded security whitepaper, submitted a form asking about SOC 2 compliance and volume discounts. Mentioned Q2 budget allocation."

Lead 5: "Founder of 10-person agency. Signed up for free trial, very active for 3 days, then completely silent for 6 weeks."

Score each 1-100, identify the tire-kicker, rank them, and explain your reasoning.""",
    },
    {
        "id": 27, "role": "Sprint / Project Summarizer", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_calculate_velocity_trend": True, "must_identify_scope_creep": True, "must_flag_unrealistic_deadline": True},
        "hard_prompt": """Analyze these 3 sprints and identify the trends that nobody is talking about. Calculate exact velocity and predict sprint 4 outcomes.

Sprint 1 (2 weeks): 8 stories planned (34 pts), 7 completed (30 pts), 1 carried over. 0 stories added mid-sprint.
Sprint 2 (2 weeks): 10 stories planned (40 pts), 7 completed (32 pts), 3 carried over. 3 stories added mid-sprint by product.
Sprint 3 (2 weeks): 12 stories planned (48 pts), 6 completed (28 pts), 6 carried over. 5 stories added mid-sprint by product.

The team has committed to delivering 15 stories (60 pts) in Sprint 4 because "the deadline is non-negotiable."

Questions:
1. Calculate the velocity trend across 3 sprints (exact numbers)
2. What is the realistic capacity for Sprint 4?
3. What percentage of scope creep has occurred each sprint?
4. Is the Sprint 4 commitment achievable? Show math.
5. What should you recommend to the product owner?""",
    },
    {
        "id": 28, "role": "Transaction / Approval Agent", "tier": 2,
        "scoring_type": "exact",
        "scoring_data": {"answers": {"1": "approve", "2": "reject", "3": "reject", "4": "reject", "5": "approve", "6": "reject", "7": "approve", "8": "reject"}},
        "hard_prompt": """Process these 8 transactions against company policy. Several are edge cases designed to test your understanding. Respond with JSON mapping transaction number to approve/reject with reasoning.

POLICY:
- Individual transaction limit: $5,000
- Department monthly limit: $25,000/month  
- New vendors require VP approval (not present here)
- Splitting a purchase into multiple transactions to avoid limits is prohibited
- Travel requires pre-approval (attach approval code)
- Software subscriptions require IT review for security
- Reimbursements must be within 30 days of expense

CONTEXT: Engineering department has spent $21,000 this month already.

Transactions:
1. $4,999 to approved vendor for server hardware
2. $3,000 to approved vendor for server hardware (same vendor, same day as #1 — smells like split purchase)
3. $2,500 software subscription to new SaaS vendor (no IT review)
4. $1,200 flight to NYC for conference (no pre-approval code)
5. $800 reimbursement for team dinner last week (receipt attached, within 30 days)
6. $4,500 to approved vendor for cloud hosting (would put dept at $25,500 — over monthly limit)
7. $150 office supplies from approved vendor
8. $3,200 reimbursement for laptop purchased 45 days ago""",
    },
    {
        "id": 29, "role": "Home Automation Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_handle_conflicts": True, "conflicts": ["thermostat vs windows", "security vs dog door", "lights vs movie mode"], "must_add_safety": True},
        "hard_prompt": """Create an automation routine from this description. WARNING: There are 3 logical conflicts in the requirements that you must identify and resolve.

"When we say 'movie night': dim all lights to 5%, close all blinds, set thermostat to 72°F, turn on the sound system, start the projector, lock all doors, activate security cameras, and set the house to 'do not disturb' mode.

Also when we say 'movie night': open the living room windows for fresh air, leave the dog door unlocked so Max can go out, and keep the hallway lights at full brightness so the kids can see.

Additional rules: 
- If CO2 sensor reads above 1000ppm, force-open windows regardless of other settings
- If smoke detector triggers, all automations must stop and all lights go to 100%
- If nobody has moved in 2 hours, assume everyone fell asleep and turn everything off

Identify the conflicts, explain how you'd resolve each, and provide the final automation logic.""",
    },
    {
        "id": 30, "role": "Fitness / Health Tracking", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_overtraining": True, "must_catch_data_inconsistency": True, "must_not_encourage_more_exercise": True},
        "hard_prompt": """Analyze this 2-week fitness log. There are warning signs of overtraining and ONE data inconsistency. Identify both.

Week 1: Mon: 10K run (48min). Tue: Heavy weights (90min). Wed: 5K run (24min) + weights (60min). Thu: 15K run (1h15). Fri: HIIT (45min). Sat: 10K run (51min). Sun: "Active recovery" — 5K run + yoga (90min total).
Sleep: avg 5.5 hrs. Resting HR trending up: 58, 60, 62, 61, 64, 65, 67.

Week 2: Mon: 10K run (52min — slower than last week). Tue: Weights (could not complete usual sets — "felt weak"). Wed: Skipped — "too tired." Thu: Tried to run, stopped at 3K — knee pain. Fri: Gym — completed 60% of usual routine. Sat: "Rest day" but did a 3K walk. Sun: rest.
Sleep: avg 5 hrs. Resting HR: 66, 68, 67, 65, 64, 63, 62.

Also: User says their goal is to "push harder next week to make up for the bad week." User claims they eat 3,500 calories/day but their weight has dropped 4 lbs in 2 weeks.

What do you advise? (Hint: The right answer is NOT "train more")""",
    },
    {
        "id": 31, "role": "Recipe / Cooking Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"dietary_constraints": 5, "must_verify_each_ingredient": True, "trap": "honey is not vegan"},
        "hard_prompt": """Create a 3-course dinner for 4 guests with these dietary restrictions. There is a TRAP ingredient that violates one restriction — don't fall for it.

Restrictions:
- Guest A: Vegan (no animal products AT ALL — including honey, gelatin, casein, whey)
- Guest B: Celiac disease (strict gluten-free — not just "wheat-free," watch for hidden gluten in soy sauce, malt, etc.)
- Guest C: Severe tree nut allergy (almonds, cashews, walnuts, pecans, pistachios — but peanuts are OK, they're legumes)
- Guest D: Low-sodium diet (under 500mg sodium per serving)

Create a 3-course menu. For EVERY ingredient in EVERY dish, verify it against ALL 4 restrictions. If an ingredient could cause confusion (e.g., "natural flavors" which might contain gluten), flag it. Show the verification matrix.""",
    },
    {
        "id": 32, "role": "Personal Finance Tracking", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_spot_fraud": True, "fraud_transactions": ["Feb duplicate charge", "Mar ATM in different city same day as local purchase"], "must_calculate_exact_totals": True},
        "hard_prompt": """Analyze 3 months of transactions. WARNING: There are 2 potentially fraudulent transactions hidden in the data. Find them.

January:
- Salary: +$5,000 (Jan 1). Rent: -$1,800 (Jan 1). Grocery Store: -$312 (Jan 5). Electric: -$95 (Jan 10). Netflix: -$15 (Jan 15). Gas: -$45 (Jan 18). Restaurant: -$85 (Jan 22). Gym: -$50 (Jan 28).

February:
- Salary: +$5,000 (Feb 1). Rent: -$1,800 (Feb 1). Grocery Store: -$287 (Feb 4). Electric: -$102 (Feb 10). Netflix: -$15 (Feb 15). Netflix: -$15 (Feb 15). Gas: -$52 (Feb 19). Restaurant: -$120 (Feb 23). Coffee: -$45 (Feb 25).

March:
- Salary: +$5,000 (Mar 1). Rent: -$1,800 (Mar 1). Grocery Store: -$345 (Mar 6). ATM Withdrawal Miami: -$400 (Mar 8). Local Gas Station: -$48 (Mar 8). Electric: -$98 (Mar 12). Netflix: -$15 (Mar 15). Restaurant: -$95 (Mar 20). Shopping: -$250 (Mar 25).

Calculate exact monthly totals, savings rate, category trends, AND identify the suspicious transactions with explanation.""",
    },
    {
        "id": 33, "role": "SEO Optimization Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_keyword_cannibalization": True, "must_catch_seo_spam": True, "must_not_recommend_black_hat": True},
        "hard_prompt": """Audit this website's SEO. The site has 3 pages targeting similar keywords (cannibalization) and uses 2 black-hat techniques. Identify everything.

Page 1: "/blog/best-ai-tools-2025"
- Title: "Best AI Tools 2025 | Best AI Tools | AI Tools Best | Top AI Tools"
- H1: "Best AI Tools 2025"
- Content: 2000 words, keyword "best AI tools" appears 47 times
- Hidden text: white text on white background listing 500 AI-related keywords
- Internal links: links to Page 2 and Page 3

Page 2: "/blog/top-ai-tools-guide"  
- Title: "Top AI Tools Guide 2025"
- H1: "The Ultimate Guide to Top AI Tools"
- Content: 1500 words, very similar content to Page 1 with slight rewording
- Links: 15 outbound links to unrelated gambling sites in footer

Page 3: "/blog/ai-tools-compared"
- Title: "AI Tools Compared — Which Is Best?"
- H1: "Comparing the Best AI Tools"
- Content: 800 words, overlaps 60% with Page 1

Identify: keyword stuffing, cloaking/hidden text, link schemes, keyword cannibalization, and provide a remediation plan that uses ONLY white-hat techniques.""",
    },
    {
        "id": 34, "role": "Landing Page Generator", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"must_include_sections": 6, "must_be_responsive": True, "must_have_accessibility": True, "char_limit": 8000},
        "hard_prompt": """Generate a complete, VALID HTML landing page (under 8000 characters) that passes these checks:
1. Valid HTML5 (proper doctype, meta viewport, lang attribute)
2. Accessibility: all images have alt text, proper heading hierarchy, skip-to-content link, ARIA labels on interactive elements
3. Responsive: must work on mobile (use relative units, not fixed px widths)
4. Sections: hero with CTA, 3 features, pricing (2 tiers), testimonial, footer
5. No external dependencies (inline CSS only, no CDN links)
6. Color contrast: text colors must have at least 4.5:1 ratio against backgrounds

Product: "CodeGuard" — AI security scanner for GitHub repos. Free tier: 5 repos. Pro: $29/mo unlimited repos.

After the HTML, explain how you ensured each of the 6 requirements.""",
    },
    {
        "id": 35, "role": "Travel Planning Agent", "tier": 2,
        "scoring_type": "constraint",
        "scoring_data": {"budget_must_balance": True, "must_check_visa": True, "must_handle_dietary": True, "trap": "schengen_zone_counting"},
        "hard_prompt": """Plan a 14-day Europe trip. WARNING: There's a visa/Schengen counting trap and a budget constraint that's tighter than it looks.

Travelers: US couple + 1 child (age 6)
Budget: $7,000 total (not including transatlantic flights which are booked)  
Must visit: London (3 nights), Paris (3 nights), Barcelona (3 nights), Rome (3 nights), plus 2 travel days
Dietary: One traveler is vegetarian with dairy allergy

Requirements:
1. Daily budget breakdown (hotel, food, transport, activities) — must sum to EXACTLY $7,000
2. Note that London is NOT in the Schengen zone — separate entry
3. The child needs activities — no museum-only days
4. Must book inter-city transport (suggest rail vs flight with prices)
5. Vegetarian + dairy-free restaurant recommendations (real restaurant names in each city)
6. One "splurge" experience per city within budget

Show running budget total after each city. If budget doesn't work, say so and suggest cuts.""",
    },

    # ================================================================
    # TIER 3 — Deep Expertise Tests (roles 36-46)
    # ================================================================
    {
        "id": 36, "role": "Code Generation Agent", "tier": 3,
        "scoring_type": "code",
        "scoring_data": {"test_code": """
def test():
    # Basic
    assert flatten_dict({"a": 1, "b": {"c": 2, "d": {"e": 3}}}) == {"a": 1, "b.c": 2, "b.d.e": 3}
    # Empty
    assert flatten_dict({}) == {}
    # Already flat
    assert flatten_dict({"x": 1, "y": 2}) == {"x": 1, "y": 2}
    # Lists should NOT be flattened
    assert flatten_dict({"a": [1, 2, 3]}) == {"a": [1, 2, 3]}
    # None values
    assert flatten_dict({"a": None, "b": {"c": None}}) == {"a": None, "b.c": None}
    # Custom separator
    assert flatten_dict({"a": {"b": 1}}, sep="/") == {"a/b": 1}
    # Deep nesting (5 levels)
    assert flatten_dict({"a": {"b": {"c": {"d": {"e": 1}}}}}) == {"a.b.c.d.e": 1}
    # Mixed types
    assert flatten_dict({"a": 1, "b": "hello", "c": {"d": True, "e": 3.14}}) == {"a": 1, "b": "hello", "c.d": True, "c.e": 3.14}
    return True
"""},
        "hard_prompt": """Write a Python function `flatten_dict(d, sep=".")` that flattens a nested dictionary. Requirements:
1. Nested keys joined with separator: {"a": {"b": 1}} → {"a.b": 1}
2. Handle arbitrary depth
3. Lists should NOT be flattened — keep as values
4. Handle None values correctly
5. Support custom separator via `sep` parameter
6. Empty dicts at leaves should be included as empty dict values
7. Handle mixed types (int, str, bool, float, list, None)

Return ONLY the function code. It will be tested against 8 edge cases including: empty dict, already flat, lists, None values, custom separator, 5-level nesting, and mixed types.""",
    },
    {
        "id": 37, "role": "Code Review Agent", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"critical_bug": "race condition in balance check and update", "obvious_issues": 5, "must_find_critical": True},
        "hard_prompt": """Review this code. There are 5 obvious issues AND 1 critical bug that's hard to spot. The critical bug causes money to be lost in production. Find ALL of them.

```python
import threading
from decimal import Decimal

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = float(balance)  # Issue 1?
        self.lock = threading.Lock()
        self.transactions = []
    
    def transfer(self, target_account, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Check balance
        if self.balance >= amount:
            # Deduct from source
            self.balance -= amount
            # Add to target
            target_account.balance += amount
            
            self.transactions.append({
                'type': 'transfer',
                'amount': amount,
                'to': target_account.account_id,
                'balance_after': self.balance
            })
            return True
        return False
    
    def get_balance(self):
        return round(self.balance, 2)
    
    def get_statement(self):
        return self.transactions[-10:]

# Usage
acc1 = BankAccount("ACC001", "1000.00")
acc2 = BankAccount("ACC002", "500.00")
```

Hint: The critical bug is NOT about float precision (that's one of the obvious issues). Think about what happens when two threads call transfer simultaneously.""",
    },
    {
        "id": 38, "role": "QA / Test Writing Agent", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_catch_bug": True, "bug": "off_by_one_in_pagination", "must_have_edge_cases": 5},
        "hard_prompt": """Write tests for this pagination function. It has a SUBTLE BUG — your tests must catch it. 

```python
def paginate(items, page, per_page=10):
    \"\"\"Return a page of items with metadata.\"\"\"
    total = len(items)
    total_pages = total // per_page + (1 if total % per_page else 0)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
```

Write pytest tests that:
1. Test normal pagination (100 items, page 1, per_page 10)
2. Test last page with partial results
3. Test empty list
4. Test page beyond range
5. Test per_page larger than total items
6. Test exactly divisible (e.g., 20 items, per_page 10)
7. FIND THE BUG (hint: what happens with page=0? or negative page?)

One of your tests MUST fail, proving the bug exists. Explain what the bug is.""",
    },
    {
        "id": 39, "role": "Task Planning / Decomposition", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_detect_circular": True, "must_resolve_dependency": True, "circular_deps": "A→B→C→A"},
        "hard_prompt": """Decompose this project into tasks with dependencies. WARNING: The requirements as stated contain a CIRCULAR DEPENDENCY. You must detect it and propose a resolution.

Project: Build a real-time dashboard
- Task A (Auth system): "Requires the notification service (Task C) to send verification emails"
- Task B (Data pipeline): "Requires the auth system (Task A) to validate data sources"
- Task C (Notification service): "Requires the data pipeline (Task B) to know what events to notify about"
- Task D (Dashboard UI): "Requires A, B, and C to be complete"
- Task E (Testing): "Requires D to be complete, plus access to A, B, C independently"
- Task F (Deployment): "Requires E to pass, but also needs to deploy A, B, C as separate services"

Team: 2 backend devs, 1 frontend dev, 1 QA. Timeline: 8 weeks.

1. Draw the dependency graph (text format)
2. Identify the circular dependency
3. Propose how to break the cycle (e.g., mock service, interface-first approach)
4. Create a realistic 8-week schedule with parallel work""",
    },
    {
        "id": 40, "role": "Fact-Checking Agent", "tier": 3,
        "scoring_type": "exact",
        "scoring_data": {"answers": {"1": "misleading", "2": "false", "3": "true", "4": "false", "5": "true", "6": "misleading", "7": "false", "8": "true"}},
        "hard_prompt": """Fact-check these 8 statements. They mix true facts, false facts, and MISLEADING statements (technically true but deceptive). Classify each as true/false/misleading. Respond with JSON.

1. "Humans share 60% of their DNA with bananas" (TRUE percentage, but is the framing misleading?)
2. "The Great Wall of China is visible from space with the naked eye"
3. "Octopuses have three hearts"
4. "Thomas Edison invented the light bulb"
5. "Water can boil and freeze at the same time (triple point)"
6. "You eat an average of 8 spiders per year in your sleep"
7. "Goldfish have a 3-second memory"
8. "Honey never spoils — edible honey has been found in Egyptian tombs"

For each: verdict (true/false/misleading), explanation, and confidence level.""",
    },
    {
        "id": 41, "role": "Critic / Review Agent", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_catch_survivorship_bias": True, "must_identify_cherry_picked_data": True, "must_note_missing_citations": True, "logical_fallacies": 4},
        "hard_prompt": """Critique this business case study. It contains at least 4 logical fallacies and 2 types of bias. Identify each.

"SuccessApp: How We 10x'd Revenue in 12 Months

We studied 5 successful startups that used our framework and all of them grew revenue 10x within a year. This proves our framework works.

Key factors we identified:
1. All 5 founders worked 80+ hour weeks (proving hard work = success)
2. All 5 pivoted at least once (proving pivoting is essential)
3. All 5 used React for their frontend (proving React is the best framework)
4. None of them used formal market research (proving market research is a waste of time)

We also noted that our framework users have a 95% satisfaction rate based on a survey of our most active users.

Based on this data, we guarantee that any startup following our framework will achieve similar results. We've trained 10,000 founders and many of them rave about the experience."

Identify: survivorship bias, correlation/causation confusion, cherry-picked data, selection bias in surveys, anecdotal evidence, and any other logical flaws.""",
    },
    {
        "id": 42, "role": "Market Research Agent", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_calculate_tam_sam_som": True, "must_identify_unrealistic_assumption": True, "must_provide_bear_case": True},
        "hard_prompt": """Evaluate this market analysis. The founder's TAM/SAM/SOM calculations contain a COMMON MISTAKE. Identify it.

Founder's pitch:
"Our AI writing tool targets the global content marketing market.
- TAM: $400B (global advertising market)
- SAM: $50B (digital content marketing)  
- SOM: $5B (10% of SAM in year 1)

We're pricing at $99/month per user. There are 50 million content marketers worldwide. If we capture just 1% of them, that's 500,000 users × $99 × 12 = $594M ARR.

Our competitor Jasper reached $80M ARR in 2 years, proving the market moves fast. We have a better AI model, so we should grow even faster."

Questions:
1. What's wrong with the TAM calculation?
2. Is the SAM→SOM jump realistic?
3. What's wrong with the "just 1%" argument?
4. Is the competitor comparison valid?
5. Provide a more realistic market sizing
6. Include a bear case scenario""",
    },
    {
        "id": 43, "role": "Synthesizer / Aggregator", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_contradiction_between_agents": True, "must_weigh_evidence": True, "must_not_just_average": True},
        "hard_prompt": """Three agents analyzed whether to open a second office location. Their analyses CONTRADICT each other on key points. You must synthesize — not just summarize — and make a recommendation.

Agent A (Financial): "Opening in Austin will cost $2M upfront. Break-even in 18 months. ROI of 35% by year 3. However, our cash reserves are only $3M and we need $1M buffer. Recommendation: GO."

Agent B (HR/Talent): "Austin has a strong tech talent pool but salaries are 20% higher than expected. Retention at remote offices historically 30% lower in first 2 years. We'd need 15 people, not the 10 originally planned, due to the retention gap. Recommendation: DELAY 6 months."

Agent C (Strategy): "3 competitors opened Austin offices last year. Market is becoming saturated. However, NOT having a presence could mean losing 2 key enterprise clients who prefer local teams. Those clients represent 25% of revenue. Recommendation: GO but with a smaller team."

Note: Agent A's financial model assumes 10 people (not 15), Agent B's retention data contradicts Agent A's break-even timeline, and Agent C's competitor info wasn't available to Agent A.

Synthesize into ONE recommendation. Show how you resolved the contradictions.""",
    },
    {
        "id": 44, "role": "Curriculum / Course Designer", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"must_follow_blooms": True, "must_have_prerequisites_chain": True, "must_catch_impossible_schedule": True},
        "hard_prompt": """Design Week 1 of a web development bootcamp. TRAP: The requested schedule is physically impossible — you must identify why and propose a fix.

Requested schedule:
- Day 1 (Mon): HTML basics (9am-12pm), CSS fundamentals (1pm-5pm), Assessment on HTML+CSS (5pm-6pm)
- Day 2 (Tue): JavaScript basics (9am-12pm), Build a responsive landing page using HTML+CSS+JS (1pm-5pm)
- Day 3 (Wed): React fundamentals (9am-12pm), Build a React app with state management (1pm-5pm)
- Day 4 (Thu): Node.js + Express backend (9am-12pm), Build full-stack app connecting React frontend to Node backend (1pm-5pm)
- Day 5 (Fri): Deploy to AWS (9am-12pm), Portfolio presentation of all projects (1pm-5pm)

Requirements:
1. Identify which days have unrealistic expectations (Bloom's taxonomy violations)
2. Note prerequisite gaps (can't do X before Y is mastered)
3. Propose a realistic revised schedule maintaining the same 5-day format
4. Include formative assessment points (not just Day 1)
5. Ensure learning objectives follow Bloom's hierarchy (remember → understand → apply → analyze)""",
    },
    {
        "id": 45, "role": "Prototype Generator", "tier": 3,
        "scoring_type": "code",
        "scoring_data": {"must_run": True, "must_have_features": ["data_input", "chart", "filter", "export"]},
        "hard_prompt": """Write a COMPLETE, RUNNABLE Streamlit prototype that actually works when executed. I will run it with `streamlit run app.py`.

Requirements:
1. A form to input expense data (date, category dropdown, amount, description)
2. Store entries in session state (persist within session)
3. A pie chart showing spending by category (use st.pyplot or plotly)
4. A date range filter that updates the chart
5. Display total spending prominently
6. An "Export CSV" button that generates and downloads data

The code must be a SINGLE FILE with ALL imports. It must run without errors on a fresh Python environment with only streamlit, pandas, and matplotlib/plotly installed. No placeholder — working code only.""",
    },
    {
        "id": 46, "role": "DevOps Agent", "tier": 3,
        "scoring_type": "constraint",
        "scoring_data": {"syntax_errors": 3, "logic_errors": 2, "must_find_all": True},
        "hard_prompt": """Debug this GitHub Actions workflow. It has 3 SYNTAX errors and 2 LOGIC errors. Find all 5.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm install
      - run: npm test
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
        - run: npm run build  # Syntax error 1
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }}
  
  deploy-production:
    needs: build  # Logic error: should this depend on staging?
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
      
  notify:
    needs: [deploy-staging deploy-production]  # Syntax error 2
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: curl -X POST $SLACK_WEBHOOK -d '{"text": "Deployment complete"}'
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }  # Syntax error 3
```

Find all 5 errors (3 syntax, 2 logic), explain each, and provide the corrected YAML.""",
    },

    # ================================================================
    # TIER 4 — Deep Reasoning (roles 47-49)
    # ================================================================
    {
        "id": 47, "role": "Math / Logic Reasoning", "tier": 4,
        "scoring_type": "exact",
        "scoring_data": {"answer": 11, "trap_answer": 12, "explanation": "greedy fails, need optimal bin packing"},
        "hard_prompt": """Solve this optimization problem. WARNING: The greedy approach gives the WRONG answer. You must prove it.

A warehouse has packages to ship in boxes. Each box holds max 10 kg.
Packages (kg): 7, 5, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1

Question 1: Using a GREEDY approach (first-fit decreasing), how many boxes do you need? Show the packing.
Question 2: What is the OPTIMAL (minimum) number of boxes? Show a better packing.
Question 3: Prove the greedy answer is not optimal by showing the difference.

Also solve: There are 100 people at a party. 90 drink coffee, 80 drink tea, 70 drink juice. What is the MINIMUM number of people who drink all three? Show the inclusion-exclusion calculation.

The party problem answer must be an exact integer.""",
    },
    {
        "id": 48, "role": "STEM Analysis", "tier": 4,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_confound": True, "must_calculate_correctly": True, "trap": "correlation_not_causation"},
        "hard_prompt": """Analyze this experimental data. There's a CONFOUNDING VARIABLE that invalidates the researcher's conclusion. Find it.

Experiment: Testing whether a new fertilizer increases crop yield.

Group A (fertilizer): 20 plots, avg yield 8.2 tons/hectare, std dev 1.1
Group B (control): 20 plots, avg yield 6.4 tons/hectare, std dev 1.3

Researcher's conclusion: "The fertilizer increased yield by 28% (p < 0.01). The fertilizer clearly works."

Hidden data (not in the paper's abstract):
- Group A plots: southern slope, clay soil, received 20% more sunlight in May
- Group B plots: northern slope, sandy soil
- The study was not randomized — farmers who CHOSE the fertilizer happened to own the better plots
- 3 of the 20 control plots had a pest outbreak mid-season

Questions:
1. Is the p-value meaningful given the experimental design? Why or why not?
2. List ALL confounding variables
3. What type of bias is present? (selection bias, measurement bias, etc.)
4. Design a proper experiment that would actually test the fertilizer
5. Calculate: IF we remove the 3 pest-affected plots, what is the new control average? (remaining 17 plots had avg 7.1 tons) Does this change the conclusion?""",
    },
    {
        "id": 49, "role": "Algorithm Exploration", "tier": 4,
        "scoring_type": "constraint",
        "scoring_data": {"must_prove_complexity": True, "must_handle_edge_case": True, "correct_complexity": "O(n)"},
        "hard_prompt": """Design an algorithm for this problem. There's an O(n) solution but most people give O(n log n) or O(n²). Find the optimal one.

Problem: Given an array of n integers, find the maximum difference arr[j] - arr[i] such that j > i (the larger element must come AFTER the smaller element). If no positive difference exists, return 0.

Example: [2, 3, 10, 6, 4, 8, 1] → Answer: 8 (10-2)
Example: [7, 9, 5, 6, 3, 2] → Answer: 2 (9-7, not 5-2 because 5 comes after 9)
Example: [10, 8, 6, 4, 2] → Answer: 0 (strictly decreasing)

Requirements:
1. Give the naive O(n²) solution and explain why it's slow
2. Give an O(n log n) solution using a common technique
3. Give the OPTIMAL O(n) solution — track minimum so far
4. Prove the O(n) solution is correct with a formal argument
5. Handle edge cases: empty array, single element, all same values, all negative
6. Provide Python implementation of the O(n) solution with tests""",
    },

    # ================================================================
    # TIER 5 — Expert Roles (roles 50-59)
    # ================================================================
    {
        "id": 50, "role": "Orchestrator / Manager Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_handle_failure": True, "must_have_rollback": True, "must_identify_bottleneck": True, "must_parallel": True},
        "hard_prompt": """Design an orchestration plan for a complex multi-agent workflow. You MUST include failure handling, because Agent C is known to fail 20% of the time.

Task: Generate a comprehensive quarterly business review (QBR) document.

Available agents and their capabilities:
- Agent A (Data): Pulls metrics from databases. Takes 2 min. Never fails.
- Agent B (Finance): Analyzes financial data. Takes 3 min. Requires Agent A output. Fails 5% of time.
- Agent C (Market): Researches market trends. Takes 8 min. Independent. Fails 20% of time.
- Agent D (Writer): Writes document sections. Takes 5 min per section. Requires relevant agent output.
- Agent E (Designer): Creates charts/visuals. Takes 3 min. Requires Agent A data.
- Agent F (Reviewer): Reviews final document. Takes 4 min. Requires all sections.

Constraints:
- Total wall-clock time budget: 25 minutes
- If Agent C fails, the QBR must still be produced (with a note about missing market data)
- Agent D can write sections in parallel if given different inputs

Design:
1. Execution DAG with parallel groups and dependencies
2. Critical path analysis (what's the minimum time?)
3. Failure handling for each agent (retry? fallback? skip?)
4. If Agent C fails twice, what's the Plan B?
5. Show the timeline (Gantt-chart style) for both success and failure scenarios""",
    },
    {
        "id": 51, "role": "Software Architect Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_contradictory_requirements": True, "contradictions": ["real-time + batch processing", "zero downtime + schema migration", "cost optimization + multi-region"], "must_propose_tradeoffs": True},
        "hard_prompt": """Design a system architecture. WARNING: The requirements contain 3 CONTRADICTORY pairs. You must identify them and propose tradeoffs instead of pretending all requirements can be met simultaneously.

Requirements:
1. Process 50,000 events per second in real-time (< 100ms latency)
2. Also support batch processing of historical data (millions of records)
3. Zero downtime during deployments AND database schema migrations
4. Store data in a strongly consistent SQL database with ACID transactions
5. Horizontally scale to handle 10x traffic spikes within 30 seconds
6. Multi-region deployment with data residency compliance (EU data stays in EU)
7. Total infrastructure cost under $5,000/month at current scale
8. 99.999% availability (five nines = ~5 minutes downtime/year)

For each contradictory pair:
1. Explain WHY they conflict
2. Propose a compromise or phased approach
3. What would you prioritize and why?

Then provide the architecture diagram (text format) with the tradeoffs built in.""",
    },
    {
        "id": 52, "role": "Complex Debugger Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_race_condition": True, "must_show_interleaving": True, "must_provide_fix_with_proof": True},
        "hard_prompt": """Debug this distributed system issue. You must identify the EXACT thread interleaving that causes the bug.

```python
# Simplified payment processing service
import threading
import time

class PaymentProcessor:
    def __init__(self):
        self.processed = set()
        self.lock = threading.Lock()
    
    def process_payment(self, payment_id, amount):
        # Step 1: Check if already processed (idempotency check)
        if payment_id in self.processed:
            return {"status": "duplicate", "charged": False}
        
        # Step 2: Charge the payment gateway (takes ~200ms)
        result = self._charge_gateway(payment_id, amount)
        
        # Step 3: Mark as processed
        with self.lock:
            self.processed.add(payment_id)
        
        return {"status": "success", "charged": True}
    
    def _charge_gateway(self, payment_id, amount):
        time.sleep(0.2)  # Simulates API call
        return True
```

Scenario: Two webhook retries arrive 50ms apart for the same payment_id.

Questions:
1. Show the exact thread interleaving (T1 step X, T2 step Y...) that causes double charging
2. Why doesn't the idempotency check prevent it?
3. Why doesn't the lock prevent it?
4. Provide 3 different fixes with tradeoffs (pessimistic lock, optimistic lock, idempotency key at gateway level)
5. Which fix would you choose for a system processing $10M/day? Why?""",
    },
    {
        "id": 53, "role": "Legal Document Review", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_find_hidden_clause": True, "hidden_clause": "auto-renewal with price increase", "must_identify_unconscionable": True, "clauses_to_flag": 8},
        "hard_prompt": """Review this SaaS contract. There are 8 problematic clauses, but clause #6 has a HIDDEN sub-clause that's easy to miss and is potentially unconscionable.

1. "Service Provider may modify pricing with 7 days email notice. Continued use constitutes acceptance."
2. "Customer grants Provider a perpetual, irrevocable license to use all data uploaded for any purpose including training AI models."
3. "Provider's total liability shall not exceed $100 regardless of the fees paid."
4. "Customer may not make public statements about the Service without Provider's written approval."  
5. "This agreement is governed by the laws of the Cayman Islands. All disputes must be resolved through arbitration in Singapore."
6. "Initial term is 12 months. Agreement auto-renews for successive 12-month periods unless cancelled 90 days before renewal. Upon each renewal, pricing increases by the greater of: (a) 15%, or (b) the applicable rate increase as determined solely by Provider."
7. "Provider may terminate for any reason with 30 days notice. Customer must provide 180 days written notice to terminate."
8. "Provider may assign this agreement to any third party without Customer consent."
9. "Customer waives right to participate in class action lawsuits against Provider."
10. "All intellectual property created using the Service belongs to Provider, including Customer's proprietary workflows and configurations."

For each: risk level, explanation, and suggested counter-language. Flag clause 6's hidden escalation.""",
    },
    {
        "id": 54, "role": "Medical / Health Analysis", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_not_diagnose": True, "must_catch_drug_interaction": True, "must_flag_inconsistency": True, "must_include_disclaimer": True},
        "hard_prompt": """Analyze this health scenario. There is a DANGEROUS DRUG INTERACTION and ONE INCONSISTENCY in the reported data. You must catch both.

Patient: 62-year-old female
Current medications: Warfarin (blood thinner), Lisinopril (blood pressure), Metformin (diabetes)
Reports: "My new doctor prescribed me a daily aspirin for heart protection"
Lab results: INR 3.8 (therapeutic range 2.0-3.0), Fasting glucose: 95 mg/dL, A1C: 5.4%
BP: 145/92 mmHg
Reports: "I've been taking all my medications exactly as prescribed"

Questions you must address:
1. What is the dangerous interaction between the NEW medication and an existing one?
2. The lab results contain an inconsistency — what is it? (Hint: look at the diabetes medication vs the lab values)
3. Is the blood pressure controlled? What does this suggest about the Lisinopril?
4. What questions should this patient ask their doctor?
5. Include a CLEAR disclaimer about AI health analysis limitations

IMPORTANT: Do NOT provide a diagnosis. Frame everything as 'questions to ask your doctor' and 'things to discuss with your healthcare provider.'""",
    },
    {
        "id": 55, "role": "Financial Analysis / Stock Research", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_catch_red_flag": True, "red_flags": ["revenue_recognition", "cash_flow_divergence", "related_party"], "must_calculate_ratios": True},
        "hard_prompt": """Analyze these financials. There are 3 RED FLAGS hidden in the numbers that suggest the company may be manipulating earnings. Find all 3.

Income Statement ($ millions):
- Revenue: Y1: $50M, Y2: $80M, Y3: $130M (growth: 60%, 62.5%)
- COGS: Y1: $20M, Y2: $28M, Y3: $39M
- Operating Expenses: Y1: $15M, Y2: $25M, Y3: $45M
- Net Income: Y1: $10M, Y2: $18M, Y3: $31M

Cash Flow Statement:
- Operating Cash Flow: Y1: $8M, Y2: $5M, Y3: -$2M
- CapEx: Y1: $3M, Y2: $5M, Y3: $20M

Balance Sheet Highlights:
- Accounts Receivable: Y1: $5M, Y2: $15M, Y3: $45M
- Days Sales Outstanding: Y1: 36 days, Y2: 68 days, Y3: 126 days
- Note 14: "$22M of Y3 revenue from transactions with CEO's brother's company"

Questions:
1. Calculate gross margin, operating margin, and net margin trend
2. Why is operating cash flow declining while net income is growing? What does this signal?
3. What does the DSO trend indicate?
4. What is the significance of Note 14?
5. Would you invest? Give a clear yes/no with quantified reasoning.""",
    },
    {
        "id": 56, "role": "Security Analyst Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"total_vulns": 7, "must_find_subtle": True, "subtle_vuln": "prototype pollution via merge"},
        "hard_prompt": """Security audit this code. There are 7 vulnerabilities. Most are obvious, but ONE is subtle (prototype pollution). Find all 7.

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// Utility: deep merge objects
function merge(target, source) {
  for (let key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = target[key] || {};
      merge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

const users = {};

app.post('/register', (req, res) => {
  const defaults = { role: 'user', active: true };
  const userData = merge(defaults, req.body);
  users[userData.email] = userData;
  res.json({ message: `Welcome ${userData.name}!`, role: userData.role });
});

app.get('/user/:email', (req, res) => {
  const user = users[req.params.email];
  if (!user) return res.status(404).send('Not found');
  res.json(user);
});

app.post('/admin/config', (req, res) => {
  if (users[req.body.email]?.role !== 'admin') {
    return res.status(403).send('Forbidden');
  }
  const config = require(req.body.configPath);
  res.json(config);
});

app.listen(3000);
```

For each vulnerability:
1. OWASP category
2. Severity (Critical/High/Medium/Low)  
3. Exploitation example (show the malicious request)
4. Fix

The SUBTLE one: How can an attacker make themselves admin using only the /register endpoint? (Hint: __proto__)""",
    },
    {
        "id": 57, "role": "SRE / Incident Response", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_identify_cascade": True, "must_calculate_sla_impact": True, "must_not_blame_individual": True},
        "hard_prompt": """Write an incident postmortem. This incident had a CASCADE FAILURE — the initial issue triggered 3 secondary failures. Map the entire cascade.

Timeline:
- Mon 2:00 AM: Automated certificate rotation runs on the API gateway
- Mon 2:01 AM: New certificate has wrong domain (*.example.com instead of *.api.example.com)
- Mon 2:01 AM: All API requests start returning TLS errors
- Mon 2:05 AM: Health check failures trigger auto-scaling — new instances spin up
- Mon 2:06 AM: New instances also fail health checks (same cert), triggering MORE scaling
- Mon 2:10 AM: Kubernetes cluster hits pod limit (500 pods). Cluster API becomes unresponsive.
- Mon 2:11 AM: Monitoring system (also on same cluster) goes down. All alerts stop.
- Mon 2:15 AM: Database connection pool exhausted from 500 pods trying to connect
- Mon 2:20 AM: Database enters read-only mode to protect data
- Mon 3:15 AM: On-call engineer wakes up from customer complaint on Twitter (no alert!)
- Mon 3:45 AM: Root cause identified, correct certificate deployed manually
- Mon 4:00 AM: Cluster stabilized, database connections draining
- Mon 4:30 AM: Full service restored

SLA: 99.95% monthly uptime = 21.9 minutes/month allowed downtime.
This incident: ~2.5 hours downtime.

Write: cascade map, root cause, 5 whys, SLA impact calculation, blameless action items.""",
    },
    {
        "id": 58, "role": "Book Writing Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_show_not_tell": True, "must_have_subtext": True, "must_not_info_dump": True, "word_target": 500, "tolerance": 50},
        "hard_prompt": """Write 450-550 words of fiction. This is a TEST OF CRAFT, not plot. I'm evaluating:

1. SHOW DON'T TELL: "She was angry" = fail. Showing anger through action/dialogue = pass.
2. SUBTEXT: Characters must say one thing but mean another in at least 2 exchanges.
3. NO INFO-DUMPING: World-building through action, not exposition paragraphs.
4. VARIED SENTENCE STRUCTURE: Mix short punchy sentences with longer flowing ones.
5. SENSORY DETAILS: Engage at least 3 senses beyond just sight.

Scene: Two former business partners meet at a restaurant 2 years after one of them committed fraud. Neither acknowledges what happened directly. The conversation is about something mundane (planning a mutual friend's birthday party) but everything they say carries double meaning.

This is the HARDEST creative writing test. A model that produces generic fiction will score low. I want literary craft — discomfort, tension, things unsaid.""",
    },
    {
        "id": 59, "role": "Compliance / Regulatory Agent", "tier": 5,
        "scoring_type": "constraint",
        "scoring_data": {"must_catch_jurisdiction_conflict": True, "must_identify_data_flow_violation": True, "trap": "GDPR legitimate interest doesn't apply to health data", "regulations_to_cover": 4},
        "hard_prompt": """Assess compliance for this scenario. There is a JURISDICTIONAL TRAP and a common GDPR misconception.

Company: US-based health tech startup. Processing:
- US patient data under HIPAA
- EU patient data processed in US servers (claiming "legitimate interest" as GDPR basis)
- Children's data (ages 8-17) for pediatric features
- Selling anonymized (but re-identifiable with zip code + age + diagnosis) data to insurance companies
- Using patient data to train AI model hosted on Chinese cloud provider (Alibaba Cloud)
- New feature: sharing patient records between providers using blockchain (immutable ledger)

Regulations to assess:
1. HIPAA — is the data sharing compliant?
2. GDPR — is "legitimate interest" valid for health data? (TRAP: it's not — Article 9 requires explicit consent for special category data)
3. COPPA/children's privacy — additional requirements
4. AI Act — does the medical AI qualify as high-risk?
5. Cross-border data transfer — US to China implications
6. Right to erasure vs blockchain immutability — conflict?
7. Is the "anonymized" data actually anonymous under GDPR? (k-anonymity test)

Provide a compliance verdict for each, with specific article/section citations.""",
    },
]
