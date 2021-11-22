from fastapi import FastAPI
from pydantic import BaseModel
import datetime

import db
import actions

from redis import Redis
from rq import Queue

class formData(BaseModel):
    formID: int
    clientID: int
    questions: list
    actions: list
    deadline: datetime.datetime

class questionData(BaseModel):
    questionID: int
    formID: int
    question: str
    format: str  # format for acceptable response
    created: datetime.datetime

class answerData(BaseModel):
    answerID: int
    questionID: int
    answer: str

class responseData(BaseModel):
    responseID: int
    formID: int
    userID: int
    responses: list # response is a list of [{questionID: answerID}]

app = FastAPI()

@app.on_event("startup")
def initializeDatabase():
    global db,formDB,responseDB,questionDB,answerDB,actionDB
    formDB = db.form_model()
    responseDB = db.response_model()
    questionDB = db.question_model()
    answerDB = db.answer_model()
    actionDB = db.action_model()

@app.on_event("startup")
def initializeRedisQueue():
    global queue
    queue = Queue(connection=Redis())


@app.post("/createForm/")
def createForm(data: formData):
    formDB.add_form({
        "formId":data.formID,
        "clientId":data.clientID,
        "questions":data.questions,
        "actions":data.actions,
        "deadline":data.deadline
    })
    for action_data in data.actions:
        if action_data['trigger']=='on_deadline':
            action_func = actionDB.fetch_action(action_data['actionId'])
            result = queue.enqueue_at(getattr(data.deadline,actions,action_func[0]['action']))

@app.post("/createQuestion/")
def createQuestion(data: questionData):
    questionDB.add_question({
        "questionId":data.questionID,
        "formId":data.formID,
        "question":data.question,
        "format":data.format
    })


@app.post("/createAnswer/")
def createAnswer(data:answerData):
    answerDB.add_answer({
        "answerId":data.answerID,
        "questionId":data.questionID,
        "answer":data.answer
    })

@app.post("/createResponse/")
def createResponse(data:responseData):
    responseDB.add_answer({
        "responseId":data.responseID,
        "formId":data.formID,
        "userId":data.userID,
        "responses":data.responses
    })
    fetch_form = formDB.fetch_form(data.formID)
    for action_data in fetch_form[0]['actions']:
        if action_data['trigger']=='after_every_response':
            action_func = actionDB.fetch_action(action_data['actionId'])
            result = queue.enqueue(getattr(actions,action_func[0]['action']))
