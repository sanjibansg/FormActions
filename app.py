from fastapi import FastAPI
from fastapi_health import health
from pydantic import BaseModel

import datetime

from db import model
from cassandra.cqlengine import connection

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

queue, scheduler = None, None

@app.on_event("startup")
def initialize():
    logging = logger("cassandraDB")
    try:
        logging.info("Establishing CassandraDB Connection")
        db_conn = model()
        connection.register_connection('FormCluster',session=db_conn.get_session_object())
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


@app.get("/")
def ping():
    return {"api_service": "up and running"}


@app.post("/createForm/")
async def createForm(data: formData):
    result = await modules.insert_form(data)
    return result


@app.post("/createQuestion/")
async def createQuestion(data: questionData):
    result = await modules.insert_question(data)
    return result


@app.post("/createAnswer/")
async def createAnswer(data: answerData):
    result = await modules.insert_answer(data)
    return result


@app.post("/createResponse/")
async def createResponse(data: responseData):
    global queue
    result = await modules.insert_response(data,queue)
    return result


@app.post("/registerAction/")
async def registerAction(data: actionData):
    global queue, scheduler
    result = await modules.register_actions(data, queue, scheduler)
    return result
