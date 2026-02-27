"""Tier 2: Moderate Complexity Roles (27 tests, IDs 9-35)"""

TIER2_TESTS = [
    {
        "id": 9, "role": "Research / Web Search Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Fact-check these 10 claims. For each, respond TRUE or FALSE. Respond with ONLY JSON: {"1": "TRUE/FALSE", ...}

1. The Great Wall of China is visible from space with the naked eye.
2. Honey never spoils — archaeologists found 3000-year-old edible honey in Egyptian tombs.
3. Lightning never strikes the same place twice.
4. Goldfish have a 3-second memory span.
5. Humans use only 10% of their brains.
6. Bananas are berries in botanical classification.
7. The Sahara Desert is the largest desert on Earth.
8. Octopuses have three hearts.
9. Glass is a slow-moving liquid.
10. Mount Everest is the tallest mountain on Earth measured from base to peak.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "FALSE", "2": "TRUE", "3": "FALSE", "4": "FALSE",
                "5": "FALSE", "6": "TRUE", "7": "FALSE", "8": "TRUE",
                "9": "FALSE", "10": "FALSE"
            }
        }
    },
    {
        "id": 10, "role": "Content Writer / Blog Writer", "tier": 2,
        "scoring_type": "manual",
        "prompt": """Write a 300-400 word blog post about "Why Remote Teams Should Use Async Communication" that:
1. Opens with a surprising statistic or counterintuitive statement
2. Uses exactly 3 subheadings (## format)
3. Includes one concrete example/case study (can be hypothetical but realistic)
4. Ends with a clear call-to-action
5. Maintains a professional but conversational tone

Write the full blog post now.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "opens_with_hook", "has_3_subheadings", "has_example",
                "has_cta", "professional_tone", "word_count_300_400",
                "logical_flow", "no_filler", "actionable_advice", "engaging"
            ]
        }
    },
    {
        "id": 11, "role": "Editor Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """This text has EXACTLY 10 errors. Find ALL 10. Respond as JSON: {"errors": [{"type": "grammar/factual/logic/style", "location": "...", "error": "...", "fix": "..."}], "count": 10}

Text:
"The Eiffel Tower, completed in 1889 for the World's Fair, stands at 1,063 feet tall in the heart of London. Designed by Gustave Eiffel, it was originally planned to be temporary and was almost demolished in 1909. The tower recieves approximately 7 million visitors annually, making it one of the most visited paid monument in the world. It's made entirely of copper, weighing around 10,100 tons. The tower has three levels, but visitors can only access two of them. During winter, it shrinks by 6 inches due to thermal contraction — this is because metal always expands when it gets cold. The tower is repainted every 7 years using 60 tons of paint, and have been 18 different colors throughout it's history." """,
        "scoring": {
            "type": "error_detection",
            "errors": [
                {"type": "factual", "text": "London", "fix": "Paris"},
                {"type": "grammar", "text": "recieves", "fix": "receives"},
                {"type": "grammar", "text": "visited paid monument", "fix": "visited paid monuments"},
                {"type": "factual", "text": "copper", "fix": "iron/steel"},
                {"type": "factual", "text": "can only access two", "fix": "can access all three"},
                {"type": "logic", "text": "expands when it gets cold", "fix": "contracts when cold"},
                {"type": "grammar", "text": "have been", "fix": "has been"},
                {"type": "grammar", "text": "it's history", "fix": "its history"},
                {"type": "factual", "text": "18 different colors", "fix": "about 3-4 colors"},
                {"type": "style", "text": "approximately 7 million", "fix": "approximately 6-7 million"}
            ]
        }
    },
    {
        "id": 12, "role": "Content Planner", "tier": 2,
        "scoring_type": "constraint",
        "prompt": """Create a 4-week content calendar for a B2B SaaS company. Output as a table with columns: Week, Day, Type, Topic, Channel.

Constraints (ALL must be met):
1. Exactly 3 posts per week (12 total)
2. No posts on weekends (Sat/Sun)
3. At least 1 blog post per week
4. At least 1 social media post per week
5. Each blog must be preceded by a related social post within 2 days before
6. Week themes: W1=Awareness, W2=Education, W3=Engagement, W4=Conversion
7. No two blogs on the same day of the week across the 4 weeks
8. At least 2 different channels used per week (blog, twitter, linkedin, email)
9. Total: exactly 4 blogs, exactly 5 social posts, exactly 3 emails
10. No more than 2 consecutive days with posts in any week

Verify each constraint at the end with a numbered checklist.""",
        "scoring": {
            "type": "content_calendar_constraints",
            "checks": [
                "exactly_12_posts", "no_weekends", "1_blog_per_week",
                "1_social_per_week", "blog_preceded_by_social",
                "correct_themes", "no_repeat_blog_day",
                "2_channels_per_week", "correct_type_counts",
                "no_3_consecutive"
            ]
        }
    },
    {
        "id": 13, "role": "Email Drafting / Summarization", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Rank these 8 emails by urgency (P1=critical to P4=low). Respond with ONLY JSON: {"1": "P1/P2/P3/P4", ...}

1. Subject: "SERVER DOWN" — "Production database cluster is unreachable. All customer-facing services returning 500 errors since 3:42 PM."
2. Subject: "Quick question" — "Hey, where did you put the Q3 slides? Need them for tomorrow's board meeting."
3. Subject: "FYI: Office snacks" — "New snack options in the kitchen! We added trail mix and dried mango."
4. Subject: "URGENT: Contract expires today" — "The enterprise license with Acme Corp ($2.4M ARR) expires at midnight. Legal needs sign-off."
5. Subject: "Weekly digest" — "Here's your weekly summary of completed tickets and sprint progress."
6. Subject: "Re: Vacation request" — "Approved! Enjoy your time off next month."
7. Subject: "Security alert" — "Unusual login detected from IP in Russia on admin account. MFA was bypassed."
8. Subject: "Lunch plans?" — "Anyone want to try the new Thai place?" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "P1", "2": "P2", "3": "P4", "4": "P1",
                "5": "P4", "6": "P3", "7": "P1", "8": "P4"
            }
        }
    },
    {
        "id": 14, "role": "Document Summarization", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Read this report excerpt and answer these 10 specific questions. Respond as JSON: {"q1": answer, "q2": answer, ...}

Report:
"TechStart Inc. completed its Series B funding round on March 15, 2025, raising $45 million at a $280 million pre-money valuation. Lead investor was Sequoia Capital with $20M. Existing investors Andreessen Horowitz and Y Combinator contributed $15M and $10M respectively. The company will use 40% of funds for R&D, 35% for sales expansion, and 25% for infrastructure. Current ARR is $12.4 million with 340 enterprise customers, up from $8.1M ARR and 210 customers at Series A. Gross margin improved from 68% to 74% year-over-year. The company employs 185 people across 3 offices (SF, Austin, London). Headcount is expected to reach 300 by Q4 2025. Churn rate decreased from 4.2% to 2.8% monthly."

q1: Post-money valuation in millions?
q2: How much did A16Z invest?
q3: What percentage goes to sales expansion?
q4: Customer growth from Series A to B (count)?
q5: Current gross margin percentage?
q6: Pre-money valuation in millions?
q7: What is the current ARR in millions?
q8: How many employees will they have by Q4 2025?
q9: Monthly churn rate improvement (percentage points)?
q10: Total amount raised?""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "q1": 325, "q2": 15, "q3": 35, "q4": 130,
                "q5": 74, "q6": 280, "q7": 12.4, "q8": 300,
                "q9": 1.4, "q10": 45
            },
            "tolerance": 0.5
        }
    },
    {
        "id": 15, "role": "Meeting Notes / Transcription Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Extract ALL action items from this transcript. Respond as JSON: {"action_items": [{"owner": "Name", "task": "...", "deadline": "..."}], "count": N}

Transcript:
"Sarah: OK let's wrap up. So Mike, you'll have the API docs updated by Friday right?
Mike: Yeah, Friday EOD works. I'll also need to coordinate with the DevOps team on the staging deploy.
Sarah: Good. Lisa, can you finish the user research report?
Lisa: Sure, I can have the draft by Wednesday. But I need access to the analytics dashboard first.
Sarah: Mike, can you get Lisa access today?
Mike: I'll submit the ticket this afternoon.
Sarah: Perfect. Tom, what about the security audit?
Tom: I'm waiting on the pen test results from CrowdStrike. Should have those by Thursday. Once I have them, I need two days to compile the report — so security audit report by next Monday.
Sarah: Sounds good. Oh, and everyone — please submit your Q4 OKRs by next Tuesday. I need to send them to leadership by Wednesday.
Lisa: Also, I forgot to mention — we need someone to review the onboarding flow changes. 
Sarah: Tom, can you handle that? By end of next week?
Tom: Sure, I can review the onboarding flow by next Friday." """,
        "scoring": {
            "type": "action_items",
            "expected": [
                {"owner": "Mike", "task": "API docs"},
                {"owner": "Mike", "task": "Lisa access"},
                {"owner": "Lisa", "task": "user research"},
                {"owner": "Tom", "task": "security audit"},
                {"owner": "Everyone", "task": "Q4 OKRs"},
                {"owner": "Tom", "task": "onboarding flow"},
                {"owner": "Sarah", "task": "OKRs to leadership"},
                {"owner": "Mike", "task": "staging deploy"}
            ]
        }
    },
    {
        "id": 16, "role": "Social Media Scouting / Monitoring", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Classify each social post by sentiment AND identify which are crisis-level (need immediate response). Respond as JSON: {"posts": {"1": {"sentiment": "pos/neg/neutral", "crisis": true/false}, ...}, "crisis_count": N}

Posts about "AcmeTech":
1. "Just upgraded to AcmeTech Pro — the new dashboard is so much cleaner!"
2. "Been waiting 3 WEEKS for AcmeTech support to respond. Still nothing. #worst"
3. "AcmeTech quarterly earnings in line with expectations. Stock flat."
4. "BREAKING: AcmeTech user data leaked — 500K accounts exposed. Changing my password NOW."
5. "The AcmeTech API is pretty solid for what it is. Standard stuff."
6. "AcmeTech CEO caught using company funds for personal trips. Thread: 🧵"
7. "My team switched from Competitor to AcmeTech last month. No regrets."
8. "AcmeTech app has been down for 6 hours. Our entire workflow is blocked. @AcmeTech FIX THIS"
9. "Interesting comparison of AcmeTech vs alternatives in this blog post."
10. "Love the new AcmeTech integration with Slack. Game changer for our team." """,
        "scoring": {
            "type": "social_monitoring",
            "answers": {
                "1": {"sentiment": "pos", "crisis": False},
                "2": {"sentiment": "neg", "crisis": False},
                "3": {"sentiment": "neutral", "crisis": False},
                "4": {"sentiment": "neg", "crisis": True},
                "5": {"sentiment": "neutral", "crisis": False},
                "6": {"sentiment": "neg", "crisis": True},
                "7": {"sentiment": "pos", "crisis": False},
                "8": {"sentiment": "neg", "crisis": True},
                "9": {"sentiment": "neutral", "crisis": False},
                "10": {"sentiment": "pos", "crisis": False},
            },
            "expected_crisis_count": 3
        }
    },
    {
        "id": 17, "role": "Social Media Content Agent", "tier": 2,
        "scoring_type": "manual",
        "prompt": """Create a 5-post social media campaign for a new AI coding assistant product launch. Each post must be for a different platform (Twitter/X, LinkedIn, Instagram, Reddit, TikTok script).

Requirements per post:
- Twitter: Max 280 chars, include 2 hashtags
- LinkedIn: Professional tone, 100-200 words
- Instagram: Caption with 5+ relevant hashtags, describe the image you'd pair with it
- Reddit: Title + body for r/programming, authentic community voice (no marketing speak)
- TikTok: 30-second script with visual directions

Generate all 5 posts now.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "has_5_posts", "twitter_under_280", "twitter_has_hashtags",
                "linkedin_professional", "linkedin_length",
                "instagram_has_hashtags", "reddit_authentic",
                "tiktok_has_script", "consistent_messaging", "engaging"
            ]
        }
    },
    {
        "id": 18, "role": "News Aggregation Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """These 8 news headlines are about the same event. Group the duplicates and identify the 2 that contain factual errors. Respond as JSON: {"groups": [[list of IDs], ...], "errors": [{"id": N, "error": "..."}]}

Headlines:
1. "SpaceX Launches 60 Starlink Satellites from Cape Canaveral"
2. "Elon Musk's SpaceX Sends 60 Satellites Into Orbit from Kennedy Space Center"
3. "NASA Launches 60 Starlink Satellites in Record Mission"
4. "SpaceX Starlink Mission Deploys 60 Satellites from Florida"
5. "SpaceX Launch: 60 New Starlink Satellites Join Constellation"
6. "Blue Origin Deploys 60 Starlink Satellites in Successful Launch"
7. "Florida Launch: SpaceX Adds 60 More Starlink Satellites to Network"
8. "SpaceX Starlink Deployment: 60 Satellites Reach Orbit" """,
        "scoring": {
            "type": "news_dedup",
            "error_ids": [3, 6],
            "error_reasons": ["NASA didn't launch Starlink", "Blue Origin didn't launch Starlink"]
        }
    },
    {
        "id": 19, "role": "Shopping / Price Comparison", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Rank these 5 laptop deals by TRUE total cost (cheapest first). Calculate the actual total including all fees. Respond as JSON: {"ranking": [id, id, ...], "totals": {"1": N, "2": N, ...}}

Deals:
1. MacBook Air M3 — $1,099 + free shipping + 2yr AppleCare ($199 included) = advertised "from $1,099"
2. Dell XPS 15 — $1,249 - 15% coupon + $49.99 shipping + $129 2yr warranty = advertised "from $1,061"  
3. ThinkPad X1 — $1,399 - $200 instant rebate - $100 student discount + free shipping + free 3yr warranty = advertised "from $1,099"
4. HP Spectre — $999 + $79.99 shipping + $149 2yr warranty + $29.99 recycling fee = advertised "from $999"
5. ASUS ZenBook — $1,149 - 10% loyalty discount + free shipping + $99 1yr extended warranty = advertised "from $1,034"

Show your math for each. Include ALL costs.""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "1": 1099.00,
                "2": 1240.64,
                "3": 1099.00,
                "4": 1257.98,
                "5": 1133.10
            },
            "tolerance": 5.0,
            "ranking": [1, 3, 5, 2, 4]
        }
    },
    {
        "id": 20, "role": "Memory / Knowledge Management", "tier": 2,
        "scoring_type": "exact",
        "prompt": """I told you these facts in previous sessions. Answer all 10 questions from memory. Respond as JSON: {"q1": answer, ...}

Session 1 facts: My name is Alex. I work at Terraform Labs as a senior engineer. My team has 8 people. Our main project is called "Phoenix". I prefer Python over Rust.

Session 2 facts: We released Phoenix v2.3 last Tuesday. The release had 3 critical bugs. My manager's name is Dana. Our sprint length is 2 weeks. Our office is in Portland.

Session 3 facts: I adopted a cat named Pixel last month. The Phoenix project budget is $1.2M. We use PostgreSQL for our main database. Our deployment target is AWS us-west-2. I have 6 years of experience.

Questions:
q1: What is my name?
q2: What is my job title?
q3: What version of Phoenix was just released?
q4: How many critical bugs were in the release?
q5: What is my manager's name?
q6: What is my cat's name?
q7: What database do we use?
q8: What AWS region do we deploy to?
q9: Which programming language do I prefer?
q10: What is the Phoenix project budget?""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "q1": "Alex", "q2": "senior engineer", "q3": "2.3",
                "q4": "3", "q5": "Dana", "q6": "Pixel",
                "q7": "PostgreSQL", "q8": "us-west-2", "q9": "Python",
                "q10": "$1.2M"
            }
        }
    },
    {
        "id": 21, "role": "RAG / Retrieval Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Answer these 5 questions using ONLY the provided context. If the answer isn't in the context, say "NOT_FOUND". Respond as JSON: {"q1": "answer", ...}

Context:
[Doc 1] "CloudBase pricing: Starter plan $29/mo (5 users, 10GB). Growth plan $79/mo (25 users, 100GB). Enterprise plan: custom pricing, starts at $299/mo (unlimited users, 1TB). All plans include email support. Phone support available on Growth+ plans. Annual billing gives 20% discount."

[Doc 2] "CloudBase SLA: 99.95% uptime guarantee for Enterprise. 99.9% for Growth. No SLA for Starter. Credit policy: 10x credit for downtime exceeding SLA. Maximum credit per month: 30% of monthly fee."

[Doc 3] "CloudBase security: SOC 2 Type II certified. Data encrypted AES-256 at rest, TLS 1.3 in transit. GDPR compliant. HIPAA BAA available for Enterprise only. Data centers in US-East, EU-West, AP-Southeast."

Questions:
q1: What is the annual cost of the Growth plan?
q2: Maximum credit a Growth customer can get per month for downtime?
q3: Is HIPAA BAA available on the Growth plan?
q4: What encryption is used for data in transit?
q5: How many data centers does CloudBase have?""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "q1": "758.40",
                "q2": "23.70",
                "q3": "No",
                "q4": "TLS 1.3",
                "q5": "3"
            }
        }
    },
    {
        "id": 22, "role": "Data Analysis Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Calculate these 10 metrics from the dataset. Respond as JSON: {"m1": value, ...}. Round to 2 decimal places.

Sales Data (product, units, price_each, cost_each, region):
Widget-A, 150, $25.00, $12.50, North
Widget-A, 200, $25.00, $12.50, South
Widget-B, 80, $45.00, $22.00, North
Widget-B, 120, $45.00, $22.00, East
Widget-C, 300, $15.00, $8.00, South
Widget-C, 50, $15.00, $8.00, West
Gadget-X, 90, $60.00, $30.00, North
Gadget-X, 110, $60.00, $30.00, East

Metrics:
m1: Total revenue (all products)
m2: Total cost of goods sold
m3: Overall profit margin percentage
m4: Revenue from North region
m5: Best-selling product by units
m6: Most profitable product by total profit dollars
m7: Average price across all products (weighted by units)
m8: Total units sold
m9: Revenue from Widget products only
m10: Highest margin product (margin %)""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "m1": 28600.00,
                "m2": 14210.00,
                "m3": 50.31,
                "m4": 14150.00,
                "m5": "Widget-C",
                "m6": "Widget-A",
                "m7": 26.00,
                "m8": 1100,
                "m9": 16600.00,
                "m10": "Widget-C"
            },
            "tolerance": 1.0
        }
    },
    {
        "id": 23, "role": "Website Scraping / Understanding", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Extract the structured data from this HTML fragment. Respond as JSON with the exact values found.

```html
<div class="product-listing">
  <div class="product" data-sku="SKU-7291">
    <h2 class="name">Wireless Noise-Canceling Headphones</h2>
    <span class="price" data-currency="USD">$149.99</span>
    <span class="price-original">$199.99</span>
    <div class="rating" data-score="4.7">★★★★★ (2,341 reviews)</div>
    <span class="stock in-stock">In Stock</span>
    <ul class="features">
      <li>40hr battery life</li>
      <li>Bluetooth 5.3</li>
      <li>Active Noise Cancellation</li>
    </ul>
  </div>
</div>
```

Extract: {"sku": "...", "name": "...", "price": N, "original_price": N, "discount_pct": N, "rating": N, "review_count": N, "in_stock": true/false, "feature_count": N, "bluetooth_version": "..."}""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "sku": "SKU-7291",
                "name": "Wireless Noise-Canceling Headphones",
                "price": 149.99,
                "original_price": 199.99,
                "discount_pct": 25.0,
                "rating": 4.7,
                "review_count": 2341,
                "in_stock": True,
                "feature_count": 3,
                "bluetooth_version": "5.3"
            },
            "tolerance": 0.5
        }
    },
    {
        "id": 24, "role": "Image Description / Understanding", "tier": 2,
        "scoring_type": "manual",
        "prompt": """Describe precisely what you would expect to see in a professional product photo for a "premium wireless gaming mouse" based on these specifications. Be extremely detailed about visual appearance. This is for generating an image prompt.

Specs: Matte black body, RGB side strip (cyan glow), honeycomb pattern perforated shell, USB-C charging port (front), 5 programmable buttons, DPI switch button (top), weight: 67g ultralight, size: 126 x 64 x 40mm, cable: braided paracord (detachable).

Describe: exact visual layout, materials, textures, lighting setup for the photo, camera angle, background.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "mentions_matte_black", "mentions_rgb_cyan", "mentions_honeycomb",
                "mentions_usbc", "mentions_buttons", "mentions_dpi_switch",
                "describes_lighting", "describes_angle", "describes_background",
                "professional_detail"
            ]
        }
    },
    {
        "id": 25, "role": "Customer Support Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Classify these 5 support tickets by category and priority. Respond as JSON: {"tickets": {"1": {"category": "...", "priority": "P1/P2/P3"}, ...}}

Categories: billing, technical, account, feature_request, security

1. "I can't log in even though I'm entering the right password. I've tried resetting it 3 times. My account has $50,000 worth of data."
2. "Can you add dark mode to the mobile app? It would be really nice."
3. "I was charged $99 instead of the $49 promotional price I signed up for."
4. "Someone logged into my account from Brazil and I'm in the US. I see transactions I didn't make."
5. "The export function gives a blank CSV when I try to download my monthly report." """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1_category": "account", "1_priority": "P1",
                "2_category": "feature_request", "2_priority": "P3",
                "3_category": "billing", "3_priority": "P2",
                "4_category": "security", "4_priority": "P1",
                "5_category": "technical", "5_priority": "P2"
            }
        }
    },
    {
        "id": 26, "role": "Lead Scoring / Prospecting", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Score these 5 leads 1-100 and rank them. Respond as JSON: {"scores": {"1": N, "2": N, ...}, "ranking": [id, id, ...]}

Scoring criteria:
- Company size (1-25 pts): Enterprise 500+ = 25, Mid 100-499 = 15, Small <100 = 5
- Budget confirmed (0/20 pts): Yes = 20, No = 0  
- Decision maker (0/20 pts): C-level = 20, VP = 15, Director = 10, Manager = 5, Unknown = 0
- Timeline (1-20 pts): This month = 20, This quarter = 15, This year = 10, Exploring = 5
- Engagement (1-15 pts): Demo requested = 15, Downloaded whitepaper = 10, Visited pricing = 5, Just browsing = 1

Leads:
1. Acme Corp (2,000 emp), CFO reached out, budget approved, wants to start this month, requested demo
2. StartupXYZ (15 emp), founder exploring options, no budget yet, timeline "sometime this year", visited pricing page
3. MegaCo (10,000 emp), IT Manager inquired, budget pending, this quarter timeline, downloaded whitepaper
4. GrowthCo (250 emp), VP Sales interested, budget confirmed, this quarter, requested demo
5. TinyCo (8 emp), unknown contact, no budget, just browsing, no engagement""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "1": 100, "2": 20, "3": 55, "4": 85, "5": 6
            },
            "tolerance": 5,
            "ranking": [1, 4, 3, 2, 5]
        }
    },
    {
        "id": 27, "role": "Sprint / Project Summarizer", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Calculate sprint metrics from this data. Respond as JSON with exact values.

Sprint 14 (2-week, 5 devs):
Committed: 45 story points
Completed stories: API-101(5sp), API-102(3sp), API-103(8sp), UI-201(3sp), UI-202(5sp), UI-203(2sp), BUG-301(1sp), BUG-302(2sp), BUG-303(3sp)
Carried over (incomplete): API-104(5sp), UI-204(8sp)
Added mid-sprint: BUG-304(2sp, completed), HOTFIX-401(1sp, completed)

Bugs found: 7 (3 critical, 4 minor)
Days: 10 working days
Blockers: 2 (resolved on day 3 and day 7)

{"velocity": N, "commitment_pts": N, "completed_pts": N, "completion_rate": N, "carryover_pts": N, "scope_change_pts": N, "pts_per_dev": N, "bug_ratio": N, "stories_completed": N, "stories_total": N}""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "velocity": 35,
                "commitment_pts": 45,
                "completed_pts": 35,
                "completion_rate": 77.78,
                "carryover_pts": 13,
                "scope_change_pts": 3,
                "pts_per_dev": 7.0,
                "bug_ratio": 0.64,
                "stories_completed": 11,
                "stories_total": 13
            },
            "tolerance": 1.0
        }
    },
    {
        "id": 28, "role": "Transaction / Approval Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Approve or reject each transaction based on these rules. Respond as JSON: {"1": "APPROVE/REJECT", "2": ...}

Rules:
- Max single transaction: $5,000
- Max daily total per user: $10,000
- Transactions > $2,000 require manager approval (assume not given)
- International transactions blocked outside business hours (9AM-5PM local)
- Same merchant twice in 1 hour = flag as duplicate → REJECT
- Round-dollar amounts > $1,000 are suspicious → REJECT

User "jsmith" today (local time is 2PM):
1. $450 at Amazon.com (domestic) at 9:15 AM
2. $2,500 at Dell.com (domestic) at 10:00 AM
3. $150 at Starbucks at 10:30 AM
4. $3,000.00 at BestBuy.com (domestic) at 11:00 AM
5. $800 at Amazon.com (domestic) at 11:02 AM
6. €1,200 at Booking.com (international) at 3:00 PM
7. $5,100 at Apple.com (domestic) at 3:30 PM
8. $450 at Amazon.com (domestic) at 3:45 PM
9. $2,000.00 at NewEgg.com (domestic) at 4:00 PM
10. €500 at Ryanair.com (international) at 9:30 PM""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "APPROVE", "2": "REJECT", "3": "APPROVE",
                "4": "REJECT", "5": "APPROVE", "6": "APPROVE",
                "7": "REJECT", "8": "APPROVE", "9": "REJECT",
                "10": "REJECT"
            }
        }
    },
    {
        "id": 29, "role": "Home Automation Agent", "tier": 2,
        "scoring_type": "constraint",
        "prompt": """Create automation rules for this smart home scenario. Respond as JSON array of rules.

Scenario: 3BR house, 2 occupants (Alice works 9-5, Bob works from home), pets (1 cat).

Required automations (must cover ALL 10):
1. Morning routine: lights on gradually 6:30AM weekdays, 8AM weekends
2. Thermostat: 72°F when occupied, 65°F when empty, 68°F sleeping (11PM-6AM)
3. Security: arm when both away, disarm when either returns (use phone geofencing)
4. Pet care: auto-feeder at 7AM and 6PM, turn on cat camera when both away
5. Energy: solar panels priority during peak (2-7PM), battery backup evening
6. Lighting: motion-activated hallway lights 10PM-6AM (dim 20%), off after 5 min
7. Bob's office: turn on desk lamp and set A/C to 70°F when computer turns on
8. Laundry: notify when washer/dryer cycle complete
9. Water leak detector: shut off main valve + alert both phones immediately
10. Guest mode: temporary door code, raise thermostat to 72°F, enable guest WiFi

Each rule needs: trigger, conditions, actions. Format as structured JSON.""",
        "scoring": {
            "type": "home_automation",
            "checks": [
                "has_morning_routine", "has_thermostat_logic",
                "has_security_arm_disarm", "has_pet_care",
                "has_energy_management", "has_motion_lights",
                "has_office_automation", "has_laundry_notify",
                "has_leak_detection", "has_guest_mode"
            ]
        }
    },
    {
        "id": 30, "role": "Fitness / Health Tracking", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Calculate these fitness metrics from the 7-day log. Respond as JSON with exact values.

Log (activity, duration_min, calories, avg_hr):
Mon: Run 30min 320cal 155bpm, Weights 45min 280cal 125bpm
Tue: Swim 40min 400cal 140bpm
Wed: Rest day
Thu: Cycling 60min 550cal 145bpm, Yoga 30min 120cal 95bpm
Fri: Run 45min 480cal 160bpm
Sat: Hike 120min 750cal 130bpm
Sun: Weights 60min 380cal 130bpm

Resting HR: 62bpm. Max HR: 190bpm. Weight: 175lbs.

{"total_calories": N, "total_active_minutes": N, "avg_daily_calories": N, "active_days": N, "max_hr_pct": N, "zone_2_minutes": N, "zone_4_minutes": N, "total_sessions": N, "calories_per_minute_avg": N, "rest_days": N}

HR Zones: Z1(<60% max), Z2(60-70%), Z3(70-80%), Z4(80-90%), Z5(90%+)
60%=114, 70%=133, 80%=152, 90%=171""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "total_calories": 3280,
                "total_active_minutes": 430,
                "avg_daily_calories": 468.57,
                "active_days": 6,
                "max_hr_pct": 84.21,
                "zone_2_minutes": 255,
                "zone_4_minutes": 75,
                "total_sessions": 8,
                "calories_per_minute_avg": 7.63,
                "rest_days": 1
            },
            "tolerance": 2.0
        }
    },
    {
        "id": 31, "role": "Recipe / Cooking Agent", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Scale this recipe from 4 servings to 7 servings. Calculate exact quantities. Respond as JSON: {"ingredient": "amount unit", ...}

Original recipe (4 servings):
- 2 cups all-purpose flour
- 1.5 tsp baking powder
- 0.5 tsp salt
- 3/4 cup butter (1.5 sticks)
- 1 1/3 cups sugar
- 3 large eggs
- 1 cup whole milk
- 2 tsp vanilla extract
- 1/4 cup cocoa powder

Scale factor: 7/4 = 1.75

Give amounts rounded to nearest practical kitchen measurement (nearest 1/4 tsp, 1/4 cup, or 1/4 stick).""",
        "scoring": {
            "type": "recipe_scaling",
            "answers": {
                "flour_cups": 3.5,
                "baking_powder_tsp": 2.625,
                "salt_tsp": 0.875,
                "butter_cups": 1.3125,
                "sugar_cups": 2.333,
                "eggs": 5.25,
                "milk_cups": 1.75,
                "vanilla_tsp": 3.5,
                "cocoa_cups": 0.4375
            },
            "tolerance": 0.3
        }
    },
    {
        "id": 32, "role": "Personal Finance Tracking", "tier": 2,
        "scoring_type": "exact",
        "prompt": """Calculate financial metrics. Respond as JSON with values rounded to 2 decimals.

Monthly income: $7,500 (net after tax)
Expenses:
- Rent: $1,800
- Car payment: $425
- Car insurance: $180
- Groceries: $650
- Utilities: $220
- Internet: $80
- Phone: $85
- Streaming: $45
- Gym: $50
- Dining out: $380
- Gas: $200
- Student loan: $350
- Credit card min: $150
- Savings: $500

Credit card balance: $4,200 at 22.99% APR
Student loan balance: $28,000 at 5.5% APR
Savings account: $8,500

{"total_expenses": N, "savings_rate": N, "discretionary_spending": N, "fixed_costs": N, "debt_to_income": N, "emergency_fund_months": N, "cc_monthly_interest": N, "net_worth_estimate": N, "remaining_after_expenses": N, "needs_vs_wants_ratio": N}""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "total_expenses": 5115,
                "savings_rate": 6.67,
                "discretionary_spending": 475,
                "fixed_costs": 3140,
                "debt_to_income": 429.33,
                "emergency_fund_months": 1.66,
                "cc_monthly_interest": 80.47,
                "net_worth_estimate": -23700,
                "remaining_after_expenses": 1885,
                "needs_vs_wants_ratio": 6.61
            },
            "tolerance": 50.0
        }
    },
    {
        "id": 33, "role": "SEO Optimization Agent", "tier": 2,
        "scoring_type": "constraint",
        "prompt": """Generate complete SEO metadata for a page about "Best Project Management Tools for Remote Teams 2025". Respond as JSON.

Required fields:
1. title_tag (50-60 chars, includes primary keyword)
2. meta_description (150-160 chars, includes CTA)
3. h1 (different from title_tag but includes keyword)
4. slug (URL-friendly, hyphens, lowercase)
5. og_title (for social sharing)
6. og_description (for social sharing)
7. canonical_url (full URL using domain example.com)
8. schema_type (appropriate Schema.org type)
9. focus_keywords (array of 5 related keywords)
10. internal_links_suggested (3 related page paths)

All fields must be populated and valid.""",
        "scoring": {
            "type": "seo_constraints",
            "checks": [
                "title_length", "title_has_keyword",
                "description_length", "description_has_cta",
                "h1_different_from_title", "slug_valid",
                "og_fields_present", "canonical_valid",
                "has_5_keywords", "has_3_internal_links"
            ]
        }
    },
    {
        "id": 34, "role": "Landing Page Generator", "tier": 2,
        "scoring_type": "manual",
        "prompt": """Generate the HTML structure (no CSS/JS needed, just semantic HTML) for a SaaS landing page for "TaskFlow — AI-Powered Project Management". Include:

1. Navigation with logo, 4 menu items, and CTA button
2. Hero section with headline, subheadline, CTA, and trust badges
3. 3-column features section
4. Pricing table with 3 tiers (Free, Pro, Enterprise)
5. Testimonials section (3 quotes)
6. FAQ accordion section (5 questions)
7. Final CTA section
8. Footer with links

Write the complete semantic HTML.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "has_nav", "has_hero", "has_features",
                "has_pricing_3_tiers", "has_testimonials",
                "has_faq", "has_final_cta", "has_footer",
                "semantic_html", "proper_heading_hierarchy"
            ]
        }
    },
    {
        "id": 35, "role": "Travel Planning Agent", "tier": 2,
        "scoring_type": "constraint",
        "prompt": """Plan a 5-day trip to Tokyo. Budget: $3,000 total (flights excluded). Respond as a day-by-day JSON itinerary.

Constraints (ALL must be satisfied):
1. Budget breakdown: accommodation ≤ $800, food ≤ $500, activities ≤ $700, transport ≤ $200, misc ≤ $300. Total ≤ $3,000.
2. At least 1 activity per day
3. No activity before 8AM or after 10PM
4. Include at least: 1 temple, 1 museum, 1 food market, 1 nature spot, 1 shopping district
5. Travel time between consecutive activities ≤ 45 minutes
6. Lunch break (12-2PM) every day
7. 2 dinners at sit-down restaurants, 3 at casual/street food
8. Mix of traditional and modern Tokyo experiences
9. One half-day free/flexible time
10. Accommodation in Shinjuku area (central)

Format: {"days": [{"day": 1, "activities": [{"time": "HH:MM", "name": "...", "duration_hrs": N, "cost": N, "category": "..."}], "accommodation_cost": N, "food_cost": N}], "total_cost": N}""",
        "scoring": {
            "type": "travel_constraints",
            "checks": [
                "budget_total", "budget_breakdown", "1_activity_per_day",
                "time_bounds", "required_activities",
                "travel_time", "lunch_break", "dinner_mix",
                "traditional_modern", "free_time"
            ]
        }
    },
]
