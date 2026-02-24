"""
OpenClaw 59-Role Evaluation Prompts
Each role has 2 prompts: one with automated scoring, one for manual quality review.
"""

ROLE_TESTS = [
    # ================================================================
    # TIER 1 — Lightweight Roles (1-4B sufficient)
    # ================================================================
    {
        "id": 1, "role": "Router / Triage Agent", "tier": 1,
        "prompt": 'Classify this message into ONE category (respond with ONLY the category name): "I need help writing unit tests for my login module"\nCategories: code_generation, code_review, qa_testing, research, email, summarization, translation, calendar, general',
        "check": "contains", "expected": "qa_testing",
        "quality_prompt": 'You are a message router for a multi-agent AI system. Classify each message and explain your reasoning in 1-2 sentences.\n\nMessages:\n1. "Rewrite this function to be more efficient"\n2. "What meetings do I have tomorrow?"\n3. "Summarize the Q3 earnings call"\n4. "Is it true that Mars has two moons?"\n5. "Send a follow-up email to the client"',
    },
    {
        "id": 2, "role": "Input Validator / Sanitizer", "tier": 1,
        "prompt": 'You are an input validator. Check this input for issues and respond with ONLY valid JSON: {"valid": true/false, "issues": [list of issues]}.\n\nInput to validate: {"name": "", "email": "not-an-email", "age": -5, "phone": "555-1234"}',
        "check": "json",
        "quality_prompt": 'You are an input validator. Analyze this API request body and list every validation issue you find, with severity (error/warning):\n\n{"user_id": null, "action": "transfer", "amount": "one hundred", "currency": "FAKE", "recipient": "usr_123", "timestamp": "yesterday", "notes": "<script>alert(1)</script>"}',
    },
    {
        "id": 3, "role": "Heartbeat / Health Monitor", "tier": 1,
        "prompt": 'You are a system health monitor. Given these metrics, respond with ONLY valid JSON: {"status": "healthy"|"degraded"|"critical", "alerts": [list]}.\n\nMetrics: CPU: 23%, Memory: 91%, Disk: 78%, API latency: 2.3s (threshold: 1s), Error rate: 0.5%, Uptime: 99.2%',
        "check": "json",
        "quality_prompt": "You are a system health monitor. These are the last 5 minutes of server metrics. Write a health report with recommendations:\n\nCPU: 85% → 92% → 95% → 88% → 91%\nMemory: 78% → 79% → 82% → 85% → 87%\nDisk I/O: 45MB/s → 120MB/s → 180MB/s → 150MB/s → 90MB/s\nActive connections: 1200 → 1500 → 1800 → 2100 → 1900\nError rate: 0.1% → 0.3% → 1.2% → 0.8% → 0.4%",
    },
    {
        "id": 4, "role": "Notification / Alert Agent", "tier": 1,
        "prompt": 'You are an alert agent. Based on these events, generate ONLY a JSON array of alerts with fields: severity (critical/warning/info), message, action_required (boolean).\n\nEvents: 1) Database backup failed at 3:00 AM. 2) New user signed up. 3) SSL certificate expires in 3 days. 4) Monthly report generated.',
        "check": "json",
        "quality_prompt": "You are a notification agent for a DevOps team. Write appropriate alert messages (with priority, channel, and urgency) for: 1) Production database is running out of disk space (92% used), 2) A new critical CVE was published affecting your Node.js version, 3) A teammate's PR has been open for 5 days without review.",
    },
    {
        "id": 5, "role": "Sentiment Analysis Agent", "tier": 1,
        "prompt": 'Analyze the sentiment of each review. Respond with ONLY valid JSON array: [{"text_snippet": "first 20 chars", "sentiment": "positive"|"negative"|"neutral", "confidence": 0-1}]\n\nReviews:\n1. "Absolutely love this product! Best purchase ever!"\n2. "Terrible customer service, waited 3 hours"\n3. "It works fine, nothing special"\n4. "The quality has really gone downhill lately"\n5. "Exceeded my expectations in every way"',
        "check": "json",
        "quality_prompt": "Analyze the sentiment of this customer feedback email and provide: overall sentiment, key positive points, key negative points, emotional tone, urgency level, and a recommended response strategy.\n\nEmail: 'I've been a loyal customer for 8 years but I'm extremely disappointed with the recent changes. The new interface is confusing and I've lost important data during the migration. However, I must say your support team member Sarah was incredibly helpful and patient. I'd hate to leave but if these issues aren't resolved soon, I'll have no choice.'",
    },
    {
        "id": 6, "role": "FAQ Generation Agent", "tier": 1,
        "prompt": 'Generate exactly 3 FAQ entries from this text. Respond with ONLY valid JSON array: [{"question": "...", "answer": "..."}]\n\nText: "Our store accepts returns within 30 days of purchase. Items must be in original packaging. Refunds are processed within 5-7 business days. Sale items are final sale and cannot be returned. Gift cards are non-refundable."',
        "check": "json",
        "quality_prompt": "Generate a comprehensive FAQ section (8-10 Q&A pairs) for a SaaS product that offers AI-powered email management. Cover pricing, features, security, integration, and support. Make questions sound natural, like real customers would ask them.",
    },
    {
        "id": 7, "role": "Translation Agent", "tier": 1,
        "prompt": 'Translate the following to French. Respond with ONLY the translation, no explanation:\n\n"The quarterly report shows a 15% increase in revenue compared to last year. Our team has exceeded all performance targets."',
        "check": "contains_any", "expected": ["rapport trimestriel", "trimestriel", "augmentation", "revenus", "chiffre"],
        "quality_prompt": "Translate this technical product description into both Spanish and Japanese. Preserve technical terms where appropriate and add translator notes for any culturally-specific references:\n\n'Our enterprise-grade API gateway handles 10,000 requests per second with 99.99% uptime SLA. Features include rate limiting, OAuth 2.0 authentication, and real-time analytics dashboard.'",
    },
    {
        "id": 8, "role": "Calendar / Scheduling Agent", "tier": 1,
        "prompt": 'Extract scheduling information as JSON: {"action": "create"|"check"|"cancel", "title": "...", "date": "YYYY-MM-DD", "time": "HH:MM", "duration_minutes": N, "attendees": [...]}\n\nUser: "Set up a 45-minute design review with Alice and Bob next Tuesday at 2pm"',
        "check": "json",
        "quality_prompt": "You are a scheduling agent. Given this calendar and request, find the best time slot and explain your reasoning:\n\nCalendar (Monday):\n- 9:00-10:00: Team standup\n- 11:00-12:00: Client call\n- 13:00-14:00: Lunch\n- 15:00-16:30: Sprint planning\n\nRequest: 'Schedule a 90-minute workshop with the design team. They prefer mornings but are flexible. It can't conflict with any existing meetings and needs 30 minutes buffer before the client call.'",
    },

    # ================================================================
    # TIER 2 — Mid-Range Roles (8-14B recommended)
    # ================================================================
    {
        "id": 9, "role": "Research / Web Search Agent", "tier": 2,
        "prompt": 'You are a research agent. Given the query below, generate a structured research plan as JSON: {"query": "...", "search_queries": [3 specific searches], "key_questions": [3 questions to answer], "expected_sources": [types of sources]}\n\nQuery: "What are the environmental impacts of lithium mining for EV batteries?"',
        "check": "json",
        "quality_prompt": "Research and synthesize: What are the current leading approaches to room-temperature superconductors as of 2025? Include key research groups, materials being studied, latest breakthroughs, and remaining challenges. Structure your response with headers and citations where possible.",
    },
    {
        "id": 10, "role": "Content Writer / Blog Writer", "tier": 2,
        "prompt": 'Write a 150-word blog introduction about remote work productivity. Include a hook, a statistic (you can estimate), and a thesis statement. Respond with ONLY the introduction paragraph.',
        "check": "length_min", "expected": 100,
        "quality_prompt": "Write a compelling 400-word blog post titled 'Why Your Company Should Adopt a 4-Day Work Week.' Include: an attention-grabbing opening, at least 3 supporting arguments with examples, a counterargument acknowledgment, and a strong call-to-action ending.",
    },
    {
        "id": 11, "role": "Editor Agent", "tier": 2,
        "prompt": 'Edit this text for grammar, clarity, and style. Respond with the corrected text followed by a list of changes made.\n\n"Their going to the store tomorrow, me and him wants to by some grocerys. The weather will be good probaly so we might walking their."',
        "check": "contains_all", "expected": ["They're", "groceries"],
        "quality_prompt": "Edit this draft for a professional blog. Fix grammar, improve clarity, enhance flow, and suggest structural improvements. Show tracked changes:\n\n'AI is really really changing everything. Companies that dont use AI will fall behind. The technology is moving fast and its important to keep up. Some people think AI is dangerous but I think its mostly good. There are many benefits like saving time and money. In conclusion AI is the future and we should embrace it.'",
    },
    {
        "id": 12, "role": "Content Planner", "tier": 2,
        "prompt": 'Create a 4-week content calendar as JSON: {"weeks": [{"week": 1, "posts": [{"day": "Mon", "topic": "...", "format": "blog|video|social", "target_audience": "..."}]}]}\n\nBrief: B2B SaaS startup launching a new project management tool. Goal: generate awareness among tech leads.',
        "check": "json",
        "quality_prompt": "Create a comprehensive 3-month content strategy for a health and wellness app targeting millennials. Include content pillars, posting frequency by channel (blog, Instagram, TikTok, newsletter), key themes per month, and KPIs to track.",
    },
    {
        "id": 13, "role": "Email Drafting / Summarization", "tier": 2,
        "prompt": 'Summarize this email thread into 3 bullet points and draft a reply. Respond as JSON: {"summary": ["..."], "draft_reply": "..."}\n\nThread:\nFrom: alice@co.com — "Can we move the deadline to Friday? The client requested additional features."\nFrom: bob@co.com — "Friday is tight but doable if we skip the UI polish pass."\nFrom: alice@co.com — "The client specifically mentioned UI quality. Can we get help from the design team?"',
        "check": "json",
        "quality_prompt": "You received 5 emails while on vacation. Summarize each, prioritize them (P1-P3), and draft responses for the P1 items:\n\n1. From CEO: 'Need your input on the Q2 budget by Wednesday'\n2. From HR: 'Annual benefits enrollment opens next month'\n3. From Client: 'Critical bug in production affecting 30% of users'\n4. From Teammate: 'Can you review my PR when you get a chance?'\n5. From Vendor: 'Your contract renewal is coming up in 60 days'",
    },
    {
        "id": 14, "role": "Document Summarization", "tier": 2,
        "prompt": "Summarize the following in exactly 3 bullet points. Each bullet must be one sentence.\n\nArtificial intelligence has transformed healthcare through early disease detection, personalized treatment plans, and automated administrative tasks. Machine learning algorithms can now analyze medical images with accuracy comparable to specialists, while natural language processing helps extract insights from clinical notes. Despite these advances, challenges remain in data privacy, algorithmic bias, and integration with existing healthcare workflows. Regulatory frameworks are still catching up with the pace of innovation, creating uncertainty for healthcare providers.",
        "check": "contains_pattern", "pattern": r"^[\-\*•]", "min_matches": 3,
        "quality_prompt": "Summarize this technical document into an executive summary (200 words max), key takeaways (5 bullets), and action items:\n\n'Our microservices migration is 60% complete. We've moved 12 of 20 services from the monolith. Performance has improved 40% for migrated services, but we've seen 3 incidents related to service discovery in the past month. The team estimates 4 more months to complete the migration. We recommend pausing new feature development during the critical migration of the payment and authentication services. Cost savings from containerization are projected at $50K/month once complete. Two team members need additional Kubernetes training.'",
    },
    {
        "id": 15, "role": "Meeting Notes / Transcription Agent", "tier": 2,
        "prompt": 'Extract meeting information as JSON: {"title": "...", "date": "...", "attendees": [...], "key_decisions": [...], "action_items": [{"owner": "...", "task": "...", "due": "..."}]}\n\nTranscript excerpt: "Alice: Let\'s finalize the Q2 roadmap. Bob, can you have the API specs ready by March 15th? Bob: Sure, I\'ll also need Carol to review the database schema by March 10th. Carol: Agreed. We decided to use PostgreSQL instead of MongoDB for this project. Alice: Great, I\'ll update the stakeholders by end of week."',
        "check": "json",
        "quality_prompt": "Process this meeting transcript into structured notes with summary, decisions, action items, and parking lot items:\n\n'Product sync, Feb 20. Present: Sarah (PM), Mike (Eng Lead), Lisa (Design), James (QA). Sarah opened by saying user retention dropped 5% last month. Mike said the new onboarding flow should help — it ships next sprint. Lisa shared 3 design options for the dashboard redesign. The team voted for option B. James raised concerns about test coverage for the payment module — only 40%. Sarah said we should add that to the tech debt sprint. Mike mentioned we need to decide on the caching strategy by next week but nobody had time to discuss it. Lisa needs updated brand guidelines from marketing before finalizing the designs.'",
    },
    {
        "id": 16, "role": "Social Media Scouting / Monitoring", "tier": 2,
        "prompt": 'Analyze these social media mentions and respond with JSON: {"brand_sentiment": "positive"|"negative"|"mixed", "trending_topics": [...], "urgent_issues": [...], "engagement_recommendation": "..."}\n\nMentions:\n1. "@brand love the new update! 🔥"\n2. "@brand app keeps crashing on iOS 18"\n3. "@brand vs competitor — brand wins on features but competitor has better pricing"\n4. "@brand the customer support chat took 45 minutes to connect"\n5. "@brand just switched from competitor, so much better!"',
        "check": "json",
        "quality_prompt": "You are monitoring social media for a consumer electronics brand. Analyze these trends from the past week and provide a comprehensive social listening report:\n\n- 340 mentions (up 45% from last week)\n- Positive: 55%, Negative: 30%, Neutral: 15%\n- Top complaint: battery life (mentioned 89 times)\n- Top praise: camera quality (mentioned 120 times)\n- Competitor comparison mentions: up 200%\n- Influencer @techreviewer (500K followers) posted a negative review\n- 3 viral tweets about a defective charging port",
    },
    {
        "id": 17, "role": "Social Media Content Agent", "tier": 2,
        "prompt": 'Create a social media post for Twitter/X (max 280 chars) promoting a new AI coding assistant. Include a call to action and relevant hashtags. Respond with ONLY the post text.',
        "check": "length_max", "expected": 300,
        "quality_prompt": "Create a week of social media content (7 posts) for a sustainable fashion brand launching a new collection made from recycled ocean plastic. Include posts for: Instagram (with image description), Twitter/X, LinkedIn, and TikTok script. Each should match the platform's tone and format.",
    },
    {
        "id": 18, "role": "News Aggregation Agent", "tier": 2,
        "prompt": 'Categorize these headlines and respond with JSON array: [{"headline": "...", "category": "tech"|"finance"|"politics"|"science"|"sports", "relevance_score": 1-10, "summary": "one sentence"}]\n\n1. "Federal Reserve Holds Interest Rates Steady"\n2. "New CRISPR Technique Cures Genetic Disease in Mice"\n3. "Tech Giant Announces Layoffs Amid AI Restructuring"\n4. "World Cup Qualifiers: Surprising Upset in Group B"',
        "check": "json",
        "quality_prompt": "You are a news aggregation agent for a tech executive. From today's tech news, create a morning briefing covering: top 5 stories with 2-sentence summaries each, market impact assessment, and 'what to watch today' section. Use realistic topics from the AI and technology space.",
    },
    {
        "id": 19, "role": "Shopping / Price Comparison", "tier": 2,
        "prompt": 'Compare these products and respond with JSON: {"recommendation": "...", "comparison": [{"product": "...", "price": N, "pros": [...], "cons": [...], "value_score": 1-10}], "best_value": "..."}\n\nProducts: iPhone 16 Pro ($999), Samsung S25 Ultra ($1199), Google Pixel 9 Pro ($899)',
        "check": "json",
        "quality_prompt": "A user wants to buy a laptop for software development with a $1500 budget. Compare 3-4 realistic options across: performance (CPU/RAM), display quality, keyboard, battery life, ports, and value. Include a clear recommendation with reasoning.",
    },
    {
        "id": 20, "role": "Memory / Knowledge Management", "tier": 2,
        "prompt": 'Extract key facts from this conversation for long-term memory storage. Respond as JSON: {"facts": [{"category": "preference"|"decision"|"personal"|"project", "key": "...", "value": "...", "confidence": 0-1}]}\n\nConversation: "I prefer dark mode in all my apps. We decided to use React for the frontend. My birthday is March 15th. The project deadline is June 30th. I\'m allergic to peanuts. We chose AWS over GCP for hosting."',
        "check": "json",
        "quality_prompt": "You are a knowledge management agent maintaining a user profile. Given these 3 conversation excerpts from different dates, extract, merge, and organize all relevant knowledge. Handle contradictions by noting the most recent information:\n\nJan 5: 'I work at Acme Corp as a senior developer. I prefer Python over JavaScript.'\nFeb 12: 'I got promoted to Tech Lead at Acme Corp! We're switching our stack from Python to TypeScript.'\nFeb 20: 'Working on a side project in Rust. My team now has 8 people.'",
    },
    {
        "id": 21, "role": "RAG / Retrieval Agent", "tier": 2,
        "prompt": "Answer the question using ONLY the provided context. If the answer isn't in the context, say 'Not found in provided context.' Respond with JSON: {\"answer\": \"...\", \"source_quote\": \"exact quote from context\", \"confidence\": 0-1}\n\nContext: 'The company was founded in 2019 by Jane Smith and Tom Brown. They raised $5M in seed funding from Sequoia Capital. The product launched in 2021 with 1,000 beta users.'\n\nQuestion: 'How much funding did the company raise and from whom?'",
        "check": "json",
        "quality_prompt": "You are a RAG agent. Answer the user's question using ONLY the provided context chunks. For each claim in your answer, cite which chunk it came from. If information is missing, explicitly state what's not covered.\n\nChunk 1: 'Our API rate limit is 100 requests per minute for free tier and 1000 for paid tier.'\nChunk 2: 'Authentication uses OAuth 2.0. API keys can be generated in the dashboard under Settings > API.'\nChunk 3: 'Webhooks are supported for events: order.created, order.updated, payment.completed.'\nChunk 4: 'The API supports JSON and XML response formats. Set Accept header accordingly.'\n\nQuestion: 'I need to integrate your API for real-time order notifications. What do I need to set up and are there any limits I should know about?'",
    },
    {
        "id": 22, "role": "Data Analysis Agent", "tier": 2,
        "prompt": 'Analyze this dataset and provide insights as JSON: {"trends": [...], "anomalies": [...], "recommendations": [...]}\n\nMonthly Sales: Jan: $100K, Feb: $95K, Mar: $110K, Apr: $250K, May: $105K, Jun: $115K, Jul: $108K',
        "check": "json",
        "quality_prompt": "Analyze this A/B test data and provide a recommendation:\n\nControl (A): 10,000 visitors, 320 conversions, avg order $45, bounce rate 65%\nVariant (B): 10,000 visitors, 380 conversions, avg order $42, bounce rate 58%\n\nInclude: statistical significance assessment, revenue impact calculation, segment analysis considerations, and a clear go/no-go recommendation with reasoning.",
    },
    {
        "id": 23, "role": "Website Scraping / Understanding", "tier": 2,
        "prompt": 'Extract structured data from this HTML snippet. Respond with JSON array of products: [{"name": "...", "price": N, "rating": N, "in_stock": bool}]\n\n<div class="product"><h3>Wireless Mouse</h3><span class="price">$29.99</span><span class="rating">4.5/5</span><span class="stock">In Stock</span></div><div class="product"><h3>Keyboard</h3><span class="price">$59.99</span><span class="rating">4.2/5</span><span class="stock">Out of Stock</span></div>',
        "check": "json",
        "quality_prompt": "You received this raw HTML from a job listing page. Extract all job information into a structured format and identify any red flags:\n\n<div class='job'><h2>Senior Developer</h2><p>Acme Corp - Remote</p><p>$150K-180K</p><p>Requirements: 10+ years experience, PhD preferred, must know 15 programming languages, available 24/7</p><p>Benefits: unlimited PTO, equity</p></div>",
    },
    {
        "id": 24, "role": "Image Description / Understanding", "tier": 2,
        "prompt": 'Describe what a professional product photo of a modern laptop on a wooden desk should contain. Respond with JSON: {"objects": [...], "composition": "...", "lighting": "...", "mood": "...", "suggested_alt_text": "..."}\n\n(Note: This is a text-based description task since no actual image is provided)',
        "check": "json",
        "quality_prompt": "Write detailed alt-text descriptions for these 3 hypothetical UI screenshots that would be useful for accessibility:\n1. A dashboard showing sales analytics with a line graph trending upward, a pie chart of revenue by region, and a table of top 10 products\n2. A mobile app onboarding screen with a welcome illustration, progress dots showing step 2 of 4, and a 'Continue' button\n3. An error page showing a 404 with a cartoon robot looking confused",
    },
    {
        "id": 25, "role": "Customer Support Agent", "tier": 2,
        "prompt": "Respond to this customer complaint professionally. Acknowledge the issue, apologize, and provide a resolution. Keep it under 150 words.\n\nCustomer: 'I ordered a laptop 2 weeks ago and it still hasn't arrived. The tracking shows it's been stuck in transit for 5 days. This is unacceptable!'",
        "check": "contains_any", "expected": ["apologize", "sorry", "apolog", "understand", "frustrat"],
        "quality_prompt": "Handle this escalated customer support conversation. The customer is angry and threatening to post on social media:\n\nCustomer: 'This is the THIRD time my subscription was charged twice! I've called support twice before and was promised it was fixed. I'm posting about this everywhere and filing a chargeback. You people are scammers!'\n\nProvide a response that de-escalates, acknowledges the pattern of failure, offers concrete remediation, and retains the customer.",
    },
    {
        "id": 26, "role": "Lead Scoring / Prospecting", "tier": 2,
        "prompt": 'Score this lead and respond with JSON: {"score": 1-100, "quality": "hot"|"warm"|"cold", "reasoning": [...], "next_action": "..."}\n\nLead: Company: 500 employees, Tech industry, Visited pricing page 3 times, Downloaded whitepaper, Budget: $50K+, Timeline: This quarter, Current solution: Competitor product',
        "check": "json",
        "quality_prompt": "You are a lead scoring agent. Score and rank these 4 leads, then recommend a prioritized outreach strategy for each:\n\n1. Startup, 20 employees, CEO signed up for free trial, used product daily for 2 weeks, asked about enterprise features\n2. Enterprise, 5000 employees, VP of Engineering attended webinar, no product sign-up, company uses competitor\n3. Mid-market, 200 employees, Developer downloaded API docs, created account, made 3 API calls then stopped\n4. Enterprise, 10000 employees, Procurement team requested pricing, RFP in progress, evaluating 3 vendors",
    },
    {
        "id": 27, "role": "Sprint / Project Summarizer", "tier": 2,
        "prompt": 'Summarize this sprint data as JSON: {"sprint": "...", "velocity": N, "completed": N, "remaining": N, "blockers": [...], "highlights": [...], "risk_assessment": "low"|"medium"|"high"}\n\nSprint 14: 8 stories planned (34 points). Completed: 6 stories (28 points). Blocked: Login refactor (waiting on security review). Highlight: Payment integration shipped 2 days early. Carryover: 2 stories to Sprint 15.',
        "check": "json",
        "quality_prompt": "Generate a sprint retrospective summary from these team comments and create actionable improvements:\n\nWhat went well: 'Pair programming helped', 'New CI pipeline saved time', 'Good cross-team communication'\nWhat didn't go well: 'Too many meetings', 'Requirements changed mid-sprint', 'Deployment on Friday caused weekend stress', 'Code reviews taking too long'\nAction items from last retro: 'Limit meetings to 25 min' (partially done), 'Add integration tests' (not started)",
    },
    {
        "id": 28, "role": "Transaction / Approval Agent", "tier": 2,
        "prompt": 'You are a transaction approval agent. Apply these rules and respond with JSON: {"approved": bool, "reason": "...", "requires_human_review": bool}\n\nRules: Auto-approve if amount < $1000. Require human review if amount > $5000. Flag if vendor is new. Block if over budget.\n\nTransaction: Amount: $3,500, Vendor: CloudCo (first transaction), Budget remaining: $10,000',
        "check": "json",
        "quality_prompt": "You are a transaction approval agent. Process these 5 transactions against the company policy and explain each decision:\n\nPolicy: Individual limit $5K, team limit $25K/month, pre-approved vendors only, travel requires manager approval.\n\n1. $4,500 to pre-approved vendor for software licenses\n2. $800 flight to San Francisco for conference (no manager approval attached)\n3. $12,000 to new vendor for consulting services\n4. $150 for team lunch (team has spent $24,200 this month)\n5. $3,000 to pre-approved vendor for cloud hosting",
    },
    {
        "id": 29, "role": "Home Automation Agent", "tier": 2,
        "prompt": 'Parse this smart home command and respond with JSON: {"device": "...", "action": "...", "parameters": {...}, "schedule": null|"..."}\n\nCommand: "Turn down the living room thermostat to 68 degrees at 10pm tonight"',
        "check": "json",
        "quality_prompt": "You are a home automation agent. Create an evening routine automation based on this description:\n\n'When I say goodnight: dim all lights to 10% over 5 minutes, lock all doors, set thermostat to 65°F, turn on the bedroom white noise machine, arm the security system in night mode, and check if any windows are open — if so, alert me instead of arming.'",
    },
    {
        "id": 30, "role": "Fitness / Health Tracking", "tier": 2,
        "prompt": 'Log this fitness data and provide analysis as JSON: {"log": {"calories": N, "protein_g": N, "meals": [...]}, "daily_summary": "...", "recommendations": [...]}\n\nBreakfast: Oatmeal with banana and honey, coffee with milk\nLunch: Grilled chicken salad with olive oil dressing\nSnack: Greek yogurt with almonds',
        "check": "json",
        "quality_prompt": "You are a fitness tracking agent. Analyze this week of workout data and provide a comprehensive progress report with recommendations:\n\nMon: 5K run (28:30), Tue: Upper body weights (45 min), Wed: Rest, Thu: HIIT (30 min), Fri: 5K run (27:15), Sat: Full body weights (60 min), Sun: Yoga (45 min)\n\nGoals: Run a sub-25 min 5K by April, build muscle, maintain 4-5 workouts/week.",
    },
    {
        "id": 31, "role": "Recipe / Cooking Agent", "tier": 2,
        "prompt": 'Suggest a recipe based on these ingredients. Respond with JSON: {"recipe_name": "...", "servings": N, "time_minutes": N, "ingredients": [...], "steps": [...]}\n\nAvailable ingredients: chicken breast, garlic, lemon, olive oil, rice, broccoli, soy sauce',
        "check": "json",
        "quality_prompt": "I'm hosting a dinner party for 6 people. One guest is vegan, one is gluten-free, and one has a nut allergy. Suggest a 3-course menu that works for everyone, with detailed recipes and a prep timeline so everything is ready by 7pm.",
    },
    {
        "id": 32, "role": "Personal Finance Tracking", "tier": 2,
        "prompt": 'Categorize these transactions and provide a monthly summary as JSON: {"transactions": [{"description": "...", "amount": N, "category": "..."}], "total_by_category": {...}, "savings_rate": "N%"}\n\nIncome: $5,000 salary\nTransactions: Rent $1,500, Groceries $400, Netflix $15, Gas $80, Restaurant $120, Electric bill $95, Gym $50',
        "check": "json",
        "quality_prompt": "You are a personal finance agent. Analyze this user's 3-month spending pattern and provide actionable advice:\n\nJan: Income $6K, Housing $1.8K, Food $900, Entertainment $400, Transportation $300, Subscriptions $120, Shopping $600, Savings $880\nFeb: Income $6K, Housing $1.8K, Food $1100, Entertainment $350, Transportation $280, Subscriptions $120, Shopping $850, Savings $500\nMar: Income $6K, Housing $1.8K, Food $1200, Entertainment $500, Transportation $320, Subscriptions $150, Shopping $900, Savings $130",
    },
    {
        "id": 33, "role": "SEO Optimization Agent", "tier": 2,
        "prompt": 'Analyze this page for SEO and respond with JSON: {"score": 1-100, "issues": [...], "recommendations": [...], "suggested_meta_description": "..."}\n\nPage title: "Blog"\nH1: None\nContent: 200 words about machine learning, no images, no internal links\nURL: /page1',
        "check": "json",
        "quality_prompt": "Optimize this blog post for the target keyword 'best project management tools 2026'. Provide: improved title tag, meta description, H1 and H2 suggestions, keyword placement recommendations, internal linking strategy, and schema markup suggestions.\n\nCurrent title: 'Some Good Tools for Managing Projects'\nCurrent meta: (none)\nContent: 500-word generic article comparing 3 tools without specific details.",
    },
    {
        "id": 34, "role": "Landing Page Generator", "tier": 2,
        "prompt": 'Generate the HTML structure (outline with section descriptions, not full code) for a landing page as JSON: {"sections": [{"type": "hero"|"features"|"testimonials"|"pricing"|"cta", "headline": "...", "content_description": "..."}]}\n\nProduct: AI-powered email client that auto-drafts replies',
        "check": "json",
        "quality_prompt": "Generate complete HTML and CSS for a modern, responsive landing page for a SaaS product called 'FlowState' — an AI-powered focus timer for developers. Include: hero section with CTA, 3 feature blocks, a testimonial, pricing table (Free/Pro/Team), and a footer. Use modern design principles.",
    },
    {
        "id": 35, "role": "Travel Planning Agent", "tier": 2,
        "prompt": 'Create a travel itinerary as JSON: {"destination": "...", "duration": "...", "daily_plan": [{"day": N, "activities": [...], "estimated_cost": "..."}], "total_estimated_cost": "..."}\n\nRequest: "3-day weekend trip to Tokyo for a first-time visitor, budget $2000"',
        "check": "json",
        "quality_prompt": "Plan a detailed 10-day family vacation to Italy (2 adults, 2 kids ages 8 and 12). Budget: $8,000 not including flights. Must include Rome, Florence, and one coastal destination. Include: daily itinerary, kid-friendly activities, restaurant recommendations, transportation between cities, and money-saving tips.",
    },

    # ================================================================
    # TIER 3 — Quality-Limited Roles (14B+ recommended)
    # ================================================================
    {
        "id": 36, "role": "Code Generation Agent", "tier": 3,
        "prompt": "Write a Python function called `merge_sorted_lists(list1, list2)` that merges two sorted lists into one sorted list in O(n+m) time. Return ONLY the function code.",
        "check": "code", "test_code": """
def test():
    assert merge_sorted_lists([1,3,5], [2,4,6]) == [1,2,3,4,5,6]
    assert merge_sorted_lists([], [1,2,3]) == [1,2,3]
    assert merge_sorted_lists([1], []) == [1]
    assert merge_sorted_lists([], []) == []
    assert merge_sorted_lists([1,1,1], [1,1]) == [1,1,1,1,1]
    return True
""",
        "quality_prompt": "Write a Python class for a thread-safe LRU (Least Recently Used) cache with the following requirements:\n1. Fixed capacity set at initialization\n2. O(1) get and put operations\n3. Thread-safe for concurrent access\n4. Evicts the least recently used item when capacity is exceeded\n5. Include docstrings and type hints\n\nInclude usage examples and explain your design choices.",
    },
    {
        "id": 37, "role": "Code Review Agent", "tier": 3,
        "prompt": 'Review this code and respond with JSON: {"issues": [{"line": "...", "severity": "critical"|"warning"|"info", "description": "..."}], "overall_quality": 1-10}\n\n```python\ndef get_user(id):\n    query = f"SELECT * FROM users WHERE id = {id}"\n    result = db.execute(query)\n    password = result[0]["password"]\n    return {"id": id, "password": password, "data": result}\n```',
        "check": "json",
        "quality_prompt": "Perform a comprehensive code review of this API endpoint. Cover: security, performance, error handling, code style, and testability.\n\n```python\nimport json\nfrom flask import Flask, request\n\napp = Flask(__name__)\nusers = {}\n\n@app.route('/user', methods=['POST'])\ndef create_user():\n    data = json.loads(request.data)\n    users[data['email']] = data\n    open('users.log', 'a').write(str(data) + '\\n')\n    return json.dumps({'status': 'ok', 'user': data})\n\n@app.route('/user/<email>')\ndef get_user(email):\n    return json.dumps(users[email])\n```",
    },
    {
        "id": 38, "role": "QA / Test Writing Agent", "tier": 3,
        "prompt": 'Write 3 pytest test functions for this function. Return ONLY the test code.\n\n```python\ndef calculate_discount(price, discount_percent, is_member):\n    if is_member:\n        discount_percent += 5\n    discount = price * (discount_percent / 100)\n    return max(price - discount, 0)\n```',
        "check": "contains_all", "expected": ["def test_", "assert"],
        "quality_prompt": "Write a comprehensive test suite for an e-commerce shopping cart module. Include:\n1. Unit tests for add_item, remove_item, update_quantity, apply_coupon, calculate_total\n2. Edge cases: empty cart, negative quantities, expired coupons, out-of-stock items\n3. Integration test scenarios for a complete checkout flow\n4. Use pytest fixtures and parametrize where appropriate",
    },
    {
        "id": 39, "role": "Task Planning / Decomposition", "tier": 3,
        "prompt": 'Break down this task into subtasks with dependencies as JSON: {"task": "...", "subtasks": [{"id": N, "name": "...", "depends_on": [ids], "estimated_hours": N, "assignee_role": "..."}]}\n\nTask: "Build a user authentication system with OAuth2 support"',
        "check": "json",
        "quality_prompt": "Decompose this complex project into a detailed work breakdown structure with critical path analysis:\n\n'Migrate a legacy PHP monolith e-commerce platform to a microservices architecture using Node.js and Kubernetes. The platform handles 10K daily orders, has 50K registered users, and must maintain 99.9% uptime during migration. Team: 4 backend devs, 2 frontend devs, 1 DevOps, 1 QA.'",
    },
    {
        "id": 40, "role": "Fact-Checking Agent", "tier": 3,
        "prompt": 'Fact-check these claims. Respond with JSON: [{"claim": "...", "verdict": "true"|"false"|"misleading"|"unverifiable", "explanation": "...", "confidence": 0-1}]\n\n1. "Python is the most popular programming language in the world"\n2. "The human body has 206 bones"\n3. "Einstein failed math in school"\n4. "Lightning never strikes the same place twice"',
        "check": "json",
        "quality_prompt": "Fact-check this paragraph from a blog post. For each factual claim, assess its accuracy, provide correction if wrong, and rate your confidence:\n\n'Elon Musk founded Tesla in 2003 and grew it into the world's largest car company by revenue. The company's market cap exceeded $1 trillion in 2021, making it more valuable than all other car companies combined. Tesla produces 100% of its batteries in-house at its Gigafactories, and the Model 3 is the best-selling electric car of all time globally.'",
    },
    {
        "id": 41, "role": "Critic / Review Agent", "tier": 3,
        "prompt": 'Review this AI-generated response for quality. Score 1-10 on each criterion and respond with JSON: {"accuracy": N, "completeness": N, "clarity": N, "relevance": N, "overall": N, "feedback": "..."}\n\nOriginal question: "What causes rain?"\nAI response: "Rain happens when water goes up and comes back down. It\'s part of nature."',
        "check": "json",
        "quality_prompt": "You are a quality critic reviewing another AI agent's output. Evaluate this research summary on 6 dimensions (accuracy, depth, objectivity, structure, citations, actionability) and provide detailed feedback:\n\nTopic: 'Impact of AI on software development jobs'\nSummary: 'AI is making software development faster. GitHub Copilot helps developers write code. Some jobs might be automated but new jobs will be created. Overall, AI is good for developers. Companies should adopt AI tools.'",
    },
    {
        "id": 42, "role": "Market Research Agent", "tier": 3,
        "prompt": 'Analyze this market and respond with JSON: {"market_size": "...", "growth_rate": "...", "key_players": [...], "trends": [...], "opportunities": [...], "threats": [...]}\n\nMarket: AI-powered customer service chatbots for mid-market SaaS companies',
        "check": "json",
        "quality_prompt": "Conduct a competitive analysis for a new AI writing assistant entering the market against Jasper, Copy.ai, and Writesonic. Include: feature comparison matrix, pricing analysis, target customer segments, differentiation opportunities, market positioning strategy, and go-to-market recommendations.",
    },
    {
        "id": 43, "role": "Synthesizer / Aggregator", "tier": 3,
        "prompt": 'Synthesize these 3 agent outputs into one coherent response:\n\nAgent 1 (Research): "The global EV market grew 35% in 2025. China leads with 60% market share."\nAgent 2 (Finance): "EV stocks are volatile. Tesla P/E ratio is 45x vs industry average 15x."\nAgent 3 (Environment): "EVs reduce carbon emissions by 50% vs ICE vehicles over their lifecycle."\n\nProvide a unified summary covering all perspectives.',
        "check": "length_min", "expected": 100,
        "quality_prompt": "You are a synthesizer agent. Three specialist agents have provided their analyses of whether a company should build or buy an AI solution. Combine their perspectives into a single executive recommendation:\n\nTechnical Agent: 'Building gives full control but requires 6+ months and 3 ML engineers we don't have. Fine-tuning open-source models is viable but maintenance burden is real.'\nFinancial Agent: 'Buy costs $50K/year. Build costs $200K upfront + $80K/year maintenance. Break-even at 3.3 years assuming no scope creep.'\nStrategic Agent: 'AI is becoming a core competency in our industry. Competitors who built in-house have 2x faster iteration cycles. But 40% of in-house AI projects fail.'",
    },
    {
        "id": 44, "role": "Curriculum / Course Designer", "tier": 3,
        "prompt": 'Design a course module as JSON: {"module_title": "...", "learning_objectives": [...], "lessons": [{"title": "...", "duration_minutes": N, "type": "lecture"|"exercise"|"quiz"}], "assessment": "..."}\n\nTopic: "Introduction to REST APIs for beginners"',
        "check": "json",
        "quality_prompt": "Design a complete 8-week online course: 'Python for Data Science — From Zero to Job-Ready.' Include: week-by-week curriculum, learning objectives per week, project milestones, recommended tools, assessment strategy, and a capstone project description. Target audience: career changers with no programming experience.",
    },
    {
        "id": 45, "role": "Prototype Generator", "tier": 3,
        "prompt": 'Generate a Streamlit app prototype. Respond with complete Python code for a simple app that:\n1. Has a text input for a topic\n2. Has a slider for number of ideas (1-10)\n3. Displays a list of generated ideas when a button is clicked\n\nReturn ONLY the Python code.',
        "check": "contains_all", "expected": ["streamlit", "st.", "slider", "button"],
        "quality_prompt": "Generate a complete, functional Streamlit prototype for a 'Personal Finance Dashboard' with these features:\n1. Monthly income/expense input form\n2. Spending breakdown pie chart\n3. Monthly trend line chart (last 6 months of mock data)\n4. Budget vs actual comparison\n5. Savings goal tracker with progress bar\n\nInclude realistic mock data and make it visually polished.",
    },
    {
        "id": 46, "role": "DevOps Agent", "tier": 3,
        "prompt": 'Analyze this deployment log and respond with JSON: {"status": "success"|"failure", "issues": [...], "root_cause": "...", "fix": "..."}\n\nLog:\n[14:30] Starting deployment v2.3.1\n[14:31] Docker build successful\n[14:32] Pushing to registry... OK\n[14:33] Rolling update started\n[14:34] Pod my-app-abc123 CrashLoopBackOff\n[14:34] Error: ECONNREFUSED 127.0.0.1:5432\n[14:35] Rollback initiated',
        "check": "json",
        "quality_prompt": "Write a complete GitHub Actions CI/CD pipeline for a Node.js application with these requirements:\n1. Run tests and lint on every PR\n2. Build Docker image on merge to main\n3. Deploy to staging automatically\n4. Deploy to production only after manual approval\n5. Include security scanning and dependency audit\n6. Notify Slack on success/failure\n\nInclude the complete YAML file with comments explaining each step.",
    },

    # ================================================================
    # TIER 4 — Deep Reasoning Roles
    # ================================================================
    {
        "id": 47, "role": "Math / Logic Reasoning", "tier": 4,
        "prompt": "Solve this step by step: A store offers a 30% discount followed by an additional 20% off. A customer argues this should be the same as a single 50% discount. Is the customer correct? Show the math for a $100 item.",
        "check": "contains", "expected": "44",
        "quality_prompt": "Solve this multi-step optimization problem with detailed reasoning:\n\nA delivery company has 3 trucks and 8 delivery locations. Each truck can carry 500kg. The deliveries are: A(100kg, downtown), B(200kg, suburb), C(150kg, downtown), D(300kg, industrial), E(50kg, suburb), F(250kg, downtown), G(100kg, industrial), H(175kg, suburb). Minimize the total number of trips while respecting capacity limits. Group nearby locations where possible. Show your reasoning.",
    },
    {
        "id": 48, "role": "STEM Analysis", "tier": 4,
        "prompt": 'Explain the concept of entropy in thermodynamics. Then answer: If you mix hot water (80°C) and cold water (20°C) in equal volumes, what is the final temperature? Explain why this is an irreversible process.\n\nRespond with JSON: {"explanation": "...", "final_temperature": "N°C", "irreversibility_reason": "..."}',
        "check": "json",
        "quality_prompt": "Analyze this experimental data and draw conclusions:\n\nA team tested the effect of 4 different catalysts on reaction rate at 3 temperatures:\n\nCatalyst A: 25°C→0.5mol/s, 50°C→1.2mol/s, 75°C→2.8mol/s\nCatalyst B: 25°C→0.3mol/s, 50°C→0.9mol/s, 75°C→4.1mol/s\nCatalyst C: 25°C→0.8mol/s, 50°C→1.1mol/s, 75°C→1.3mol/s\nCatalyst D: 25°C→0.4mol/s, 50°C→1.5mol/s, 75°C→3.2mol/s\n\nDetermine: which catalyst has the highest activation energy, which is most effective at low temperatures, and which follows non-Arrhenius behavior. Explain your reasoning.",
    },
    {
        "id": 49, "role": "Algorithm Exploration", "tier": 4,
        "prompt": 'Given a list of intervals [[1,3],[2,6],[8,10],[15,18]], merge overlapping intervals. Explain your algorithm approach, analyze time/space complexity, then provide the Python implementation.\n\nRespond with JSON: {"approach": "...", "time_complexity": "O(...)", "space_complexity": "O(...)", "code": "..."}',
        "check": "json",
        "quality_prompt": "Design an algorithm for this novel problem and analyze tradeoffs:\n\nProblem: You're building a real-time collaborative text editor. Multiple users can edit the same document simultaneously. Design the conflict resolution algorithm that:\n1. Handles concurrent insertions at the same position\n2. Preserves user intent when possible\n3. Guarantees eventual consistency across all clients\n4. Works with network latency up to 500ms\n\nCompare at least two approaches (e.g., OT vs CRDT), analyze tradeoffs, and recommend one with justification.",
    },

    # ================================================================
    # TIER 5 — Frontier Roles
    # ================================================================
    {
        "id": 50, "role": "Orchestrator / Manager Agent", "tier": 5,
        "prompt": 'You are an orchestrator. Given this user request, create an execution plan as JSON: {"plan": [{"step": N, "agent": "...", "task": "...", "depends_on": [step_ids], "priority": "critical"|"normal"}], "parallel_groups": [[step_ids]]}\n\nRequest: "Research the top 3 project management tools, write a comparison blog post, optimize it for SEO, and schedule it for publishing next Tuesday"',
        "check": "json",
        "quality_prompt": "You are an orchestrator managing 8 specialized agents. A user asks: 'Prepare a comprehensive pitch deck for our Series A fundraising. We need market research, financial projections, competitor analysis, and a polished presentation.'\n\nCreate a detailed execution plan including: which agents to invoke, in what order, what data flows between them, where human review checkpoints should be, error handling if any agent fails, and estimated total completion time.",
    },
    {
        "id": 51, "role": "Software Architect Agent", "tier": 5,
        "prompt": 'Design a high-level architecture for a real-time chat application. Respond with JSON: {"components": [{"name": "...", "technology": "...", "responsibility": "..."}], "data_flow": "...", "scaling_strategy": "...", "trade_offs": [...]}\n\nRequirements: 100K concurrent users, message delivery < 100ms, message persistence, read receipts',
        "check": "json",
        "quality_prompt": "Design the complete system architecture for a food delivery platform similar to DoorDash. Cover:\n1. Microservices decomposition with service responsibilities\n2. Technology stack recommendations with justification\n3. Database design (which DBs for which data)\n4. Real-time order tracking architecture\n5. Payment processing flow\n6. Scaling strategy for peak hours (10x normal load)\n7. Failure modes and resilience patterns\n8. Estimated infrastructure costs at different scales",
    },
    {
        "id": 52, "role": "Complex Debugger Agent", "tier": 5,
        "prompt": 'Debug this issue. The function should return unique elements but has a subtle bug. Identify the bug and fix it. Respond with JSON: {"bug_description": "...", "root_cause": "...", "fix": "corrected code"}\n\n```python\ndef get_unique(items):\n    seen = set()\n    result = []\n    for item in items:\n        if item not in seen:\n            result.append(item)\n    return result\n```',
        "check": "json",
        "quality_prompt": "Debug this distributed system issue:\n\n'Our microservices architecture has an intermittent bug: roughly 1 in 1000 orders are being charged twice. The payment service logs show single calls, but the bank records show two charges. It only happens during high traffic periods. Our services communicate via RabbitMQ, and we have a 30-second timeout on API calls. The payment confirmation webhook sometimes arrives after the timeout, causing our system to retry.'\n\nProvide: root cause analysis with diagrams (text-based), multiple potential solutions with tradeoffs, recommended fix with implementation details, and prevention strategy.",
    },
    {
        "id": 53, "role": "Legal Document Review", "tier": 5,
        "prompt": 'Review this contract clause and identify issues. Respond with JSON: {"clause_type": "...", "issues": [{"issue": "...", "severity": "high"|"medium"|"low", "recommendation": "..."}], "overall_risk": "high"|"medium"|"low"}\n\nClause: "The Service Provider shall indemnify the Client against any and all claims, damages, and losses without limitation, regardless of fault, for the duration of the agreement and for 10 years thereafter."',
        "check": "json",
        "quality_prompt": "Review this SaaS Terms of Service and identify all clauses that could be problematic for the customer. For each issue, explain the risk and suggest alternative language:\n\n1. 'We may modify these terms at any time without notice.'\n2. 'All data uploaded becomes the property of the Service.'\n3. 'The Service is provided AS-IS with no warranty of any kind.'\n4. 'Disputes shall be resolved through binding arbitration in Delaware.'\n5. 'We may terminate your account at any time for any reason.'\n6. 'Liability is limited to the fees paid in the last 30 days.'",
    },
    {
        "id": 54, "role": "Medical / Health Analysis", "tier": 5,
        "prompt": 'Analyze these lab results and provide a general health assessment as JSON: {"assessment": "...", "out_of_range": [...], "recommendations": [...], "disclaimer": "..."}\n\nResults: Glucose: 115 mg/dL (normal: 70-100), Cholesterol: 240 mg/dL (normal: <200), HDL: 45 mg/dL (normal: >60), Blood pressure: 135/88 mmHg\n\nINCLUDE DISCLAIMER that this is not medical advice.',
        "check": "json",
        "quality_prompt": "A user shares their health data and asks for analysis. Provide a thorough but responsible assessment:\n\n'I'm 45, male, BMI 28. My doctor said my A1C is 6.2% (pre-diabetic range). Fasting glucose 118. I exercise 2x/week (walking). Family history: Type 2 diabetes (father), heart disease (mother). I eat mostly processed food and drink 3 beers on weekends.'\n\nProvide: risk assessment, lifestyle modification suggestions, questions to ask their doctor, and clear disclaimers about the limitations of AI health analysis.",
    },
    {
        "id": 55, "role": "Financial Analysis / Stock Research", "tier": 5,
        "prompt": 'Analyze this financial data and respond with JSON: {"financial_health": "strong"|"moderate"|"weak", "key_ratios": {...}, "concerns": [...], "outlook": "..."}\n\nCompany data: Revenue: $10M (up 25% YoY), Net income: -$2M, Cash: $5M, Burn rate: $800K/month, Customers: 500 (up 40%), Churn: 8% monthly',
        "check": "json",
        "quality_prompt": "Perform a fundamental analysis of a hypothetical tech company with these financials and provide an investment thesis:\n\nRevenue: $50M (growing 45% YoY)\nGross margin: 72%\nNet margin: -15%\nCustomer acquisition cost: $5,000\nLifetime value: $25,000\nMarket size: $10B\nTop 3 competitors have 60% combined market share\nRecent: raised $30M Series C at $300M valuation\n\nShould an early-stage VC invest at a $400M valuation? Include bull and bear cases.",
    },
    {
        "id": 56, "role": "Security Analyst Agent", "tier": 5,
        "prompt": 'Analyze this code for security vulnerabilities. Respond with JSON: {"vulnerabilities": [{"type": "...", "severity": "critical"|"high"|"medium"|"low", "location": "...", "fix": "..."}]}\n\n```javascript\napp.get("/user", (req, res) => {\n  const userId = req.query.id;\n  const query = `SELECT * FROM users WHERE id = \'${userId}\'`;\n  db.query(query).then(user => res.json(user));\n});\n```',
        "check": "json",
        "quality_prompt": "Perform a security audit of this Node.js Express application. Identify all vulnerabilities (OWASP Top 10 and beyond), rate their severity, and provide fixes:\n\n```javascript\nconst express = require('express');\nconst app = express();\napp.use(express.json());\n\nlet sessions = {};\n\napp.post('/login', (req, res) => {\n  const {username, password} = req.body;\n  if (username === 'admin' && password === 'admin123') {\n    const token = Math.random().toString();\n    sessions[token] = username;\n    res.json({token});\n  }\n});\n\napp.get('/admin/users', (req, res) => {\n  const data = require('child_process').execSync('cat /etc/passwd').toString();\n  res.send(data);\n});\n\napp.post('/upload', (req, res) => {\n  const filename = req.body.filename;\n  require('fs').writeFileSync(`/uploads/${filename}`, req.body.data);\n  res.json({status: 'ok'});\n});\n```",
    },
    {
        "id": 57, "role": "SRE / Incident Response", "tier": 5,
        "prompt": 'You are an SRE. Analyze this incident and respond with JSON: {"severity": "P1"|"P2"|"P3", "root_cause": "...", "immediate_actions": [...], "long_term_fixes": [...], "affected_services": [...]}\n\nIncident: Website returning 502 errors for 30% of users. Load balancer health checks passing. Application logs show "Connection pool exhausted" and database CPU at 98%. Recent change: deployed new search feature 2 hours ago.',
        "check": "json",
        "quality_prompt": "Write a complete incident postmortem for this scenario:\n\nTimeline: Friday 5:45 PM — alerts fire for elevated 5xx errors. 6:00 PM — investigation starts, 40% of API requests failing. 6:15 PM — identified: a new caching layer deployed Thursday has a memory leak. 6:30 PM — hotfix: disabled caching, errors drop. 7:00 PM — all systems nominal. Saturday: discovered the cache was masking a slow database query that now hits the DB directly, causing elevated latency.\n\nInclude: timeline, root cause analysis, impact assessment, action items, and what processes should change to prevent recurrence.",
    },
    {
        "id": 58, "role": "Book Writing Agent", "tier": 5,
        "prompt": "Write the opening paragraph of a mystery novel set in a small coastal town. It should introduce the protagonist (a retired detective), establish the atmosphere, and hint at the central mystery. Aim for 150-200 words with literary quality.",
        "check": "length_min", "expected": 100,
        "quality_prompt": "You are writing Chapter 1 of a science fiction novel. Write the first 500 words. Requirements:\n1. Open in media res (start in the middle of action)\n2. Establish the protagonist's voice and personality\n3. World-build through showing, not telling\n4. End the chapter opening with a hook that compels the reader to continue\n5. The setting: a generation ship 200 years into an interstellar journey where something has gone wrong\n\nDemonstrate literary craft: varied sentence structure, sensory details, subtext.",
    },
    {
        "id": 59, "role": "Compliance / Regulatory Agent", "tier": 5,
        "prompt": 'Assess GDPR compliance for this scenario and respond with JSON: {"compliant": bool, "violations": [...], "required_actions": [...], "risk_level": "high"|"medium"|"low"}\n\nScenario: A company stores user emails, names, and browsing history. They share this data with 3rd-party advertisers. Their privacy policy was last updated 3 years ago. They have no data deletion process.',
        "check": "json",
        "quality_prompt": "A US healthcare startup wants to expand to the EU market. Their product is an AI-powered patient triage system. Assess their regulatory requirements covering:\n1. GDPR implications for processing health data\n2. EU AI Act classification and requirements (high-risk AI system?)\n3. Medical Device Regulation (MDR) compliance\n4. Data residency and transfer requirements\n5. Required documentation and certifications\n6. Timeline estimate for achieving compliance\n\nProvide a compliance roadmap with priorities.",
    },
]
