"""Model explanations with optional SHAP and deterministic sklearn fallbacks."""
import numpy as np

def explain_linear(model, feature_names, row):
    estimator = model.named_steps.get("classifier", model)
    values = np.asarray(row).ravel()
    coef = np.asarray(estimator.coef_).ravel()
    pairs = sorted(({"feature": str(n), "contribution": float(c*v), "direction": "increases_risk" if c*v >= 0 else "decreases_risk"} for n,c,v in zip(feature_names, coef, values)), key=lambda x: abs(x["contribution"]), reverse=True)
    return {"method":"coefficient_contribution", "top_features":pairs[:10], "limitation":"Contributions explain model association, not causation."}

def explain_tree(model, feature_names):
    estimator = model.named_steps.get("classifier", model)
    importance = getattr(estimator, "feature_importances_", np.zeros(len(feature_names)))
    pairs = sorted(({"feature":str(n),"importance":float(v)} for n,v in zip(feature_names, importance)), key=lambda x:x["importance"], reverse=True)
    return {"method":"feature_importance", "top_features":pairs[:10], "limitation":"Importance is global association, not proof of fraud causation."}
