from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Model.QuestionModel import Question
from Model.ResponseModel import ResponseModel
from Controller.Prediction import prediction
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=ResponseModel)
async def predict(question: Question):
    return prediction(question)