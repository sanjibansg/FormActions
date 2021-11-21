from fastapi import FastAPI
from pydantic import BaseModel
import datetime

class formData(BaseModel):
    formID: int
    clientID: int
    questionID: list
    actionID: list
    deadline: datetime.datetime

class questionData(BaseModel):
    questionID: int
    formID: int
    question: str
    format: str  # format for acceptable response

class answerData(BaseModel):
    answerID: int
    questionID: int
    answer: str

class responseData(BaseModel):
    responseID: int
    formID: int
    userID: int
    response: list # response is a list of [{questionID: answerID}]

app = FastAPI()


@app.post("/createForm/")
def createForm(data: formData):
    return data

@app.post("/createQuestion/")
def createQuestion(data: questionData):
    return data


@app.post("/createAnswer/")
def createAnswer(data:answerData):
    return data

@app.post("/createResponse/")
def createResponse(data:responseData):
    return data
