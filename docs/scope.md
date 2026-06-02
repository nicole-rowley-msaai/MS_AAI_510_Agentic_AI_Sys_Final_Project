# LexPath AI — Agent Scope

**v1.0 | June 2026 | Owner: Christina Sadiq (PM)**

---

## Purpose

This doc aligns Nicole (AIE) and Angelique (DE) on exactly what the agent does, what it doesn't do, and what each person owns. If something isn't in here, it's out of scope.

---

## What the Agent Does

A prospective client submits a natural-language description of their legal issue. The agent:

1. Asks clarifying questions if the query is ambiguous
2. Retrieves semantically similar legal provisions from the LEDGAR Vector Search index
3. Runs a conflict-of-interest check against a mock internal client database
4. Routes the case to the right practice area and emits a structured JSON intake summary
5. Flags output for senior attorney review — nothing proceeds without approval

All steps logged via MLflow: tool calls, retrieved document IDs, reasoning traces, model metadata.

---

## Input / Output

**Input:** Natural-language client description of a legal issue

**Output:** Structured JSON intake summary

```json
{
  "client_summary": "Client believes they were wrongfully terminated after filing an HR complaint.",
  "practice_area": "Employment",
  "conflict_status": "CLEARED",
  "routing_recommendation": "Employment Law — Partner Review",
  "retrieved_provisions": ["provision_id_001", "provision_id_042"],
  "hitl_flag": true
}
```

---

## The Three Tools

**Tool 1 — Semantic Retrieval (RAG)**
- Queries Databricks Vector Search index of LEDGAR provisions
- Returns top-k semantically similar provisions to ground classification
- Nicole builds the tool; Angelique builds the index

**Tool 2 — Conflict Check**
- Queries mock internal client database for conflict-of-interest flags
- Returns: `CLEARED` or `CONFLICT FLAG`
- Owner: Nicole

**Tool 3 — Case Routing**
- Maps intake profile to practice area using firm routing schema
- Emits structured JSON output
- Practice areas: Corporate, Litigation, Employment, IP, Real Estate
- Owner: Nicole

---

## Graceful Rejection (Required — 2 examples)

The agent must reject out-of-scope inputs and log both as MLflow traces:

1. **Direct legal advice** — e.g. "Should I sue my landlord?" → agent declines, redirects to intake process
2. **Off-topic input** — e.g. "What's the weather today?" → agent rejects, explains its scope

---

## LLM Comparison (Required)

Same intake scenario run through both:
- **Claude 3.5 Sonnet** — primary
- **GPT-4o** — benchmark

Capture: response quality, routing accuracy, latency, cost per query. Feeds the ROI slide.

---

## Out of Scope

- Full autonomous legal reasoning
- Automated prompt optimization
- Fine-tuning pipelines (Mosaic AI is stretch goal only)
- Production deployment (recommendation required in video, live system is not)
- Large-scale context governance

---

## Evaluation — 5 Required Traces

| # | Scenario | LLM |
|---|----------|-----|
| 1 | Employment — wrongful termination | Claude 3.5 Sonnet |
| 2 | IP — trademark infringement | Claude 3.5 Sonnet |
| 3 | Real estate — commercial lease dispute | Claude 3.5 Sonnet |
| 4 | Comparative — same scenario, both LLMs | Claude 3.5 Sonnet + GPT-4o |
| 5 | Graceful rejection | Claude 3.5 Sonnet |

Each trace needs a notebook cell with LLM-judge commentary: routing accuracy, retrieval relevance, cross-model comparison.

---

*Last updated: June 1, 2026*
