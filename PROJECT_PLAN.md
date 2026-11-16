# Project Plan

1. Scaffold and environment verification.
2. Reproducible synthetic data and provenance.
3. Leakage-safe features and supervised baseline.
4. Anomaly, behavioral, and graph components.
5. Deterministic agent workflow and evidence reports.
6. Optional local Ollama summaries.
7. Dashboard, robustness tests, ablations, and report.

Acceptance requires executed notebooks, actual saved metrics, repeatable tests, and
explicit limitations; file creation alone is not completion. The current executable
pipeline is `scripts/run_pipeline.py`; it produces the synthetic offline artifacts
used by the report and is the source of truth for recorded metrics.
