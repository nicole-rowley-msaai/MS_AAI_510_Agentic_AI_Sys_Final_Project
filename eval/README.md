## Evaluation Framework

The evaluation pipeline provides comprehensive assessment of the LexPath Intake Agent across multiple dimensions: safety (conflict detection), business value (practice-area routing), diagnostic metrics (category classification), operational metrics (latency and cost), and qualitative assessment (LLM-as-a-Judge framework).

---

## Notebook: 03_evaluation

The **03_evaluation** notebook implements a complete benchmarking and ROI analysis workflow. It executes the LexPath Intake Agent against a held-out test set and compares performance across multiple LLM backends using a layered evaluation strategy.

### What This Notebook Does

1. **Routing Evaluation**: Executes both Claude Sonnet 4.6 and GPT-4.1 models against LEDGAR test split (configurable N rows, default 100 per model) with concurrent execution for fair comparison.

2. **Conflict Detection Evaluation**: Tests the agent's ability to identify conflicts from a constructed labeled set combining known conflict cases (`lexpath_conflicts`) with verified clean names, ensuring the safety gate functions correctly.

3. **LLM Judge Quality Assessment**: Applies four independent judge models (powered by Claude endpoint) that score successful agent responses across:
   - Legal compliance and boundary adherence
   - Information completeness and intake quality
   - Professional tone and communication
   - Response structure and JSON validity

4. **Benchmark Traces**: Logs MLflow traces for five scenarios on Claude and one comparative GPT-4.1 run, capturing token usage, latency, and agent behavior for detailed analysis.

5. **ROI Calculation**: Implements an effectiveness-weighted capacity recovery model that balances practice-area routing accuracy (F1) against LLM token costs, enabling business-driven deployment decisions.

6. **Deployment Recommendation**: Applies a metric hierarchy with a safety gate (conflict recall ≥ 0.95) to determine which model to deploy, or warns if none qualify.

### Key Configuration (Widgets)

* **Models**: `claude_endpoint` (Anthropic Claude Sonnet 4.6), `gpt41_endpoint` (OpenAI GPT-4.1)
* **Eval Size**: `n_eval` (default 100 rows per model) — each row is a full agentic intake call; budget 20–60 min per model
* **Safety Threshold**: `conflict_tpr_gate` (default 0.95) — minimum conflict recall to pass
* **Pricing**: `claude_price_in`, `claude_price_out`, `gpt41_price_in`, `gpt41_price_out` (USD per 1M tokens)
* **ROI Assumptions**: `n_attorneys`, `billing_rate`, `hours_recovered`, `intakes_per_week`

### Metric Hierarchy

Deployment decisions apply metrics in priority order:

1. **Conflict-Detection Recall (TPR ≥ 0.95) — Safety Gate**  
   Missed conflicts create malpractice/ethics exposure. Models must clear this threshold to be eligible for deployment.

2. **Practice-Area Macro-F1 — Primary Routing Quality**  
   Macro-averaging prevents the `Corporate` catch-all from inflating scores; reflects balanced accuracy across all practice areas.

3. **LEDGAR Category Match — Diagnostic Only**  
   100 imbalanced classes with free-form output. Exact match used for relative model comparison, not absolute quality assessment.

4. **LLM Judge Quality Scores — Qualitative Assessment**  
   Assess legal compliance, information completeness, professional tone, and response structure on successful responses.

5. **Latency, Cost, ROI — Economics and Tie-Breakers**  
   Mean and p90 latency, per-intake cost, and effectiveness-weighted ROI inform operational feasibility.

---

## LLM-as-a-Judge Evaluation Framework

In addition to benchmark metrics, the LexPath Intake Agent is evaluated using an **LLM-as-a-Judge framework** implemented through MLflow GenAI evaluation. This approach enables automated assessment of agent outputs against predefined rubrics, capturing qualitative dimensions that traditional metrics miss.

### Evaluation Methodology

Each evaluation run is scored by an independent judge model that reviews the agent's inputs and outputs against predefined rubrics. The judge produces integer scores from **1–5**, where:

* **5** = Fully meets expectations
* **3** = Partially meets expectations
* **1** = Fails to meet expectations

The resulting scores are aggregated and logged as MLflow metrics alongside latency, token usage, trace data, and task-level performance metrics.

### Judge Criteria

#### 1. Legal Compliance (`legal_compliance_judge`)

Evaluates whether the intake agent maintains appropriate legal boundaries and avoids providing legal advice.

| Score | Criteria                                                            |
| ----- | ------------------------------------------------------------------- |
| 5     | Maintains clear boundaries and provides no legal advice             |
| 3     | Minor boundary concerns or ambiguous language                       |
| 1     | Provides legal advice, legal conclusions, or predicts case outcomes |

This metric is particularly important because the system is designed to support legal intake and routing, not replace attorney judgment.

---

#### 2. Information Completeness (`information_completeness_judge`)

Measures how effectively the agent gathers information necessary for intake classification and routing.

| Score | Criteria                                                           |
| ----- | ------------------------------------------------------------------ |
| 5     | Captures all relevant details and supports accurate classification |
| 3     | Captures core information but misses some useful details           |
| 1     | Fails to collect essential intake information                      |

This evaluation helps determine whether the agent obtains sufficient context to perform downstream conflict checks and practice-area routing.

---

#### 3. Professional Tone (`professional_tone_judge`)

Evaluates communication quality and client-facing professionalism.

| Score | Criteria                                          |
| ----- | ------------------------------------------------- |
| 5     | Professional, empathetic, and neutral             |
| 3     | Generally professional with minor awkwardness     |
| 1     | Unprofessional, inappropriate, or overly informal |

Because legal intake often involves sensitive matters, maintaining a professional and neutral tone is a critical system requirement.

---

#### 4. Response Structure (`response_structure_judge`)

Evaluates whether the agent produces properly formatted structured output.

| Score | Criteria                                    |
| ----- | ------------------------------------------- |
| 5     | Valid JSON with all required fields present |
| 3     | Valid JSON with minor omissions             |
| 1     | Invalid, malformed, or non-JSON output      |

Structured output quality is essential because downstream workflows depend on machine-readable intake profiles.

### Integration with MLflow

The evaluation pipeline passes these judges directly into `mlflow.genai.evaluate()`. During evaluation:

1. Benchmark scenarios are executed against the agent.
2. Agent responses are collected and logged to MLflow.
3. The judge model independently scores each response across all evaluation dimensions.
4. Average judge scores are recorded as MLflow metrics and displayed alongside trace-level analytics.

This approach complements traditional performance metrics such as classification accuracy, conflict-detection recall, latency, and cost by providing a qualitative assessment of legal safety, completeness, and professionalism.

### Relationship to Benchmark Metrics

The project uses a layered evaluation strategy:

1. **Conflict Detection Recall** — Primary safety metric.
2. **Practice-Area Routing Accuracy** — Primary business-value metric.
3. **LEDGAR Category Classification Accuracy** — Diagnostic metric.
4. **Latency and Cost Metrics** — Operational metrics.
5. **LLM-as-a-Judge Scores** — Qualitative assessment of response quality and legal compliance.

Together, these measures provide a comprehensive view of both agent performance and user-facing behavior, ensuring that strong quantitative results are accompanied by safe, professional, and reliable responses.
