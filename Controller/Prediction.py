from Model.QuestionModel import Question
from Controller.PreProccess import preProcess
from Model.ResponseModel import ResponseModel
import Core.ModelDeployment as ModelDeployment


def prediction(question: Question):
    data_df = preProcess(question)
    # predict with optimal threshold
    response = ResponseModel(
        prediction='Not Churn',
        prediction_proba=0.0,
        trashold=0
    )
    
    response.prediction_proba = ModelDeployment.modelprediction_proba_percent(data_df)
    if (ModelDeployment.modelprediction_proba(data_df) >= ModelDeployment.OPTIMAL_THRESHOLD).astype(bool) == True:
        response.prediction = 'Churn'
    else:
        response.prediction = 'Not Churn'
    # prediction probability calculation
    print (ModelDeployment.modelprediction_proba(data_df))
    
    return response