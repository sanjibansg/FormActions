import os
import glob
from fastapi import FastAPI
from fastapi_health import health
from pydantic import BaseModel

import datetime

from db import (
    model,
    action_model,
    form_model,
    response_model,
    question_model,
    answer_model,
)
from db import action_meta_data
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import management


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
        if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
            os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
        db_conn = model()
        connection.register_connection(
            "FormCluster", session=db_conn.get_session_object()
        )
        logging.info("CassandraDB Connection established sucessfully!")
    except Exception:
        logging.exception("CassandraDB Connection failed ", exc_info=True)

    try:
        logging.info("Instantiating tables in keyspace if they don't exist")
        cql_files = [f for f in glob.glob("db/init/*.cql")]
        session = db_conn.get_session_object()
        for file in cql_files:
            with open(file, mode="r") as f:
                lines = f.read()
                statements = lines.split(r";")
                for i in statements:
                    statement = i.strip()
                    if statement != "":
                        session.execute(statement)
        logging.info("All tables found/instantiated.")
    except Exception:
        logging.exception("Error while finding/instantiating tables ", exc_info=True)

    try:
        logging.info("Syncing tables for object mapping")
        management.sync_type("formactions", action_meta_data)
        sync_table(action_model)
        sync_table(form_model)
        sync_table(question_model)
        sync_table(answer_model)
        sync_table(response_model)
        logging.info("All tables synced")
    except Exception:
        logging.exception("Error while syncing tables ", exc_info=True)

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
    result = await modules.insert_response(data, queue)
    return result


@app.post("/registerAction/")
async def registerAction(data: actionData):
    global queue, scheduler
    result = await modules.register_actions(data, queue, scheduler)
    return result
