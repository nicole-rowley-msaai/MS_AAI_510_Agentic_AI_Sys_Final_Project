## LLM-as-a-Judge Evaluation Framework

In addition to benchmark metrics, the LexPath Intake Agent is evaluated using an **LLM-as-a-Judge framework** implemented through MLflow GenAI evaluation. This approach enables automated assessment of response quality, legal safety, and structured output generation using a separate large language model acting as an evaluator.

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

This approach complements traditional performance metrics such as classification accuracy, conflict-detection recall, latency, and cost by providing a qualitative assessment of legal safety, completeness, professionalism, and output reliability.

### Relationship to Benchmark Metrics

The project uses a layered evaluation strategy:

1. **Conflict Detection Recall** — Primary safety metric.
2. **Practice-Area Routing Accuracy** — Primary business-value metric.
3. **LEDGAR Category Classification Accuracy** — Diagnostic metric.
4. **Latency and Cost Metrics** — Operational metrics.
5. **LLM-as-a-Judge Scores** — Qualitative assessment of response quality and legal compliance.

Together, these measures provide a comprehensive view of both agent performance and user-facing behavior, ensuring that strong quantitative results are accompanied by safe, professional, and reliable interactions.
