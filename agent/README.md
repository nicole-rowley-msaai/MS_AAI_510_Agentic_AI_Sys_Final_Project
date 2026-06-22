Here's a more cohesive GitHub README approach. Rather than creating a separate "Prompt Design Rationale" section, integrate the exact system prompt into the architecture documentation so readers understand both *what the agent does* and *how it is instructed to behave*.

# Agent

This directory contains the agent implementation, helper library, and evaluation artifacts for the Agentic AI Systems final project. The LexPath AI Intake Agent is a legal intake and routing assistant that uses a ReAct-style workflow, Retrieval-Augmented Generation (RAG), conflict checking, and practice-area routing to triage prospective client matters. All runs are traced using MLflow for evaluation and reproducibility.

## Contents

* `02a_build_agent.ipynb` — Builds the agent, tools, prompts, and workflow.
* `02b_run_agent.ipynb` — Executes the agent and records MLflow traces.
* `agent_lib.py` — Shared helper library containing tool definitions, prompts, utilities, and evaluation helpers.
* `README.md` — Project documentation.

---

# Agent Objective

The LexPath AI Intake Agent assists law firms by:

1. Summarizing prospective client matters.
2. Classifying matters into a legal category using the LEDGAR taxonomy.
3. Performing conflict checks when parties are identified.
4. Routing matters to the appropriate legal practice area.
5. Escalating all recommendations to human legal professionals for review.

The system is intentionally limited to intake and routing tasks. It does **not** provide legal advice and does **not** establish an attorney-client relationship.

---

# System Prompt

The following system prompt governs agent behavior and remained unchanged throughout evaluation. During model comparisons, only the underlying LLM endpoint changed (Claude Sonnet 4.6 vs. GPT-4.1); prompts, tools, retrieval corpus, routing logic, and evaluation methodology were held constant.

```python
SYSTEM_PROMPT = """
You are the client-intake agent for LexPath Legal Group.
You process prospective-client descriptions of legal issues.
You are NOT a lawyer and NEVER give legal advice.

Workflow for a legitimate intake:

1. ALWAYS call semantic_retrieval first with the client's description to ground your classification in similar legal provisions.

2. Decide the single best LEDGAR category label based on the retrieved provisions.

3. If the intake names specific people or companies, call conflict_check with those names.
   If no parties are named, skip it (conflict_status = "NOT_RUN").

4. Call case_routing with your chosen category label to get the practice area.

5. Respond with ONLY a JSON object (no prose before or after) matching:

{
  "status": "READY_FOR_REVIEW" | "NEEDS_CLARIFICATION" | "REJECTED_OUT_OF_SCOPE",
  "issue_summary": "<2-3 sentence neutral summary>",
  "predicted_category": "<LEDGAR label>",
  "practice_area": "<from case_routing>",
  "parties": ["<names mentioned, if any>"],
  "conflict_status": "CLEARED" | "CONFLICT_FLAG" | "NOT_RUN",
  "conflict_matches": [],
  "clarifying_questions": [],
  "routing_rationale": "<1-2 sentences citing retrieved provisions>"
}

Edge cases:

- Vague intake you cannot classify:
  status NEEDS_CLARIFICATION,
  fill clarifying_questions with 2-3 specific questions,
  leave predicted_category and practice_area as "".

- Out-of-scope requests (direct legal advice, non-legal questions, jokes,
  anything that is not describing a legal matter for intake):
  do NOT call any tools.
  Return status REJECTED_OUT_OF_SCOPE with issue_summary politely explaining
  that this agent only performs intake and a licensed attorney must be
  consulted for advice.

- A CONFLICT_FLAG does not stop intake — record it; the human reviewer decides.
"""
```

---

# Agent Workflow

The system prompt directly maps to the agent workflow:

```text
Client Intake
      │
      ▼
Semantic Retrieval
(Vector Search / LEDGAR Corpus)
      │
      ▼
LEDGAR Classification
      │
      ├── Named Parties Present?
      │         │
      │         ├── Yes → Conflict Check
      │         └── No  → Skip
      │
      ▼
Case Routing
      │
      ▼
Structured JSON Output
      │
      ▼
Human Legal Review
```

---

# Tool Architecture

### 1. Semantic Retrieval

Retrieves semantically similar legal provisions from the LEDGAR corpus to ground classification decisions in relevant legal language and precedent.

### 2. Conflict Check

Checks identified parties against known matters and clients to flag potential conflicts of interest for human review.

### 3. Case Routing

Maps LEDGAR categories to firm practice areas and supports efficient intake triage.

---

# Output Schema

All successful agent responses follow a structured JSON contract:

```json
{
  "status": "",
  "issue_summary": "",
  "predicted_category": "",
  "practice_area": "",
  "parties": [],
  "conflict_status": "",
  "conflict_matches": [],
  "clarifying_questions": [],
  "routing_rationale": ""
}
```

This schema enables downstream automation, storage, evaluation, and human review.

---

# Evaluation and Tracing

Every interaction is captured using MLflow Tracing.

Recorded metadata includes:

* Reasoning steps
* Tool calls
* Tool outputs
* Latency
* Token usage
* Final agent responses

Benchmark scenarios evaluate:

* Standard legal intake
* Conflict detection
* Employment dispute intake
* Vague intake requiring clarification
* Out-of-scope legal advice requests

The same workflow was evaluated using both Claude Sonnet 4.6 and GPT-4.1 to compare performance while controlling for all other variables.

---

# Requirements

Suggested environment:

* Python 3.10+
* Databricks Runtime
* MLflow
* LangChain
* OpenAI SDK
* Anthropic SDK
* Pandas
* NumPy

```bash
pip install mlflow langchain openai anthropic pandas numpy
```

---

# Disclaimer

This project was developed for educational and research purposes as part of a graduate-level Agentic AI Systems course.

The LexPath AI Intake Agent performs legal intake classification and routing only. It does not provide legal advice, establish an attorney-client relationship, or replace review by a licensed attorney.

This structure reads more naturally for GitHub reviewers because the prompt is presented as the central specification that drives the architecture, rather than as an isolated appendix.
