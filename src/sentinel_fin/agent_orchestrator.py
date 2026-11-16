from dataclasses import dataclass, field
from datetime import datetime, timezone
from .risk_scoring import aggregate_risk

@dataclass
class InvestigationState:
    transaction: dict
    outputs: dict = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)

def investigate(transaction, *, model_score=0.0, anomaly_score=0.0,
                behavioral_score=0.0, graph_score=0.0):
    state = InvestigationState(dict(transaction))
    state.outputs["transaction"] = {"valid": bool(transaction), "fields": sorted(transaction)}
    signals = {"supervised": model_score, "anomaly": anomaly_score,
               "behavioral": behavioral_score, "graph": graph_score}
    state.outputs["risk"] = aggregate_risk(signals)
    state.outputs["explanation"] = {
        "evidence": [name for name, value in signals.items() if value >= .6],
        "next_step": "Human analyst review"}
    state.audit.append({"timestamp": datetime.now(timezone.utc).isoformat(),
                        "event": "investigation_completed", "risk": state.outputs["risk"]})
    return state
