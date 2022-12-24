import joblib

model = joblib.load('Model/Model.pkl')
OPTIMAL_THRESHOLD = 0.27080240490624297

def modelprediction(data):
    return model.predict(data)

def modelprediction_proba_percent(data):
    prediction_proba = 0
    if OPTIMAL_THRESHOLD < 0.5:
        prediction_proba = modelprediction_proba(data) / (OPTIMAL_THRESHOLD * 2 - (OPTIMAL_THRESHOLD-modelprediction_proba(data)))
    elif OPTIMAL_THRESHOLD > 0.5:
        prediction_proba = modelprediction_proba(data) / (OPTIMAL_THRESHOLD * 2 + (OPTIMAL_THRESHOLD-modelprediction_proba(data)))
    else :
        prediction_proba = modelprediction_proba(data)
    if prediction_proba > 1:
        return 0.989
    else:
        return prediction_proba

def modelprediction_proba(data):
    return model.predict_proba(data)[:, 1][0]
