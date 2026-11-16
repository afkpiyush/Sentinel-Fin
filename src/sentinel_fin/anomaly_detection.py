from sklearn.ensemble import IsolationForest

def fit_isolation_forest(X, *, contamination="auto", random_state=42):
    model = IsolationForest(contamination=contamination, random_state=random_state, n_estimators=100)
    return model.fit(X)

def anomaly_scores(model, X):
    return -model.score_samples(X)
