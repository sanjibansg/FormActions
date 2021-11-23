from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

import datetime

import db
import actions

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

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
    global formDB,responseDB,questionDB,answerDB,actionDB
    formDB = db.form_model()
    responseDB = db.response_model()
    questionDB = db.question_model()
    answerDB = db.answer_model()
    actionDB = db.action_model()

@app.on_event("startup")
def initializeRedisQueue():
    global queue,scheduler
    queue = Queue(connection=Redis())
    scheduler = Scheduler(queue=queue)

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
            result = queue.enqueue_at(data.deadline,getattr(actions,action_func[0]['action']))
        elif action_data['trigger']=='daily':
            action_func = actionDB.fetch_action(action_data['actionId'])
            result = scheduler.cron(cron_string="0 5 * * *",func=getattr(data.deadline,actions,action_func[0]['action']))


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

# Cron job for every day
@repeat_every(seconds=86400)
def cron_daily():
    forms = formDB.fetchAll()
    for form in forms:
        for action_func in form['actions']:
            if action_func['trigger']=='daily':
                result = queue.enqueue(getattr(actions,action_func[0]['action']))
