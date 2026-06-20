# data/ — Data engineering & preprocessing

This folder contains the data engineering notebooks used to prepare the LEDGAR dataset, build embeddings, and create mock data used by the LexPath AI agent.

Contents
- 01a_load_ledgar_to_delta.ipynb — Ingest LEDGAR provisions into Delta (Spark/Databricks).
- 01b_embeddings_vector_search.ipynb — Compute embeddings and populate Databricks Vector Search (RAG index).
- 01c_mock_data.ipynb — Create small/mock intake examples for development and agent testing.

Recommended run order
1. 01a_load_ledgar_to_delta.ipynb
2. 01b_embeddings_vector_search.ipynb
3. 01c_mock_data.ipynb

Overview
- 01a: Loads raw LEDGAR files (CSV/JSON) into Spark, performs cleaning and normalization, and writes a Delta table suitable for retrieval and downstream processing.
- 01b: Reads the Delta table, computes embeddings for provisions, and indexes vectors in your vector search backend (Databricks Vector Search / Mosaic AI or an alternative like FAISS). Also stores metadata needed for retrieval (doc id, provision text, labels).
- 01c: Produces small/mock client-intake records and example queries that the agent uses for local testing and eval. Useful for development without querying the full dataset.

Prerequisites
- Databricks workspace or local Spark environment (PySpark) with Delta Lake support.
- Python 3.9+ (or the runtime matching your Databricks cluster).
- Recommended packages (install in cluster or venv):
  - pyspark, delta-spark
  - pandas, numpy
  - mlflow (if tracing experiments)
  - a embeddings client / library (Databricks Mosaic/Vector Search, openai, sentence-transformers, or other)
  - databricks-sdk (if programmatic Databricks operations are used)
- Access to LEDGAR raw data (downloaded to a storage location accessible by the cluster).

Configuration / Environment variables
Set these (or configure in notebooks) before running:
- LEDGAR_RAW_PATH — path to raw LEDGAR files (DBFS, S3, local)
- DELTA_OUTPUT_PATH — Delta table path to write cleaned provisions
- EMBEDDINGS_MODEL — model or provider id used for embeddings (e.g., `openai-embedding-...` or `sentence-transformers/...`)
- VECTOR_INDEX_NAME — name for the vector index in Databricks or the local index file path
- DATABRICKS_HOST, DATABRICKS_TOKEN — if using Databricks REST/SDK operations
- MLFLOW_TRACKING_URI — (optional) if using MLflow for logging/tracing

How to run
- Databricks:
  - Import each notebook into your workspace.
  - Attach to a cluster with the required libraries and run cells in order.
- Local Jupyter / VS Code:
  - Install required packages.
  - Open notebooks and run cells sequentially; for large data you will need a Spark cluster or configure an appropriate local Spark runtime.
- Automation:
  - Notebooks can be parameterized and executed with papermill if automated runs are desired.

Expected outputs
- Delta table of cleaned LEDGAR provisions at DELTA_OUTPUT_PATH (partitioning depends on notebook).
- Vector index registered in your Vector Search backend (name = VECTOR_INDEX_NAME).
- A small mock dataset CSV/JSON for testing (produced by 01c_mock_data.ipynb).
- Optional MLflow experiment runs capturing embeddings and indexing metrics.

Notes & tips
- Start with a small subset of LEDGAR when developing locally to speed iteration.
- If you do not have access to Databricks Vector Search, the embeddings step can output to a local FAISS index or a persisted Parquet of (id, embedding) pairs for offline retrieval.
- Monitor memory when computing dense embeddings — batch inference is recommended.
- Keep secrets (API keys, tokens) out of notebooks — use Databricks secrets or environment variables.
- Cell comments indicate configurable knobs (batch size, model choice, delta partition key). Update those for your environment.

Troubleshooting
- Spark errors: ensure cluster has Delta and correct Spark/Python versions.
- Embedding timeouts: reduce batch sizes and/or retry with exponential backoff.
- Permissions: confirm read/write access to configured storage paths.

Where these outputs fit in the project
- The Delta table + vector index are the retrieval backbone for the agent (used by agent/ notebooks).
- Mock data is used for local agent behavior testing and evaluation artifacts under eval/.

Contact
- Nicole Rowley (AI Engineer) — for data pipeline questions and notebook clarifications.
- See top-level README.md for project-level details, architecture, and team contacts.

License
- Project artifacts follow the repository license (see root). Cite LEDGAR/LexGLUE data according to their terms.
