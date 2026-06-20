# Agent

Owner: Nicole (AIE)

This directory contains the agent implementation, helper library, and evaluation traces for the Agentic AI Systems final project (Part A). The agent follows a ReAct-style loop, defines and uses external tools, implements graceful rejection behavior, and records runs using MLflow. An LLM-based judge provides commentary on selected traces.

## Contents

- 02a_build_agent.ipynb — Notebook that defines and builds the agent and its tools (tool wrappers, prompt templates, ReAct loop setup).
- 02b_run_agent.ipynb — Notebook that runs the agent on evaluation prompts and records MLflow traces for each run. Contains experiment code and evaluation harness.
- agent_lib.py — Python helper library used by the notebooks (utility functions, tool definitions, wrappers, and small helpers for running experiments and logging).
- README.md — This file.

## Key features

- ReAct loop agent architecture (reasoning + actions)
- Tool definitions and integration
- Graceful rejection (agent fallback/decline behavior when it cannot answer)
- MLflow traces for reproducible runs and experiment tracking
- LLM-based judge commentary for qualitative evaluation

## Requirements

Suggested environment:

- Python 3.8+
- Jupyter / JupyterLab
- MLflow
- openai (or whichever LLM client configured in the notebooks)
- pandas, numpy, requests, and other common data libs

You can create a virtual environment and install common packages with:

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install --upgrade pip
pip install jupyterlab mlflow openai pandas numpy requests
