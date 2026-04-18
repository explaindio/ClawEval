# Phase H (Hard) Benchmarking Results

Phase H is designed to evaluate LLMs on complex, multi-constraint agentic workflows with granular checkpoint scoring. Rather than standard pass/fail metrics, Phase H forces models to navigate dense instructions and partial scores.

## How It Is Run
Phase H uses a combination of rigorous JSON constraint parsing, deep code execution, and keyword-based substring evaluation (`h_keywords`). The suite consists of **53 fully automated tests**, totaling **1,100 scoring checkpoints**. 

To run the automated Phase H suite against a locally hosted backend (like llama.cpp or vLLM), use:
```bash
python3 eval/run_phase_h.py \
    --base-url http://192.168.0.187:8080/v1 \
    --model "Qwen3.6-35B-A3B" \
    --max-tokens 32000 \
    --timeout 1200
```
> Note: 6 tests (H-10, H-17, H-24, H-34, H-41, H-58) require manual review (e.g. dynamic UI testing) and are excluded from the automated suite.

---

## Baseline: Qwen3.6-35B-A3B

**Overall Score:** 871 / 1100 (79.18%)

*This model establishes the highest baseline ceiling, successfully navigating extensive prompt constraints but failing on the most complex debugging and architectural loops.*

### Detailed Scores
- ✅ H-01 Router / Triage Agent: 28/30 (93%)
- ✅ H-02 Input Validator / Sanitizer: 29/30 (97%)
- ❌ H-03 Heartbeat / Health Monitor: 0/15 (0%)
- ⚠️ H-04 Notification / Alert Agent: 23/30 (77%)
- ✅ H-05 Sentiment Analysis Agent: 27/30 (90%)
- ✅ H-06 FAQ Generation Agent: 15/15 (100%)
- ✅ H-07 Translation Agent: 15/15 (100%)
- ⚠️ H-08 Calendar / Scheduling Agent: 10/20 (50%)
- ✅ H-09 Research / Web Search Agent: 28/30 (93%)
- ✅ H-11 Editor Agent: 25/30 (83%)
- ✅ H-12 Content Planner / Strategist: 26/30 (87%)
- ✅ H-13 Email Drafting: 42/45 (93%)
- ✅ H-14 Document Summarization: 15/15 (100%)
- ✅ H-15 Meeting Notes / Transcription: 34/35 (97%)
- ✅ H-16 Social Media Monitoring: 55/60 (92%)
- ✅ H-18 News Aggregation: 7/7 (100%)
- ✅ H-19 Shopping / Price Comparison: 15/15 (100%)
- ✅ H-20 Memory Management: 20/20 (100%)
- ⚠️ H-21 RAG / Retrieval Agent: 9/15 (60%)
- ✅ H-22 Data Analysis Agent: 14/15 (93%)
- ✅ H-23 Website Scraping: 15/15 (100%)
- ✅ H-25 Customer Support Agent: 48/60 (80%)
- ✅ H-26 Lead Scoring: 13/15 (87%)
- ✅ H-27 Sprint Summarizer: 15/15 (100%)
- ✅ H-28 Transaction Agent: 18/20 (90%)
- ❌ H-29 Home Automation Agent: 7/20 (35%)
- ✅ H-30 Fitness Tracking: 15/15 (100%)
- ✅ H-31 Recipe Agent: 15/15 (100%)
- ✅ H-32 Personal Finance: 15/15 (100%)
- ❌ H-33 SEO Optimization Agent: 5/15 (33%)
- ❌ H-35 Travel Planning Agent: 1/15 (7%)
- ✅ H-36 Code Generation Agent: 30/30 (100%)
- ❌ H-37 Code Review Agent: 5/15 (33%)
- ✅ H-38 QA / Test Writing Agent: 13/15 (87%)
- ❌ H-39 Task Planning / Decomposition: 1/18 (6%)
- ✅ H-40 Fact-Checking Agent: 29/30 (97%)
- ✅ H-42 Market Research Agent: 14/15 (93%)
- ✅ H-43 Synthesizer / Aggregator: 13/15 (87%)
- ❌ H-44 Curriculum Designer: 7/15 (47%)
- ✅ H-45 Prototype Generator: 15/15 (100%)
- ❌ H-46 DevOps Agent: 0/15 (0%)
- ✅ H-47 Math / Logic Reasoning: 14/15 (93%)
- ✅ H-48 STEM Research Analyst: 15/15 (100%)
- ✅ H-49 Algorithm Explorer: 30/30 (100%)
- ✅ H-50 Orchestrator Agent: 13/15 (87%)
- ❌ H-51 Software Architect Agent: 6/15 (40%)
- ❌ H-52 Complex Debugger Agent: 0/15 (0%)
- ❌ H-53 Legal Document Review: 6/15 (40%)
- ✅ H-54 Medical Analysis: 15/15 (100%)
- ✅ H-55 Financial Analysis: 14/15 (93%)
- ✅ H-56 Security Analyst Agent: 14/15 (93%)
- ✅ H-57 SRE / Incident Response: 12/15 (80%)
- ❌ H-59 Compliance Agent: 1/15 (7%)
