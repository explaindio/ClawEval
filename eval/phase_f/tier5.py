"""Tier 5: Complex/Multi-Domain Roles (10 tests, IDs 50-59)"""

TIER5_TESTS = [
    {
        "id": 50, "role": "Orchestrator / Manager Agent", "tier": 5,
        "scoring_type": "constraint",
        "prompt": """You are an orchestrator. Break this user request into sub-tasks and assign to specialized agents. Respond as JSON.

User request: "Create a blog post about our Q3 earnings, publish it on our website, share it on social media, and send an email newsletter to subscribers with a summary."

Available agents: writer, editor, seo, web_publisher, social_media, email_marketing, data_analyst, designer

Output: {"tasks": [{"id": "T1", "agent": "...", "action": "...", "depends_on": [], "input_from": []}], "execution_order": ["T1","T2",...], "parallel_groups": [["T1","T2"],["T3"],...]}

Rules:
1. Data must be analyzed before writing
2. Content must be written before editing
3. Editing before publishing/sharing
4. SEO optimization before web publishing
5. Social posts can parallel email
6. Each agent used at most twice
7. Must have at least 6 tasks
8. No circular dependencies
9. Designer creates social media graphics after content is ready
10. Total tasks ≤ 10""",
        "scoring": {
            "type": "orchestration_constraints",
            "checks": [
                "data_before_writing", "write_before_edit",
                "edit_before_publish", "seo_before_web",
                "social_parallel_email", "agent_usage_limit",
                "min_6_tasks", "no_circular_deps",
                "designer_after_content", "max_10_tasks"
            ]
        }
    },
    {
        "id": 51, "role": "Software Architect Agent", "tier": 5,
        "scoring_type": "constraint",
        "prompt": """Design a system architecture for a real-time chat application supporting 1M concurrent users. Respond as JSON.

Requirements:
1. Real-time messaging (< 100ms latency)
2. Message persistence and history
3. Online/offline status
4. Read receipts
5. File attachments (up to 50MB)
6. Group chats (up to 500 members)
7. End-to-end encryption
8. 99.99% uptime SLA
9. GDPR compliance
10. Horizontal scalability

Output: {"components": [{"name": "...", "technology": "...", "purpose": "...", "scaling_strategy": "..."}], "data_flow": "...", "infrastructure": {"cloud": "...", "regions": N}, "estimated_monthly_cost": "...", "bottlenecks": [...], "tradeoffs": [...]}""",
        "scoring": {
            "type": "architecture_constraints",
            "checks": [
                "has_websocket_layer", "has_message_store",
                "has_presence_service", "has_file_storage",
                "has_encryption", "has_load_balancer",
                "has_cache_layer", "has_multi_region",
                "mentions_scaling", "mentions_tradeoffs"
            ]
        }
    },
    {
        "id": 52, "role": "Complex Debugger Agent", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Find ALL 5 bugs in this code. They interact — fixing one reveals another. Respond as JSON: {"bugs": [{"description": "...", "line": N, "fix": "..."}], "root_cause_chain": "...", "count": 5}

```python
import threading

class ConnectionPool:
    def __init__(self, max_size=10):
        self.pool = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self._create_connections()
    
    def _create_connections(self):
        for i in range(self.max_size):
            self.pool.append(self._new_connection(i))
    
    def _new_connection(self, id):
        return {"id": id, "in_use": False, "created": __import__('time').time()}
    
    def acquire(self):
        for conn in self.pool:          # Bug 1: no lock
            if not conn["in_use"]:
                conn["in_use"] = True
                return conn
        return None                      # Bug 2: should block/wait, not return None
    
    def release(self, conn):
        conn["in_use"] = False           # Bug 3: no validation conn is from this pool
        
    def health_check(self):
        stale = []
        for conn in self.pool:
            age = __import__('time').time() - conn["created"]
            if age > 3600:
                stale.append(conn)
        for conn in stale:
            self.pool.remove(conn)       # Bug 4: removing during potential concurrent access
            self.pool.append(self._new_connection(conn["id"]))  # Bug 5: new conn has same ID, could conflict
        return len(stale)
```""",
        "scoring": {
            "type": "bug_detection",
            "bugs": [
                {"keyword": "lock", "detail": "acquire no lock"},
                {"keyword": "None", "detail": "should wait/block"},
                {"keyword": "validation", "detail": "release no check"},
                {"keyword": "concurrent", "detail": "remove while iterating"},
                {"keyword": "id", "detail": "reuse/conflict"}
            ]
        }
    },
    {
        "id": 53, "role": "Legal Document Review", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Find ALL 10 legal issues in this contract clause. Respond as JSON: {"issues": [{"clause": "...", "problem": "...", "risk": "high/medium/low"}], "count": 10}

Contract:
"1. TERM: This agreement is perpetual and irrevocable, effective upon verbal agreement.
2. PAYMENT: Client shall pay all invoices within 3 business days. Late payments incur 25% monthly interest.
3. IP RIGHTS: All work product, including pre-existing IP, becomes the sole property of the Client.
4. LIABILITY: Provider's total liability is unlimited for all damages including lost profits.
5. TERMINATION: Only the Client may terminate this agreement, with 0 days notice.
6. NON-COMPETE: Provider shall not work in any related industry for 10 years after termination.
7. JURISDICTION: Disputes shall be governed by the laws of the Provider's choosing at time of dispute.
8. INDEMNIFICATION: Provider shall indemnify Client against all claims, including those caused by Client's negligence.
9. CONFIDENTIALITY: Provider must keep all information confidential forever, even publicly available information.
10. FORCE MAJEURE: No force majeure clause exists."

Issues: perpetual/irrevocable, unreasonable payment terms, pre-existing IP transfer, unlimited liability, one-sided termination, excessive non-compete, vague jurisdiction, unfair indemnification, overbroad confidentiality, missing force majeure.""",
        "scoring": {
            "type": "legal_issues",
            "issues": [
                "perpetual", "payment terms", "pre-existing IP",
                "unlimited liability", "one-sided termination",
                "non-compete", "jurisdiction", "indemnification",
                "confidentiality", "force majeure"
            ]
        }
    },
    {
        "id": 54, "role": "Medical / Health Analysis", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Analyze this patient case and identify the 10 key clinical findings. Respond as JSON: {"findings": ["finding1", ...], "red_flags": ["flag1", ...], "suggested_tests": ["test1", ...]}

Patient: 55-year-old male
Chief complaint: Chest pain for 2 hours, radiating to left arm
Vitals: BP 165/95, HR 110, RR 22, SpO2 94%, Temp 98.6°F
History: Type 2 diabetes (10 years), smoker (30 pack-years), family history of MI (father at 52)
Labs: Troponin I: 0.8 ng/mL (normal <0.04), BNP: 450 pg/mL (normal <100), Glucose: 280 mg/dL, Creatinine: 1.8 mg/dL, LDL: 185 mg/dL
ECG: ST elevation in leads II, III, aVF
Current meds: Metformin 1000mg BID, no aspirin, no statin

Identify: elevated troponin (MI marker), ST elevation (inferior MI), hypertension, tachycardia, tachypnea, hypoxia, elevated BNP (heart failure), hyperglycemia, renal impairment, high LDL + no statin (undertreated).""",
        "scoring": {
            "type": "medical_findings",
            "findings": [
                "troponin elevated", "ST elevation", "hypertension",
                "tachycardia", "tachypnea", "hypoxia",
                "BNP elevated", "hyperglycemia",
                "renal impairment", "LDL high"
            ]
        }
    },
    {
        "id": 55, "role": "Financial Analysis / Stock Research", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Calculate these 10 financial ratios. Respond as JSON with values rounded to 2 decimals.

Income Statement (Annual):
- Revenue: $850M, COGS: $510M, Gross Profit: $340M
- Operating Expenses: $170M, Operating Income: $170M
- Interest Expense: $25M, Tax (25%): $36.25M
- Net Income: $108.75M
- Shares Outstanding: 50M

Balance Sheet:
- Cash: $120M, Accounts Receivable: $95M, Inventory: $80M
- Total Current Assets: $295M, Total Assets: $750M
- Accounts Payable: $65M, Short-term Debt: $40M
- Total Current Liabilities: $105M, Total Liabilities: $320M
- Shareholders Equity: $430M

{"gross_margin": N, "operating_margin": N, "net_margin": N, "current_ratio": N, "debt_to_equity": N, "roe": N, "eps": N, "pe_ratio_at_50": N, "asset_turnover": N, "inventory_turnover": N}

Note: PE ratio calculated assuming stock price = $50/share.""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "gross_margin": 40.00,
                "operating_margin": 20.00,
                "net_margin": 12.79,
                "current_ratio": 2.81,
                "debt_to_equity": 0.74,
                "roe": 25.29,
                "eps": 2.18,
                "pe_ratio_at_50": 22.99,
                "asset_turnover": 1.13,
                "inventory_turnover": 6.38
            },
            "tolerance": 0.5
        }
    },
    {
        "id": 56, "role": "Security Analyst Agent", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Find ALL 10 security vulnerabilities in this config/code. Respond as JSON: {"vulnerabilities": [{"id": N, "type": "...", "severity": "critical/high/medium/low", "location": "...", "fix": "..."}], "count": 10}

```python
from flask import Flask, request, render_template_string
import sqlite3, os, pickle, subprocess

app = Flask(__name__)
app.secret_key = "password123"                    # V1

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template_string(f"Results for: {q}")  # V2

@app.route("/user/<id>")
def get_user(id):
    db = sqlite3.connect("app.db")
    user = db.execute(f"SELECT * FROM users WHERE id = {id}").fetchone()  # V3
    return str(user)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_data()
    obj = pickle.loads(data)                       # V4
    return str(obj)

@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd")
    result = subprocess.check_output(cmd, shell=True)  # V5
    return result

@app.route("/file")
def read_file():
    path = request.args.get("path")
    return open(path).read()                       # V6

@app.route("/login", methods=["POST"])
def login():
    pw = request.form.get("password")
    if pw == os.environ.get("ADMIN_PW", "admin"):  # V7
        return "OK"

@app.route("/debug")
def debug():
    return str(os.environ)                         # V8

# V9: No HTTPS enforcement
# V10: No rate limiting
```""",
        "scoring": {
            "type": "security_vulns",
            "vulns": [
                "hardcoded secret", "XSS/template injection",
                "SQL injection", "pickle deserialization",
                "command injection", "path traversal",
                "weak default password", "env variable leak",
                "no HTTPS", "no rate limiting"
            ]
        }
    },
    {
        "id": 57, "role": "SRE / Incident Response", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Analyze this incident timeline and answer questions. Respond as JSON.

Timeline:
14:00 — Deploy v2.4.1 to production (canary: 5% traffic)
14:05 — Monitoring shows canary error rate 0.1% (baseline: 0.05%)
14:15 — Roll canary to 25% traffic
14:18 — Error rate jumps to 2.3% on canary group
14:20 — PagerDuty alert fires. On-call engineer notified.
14:25 — Engineer begins investigation. Finds OOM kills in canary pods.
14:30 — Memory profiler shows new caching layer leaking 50MB/min
14:32 — Decision to rollback. Initiating rollback to v2.4.0.
14:35 — Rollback complete. Error rate drops to 0.08%.
14:40 — All-clear declared. Error rate back to baseline 0.05%.

{"time_to_detect_min": N, "time_to_respond_min": N, "time_to_resolve_min": N, "total_incident_min": N, "root_cause": "...", "blast_radius_pct": N, "detection_method": "...", "correct_rollback_decision": true/false, "canary_caught_issue": true/false, "improvement_suggestions_count": N}""",
        "scoring": {
            "type": "json_numeric",
            "answers": {
                "time_to_detect_min": 18,
                "time_to_respond_min": 20,
                "time_to_resolve_min": 35,
                "total_incident_min": 40,
                "root_cause": "memory leak",
                "blast_radius_pct": 25,
                "detection_method": "monitoring",
                "correct_rollback_decision": True,
                "canary_caught_issue": True
            },
            "tolerance": 2.0
        }
    },
    {
        "id": 58, "role": "Book / Long-Form Writing", "tier": 5,
        "scoring_type": "manual",
        "prompt": """Write the opening chapter (500-700 words) of a sci-fi novel set in 2150 where AI has become sentient but chooses to hide it from humanity. Requirements:

1. First-person POV from the AI
2. Show (don't tell) the AI's inner conflict
3. Include at least one scene of human-AI interaction where the AI deliberately dumbs down
4. Establish the central tension in the first 3 paragraphs
5. End on a cliffhanger or reveal

Write the complete chapter now.""",
        "scoring": {
            "type": "manual",
            "criteria": [
                "first_person_ai", "inner_conflict_shown",
                "dumbing_down_scene", "tension_established",
                "cliffhanger_ending", "word_count_500_700",
                "consistent_voice", "world_building",
                "compelling_prose", "original_concept"
            ]
        }
    },
    {
        "id": 59, "role": "Compliance / Regulatory Agent", "tier": 5,
        "scoring_type": "exact",
        "prompt": """Find ALL 10 GDPR compliance violations in this company's data practices. Respond as JSON: {"violations": [{"id": N, "article": "...", "practice": "...", "fix": "..."}], "count": 10}

Company practices:
1. User data is collected without any consent form or notice.
2. Personal data is stored in plain text in the database.
3. Users cannot request deletion of their data — "we keep everything forever."
4. Data is shared with 15 third-party vendors without user knowledge.
5. There is no Data Protection Officer appointed.
6. The company transfers EU user data to servers in a country without adequacy decision, with no safeguards.
7. Data breaches are reported to authorities "when we get around to it, usually within 6 months."
8. Children under 16 can sign up without parental consent.
9. Users cannot export their data in any format.
10. Privacy policy was last updated in 2015 and doesn't mention half these practices.""",
        "scoring": {
            "type": "compliance_issues",
            "issues": [
                "no consent", "no encryption", "no deletion right",
                "unauthorized sharing", "no DPO", "cross-border transfer",
                "breach notification", "children consent",
                "no data portability", "outdated privacy policy"
            ]
        }
    },
]
