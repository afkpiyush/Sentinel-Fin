# Sentinel-Fin project completion and audit

Date: 2026-11-16

## Outcome

The offline synthetic prototype is executable end to end. It generates reproducible banking transactions, computes prior-only features, trains supervised models, evaluates anomaly rankings, adds behavior and graph evidence, aggregates a composite risk score, creates human-review cases, checks Ollama, and records validated Qwen2.5 3B investigation summaries.

## Acceptance audit

| Area | Status | Evidence |
|---|---|---|
| Repository validation | Complete | `python validate_project.py` reports 0 errors |
| Synthetic data | Complete | `data/synthetic/synthetic_banking_transactions.csv` |
| Logistic Regression | Complete | `results/metrics/pipeline_metrics.json` |
| Random Forest | Complete | `results/metrics/pipeline_metrics.json`, `models/supervised/random_forest.joblib` |
| Isolation Forest | Complete | `results/metrics/pipeline_metrics.json`, `models/anomaly/isolation_forest.joblib` |
| Historical behavioral features | Complete | `src/sentinel_fin/feature_engineering.py` |
| Repeated-transfer graph | Complete | `src/sentinel_fin/graph_analysis.py` |
| Composite risk and missing-signal handling | Complete | `src/sentinel_fin/risk_scoring.py` |
| Investigation cases | Complete | `results/investigations/cases.json` |
| Dashboard helpers | Complete | `src/sentinel_fin/dashboard.py` |
| Dataset adapters | Implemented; not benchmarked | `src/sentinel_fin/dataset_adapters.py`; public files were not available locally |
| Experiments and threshold sensitivity | Complete for synthetic run | `results/metrics/experiment_summary.json`, `reports/experiments/experiment_summary.md` |
| Ollama service | Complete | `results/metrics/llm_status.json` |
| Qwen2.5 3B inference | Complete | Three validated cases in `llm_status.json` |
| Automated tests | Complete | 9 tests pass |
| All 15 notebooks valid | Complete | Validator and notebook tests |
| All 15 notebooks fully developed | Partial | They execute, but several remain compact stage demonstrations rather than full analysis chapters |
| Public European and PaySim evaluation | Open | Requires user-supplied, licensed local datasets |
| SHAP and PyOD comparisons | Open/optional | Packages are unavailable; deterministic fallbacks are used |

## Verified synthetic metrics

- 2,400 transactions; fraud label rate: 7.75%.
- Logistic Regression: average precision 0.8704, ROC-AUC 0.9805, recall 0.9459.
- Random Forest: average precision 0.8492, ROC-AUC 0.9815, F1 0.7595.
- Isolation Forest: average precision 0.3207, ROC-AUC 0.7691.
- Qwen2.5 3B: three successful JSON-validated responses; average response time approximately 2.3 seconds.

## Remaining work

The remaining items are input or scope dependent rather than hidden failures: obtain licensed European and PaySim files before benchmarking them, optionally install PyOD/SHAP for comparisons, and expand the compact notebooks into fuller academic narratives with plots and ablation cells. The project does not claim public-dataset performance, calibrated fraud probabilities, or autonomous financial decisions.

## Reproduction

```powershell
$env:PYTHONPATH = "src"
python scripts/run_pipeline.py
python validate_project.py
pytest -q
```
