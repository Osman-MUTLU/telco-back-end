from pydantic import BaseModel

class ResponseModel(BaseModel):
    prediction: str
    prediction_proba: float
    trashold: float
