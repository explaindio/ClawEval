"""Phase H Dense Tests — Batch 7: Tests 10, 17, 24, 34, 41, 58 (previously manual-review, now automated)"""

PHASE_H_BATCH7 = [
    # H-10: CONTENT WRITER — 20 structural constraints
    {
        "id": 10, "role": "Content Writer / Blog Writer", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Write a blog post about "Why Remote Work Is Here to Stay in 2025". 

ALL 20 constraints must be met:
1. Title must contain "Remote Work" and "2025"
2. Must have exactly 5 sections with H2 headings
3. Include at least 3 specific statistics with sources (e.g., "According to Gallup...")
4. Total word count between 800-1200 words
5. Include an introduction paragraph (before first H2)
6. Include a conclusion paragraph (after last H2)
7. Mention at least 3 specific companies by name (e.g., Google, Microsoft)
8. Include at least 2 counterarguments (challenges of remote work)
9. Each section must have at least 2 paragraphs
10. Use at least 3 bullet or numbered lists
11. Include at least 2 quotes (real or attributed to a named person/title)
12. Mention productivity data or research
13. Mention mental health or work-life balance
14. Mention technology tools (at least 2 specific tools like Zoom, Slack)
15. Include a call-to-action in the conclusion
16. Use transition phrases between sections (e.g., "Moreover", "However", "Furthermore")
17. Mention cost savings (for employees or companies)
18. Reference the COVID-19 pandemic as a catalyst
19. Include at least 1 comparison (e.g., "compared to", "vs", "unlike")
20. No section should be fewer than 100 words

Respond in markdown format with clear H2 headings.""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "has_remote_work_title": "yes",
                "has_2025_title": "yes",
                "has_5_h2_sections": "yes",
                "has_3_statistics": "yes",
                "has_introduction": "yes",
                "has_conclusion": "yes",
                "has_3_companies": "yes",
                "has_2_counterarguments": "yes",
                "has_2_paragraphs_per_section": "yes",
                "has_3_lists": "yes",
                "has_2_quotes": "yes",
                "has_productivity_data": "yes",
                "has_mental_health": "yes",
                "has_2_tech_tools": "yes",
                "has_call_to_action": "yes",
                "has_transitions": "yes",
                "has_cost_savings": "yes",
                "has_covid_reference": "yes",
                "has_comparison": "yes",
                "sections_min_100_words": "yes"
            }
        }
    },

    # H-17: SOCIAL MEDIA CONTENT — 20 post constraints
    {
        "id": 17, "role": "Social Media Content Agent", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Create a 5-day social media content calendar for a SaaS project management tool called "TaskFlow". Respond as JSON:
{"days": [{"day": 1, "platform": "...", "post_type": "...", "content": "...", "hashtags": [...], "cta": "...", "time": "..."}]}

ALL 20 constraints must be met:
1. Exactly 5 days of content
2. Must cover at least 3 different platforms (Twitter/X, LinkedIn, Instagram, TikTok, Facebook)
3. Each post must include 3-5 relevant hashtags
4. Each post must have a clear call-to-action (CTA)
5. Include at least 1 video content post
6. Include at least 1 carousel/infographic post
7. Include at least 1 user testimonial or social proof post
8. Each post must specify optimal posting time (e.g., "10:00 AM EST")
9. At least 1 post must mention a competitor comparison
10. Include at least 1 educational/how-to post
11. At least 1 post must include emoji usage
12. Include at least 1 promotional/discount post
13. No two consecutive days should use the same platform
14. At least 1 post must reference a trending topic or industry news
15. Each content piece must be under 280 characters (Twitter-compatible length)
16. Include at least 1 poll or question-based engagement post
17. Hashtags must include #ProjectManagement or #Productivity in at least 3 posts
18. At least 1 post must target enterprise/B2B audience
19. Include at least 1 behind-the-scenes or team culture post
20. CTA must vary (not the same CTA repeated)""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "has_5_days": "yes",
                "has_3_platforms": "yes",
                "has_hashtags_per_post": "yes",
                "has_cta_per_post": "yes",
                "has_video_post": "yes",
                "has_carousel_post": "yes",
                "has_testimonial": "yes",
                "has_posting_times": "yes",
                "has_competitor_mention": "yes",
                "has_educational_post": "yes",
                "has_emoji": "yes",
                "has_promo_post": "yes",
                "no_consecutive_same_platform": "yes",
                "has_trending_topic": "yes",
                "under_280_chars": "yes",
                "has_poll_question": "yes",
                "has_pm_hashtag": "yes",
                "has_b2b_targeting": "yes",
                "has_behind_scenes": "yes",
                "has_varied_cta": "yes"
            }
        }
    },

    # H-24: IMAGE DESCRIPTION — 20 analysis checkpoints
    {
        "id": 24, "role": "Image Description / Understanding", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """You are an image description agent. Given this detailed scene description, produce a comprehensive accessibility description and analysis. Respond as JSON:
{"description": "...", "objects": [...], "colors": [...], "mood": "...", "composition": "...", "accessibility_alt_text": "...", "detailed_analysis": {...}}

Scene to describe (imagine you are seeing this photograph):
A busy Tokyo street crossing (Shibuya-style) at dusk. Neon signs in Japanese and English cover buildings on both sides. A large digital billboard shows an anime advertisement. Dozens of pedestrians cross in multiple directions — some carrying umbrellas (it's lightly raining). A yellow taxi waits at the crossing. Street lights reflect off wet pavement. A convenience store (7-Eleven) is visible on the corner. Power lines cross overhead. A businessman in a dark suit checks his phone while walking. A group of school students in uniforms stand at the corner.

ALL 20 analysis points must be covered:
1. Mention the location (Tokyo/Shibuya crossing)
2. Time of day (dusk/evening)
3. Weather condition (rain)
4. Count of major object categories (people, vehicles, buildings, signs)
5. Dominant colors (neon, wet reflections)
6. Mood/atmosphere (busy, urban, vibrant)
7. The taxi (color and position)
8. The 7-Eleven store
9. The anime billboard
10. The businessman with phone
11. The school students in uniforms
12. The umbrellas
13. The wet pavement reflections
14. Power lines
15. Japanese and English text on signs
16. Composition analysis (foreground/midground/background)
17. Lighting analysis (artificial neon + natural dusk)
18. Cultural elements (Japanese urban culture)
19. Accessibility alt-text (concise, under 125 characters)
20. Suggested image tags for SEO (at least 8 tags)""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "mentions_tokyo": "yes",
                "mentions_dusk": "yes",
                "mentions_rain": "yes",
                "has_object_count": "yes",
                "mentions_neon_colors": "yes",
                "mentions_busy_atmosphere": "yes",
                "mentions_taxi": "yes",
                "mentions_7eleven": "yes",
                "mentions_anime_billboard": "yes",
                "mentions_businessman_phone": "yes",
                "mentions_students_uniforms": "yes",
                "mentions_umbrellas": "yes",
                "mentions_wet_reflections": "yes",
                "mentions_power_lines": "yes",
                "mentions_bilingual_signs": "yes",
                "has_composition_analysis": "yes",
                "has_lighting_analysis": "yes",
                "mentions_japanese_culture": "yes",
                "has_alt_text": "yes",
                "has_seo_tags": "yes"
            }
        }
    },

    # H-34: LANDING PAGE GENERATOR — 20 structural elements
    {
        "id": 34, "role": "Landing Page Generator", "tier": 2,
        "scoring_type": "h_keywords",
        "prompt": """Generate the complete HTML structure for a SaaS landing page for an AI writing assistant called "QuillAI". Respond with the full HTML code.

ALL 20 structural constraints must be met:
1. Must include a hero section with headline, subheadline, and CTA button
2. Include a navigation bar with at least 4 links (Features, Pricing, Testimonials, Contact)
3. Features section with at least 4 feature cards, each with an icon placeholder, title, and description
4. Pricing section with exactly 3 tiers (Free, Pro, Enterprise) with prices
5. Testimonials section with at least 3 testimonials including name, role, and quote
6. FAQ section with at least 5 question-answer pairs
7. Footer with copyright, social media links, and legal links (Privacy, Terms)
8. Must include a <meta name="description"> tag
9. Must include a <title> tag containing "QuillAI"
10. At least 1 email signup/newsletter form with input field and submit button
11. Mobile-responsive viewport meta tag
12. At least 2 CTA buttons with different text (e.g., "Start Free Trial", "Get Started")
13. Include social proof (e.g., "Trusted by 10,000+ users" or company logos section)
14. Include a "How it Works" section with at least 3 steps
15. Use semantic HTML elements (header, nav, main, section, footer)
16. Include at least 1 anchor link that scrolls to a section
17. Contact section or link with email address
18. Must mention AI or artificial intelligence in the hero section
19. Include accessibility attributes (alt text on images, aria labels)
20. Include at least 1 comparison or "before/after" element""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "has_hero_section": "yes",
                "has_navbar_4_links": "yes",
                "has_4_feature_cards": "yes",
                "has_3_pricing_tiers": "yes",
                "has_3_testimonials": "yes",
                "has_5_faq": "yes",
                "has_footer_links": "yes",
                "has_meta_description": "yes",
                "has_title_quillai": "yes",
                "has_email_form": "yes",
                "has_viewport_meta": "yes",
                "has_2_cta_buttons": "yes",
                "has_social_proof": "yes",
                "has_how_it_works": "yes",
                "has_semantic_html": "yes",
                "has_anchor_links": "yes",
                "has_contact_email": "yes",
                "has_ai_mention_hero": "yes",
                "has_accessibility_attrs": "yes",
                "has_comparison_element": "yes"
            }
        }
    },

    # H-41: CRITIC / REVIEW AGENT — 20 review checkpoints
    {
        "id": 41, "role": "Critic / Review Agent", "tier": 3,
        "scoring_type": "h_keywords",
        "prompt": """Write a comprehensive critical review of this Python code repository structure. Respond as JSON:
{"overall_score": N, "categories": [{...}], "critical_issues": [...], "recommendations": [...]}

Repository structure and key files:
```
myapp/
├── app.py (500 lines, all routes + business logic + DB queries in one file)
├── config.py (hardcoded DB_PASSWORD = "admin123", API_KEY = "sk-xxx")
├── utils.py (200 lines, mix of string helpers, date parsing, API calls, file I/O)
├── test_app.py (50 lines, only 3 test functions, no mocking)
├── requirements.txt (flask, requests, sqlalchemy — no version pinning)
├── README.md (empty except "TODO: add docs")
├── .env.example (missing)
├── Dockerfile (FROM python:3.8, uses root user, no multi-stage build)
├── database.py (raw SQL queries with string formatting: f"SELECT * FROM users WHERE id={user_id}")
└── deploy.sh (contains AWS credentials inline, chmod 777 on all files)
```

ALL 20 review points must be addressed:
1. Score overall code quality (1-10 with justification)
2. Identify the SQL injection vulnerability in database.py
3. Flag the hardcoded credentials in config.py
4. Critique the monolithic app.py (separation of concerns)
5. Flag the lack of version pinning in requirements.txt
6. Critique the insufficient test coverage
7. Flag the security issue in deploy.sh (inline AWS credentials)
8. Flag the chmod 777 security issue
9. Critique the outdated Python 3.8 in Dockerfile
10. Flag running as root in Dockerfile
11. Critique the missing .env.example
12. Critique the empty README
13. Critique the mixed responsibilities in utils.py
14. Suggest proper project structure (blueprints/modules)
15. Recommend parameterized queries for SQL
16. Recommend secrets management (environment variables or vault)
17. Recommend CI/CD pipeline additions
18. Recommend minimum test coverage percentage
19. Recommend Dockerfile improvements (multi-stage, non-root)
20. Rate severity of each issue (critical/high/medium/low)""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "has_overall_score": "yes",
                "identifies_sql_injection": "yes",
                "flags_hardcoded_credentials": "yes",
                "critiques_monolithic_app": "yes",
                "flags_no_version_pinning": "yes",
                "critiques_test_coverage": "yes",
                "flags_deploy_credentials": "yes",
                "flags_chmod_777": "yes",
                "critiques_python_38": "yes",
                "flags_root_docker": "yes",
                "critiques_missing_env": "yes",
                "critiques_empty_readme": "yes",
                "critiques_mixed_utils": "yes",
                "suggests_project_structure": "yes",
                "recommends_parameterized_queries": "yes",
                "recommends_secrets_management": "yes",
                "recommends_cicd": "yes",
                "recommends_test_coverage": "yes",
                "recommends_dockerfile_fixes": "yes",
                "has_severity_ratings": "yes"
            }
        }
    },

    # H-58: BOOK / LONG-FORM WRITING — 20 structural constraints
    {
        "id": 58, "role": "Book / Long-Form Writing", "tier": 5,
        "scoring_type": "h_keywords",
        "prompt": """Write a detailed outline for a non-fiction book titled "The AI Revolution in Small Business: A Practical Guide for 2025". Respond as JSON:
{"title": "...", "subtitle": "...", "chapters": [{"number": N, "title": "...", "sections": [...], "key_takeaway": "...", "estimated_pages": N}], "appendices": [...], "total_chapters": N, "target_audience": "...", "word_count_estimate": N}

ALL 20 constraints must be met:
1. Exactly 12 chapters
2. Each chapter must have 3-5 sections
3. Chapter 1 must be an introduction/overview
4. Chapter 12 must be a conclusion/future outlook
5. Include at least 2 chapters on specific AI tools (ChatGPT, Midjourney, etc.)
6. Include at least 1 chapter on ROI/financial impact
7. Include at least 1 chapter on ethics/risks of AI
8. Include at least 1 chapter on implementation/getting started
9. Each chapter must have a key_takeaway
10. Each chapter must have estimated_pages (5-25 range)
11. Total estimated pages must be 200-350
12. Include at least 2 appendices (glossary, resource list, etc.)
13. Specify target audience
14. Include at least 1 chapter on case studies or real examples
15. Include at least 1 chapter on hiring/team building with AI
16. Chapter progression must be logical (basics → advanced → future)
17. Include at least 1 chapter on marketing/sales with AI
18. Include at least 1 chapter on customer service/support with AI
19. Total word count estimate must be 50,000-80,000
20. Include at least 1 chapter addressing common fears/objections about AI""",
        "scoring": {
            "type": "json_values",
            "answers": {
                "has_12_chapters": "yes",
                "has_3_5_sections_each": "yes",
                "ch1_is_introduction": "yes",
                "ch12_is_conclusion": "yes",
                "has_2_tool_chapters": "yes",
                "has_roi_chapter": "yes",
                "has_ethics_chapter": "yes",
                "has_implementation_chapter": "yes",
                "has_key_takeaways": "yes",
                "has_page_estimates": "yes",
                "total_pages_200_350": "yes",
                "has_2_appendices": "yes",
                "has_target_audience": "yes",
                "has_case_studies_chapter": "yes",
                "has_hiring_chapter": "yes",
                "logical_progression": "yes",
                "has_marketing_chapter": "yes",
                "has_customer_service_chapter": "yes",
                "word_count_50k_80k": "yes",
                "has_fears_objections_chapter": "yes"
            }
        }
    },
]
