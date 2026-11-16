"""Saved, reproducible experiment summaries derived from pipeline artifacts."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

def run_experiments(root="."):
    root=Path(root); metrics=json.loads((root/"results/metrics/pipeline_metrics.json").read_text(encoding="utf-8")); pred=pd.read_csv(root/"results/predictions/transaction_predictions.csv")
    thresholds=[]
    for threshold in [.3,.4,.5,.6,.7,.8]:
        thresholds.append({"threshold":threshold,"high_count":int((pred.risk_score>=threshold).sum()),"high_rate":float((pred.risk_score>=threshold).mean())})
    output={"model_comparison":metrics["models"],"threshold_sensitivity":thresholds,"ablation_notes":{"supervised_vs_anomaly":"Scores are recorded separately; combined risk uses configured normalized weights.","behavioral_and_graph":"Evidence is included in the row-level prediction artifact.","agent_workflow":"Every generated case contains deterministic audit output and human-review status."}}
    target=root/"results/metrics/experiment_summary.json"; target.write_text(json.dumps(output,indent=2,default=str),encoding="utf-8")
    report=root/"reports/experiments/experiment_summary.md"; report.parent.mkdir(parents=True,exist_ok=True); report.write_text("# Experiment summary\n\nThis report is generated from saved pipeline outputs.\n\n## Model comparison\n\n"+json.dumps(metrics["models"],indent=2)+"\n\n## Threshold sensitivity\n\n"+json.dumps(thresholds,indent=2)+"\n",encoding="utf-8")
    return output
