# eval — Evaluation artifacts & MLflow traces

This directory contains MLflow traces, metrics, visualizations, and other evaluation artifacts produced when running the agent notebooks. Use this folder to store reproducible results (screenshots, JSON exports, CSVs, saved model/embedding metadata, and any summary reports).

## Purpose
- Collect and organize evaluation outputs from agent/notebook runs.
- Provide a single place for experiment traces (MLflow), human-readable exports (screenshots/JSON), and reproducibility notes.
- Make it easy for reviewers and teammates to inspect results without re-running full pipelines.

## Typical contents
- mlruns/ or exported MLflow artifacts (if stored in-repo)
- screenshots/ — PNG/JPG captures of notable behaviors, UI, or visualizations
- exports/ — JSON, CSV, or other data exports used for offline analysis
- metrics/ — aggregated evaluation metrics or summary tables (CSV/Markdown)
- notebooks/ — short evaluation notebooks or scripts that generated the artifacts
- README.md — (this file) explains the structure and how to reproduce

> Note: The exact layout may vary depending on how MLflow/Databricks is configured. If MLflow is remote (e.g., tracking server), prefer exporting run snapshots or JSON summaries into this folder for portability.

## How artifacts are produced
1. Run the agent evaluation notebooks (see top-level notebooks under `agent/` or `eval/`).
2. The notebooks log metrics, parameters, and artifacts to MLflow (or the configured tracking backend).
3. Notable outputs (screenshots, JSON exports, small CSV summaries) are copied or saved into this `eval/` directory for easier sharing.

## Reproducing the evaluation (local)
Prerequisites:
- Python 3.9+
- Required packages from the project (see root README or environment file)
- MLflow (same version used during experiments) and access to the MLflow tracking server if runs were remote

Steps:
1. Configure environment variables or notebook parameters matching how the original run logged artifacts (e.g., MLFLOW_TRACKING_URI).
2. Open and run the evaluation notebook(s) in order. Prefer running with a small mock dataset first (see data/01c_mock_data.ipynb).
3. After runs complete, export MLflow runs or download artifacts:
   - MLflow UI: open the tracking server, find the experiment, and download run artifacts.
   - To export a run programmatically: use `mlflow.tracking.MlflowClient()` to fetch artifacts and write them to `eval/exports/`.
4. Commit any portable artifact snapshots (small JSON summaries, screenshots) into `eval/` for sharing.

## Viewing and sharing
- MLflow UI: the primary interface for exploring runs, parameters, and metrics.
- For long-term, shareable artifacts: include JSON/CSV summaries and screenshots in `eval/exports/` and `eval/screenshots/`.
- When sharing the repository, avoid committing large binary artifacts; prefer compact summaries or links to externally hosted artifacts.

## Naming & contribution guidelines
- Use descriptive filenames with timestamps and run IDs:
  - metrics_YYYYMMDD_run-<id>.csv
  - screenshot_YYYYMMDD_<short-desc>.png
  - run_summary_run-<id>.json
- Include a small text file describing how the artifact was produced when the generation process is not obvious.

## Troubleshooting
- Missing artifacts:
  - Verify MLflow tracking URI and permissions.
  - Check notebook logs for upload errors.
- MLflow UI not accessible:
  - Confirm server address and that it is running.
  - If using Databricks tracking, use the Databricks UI to locate experiment runs.
- Large files:
  - Replace with compressed or summarized exports and keep full raw artifacts off-repo (cloud storage or Databricks workspace).

## Example folder layout
