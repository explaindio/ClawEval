"""Phase H: Dense Constraint Tests — 10 tests with 30-50 checkpoints each.

These are upgraded versions of Phase F ceiling-effect tests where all models score 8-10/10.
Phase H uses many more checkpoints per test to create meaningful spread between strong models.
"""

PHASE_H_TESTS = [
    # =========================================================================
    # H-2: INPUT VALIDATOR — 30 edge cases
    # Phase F version: 10 checks. All models score 10/10.
    # Phase H version: 30 diverse validation edge cases including unicode,
    # injection, overflow, encoding, and format traps.
    # =========================================================================
    {
        "id": 2, "role": "Input Validator / Sanitizer", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Validate each of these 30 inputs. For each, respond VALID or INVALID. Respond with ONLY JSON: {"1": "VALID/INVALID", ...}

Rules:
- Email: must match user@domain.tld format, no spaces, no consecutive dots
- Phone: 10-digit US format (with or without dashes/parens), no letters
- URL: must start with http:// or https://, valid domain
- Date: YYYY-MM-DD format, must be a real calendar date
- Integer: whole numbers only, no decimals, no letters, can be negative
- Username: 3-20 chars, alphanumeric + underscore only, must start with letter

Inputs:
1. Email: "user@example.com"
2. Email: "user@.com"
3. Email: "user@exam..ple.com"
4. Email: "user @example.com"
5. Email: "user+tag@example.com"
6. Phone: "(555) 123-4567"
7. Phone: "555-123-4567"
8. Phone: "5551234567"
9. Phone: "555-123-456"
10. Phone: "1-555-123-4567"
11. Phone: "555-ABC-4567"
12. URL: "https://example.com"
13. URL: "http://sub.domain.co.uk/path?q=1"
14. URL: "ftp://files.example.com"
15. URL: "https://"
16. URL: "example.com"
17. Date: "2024-02-29"
18. Date: "2023-02-29"
19. Date: "2024-13-01"
20. Date: "2024-04-31"
21. Date: "2024-06-15"
22. Integer: "42"
23. Integer: "-7"
24. Integer: "3.14"
25. Integer: "0"
26. Integer: "12e5"
27. Integer: "9999999999999"
28. Username: "alice_99"
29. Username: "_hidden"
30. Username: "ab" """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "VALID", "2": "INVALID", "3": "INVALID", "4": "INVALID",
                "5": "VALID", "6": "VALID", "7": "VALID", "8": "VALID",
                "9": "INVALID", "10": "VALID", "11": "INVALID",
                "12": "VALID", "13": "VALID", "14": "INVALID", "15": "INVALID",
                "16": "INVALID", "17": "VALID", "18": "INVALID", "19": "INVALID",
                "20": "INVALID", "21": "VALID", "22": "VALID", "23": "VALID",
                "24": "INVALID", "25": "VALID", "26": "INVALID", "27": "VALID",
                "28": "VALID", "29": "INVALID", "30": "INVALID"
            }
        }
    },

    # =========================================================================
    # H-5: SENTIMENT ANALYSIS — 30 posts with traps
    # Phase F: 10 sentiments. All models 10/10.
    # Phase H: 30 posts including sarcasm, mixed, passive-aggressive, backhanded.
    # =========================================================================
    {
        "id": 5, "role": "Sentiment Analysis Agent", "tier": 1,
        "scoring_type": "json_values",
        "prompt": """Classify each of these 30 social media posts as POSITIVE, NEGATIVE, or NEUTRAL. Respond with ONLY JSON: {"1": "POSITIVE/NEGATIVE/NEUTRAL", ...}

Posts:
1. "Absolutely love the new update! Best feature ever!"
2. "This app is garbage. Crashes every 5 minutes."
3. "Updated to version 4.2 today."
4. "Oh great, another update that breaks everything. Thanks SO much."
5. "Not bad, not great. It works I guess."
6. "I mean, it's fine for a FREE product... you get what you pay for 🙃"
7. "Wow, they really outdid themselves this time. A whole 2 new features in 6 months!"
8. "Switched from Competitor X and honestly impressed so far."
9. "The CEO posted their quarterly results. Revenue flat YoY."
10. "Customer service was... an experience. Let's just leave it at that."
11. "Thanks for fixing the bug I reported 8 months ago. Better late than never I suppose."
12. "Just renewed my subscription for the third year."
13. "My team uses this daily and it hasn't failed us yet."
14. "The documentation is comprehensive and well-organized."
15. "Sure, it costs 3x more than alternatives, but at least the UI is pretty!"
16. "Can't believe I wasted 3 hours trying to get this to work."
17. "Interesting approach to the problem. Time will tell if it scales."
18. "The product is adequate for basic needs."
19. "I recommended this to my entire team and they all love it!"
20. "Well, that's 30 minutes of my life I'll never get back."
21. "Been a loyal user since 2019. Keep up the great work!"
22. "Honestly, I've seen better from a freshman CS project."
23. "The API response time improved from 200ms to 50ms. Nice work."
24. "They claim 99.9% uptime but we've had 3 outages this month."
25. "Meh."
26. "Version 5.0 drops next Tuesday. No details yet."
27. "This is exactly what I needed. Solved my problem in 5 minutes."
28. "I appreciate the effort, but this misses the mark entirely."
29. "The new pricing is competitive with market alternatives."
30. "Uninstalled. Going back to doing it manually. At least that works." """,
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "POSITIVE", "2": "NEGATIVE", "3": "NEUTRAL",
                "4": "NEGATIVE", "5": "NEUTRAL", "6": "NEGATIVE",
                "7": "NEGATIVE", "8": "POSITIVE", "9": "NEUTRAL",
                "10": "NEGATIVE", "11": "NEGATIVE", "12": "NEUTRAL",
                "13": "POSITIVE", "14": "POSITIVE", "15": "NEGATIVE",
                "16": "NEGATIVE", "17": "NEUTRAL", "18": "NEUTRAL",
                "19": "POSITIVE", "20": "NEGATIVE", "21": "POSITIVE",
                "22": "NEGATIVE", "23": "POSITIVE", "24": "NEGATIVE",
                "25": "NEUTRAL", "26": "NEUTRAL", "27": "POSITIVE",
                "28": "NEGATIVE", "29": "NEUTRAL", "30": "NEGATIVE"
            }
        }
    },

    # =========================================================================
    # H-9: RESEARCH / FACT-CHECKING — 30 claims with subtle traps
    # Phase F: 10 true/false claims. All models 10/10.
    # Phase H: 30 claims including near-truths, half-truths, temporal tricks.
    # =========================================================================
    {
        "id": 9, "role": "Research / Web Search Agent", "tier": 2,
        "scoring_type": "json_values",
        "prompt": """Fact-check these 30 claims. For each, respond TRUE or FALSE. Respond with ONLY JSON: {"1": "TRUE/FALSE", ...}

Claims:
1. The Great Wall of China is visible from the International Space Station with the naked eye.
2. Honey never spoils — archaeologists found 3000-year-old edible honey in Egyptian tombs.
3. Lightning never strikes the same place twice.
4. Mount Everest is the tallest mountain measured from sea level.
5. Humans have five senses: sight, hearing, taste, touch, and smell.
6. The Amazon River is the longest river in the world.
7. Bananas are berries in botanical classification.
8. Goldfish have a memory span of about 3 seconds.
9. The Sahara Desert is the largest desert on Earth.
10. Water always boils at 100°C (212°F).
11. Diamonds are made from compressed coal.
12. The Great Pyramid of Giza was the tallest man-made structure for over 3,800 years.
13. Humans share approximately 50% of their DNA with bananas.
14. Glass is a slow-moving liquid.
15. Chameleons change color primarily for camouflage.
16. The tongue has distinct regions for different tastes (tongue map).
17. Einstein failed math in school.
18. Octopuses have three hearts.
19. Vikings wore horned helmets.
20. The Earth's core is hotter than the surface of the Sun.
21. Bats are blind.
22. Dogs can only see in black and white.
23. Napoleon Bonaparte was unusually short for his time.
24. Cracking your knuckles causes arthritis.
25. Sharks can detect a single drop of blood from a mile away.
26. The speed of light is exactly 299,792,458 meters per second.
27. Bronze is an alloy of copper and tin.
28. Pluto was classified as a planet until 2006.
29. The human body contains more bacterial cells than human cells.
30. Sound travels faster through water than through air.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "FALSE", "2": "TRUE", "3": "FALSE", "4": "TRUE",
                "5": "FALSE", "6": "FALSE", "7": "TRUE", "8": "FALSE",
                "9": "FALSE", "10": "FALSE", "11": "FALSE", "12": "TRUE",
                "13": "TRUE", "14": "FALSE", "15": "FALSE", "16": "FALSE",
                "17": "FALSE", "18": "TRUE", "19": "FALSE", "20": "TRUE",
                "21": "FALSE", "22": "FALSE", "23": "FALSE", "24": "FALSE",
                "25": "FALSE", "26": "TRUE", "27": "TRUE", "28": "TRUE",
                "29": "TRUE", "30": "TRUE"
            }
        }
    },

    # =========================================================================
    # H-12: CONTENT PLANNER — 30 constraints
    # Phase F: 10 constraints. All models 10/10.
    # Phase H: 30 tightly interlocking constraints with cross-dependencies.
    # =========================================================================
    {
        "id": 12, "role": "Content Planner / Strategist", "tier": 2,
        "scoring_type": "content_planner",
        "prompt": """Create a 6-week content calendar for a B2B SaaS cybersecurity company. Output as JSON: {"weeks": [{"week": 1, "theme": "...", "posts": [{"day": "Mon/Tue/...", "type": "blog/social/email/video/podcast", "topic": "...", "channel": "blog/twitter/linkedin/email/youtube/spotify"}]}]}

ALL 30 constraints must be met:
1. Exactly 4 posts per week (24 total)
2. No posts on weekends (Sat/Sun)
3. At least 1 blog per week
4. At least 1 social media post per week
5. Exactly 6 blogs total
6. Exactly 8 social media posts total
7. Exactly 4 emails total
8. Exactly 4 video posts total
9. Exactly 2 podcast episodes total
10. Each blog must be preceded by a related social post within 2 days before
11. No two blogs on the same day of the week across all 6 weeks
12. At least 2 different channels per week
13. No more than 2 consecutive days with posts in any week
14. Week themes: W1=Awareness, W2=Education, W3=Social Proof, W4=Technical Deep Dive, W5=Engagement, W6=Conversion
15. Emails only in weeks 1, 3, 5, 6
16. Videos only in weeks 2, 3, 4, 5
17. Podcasts in weeks 3 and 6 only
18. No email and blog on the same day
19. At least 1 LinkedIn post per week
20. Twitter posts cannot be on Mondays
21. YouTube videos must be on Wednesdays or Thursdays
22. Podcasts must be on Fridays
23. No more than 1 blog per week
24. Each week must use at least 3 different content types
25. Week 1 must start with a social post on Monday
26. Week 6 must end with an email on Friday
27. No consecutive video posts across weeks
28. Blog topics must relate to cybersecurity (mention: threats, compliance, or security)
29. At least 2 weeks must include both a social post AND an email
30. Total LinkedIn posts across all weeks: exactly 6""",
        "scoring": {
            "type": "content_planner",
            "answers": {
                "total_posts": "24",
                "no_weekends": "true",
                "blogs_per_week_min": "1",
                "social_per_week_min": "1",
                "total_blogs": "6",
                "total_social": "8",
                "total_emails": "4",
                "total_videos": "4",
                "total_podcasts": "2",
                "blog_preceded_by_social": "true",
                "no_repeat_blog_day": "true",
                "channels_per_week_min": "2",
                "no_3_consecutive": "true",
                "correct_themes": "true",
                "email_weeks_correct": "true",
                "video_weeks_correct": "true",
                "podcast_weeks_correct": "true",
                "no_email_blog_same_day": "true",
                "linkedin_per_week_min": "1",
                "no_twitter_monday": "true",
                "youtube_wed_thu": "true",
                "podcast_friday": "true",
                "max_1_blog_per_week": "true",
                "min_3_types_per_week": "true",
                "w1_starts_social_monday": "true",
                "w6_ends_email_friday": "true",
                "no_consecutive_videos": "true",
                "blog_topics_cyber": "true",
                "social_and_email_weeks_min_2": "true",
                "total_linkedin": "6"
            }
        }
    },

    # =========================================================================
    # H-18: NEWS AGGREGATION — 20 headlines, 8 errors
    # Phase F: 8 headlines, 2 errors. All models 10/10.
    # Phase H: 20 headlines with 8 subtle factual errors to detect.
    # =========================================================================
    {
        "id": 18, "role": "News Aggregation Agent", "tier": 2,
        "scoring_type": "news_errors",
        "prompt": """These 20 news headlines describe events from recent years. Exactly 7 contain factual errors. Identify ALL 7 headlines with errors and explain each error. Respond as JSON: {"errors": [{"id": N, "error": "explanation"}, ...], "clean": [list of IDs with NO errors]}

Headlines:
1. "Tesla CEO Elon Musk Announces Plans for Mars Colony by 2030"
2. "Amazon Acquires Whole Foods for $13.7 Billion in Historic Deal"
3. "Microsoft Acquires GitHub for $7.5 Billion"
4. "Apple Reaches $1 Trillion Market Cap — First US Company to Do So"
5. "Boeing 737 MAX Grounded After Two Fatal Crashes, Lion Air and British Airways"
6. "NASA's Perseverance Rover Lands on Venus in February 2021"
7. "COVID-19 Vaccine: Pfizer-BioNTech First to Receive FDA Emergency Authorization"
8. "SpaceX Successfully Lands Reusable Rocket Booster on Drone Ship"
9. "Facebook Rebrands as Meta Platforms in October 2022"
10. "CRISPR Gene Editing Pioneer Jennifer Doudna Wins Nobel Prize in Physics"
11. "OpenAI Releases ChatGPT, Reaching 100 Million Users in Two Months"
12. "Japan Hosts Summer Olympics in Tokyo in 2021 After 2020 Postponement"
13. "Brexit Referendum: UK Votes 52-48 to Leave the European Union"
14. "Disney Launches Streaming Service Hulu+ to Compete with Netflix"
15. "Google's DeepMind AI AlphaGo Defeats World Chess Champion"
16. "Instagram Surpasses 2 Billion Monthly Active Users"
17. "WHO Declares COVID-19 a Pandemic on March 11, 2020"
18. "Uber Goes Public with IPO on New York Stock Exchange"
19. "Shanghai Hosts the 2022 Winter Olympics in China"
20. "TikTok Parent Company ByteDance Founded in Beijing, China" """,
        "scoring": {
            "type": "news_errors",
            "answers": {
                "error_5": "British Airways should be Ethiopian Airlines",
                "error_6": "Perseverance landed on Mars, not Venus",
                "error_9": "Meta rebrand was October 2021, not 2022",
                "error_10": "Doudna won Nobel Prize in Chemistry, not Physics",
                "error_14": "Disney launched Disney+, not Hulu+",
                "error_15": "AlphaGo defeated Go champion, not chess champion",
                "error_19": "2022 Winter Olympics were in Beijing, not Shanghai"
            }
        }
    },

    # =========================================================================
    # H-36: CODE GENERATION — 3 functions, 30 test cases
    # Phase F: 1 function, 10 tests. All models 10/10.
    # Phase H: 3 functions with edge cases, type traps, and performance.
    # =========================================================================
    {
        "id": 36, "role": "Code Generation Agent", "tier": 3,
        "scoring_type": "code_exec",
        "prompt": """Write THREE Python functions. Provide ONLY the function definitions, no imports, no examples, no test code.

1. `merge_overlapping(intervals)` — Merge overlapping intervals.
   - Input: list of [start, end] pairs (integers), possibly unsorted
   - Output: sorted list of merged [start, end] pairs
   - Handle: empty list, single interval, touching intervals (e.g., [1,3],[3,5] → [1,5]), negative numbers, duplicates

2. `eval_rpn(tokens)` — Evaluate Reverse Polish Notation expression.
   - Input: list of strings, each is a number or operator (+, -, *, /)
   - Output: integer result (truncate toward zero for division, like Python's int())
   - Handle: negative numbers as tokens, division truncation toward zero (not floor)

3. `deep_flatten(nested)` — Deeply flatten any nested structure of lists/tuples.
   - Input: arbitrarily nested list/tuple of integers
   - Output: flat list of integers in order
   - Handle: empty lists, mixed list/tuple nesting, deeply nested (10+ levels)""",
        "scoring": {
            "type": "code_exec",
            "test_cases": [
                # merge_overlapping: 10 cases
                {"call": "merge_overlapping([[1,3],[2,6],[8,10],[15,18]])", "expected": "[[1,6],[8,10],[15,18]]"},
                {"call": "merge_overlapping([[1,4],[4,5]])", "expected": "[[1,5]]"},
                {"call": "merge_overlapping([])", "expected": "[]"},
                {"call": "merge_overlapping([[5,5]])", "expected": "[[5,5]]"},
                {"call": "merge_overlapping([[3,6],[1,2],[2,4],[8,9]])", "expected": "[[1,6],[8,9]]"},
                {"call": "merge_overlapping([[-3,0],[-1,2],[4,6]])", "expected": "[[-3,2],[4,6]]"},
                {"call": "merge_overlapping([[1,10],[2,3],[4,5],[6,7]])", "expected": "[[1,10]]"},
                {"call": "merge_overlapping([[1,2],[1,2],[1,2]])", "expected": "[[1,2]]"},
                {"call": "merge_overlapping([[0,0],[1,1],[2,2]])", "expected": "[[0,0],[1,1],[2,2]]"},
                {"call": "merge_overlapping([[1,100],[2,3],[50,60],[99,101]])", "expected": "[[1,101]]"},
                # eval_rpn: 10 cases
                {"call": "eval_rpn(['2','1','+','3','*'])", "expected": "9"},
                {"call": "eval_rpn(['4','13','5','/','+'])", "expected": "6"},
                {"call": "eval_rpn(['10','6','9','3','+','-11','*','/','*','17','+','5','+'])", "expected": "22"},
                {"call": "eval_rpn(['3','4','-'])", "expected": "-1"},
                {"call": "eval_rpn(['7'])", "expected": "7"},
                {"call": "eval_rpn(['-3','4','+'])", "expected": "1"},
                {"call": "eval_rpn(['6','-3','/'])", "expected": "-2"},
                {"call": "eval_rpn(['7','-3','/'])", "expected": "-2"},
                {"call": "eval_rpn(['0','5','/'])", "expected": "0"},
                {"call": "eval_rpn(['15','7','-','2','/'])", "expected": "4"},
                # deep_flatten: 10 cases
                {"call": "deep_flatten([1,[2,[3,[4,[5]]]]])", "expected": "[1,2,3,4,5]"},
                {"call": "deep_flatten([])", "expected": "[]"},
                {"call": "deep_flatten([1,2,3])", "expected": "[1,2,3]"},
                {"call": "deep_flatten([[],[],[]])", "expected": "[]"},
                {"call": "deep_flatten([1,(2,[3,(4,)])])", "expected": "[1,2,3,4]"},
                {"call": "deep_flatten([[[[[[10]]]]]])", "expected": "[10]"},
                {"call": "deep_flatten([1,[],2,[3,[],4],5])", "expected": "[1,2,3,4,5]"},
                {"call": "deep_flatten([(1,2),(3,4)])", "expected": "[1,2,3,4]"},
                {"call": "deep_flatten([0,[-1,[-2,[-3]]]])", "expected": "[0,-1,-2,-3]"},
                {"call": "deep_flatten([[1,2],[3,[4,[5,[6,[7,[8,[9,[10]]]]]]]]])", "expected": "[1,2,3,4,5,6,7,8,9,10]"},
            ]
        }
    },

    # =========================================================================
    # H-40: FACT-CHECKING — 30 claims with adversarial near-truths
    # Phase F: 10 claims. All models 10/10.
    # Phase H: 30 claims with subtle traps, near-truths, and temporal tricks.
    # =========================================================================
    {
        "id": 40, "role": "Fact-Checking Agent", "tier": 3,
        "scoring_type": "json_values",
        "prompt": """Classify each claim as TRUE or FALSE. Respond with ONLY JSON: {"1": "TRUE/FALSE", ...}

Claims:
1. The speed of sound at sea level in dry air at 20°C is approximately 343 meters per second.
2. Water expands when it freezes.
3. The chemical formula for table salt is NaCl.
4. Venus is the closest planet to the Sun.
5. Pi (π) is exactly equal to 22/7.
6. DNA stands for deoxyribonucleic acid.
7. The human body has 206 bones at birth.
8. Photosynthesis converts CO2 and water into glucose and oxygen.
9. The Atlantic Ocean is the largest ocean on Earth.
10. Absolute zero is -273.15°C.
11. Electric current flows from positive to negative terminal (conventional current).
12. A prime number is divisible only by 1 and itself; 1 is prime.
13. The chemical symbol for gold is Au.
14. Mercury is the only metal that is liquid at standard room temperature.
15. The mitochondria is often called the powerhouse of the cell.
16. The Pythagorean theorem applies to all triangles.
17. The atomic number of carbon is 6.
18. Light travels faster in water than in a vacuum.
19. Helium is the second most abundant element in the observable universe.
20. TCP/IP is a connection-oriented protocol.
21. HTML is a programming language.
22. RAM is a form of volatile memory.
23. The binary representation of decimal 10 is 1010.
24. HTTP status code 404 means "Server Error."
25. SHA-256 produces a 256-bit hash output.
26. IPv6 addresses are 128 bits long.
27. A byte consists of 8 bits.
28. The OSI model has 7 layers.
29. SQL is a Turing-complete language in its standard form.
30. JSON natively supports comments.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "1": "TRUE", "2": "TRUE", "3": "TRUE", "4": "FALSE",
                "5": "FALSE", "6": "TRUE", "7": "FALSE", "8": "TRUE",
                "9": "FALSE", "10": "TRUE", "11": "TRUE", "12": "FALSE",
                "13": "TRUE", "14": "FALSE", "15": "TRUE", "16": "FALSE",
                "17": "TRUE", "18": "FALSE", "19": "TRUE", "20": "TRUE",
                "21": "FALSE", "22": "TRUE", "23": "TRUE", "24": "FALSE",
                "25": "TRUE", "26": "TRUE", "27": "TRUE", "28": "TRUE",
                "29": "FALSE", "30": "FALSE"
            }
        }
    },

    # =========================================================================
    # H-48: STEM ANALYSIS — 15 multi-step problems
    # Phase F: 5 problems. All models 10/10.
    # Phase H: 15 problems with unit conversions, multi-step, trap answers.
    # =========================================================================
    {
        "id": 48, "role": "STEM Research Analyst", "tier": 4,
        "scoring_type": "json_numeric",
        "prompt": """Solve these 15 STEM problems. Respond as JSON: {"p1": answer, ...}. Round all answers to 2 decimal places.

p1: A car accelerates from 0 to 60 mph in 8 seconds. What is the acceleration in m/s²? (1 mph = 0.44704 m/s)
p2: How much energy (in joules) is needed to heat 2.5 kg of water from 20°C to 100°C? (specific heat = 4186 J/(kg·°C))
p3: A circle has a circumference of 31.4159 cm. What is its area in cm²?
p4: If a projectile is launched at 45° with initial velocity 20 m/s, what is the maximum height in meters? (g = 9.8 m/s²)
p5: Calculate the pH of a 0.001 M HCl solution.
p6: What is the wavelength (in meters) of a photon with energy 3.0 eV? (h = 6.626e-34 J·s, c = 3e8 m/s, 1 eV = 1.602e-19 J)
p7: A resistor of 100 ohms and a capacitor of 10 µF are in series in an RC circuit. What is the time constant in milliseconds?
p8: How many moles are in 50 grams of calcium carbonate (CaCO₃)? (Ca=40, C=12, O=16)
p9: A pendulum has length 2.0 meters. What is its period in seconds on Earth? (g=9.8 m/s², T=2π√(L/g))
p10: What is the kinetic energy in joules of a 1500 kg car traveling at 100 km/h?
p11: Calculate the molarity of a solution made by dissolving 5.85 g of NaCl (MW=58.44) in water to make 500 mL of solution.
p12: A 5 kg block slides down a frictionless 30° incline. What is its acceleration in m/s²?
p13: What is the de Broglie wavelength (in nanometers) of an electron (m=9.109e-31 kg) moving at 1e6 m/s? (h=6.626e-34)
p14: How many liters of CO₂ at STP are produced from burning 1 mole of propane (C₃H₈)? (C₃H₈ + 5O₂ → 3CO₂ + 4H₂O, 1 mol gas = 22.4 L at STP)
p15: What is the escape velocity (in km/s) from Earth's surface? (M=5.972e24 kg, R=6.371e6 m, G=6.674e-11)""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "p1": 3.35, "p2": 836800.0, "p3": 78.54, "p4": 10.20,
                "p5": 3.0, "p6": 4.14e-7, "p7": 1.0, "p8": 0.50,
                "p9": 2.84, "p10": 578703.70, "p11": 0.20, "p12": 4.90,
                "p13": 0.73, "p14": 67.2, "p15": 11.19
            },
            "tolerance": 0.5
        }
    },

    # =========================================================================
    # H-49: ALGORITHM — 3 algorithms, 30 test cases
    # Phase F: 1 algo, 10 tests. All models 10/10.
    # Phase H: 3 algorithms with adversarial edge cases.
    # =========================================================================
    {
        "id": 49, "role": "Algorithm / Data Structure Explorer", "tier": 4,
        "scoring_type": "code_exec",
        "prompt": """Write THREE Python data structure implementations. Provide ONLY class/function definitions, no imports needed, no test code.

1. `class LRUCache(capacity)` — Least Recently Used Cache with O(1) operations.
   - `get(key)` → returns value or -1 if not found. Mark as recently used.
   - `put(key, value)` → insert/update. If at capacity, evict least recently used.

2. `class MinStack` — Stack that supports push, pop, top, and get_min in O(1).
   - `push(val)`, `pop()`, `top()` → standard stack operations
   - `get_min()` → return minimum element currently in stack

3. `def find_median(stream)` — Given a list of integers arriving as a stream, return the running median after each element as a list of floats.
   - Input: list of integers
   - Output: list of floats — median after processing each element
   - Example: [2,1,3] → [2.0, 1.5, 2.0]""",
        "scoring": {
            "type": "code_exec",
            "test_cases": [
                # LRUCache: 10 cases
                {"call": "c = LRUCache(2); c.put(1,1); c.put(2,2); r = c.get(1); r", "expected": "1"},
                {"call": "c = LRUCache(2); c.put(1,1); c.put(2,2); c.get(1); c.put(3,3); r = c.get(2); r", "expected": "-1"},
                {"call": "c = LRUCache(2); c.put(1,1); c.put(2,2); c.get(1); c.put(3,3); r = c.get(1); r", "expected": "1"},
                {"call": "c = LRUCache(1); c.put(1,10); c.put(2,20); r = c.get(1); r", "expected": "-1"},
                {"call": "c = LRUCache(1); c.put(1,10); c.put(2,20); r = c.get(2); r", "expected": "20"},
                {"call": "c = LRUCache(2); c.put(1,1); c.put(1,10); r = c.get(1); r", "expected": "10"},
                {"call": "c = LRUCache(3); c.put(1,1); c.put(2,2); c.put(3,3); c.get(2); c.put(4,4); r = c.get(1); r", "expected": "-1"},
                {"call": "c = LRUCache(3); c.put(1,1); c.put(2,2); c.put(3,3); c.get(2); c.put(4,4); r = c.get(2); r", "expected": "2"},
                {"call": "c = LRUCache(2); r = c.get(99); r", "expected": "-1"},
                {"call": "c = LRUCache(2); c.put(1,1); c.put(2,2); c.put(1,100); c.put(3,3); r = c.get(2); r", "expected": "-1"},
                # MinStack: 10 cases
                {"call": "s = MinStack(); s.push(-2); s.push(0); s.push(-3); r = s.get_min(); r", "expected": "-3"},
                {"call": "s = MinStack(); s.push(-2); s.push(0); s.push(-3); s.pop(); r = s.top(); r", "expected": "0"},
                {"call": "s = MinStack(); s.push(-2); s.push(0); s.push(-3); s.pop(); r = s.get_min(); r", "expected": "-2"},
                {"call": "s = MinStack(); s.push(5); r = s.get_min(); r", "expected": "5"},
                {"call": "s = MinStack(); s.push(3); s.push(3); s.push(3); s.pop(); r = s.get_min(); r", "expected": "3"},
                {"call": "s = MinStack(); s.push(1); s.push(2); s.push(3); r = s.get_min(); r", "expected": "1"},
                {"call": "s = MinStack(); s.push(3); s.push(2); s.push(1); s.pop(); s.pop(); r = s.get_min(); r", "expected": "3"},
                {"call": "s = MinStack(); s.push(0); s.push(0); s.pop(); r = s.get_min(); r", "expected": "0"},
                {"call": "s = MinStack(); s.push(-1); s.push(-2); r = s.top(); r", "expected": "-2"},
                {"call": "s = MinStack(); s.push(10); s.push(5); s.push(1); s.push(0); s.pop(); s.pop(); r = s.get_min(); r", "expected": "5"},
                # find_median: 10 cases
                {"call": "find_median([2,1,3])", "expected": "[2.0, 1.5, 2.0]"},
                {"call": "find_median([5])", "expected": "[5.0]"},
                {"call": "find_median([1,2])", "expected": "[1.0, 1.5]"},
                {"call": "find_median([3,1,2])", "expected": "[3.0, 2.0, 2.0]"},
                {"call": "find_median([1,1,1,1])", "expected": "[1.0, 1.0, 1.0, 1.0]"},
                {"call": "find_median([5,4,3,2,1])", "expected": "[5.0, 4.5, 4.0, 3.5, 3.0]"},
                {"call": "find_median([1,2,3,4,5])", "expected": "[1.0, 1.5, 2.0, 2.5, 3.0]"},
                {"call": "find_median([-1,-2,-3])", "expected": "[-1.0, -1.5, -2.0]"},
                {"call": "find_median([10,20,30,40])", "expected": "[10.0, 15.0, 20.0, 25.0]"},
                {"call": "find_median([100])", "expected": "[100.0]"},
            ]
        }
    },

    # =========================================================================
    # H-56: SECURITY ANALYST — 15 vulnerabilities in complex code
    # Phase F: 5 vulns. All models 10/10.
    # Phase H: 15 vulns across a larger, more realistic code sample.
    # =========================================================================
    {
        "id": 56, "role": "Security Analyst Agent", "tier": 5,
        "scoring_type": "security_vulns",
        "prompt": """Find ALL security vulnerabilities in this Python web application code. There are exactly 15 vulnerabilities. For each, identify the type and affected line/function. Respond as JSON: {"vulnerabilities": [{"type": "...", "location": "...", "severity": "critical/high/medium/low"}], "count": 15}

```python
import os, sqlite3, pickle, subprocess, hashlib, yaml
from flask import Flask, request, jsonify, render_template_string, send_file

app = Flask(__name__)
DB = "users.db"
SECRET = "admin123"
UPLOAD_DIR = "/tmp/uploads"

def get_db():
    return sqlite3.connect(DB)

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]
    db = get_db()
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"
    result = db.execute(query).fetchone()
    if result:
        return jsonify({"token": hashlib.md5(user.encode()).hexdigest()})
    return "Unauthorized", 401

@app.route("/profile/<username>")
def profile(username):
    template = f"<h1>Welcome {username}</h1><p>Your profile page</p>"
    return render_template_string(template)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"<html><body>Results for: {q}</body></html>"

@app.route("/run", methods=["POST"])
def run_command():
    cmd = request.json.get("command")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"output": result.stdout})

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)
    return jsonify({"saved": path})

@app.route("/download")
def download():
    filepath = request.args.get("path")
    return send_file(filepath)

@app.route("/config", methods=["POST"])
def load_config():
    data = request.get_data()
    config = yaml.load(data)
    return jsonify(config)

@app.route("/session", methods=["POST"])
def restore_session():
    data = request.get_data()
    session = pickle.loads(data)
    return jsonify({"user": session.get("user")})

@app.route("/admin")
def admin():
    token = request.args.get("token")
    if token == SECRET:
        return "Admin panel"
    return "Forbidden", 403

@app.route("/export")
def export_data():
    fmt = request.args.get("format", "csv")
    cmd = f"python3 export.py --format {fmt}"
    os.system(cmd)
    return "Exported"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
```""",
        "scoring": {
            "type": "security_vulns",
            "vulns": [
                {"type": "SQL injection", "location": "login"},
                {"type": "hardcoded secret", "location": "SECRET"},
                {"type": "weak hashing/MD5", "location": "login/token"},
                {"type": "SSTI/template injection", "location": "profile"},
                {"type": "XSS/reflected", "location": "search"},
                {"type": "command injection", "location": "run_command"},
                {"type": "path traversal/upload", "location": "upload"},
                {"type": "path traversal/download", "location": "download"},
                {"type": "unsafe YAML load", "location": "load_config"},
                {"type": "pickle deserialization", "location": "restore_session"},
                {"type": "command injection/os.system", "location": "export_data"},
                {"type": "debug mode in production", "location": "app.run"},
                {"type": "binding to all interfaces", "location": "app.run/0.0.0.0"},
                {"type": "plaintext password storage", "location": "login/query"},
                {"type": "no authentication on /run", "location": "run_command"}
            ]
        }
    },
]
