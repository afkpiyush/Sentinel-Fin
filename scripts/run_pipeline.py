from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sentinel_fin.pipeline import run_experiment
from sentinel_fin.experiments import run_experiments
from sentinel_fin.local_llm import ollama_status, summarize_locally

root=Path(__file__).resolve().parents[1]
metrics=run_experiment(root)
experiments=run_experiments(root)
llm_status=ollama_status()
cases=[
 {"case":"normal","risk_score":.08,"signals":[],"facts":"Amount 25, familiar device, daytime purchase."},
 {"case":"unusual_but_potentially_legitimate","risk_score":.48,"signals":["new_device"],"facts":"Amount 310, new device, daytime travel purchase."},
 {"case":"high_risk_suspicious","risk_score":.91,"signals":["large_amount","rapid_repeat","new_location"],"facts":"Amount 1800, three transfers in ten minutes, new location."},
]
llm_results=[summarize_locally(c, model="qwen2.5:3b") for c in cases]
(root/"results"/"metrics"/"llm_status.json").write_text(json.dumps({"status":llm_status,"model":"qwen2.5:3b","cases":llm_results},indent=2,default=str),encoding="utf-8")
print(json.dumps({"metrics":metrics,"experiments":experiments,"ollama":llm_status,"llm_cases":llm_results},indent=2,default=str))
