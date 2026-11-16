"""End-to-end CPU-friendly experiment pipeline used by notebooks and CLI checks."""
from __future__ import annotations
from pathlib import Path
import json, time
import numpy as np, pandas as pd
from joblib import dump
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from .synthetic_data import generate_synthetic_transactions
from .feature_engineering import add_transaction_features
from .preprocessing import build_preprocessor
from .behavioral_analytics import customer_baselines, score_behavior
from .graph_analysis import build_transaction_graph, graph_features
from .risk_scoring import aggregate_risk
from .agent_orchestrator import investigate
from .investigation import InvestigationCase
from .explainability import explain_tree

ROOT = Path(__file__).resolve().parents[2]

def _metrics(y, scores, threshold=.5):
    pred=(np.asarray(scores)>=threshold).astype(int)
    return {"precision":float(precision_score(y,pred,zero_division=0)),"recall":float(recall_score(y,pred,zero_division=0)),"f1":float(f1_score(y,pred,zero_division=0)),"average_precision":float(average_precision_score(y,scores)),"roc_auc":float(roc_auc_score(y,scores)) if len(np.unique(y))>1 else None,"confusion_matrix":confusion_matrix(y,pred).tolist(),"false_positive_rate":float(((pred==1)&(np.asarray(y)==0)).sum()/max(1,(np.asarray(y)==0).sum()))}

def run_experiment(root: str | Path = ROOT, n: int = 2400, seed: int = 42) -> dict:
    root=Path(root); paths={k:root/"results"/k for k in ["metrics","predictions","figures","investigations","logs"]}
    for p in paths.values(): p.mkdir(parents=True,exist_ok=True)
    (root/"data"/"synthetic").mkdir(parents=True,exist_ok=True); (root/"data"/"processed").mkdir(parents=True,exist_ok=True)
    frame=generate_synthetic_transactions(n,seed); frame.to_csv(root/"data"/"synthetic"/"synthetic_banking_transactions.csv",index=False)
    feat=add_transaction_features(frame)
    feat["timestamp"] = pd.to_datetime(feat["timestamp"])
    numeric=["amount","previous_transaction_count","previous_amount","amount_deviation","customer_historical_average","customer_transaction_frequency","hours_since_previous","transaction_hour","day_of_week","is_unusual_hour","unusual_amount","rapid_repeat","new_device_id","new_location"]
    categorical=["transaction_type","channel","location"]
    X=feat[numeric+categorical]; y=feat["is_fraud"].astype(int)
    train_idx,test_idx=train_test_split(np.arange(len(feat)),test_size=.2,stratify=y,random_state=seed)
    pre=build_preprocessor(numeric,categorical)
    Xtr=pre.fit_transform(X.iloc[train_idx]); Xte=pre.transform(X.iloc[test_idx])
    names=list(pre.get_feature_names_out())
    results={"seed":seed,"rows":len(feat),"fraud_rate":float(y.mean()),"models":{}}
    for label, model in [("logistic", __import__("sklearn.linear_model",fromlist=["LogisticRegression"]).LogisticRegression(max_iter=500,class_weight="balanced",random_state=seed)),("random_forest",RandomForestClassifier(n_estimators=120,max_depth=12,class_weight="balanced_subsample",random_state=seed,n_jobs=-1))]:
        started=time.perf_counter(); model.fit(Xtr,y.iloc[train_idx]); scores=model.predict_proba(Xte)[:,1]
        results["models"][label]=_metrics(y.iloc[test_idx],scores); results["models"][label]["fit_seconds"]=time.perf_counter()-started
        dump({"preprocessor":pre,"model":model,"numeric":numeric,"categorical":categorical},root/"models"/"supervised"/f"{label}.joblib")
    iso=IsolationForest(n_estimators=150,contamination=.08,random_state=seed,n_jobs=-1); iso.fit(Xtr); raw=-iso.score_samples(Xte); anomaly=(raw-raw.min())/(raw.max()-raw.min()+1e-9)
    results["models"]["isolation_forest"]=_metrics(y.iloc[test_idx],anomaly,.65); dump({"preprocessor":pre,"model":iso},root/"models"/"anomaly"/"isolation_forest.joblib")
    behavior=score_behavior(feat,customer_baselines(feat)); bscore=np.clip(behavior["amount_zscore"].abs().fillna(0).astype(float)/6,0,1).to_numpy()
    graph=build_transaction_graph(feat.rename(columns={"sender_account":"source_account","receiver_account":"destination_account"})); gf=graph_features(graph)
    graph_map=gf.set_index("account")["degree"].to_dict(); gscore=np.array([min(1,float(graph_map.get(a,0))/10) for a in feat["sender_account"]])
    sup_all=np.zeros(len(feat)); anom_all=np.zeros(len(feat)); sup_all[test_idx]=results["models"]["logistic"].get("_unused",0); sup_model=__import__("sklearn.linear_model",fromlist=["LogisticRegression"]).LogisticRegression()
    # Refit the persisted supervised model on all rows for reproducible artifact predictions.
    final_model=__import__("sklearn.linear_model",fromlist=["LogisticRegression"]).LogisticRegression(max_iter=500,class_weight="balanced",random_state=seed).fit(pre.fit_transform(X),y)
    sup_all=final_model.predict_proba(pre.transform(X))[:,1]; anom_all=np.clip((-iso.score_samples(pre.transform(X)) - raw.min())/(raw.max()-raw.min()+1e-9),0,1)
    risk_rows=[]
    for i in range(len(feat)):
        risk=aggregate_risk({"supervised":sup_all[i],"anomaly":anom_all[i],"behavioral":bscore[i],"graph":gscore[i]},weights={"supervised":.4,"anomaly":.2,"behavioral":.25,"graph":.15})
        risk_rows.append(risk)
    pred=feat[["transaction_id","customer_id","timestamp","amount","is_fraud"]].copy(); pred["supervised_score"]=sup_all; pred["anomaly_score"]=anom_all; pred["behavioral_score"]=bscore; pred["graph_score"]=gscore; pred["risk_score"]=[r["score"] for r in risk_rows]; pred["risk_category"]=[r["category"] for r in risk_rows]; pred.to_csv(paths["predictions"]/"transaction_predictions.csv",index=False)
    cases=[]
    for i in np.argsort(pred.risk_score.to_numpy())[-20:][::-1]:
        state=investigate(feat.iloc[i].to_dict(),model_score=float(sup_all[i]),anomaly_score=float(anom_all[i]),behavioral_score=float(bscore[i]),graph_score=float(gscore[i]))
        case=InvestigationCase(str(feat.iloc[i].transaction_id),state.outputs["risk"],state.outputs["explanation"]); cases.append(case.to_dict())
    (paths["investigations"]/"cases.json").write_text(json.dumps(cases,indent=2,default=str),encoding="utf-8")
    results["artifacts"]={"dataset":"data/synthetic/synthetic_banking_transactions.csv","predictions":"results/predictions/transaction_predictions.csv","cases":"results/investigations/cases.json"}; (paths["metrics"]/"pipeline_metrics.json").write_text(json.dumps(results,indent=2,default=str),encoding="utf-8")
    return results
