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

LexPath AI is a ReAct-pattern agentic system built for LexPath Legal Group. The agent handles legal client intake end-to-end — it interviews prospective clients in natural language, classifies their legal issue, checks for conflicts of interest, routes the case to the right practice area, and generates a structured intake summary for attorney review.

The goal is to cut the hours staff spend on intake that never converts, and let attorneys focus on billable work. No matter proceeds without senior attorney approval — human-in-the-loop is built into the workflow.

---

## Dataset

**LEDGAR** (LexGLUE Benchmark Suite)
- ~80,000 contractual provisions from SEC EDGAR filings
- Labeled across 100 legal provision categories
- Grounds the agent's retrieval and classification pipeline via Databricks Vector Search

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| LLMs | Claude 3.5 Sonnet (primary), GPT-4o (benchmark) |
| Orchestration | LangChain (ReAct executor) |
| Infrastructure | Databricks — Delta Tables, Vector Search, Mosaic AI |
| Tracing & Eval | MLflow |
| Version Control | GitHub |

---

## Agent Architecture

ReAct (Reasoning and Acting) design pattern:
