# Sentinel-Fin final prototype report

## Scope

This report describes the reproducible offline prototype run from the custom synthetic banking dataset. No public dataset was downloaded and no customer data is included. Synthetic values are illustrative and are not evidence about real banking behavior.

## Method

The pipeline generates timestamped customer transactions, computes historical features using only prior rows, fits class-weighted Logistic Regression and Random Forest baselines, scores Isolation Forest anomalies, computes behavioral and multi-edge transaction graph evidence, and combines normalized signals into a configurable composite risk score. Cases are routed to deterministic investigation records with human review status. Ollama is optional and never required for detection.

## Actual artifacts

After execution, metrics are saved in `results/metrics/pipeline_metrics.json`, row-level scores in `results/predictions/transaction_predictions.csv`, and high-risk investigation records in `results/investigations/cases.json`. The final report must be regenerated after each experiment rather than using hardcoded values.

## Limitations

The synthetic generator is not representative of any bank. The composite score is not a calibrated fraud probability. Isolation Forest scores are anomaly rankings. Graph and behavioral evidence are prioritization signals. Public dataset adapters and SHAP/PyOD comparisons remain optional extensions when their dependencies and licensed inputs are available. Ollama `qwen2.5:3b` is installed locally and real JSON-constrained inference succeeded for three synthetic cases; the LLM remains an explanation aid rather than a detector or decision maker.
