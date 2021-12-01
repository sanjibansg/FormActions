from fastapi import FastAPI
from fastapi_health import health
from pydantic import BaseModel

import datetime

import db
from utils import logger
from healthcheck import db_health, redis_health
import modules

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler


class formData(BaseModel):
    clientID: str
    deadline: datetime.datetime


class questionData(BaseModel):
    formID: str
    question: str
    format: str  # format for acceptable response


class answerData(BaseModel):
    questionID: str
    answer: str


class responseData(BaseModel):
    formID: str
    userID: str
    responses: list  # response is a list of answerIds


class actionData(BaseModel):
    formID: str
    action: str
    trigger: str
    meta: list


app = FastAPI()
app.add_api_route("/health", health([db_health, redis_health]))

formDB, responseDB, questionDB, answerDB, actionDB = [None] * 5
queue, scheduler = None, None


@app.on_event("startup")
async def initialize():
    logging = logger("cassandraDB")
    try:
        logging.info("Establishing CassandraDB Connection")
        global formDB, responseDB, questionDB, answerDB, actionDB
        formDB = db.form_model()
        responseDB = db.response_model()
        questionDB = db.question_model()
        answerDB = db.answer_model()
        actionDB = db.action_model()
        logging.info("CassandraDB Connection established sucessfully!")
    except Exception:
        logging.exception("CassandraDB Connection failed ", exc_info=True)

    logging = logger("redis")
    try:
        logging.info("Establishing Redis Connection")
        global queue, scheduler
        queue = Queue(connection=Redis())
        scheduler = Scheduler(connection=Redis())
        logging.info("Redis Connection sucessfully established")
    except Exception:
        logging.exception("Redis Connection failed ", exc_info=True)


@app.post("/createForm/")
async def createForm(data: formData):
    global formDB
    return modules.insert_form(data, formDB)


@app.post("/createQuestion/")
async def createQuestion(data: questionData):
    global questionDB, formDB
    return modules.insert_question(data, questionDB, formDB)


@app.post("/createAnswer/")
async def createAnswer(data: answerData):
    global answerDB
    return modules.insert_answer(data, answerDB)


@app.post("/createResponse/")
async def createResponse(data: responseData):
    global responseDB, formDB, actionDB, queue
    return modules.insert_response(data, responseDB, formDB, actionDB, queue)


@app.post("/registerAction/")
async def registerAction(data: actionData):
    global formDB, actionDB, scheduler
    return modules.register_actions(data, formDB, actionDB, scheduler)
