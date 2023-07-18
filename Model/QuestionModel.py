from pydantic import BaseModel
from datetime import datetime


class Question(BaseModel):
    birthday: datetime
    hasPartner: bool
    hasDependents: bool
    tenure: int
    InternetService: str
    hasOnlineSecurity: bool
    hasTechSupport: bool
    contractType: str
    paperlessBilling: bool
    paymentMethod: str
    monthlyCharges: float
    totalCharges: float
    totalServices: int
