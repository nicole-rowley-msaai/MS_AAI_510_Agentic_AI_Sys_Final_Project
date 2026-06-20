# LexPath AI — Intelligent Legal Intake and Case Routing Agent

**AAI-510 Agentic AI Systems | Team 7 | University of San Diego**

---

## Team

| Name | Role |
|------|------|
| Christina Sadiq | Project Manager (PM) |
| Marie Angelique Membrido | Data Engineer (DE) |
| Nicole Rowley | AI Engineer (AIE) |

---

## Project Overview

LexPath AI is a ReAct-pattern agentic system built for LexPath Legal Group. The agent handles legal client intake end-to-end — it interviews prospective clients in natural language, classifies their legal issues, checks for conflicts of interest, and routes cases to the appropriate practice area.

The goal is to cut the hours staff spend on intake that never converts, and let attorneys focus on billable work. No matter proceeds without senior attorney approval — human-in-the-loop is built in.

---

## Dataset & Data Pipeline

**LEDGAR** (LexGLUE Benchmark Suite)
- 60,000 contractual provisions from SEC EDGAR filings
- Labeled across 100 legal provision categories
- Grounds the agent's retrieval and classification pipeline via Databricks Vector Search

**Processing:**
- **01a:** Load raw LEDGAR → Delta Lake (cleaning, normalization)
- **01b:** Compute embeddings & index vectors in Vector Search
- **01c:** Generate mock intake examples for local development & testing

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| **LLMs** | Claude 4.6 Sonnet (primary), GPT-4.1 (benchmark) |
| **Embedding Model** | databricks-gte-large-en |
| **Orchestration** | LangChain + LangGraph (ReAct executor) |
| **Infrastructure** | Databricks — Delta Lake, Vector Search |
| **Tracing & Eval** | MLflow, LLM-based judge commentary |
| **Data** | PySpark, pandas |
| **Version Control** | GitHub |

---

## Agent Architecture

**ReAct (Reasoning and Acting)** pattern executed via **LangGraph**:

**Flow:** Client Query → Reason → Act (tool call) → Observe → Iterate → JSON Output

**Three tools:**
1. **Semantic Retrieval** — retrieve top-5 LEDGAR provisions similar to client's issue (grounded in legal language)
2. **Conflict Check** — verify party names against internal conflicts table
3. **Case Routing** — map LEDGAR category → firm's practice area

**LLM:** Claude 4.6 Sonnet (via Databricks endpoint)  
**Framework:** LangChain + LangGraph  
**Configuration:** System prompt built into `agent_lib.py`; all tool calls logged via MLflow

**Executor:** `agent_lib.build_agent()` returns a stateless ReAct loop that rejects out-of-scope requests without tool invocation.

---

## Repo Structure

```
/
├── data/                            # DE: data engineering & preprocessing
│   ├── 01a_load_ledgar_to_delta.ipynb           # Ingest LEDGAR → Delta Lake
│   ├── 01b_embeddings_vector_search.ipynb       # Compute embeddings & index vectors
│   ├── 01c_mock_data.ipynb                      # Generate mock intake examples
│   └── README.md
│
├── agent/                           # AIE: agent implementation
│   ├── 02a_build_agent.ipynb        # Define agent & tools (ReAct setup)
│   ├── 02b_run_agent.ipynb          # Run agent & log MLflow traces
│   ├── agent_lib.py                 # Shared library: tools, prompts, executor
│   └── README.md
│
├── eval/                            # Evaluation artifacts & MLflow traces
│   ├── 03_evaluation.ipynb          # Evaluation notebook & metrics
│   └── README.md
│
├── slides/                          # PM: presentation assets
├── docs/
│   └── scope.md
└── README.md
```

---

## Getting Started

**Recommended run order:**
1. **Data pipeline** (Marie): run `data/01a_load_ledgar_to_delta.ipynb`, then `01b_embeddings_vector_search.ipynb`, then `01c_mock_data.ipynb`
2. **Agent build** (Nicole): run `agent/02a_build_agent.ipynb`
3. **Agent execution & eval** (Nicole): run `agent/02b_run_agent.ipynb`, then `eval/03_evaluation.ipynb`

**Requirements:**
- Python 3.9+, Jupyter
- Databricks workspace access (or local PySpark + embedding service)
- Environment: MLflow, LangChain, LangGraph, pyspark, pandas
- API keys: Databricks token (or equivalent LLM endpoint)

See subdirectory READMEs for detailed setup.

---

## Submission

Due: **June 22, 2026** | One teammate submits (Christina Sadiq)
- GitHub repo zip
- Video presentation (10-15 min)
