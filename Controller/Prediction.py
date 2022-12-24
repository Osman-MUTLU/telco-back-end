from Model.QuestionModel import Question
from Controller.PreProccess import preProcess
from Model.ResponseModel import ResponseModel
import joblib


#OPTIMAL_THRESHOLD = 0.1990166589920821

OPTIMAL_THRESHOLD = 0.5
def prediction(question: Question):
    data_df = preProcess(question)
    # load model
    model = joblib.load('Model/Model.pkl')
    # predict with optimal threshold
    response = ResponseModel(
        prediction='Not Churn',
        prediction_proba=0.0,
        trashold=OPTIMAL_THRESHOLD
    )
    if (model.predict_proba(data_df)[:, 1] >= OPTIMAL_THRESHOLD).astype(bool) == True:
        response.prediction = 'Churn'
    else:
        response.prediction = 'Not Churn'
    # prediction probability calculation
    print (model.predict_proba(data_df)[:, 1][0])
    if OPTIMAL_THRESHOLD < 0.5:
        response.prediction_proba = model.predict_proba(data_df)[:, 1][0] / (OPTIMAL_THRESHOLD * 2 - (OPTIMAL_THRESHOLD-model.predict_proba(data_df)[:, 1][0]))
    elif OPTIMAL_THRESHOLD > 0.5:
        response.prediction_proba = model.predict_proba(data_df)[:, 1][0] / (OPTIMAL_THRESHOLD * 2 + (OPTIMAL_THRESHOLD-model.predict_proba(data_df)[:, 1][0]))
    else :
        response.prediction_proba = model.predict_proba(data_df)[:, 1][0]
    if response.prediction_proba > 1:
        response.prediction_proba = 0.989
    
    return response