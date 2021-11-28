from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

import datetime

import db
import actions
from utils import logger
from healthcheck import db_health,redis_health

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
    responses: list # response is a list of [{questionId: {questionID},answerId:{answerID}}]


app = FastAPI()

@app.on_event("startup")
def initialize():
    logging=logger("cassandraDB")
    try:
        logging.info("Establishing CassandraDB Connection")
        global formDB,responseDB,questionDB,answerDB,actionDB
        formDB = db.form_model()
        responseDB = db.response_model()
        questionDB = db.question_model()
        answerDB = db.answer_model()
        actionDB = db.action_model()
        logging.info("CassandraDB Connection established sucessfully!")
    except Exception:
        logging.exception("CassandraDB Connection failed ",exc_info=True)

    logging=logger("redis")
    try:
        logging.info("Establishing Redis Connection")
        global queue,scheduler
        queue = Queue(connection=Redis())
        scheduler = Scheduler(connection=Redis())
        logging.info("Redis Connection sucessfully established")
    except Exception:
        logging.exception("Redis Connection failed ",exc_info=True)


@app.post("/createForm/")
def createForm(data: formData):
    logging=logger("create form")
    try:
        while(not formDB or not db_health(formDB.get_session_object())):
            formDB = db.form_model()
        logging.info("Creating new form")
        formDB.add_form({
            "formId":data.formID,
            "clientId":data.clientID,
            "questions":data.questions,
            "actions":data.actions,
            "deadline":data.deadline
        })
        logging.info("Form details added to DB successfully")
        while(not actionDB  or not db_health(formDB.get_session_object())):
            actionDB = db.action_model()
        while(not queue or not redis_health(Redis())):
                queue = Queue(connection=Redis())
                scheduler = Scheduler(queue=queue)
        for action_data in data.actions:
            if action_data['trigger']=='on_deadline':
                action_func = actionDB.fetch_action(action_data['actionId'])
                result = queue.enqueue_at(data.deadline,getattr(actions,action_func[0]['action']))
            elif action_data['trigger']=='daily':
                action_func = actionDB.fetch_action(action_data['actionId'])
                result = scheduler.cron(cron_string="0 5 * * *",func=getattr(data.deadline,actions,action_func[0]['action']))
    except Exception:
        logging.exception("Creating new form failed ",exc_info=True)


@app.post("/createQuestion/")
def createQuestion(data: questionData):
    logging=logger("create question")
    try:
        while(not questionDB or not db_health(questionDB.get_session_object())):
            global formDB, actionDB
            questionDB = db.question_model()
        logging.info("Creating new question")
        questionDB.add_question({
            "questionId":data.questionID,
            "formId":data.formID,
            "question":data.question,
            "format":data.format
        })
    except Exception:
        logging.exception("Creating new question failed ",exc_info=True)


@app.post("/createAnswer/")
def createAnswer(data:answerData):
    logging=logger("create answer")
    try:
        while(not answerDB or not db_health(answerDB.get_session_object())):
            answerDB = db.answer_model()
        logging.info("Creating new answer")
        answerDB.add_answer({
            "answerId":data.answerID,
            "questionId":data.questionID,
            "answer":data.answer
        })
    except Exception:
        logging.exception("Creating new answer failed ",exc_info=True)

@app.post("/createResponse/")
def createResponse(data:responseData):
    logging=logger("create response")
    try:
        while(not responseDB or not db_health(responseDB.get_session_object())):
            responseDB = db.answer_model()
        logging.info("Creating new response")
        responseDB.add_answer({
            "responseId":data.responseID,
            "formId":data.formID,
            "userId":data.userID,
            "responses":data.responses
        })
        fetch_form = formDB.fetch_form(data.formID)
        logging.info("Triggering actions for the response if any")
        while(not queue or not redis_health(Redis())):
            queue = Queue(connection=Redis())
            scheduler = Scheduler(queue=queue)
        for action_data in fetch_form[0]['actions']:
            if action_data['trigger']=='after_every_response':
                action_func = actionDB.fetch_action(action_data['actionId'])
                result = queue.enqueue(getattr(actions,action_func[0]['action']))
    except Exception:
        logging.exception("Creating new response failed ",exc_info=True)
