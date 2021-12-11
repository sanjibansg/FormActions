import uuid
import datetime
from utils import logger
from healthcheck import db_health, redis_health

from cassandra.cqlengine.management import sync_table
from db import response_model, form_model, action_model

import actions

from redis import Redis
from rq import Queue


async def insert_response(data, responseDB, formDB, actionDB, queue):
    """Function for inserting response via responses model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param responseDB: Object to interact with the responses model
    :param formDB: Object to interact with the forms model
    :param actionDB: Object to interact with the actions model
    :param queue: Redis queue object

    :return responseId: string representation of the UUID of the newly response
    """
    logging = logger("create response")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")
        sync_table(response_model)
        sync_table(form_model)
        sync_table(action_model)

        if queue is None or not redis_health():
            queue = Queue(connection=Redis())
        logging.info("Redis Connection sucessfully established")

        logging.info("Creating new response")
        result = response_model.create(
            responseID=uuid.uuid4(),
            formID=data.formID,
            userID=data.userID,
            responses=data.responses,
            created=datetime.datetime.now(),
        )

        # recording response into the form
        form_model.objects(formID=data.formID).if_exists().update(
            responses__append=result.responseID
        )

        # enqueing actions required to be triggered after every response
        fetch_form = form_model.objects.filter(formID=data.formID)
        logging.info("Triggering actions for the response if any")

        for actionId in fetch_form.actions:
            action_data = action_model.objects.filter(actionID=actionId)
            if action_data.trigger == "after_every_response":
                action_data.responseId = result.responseID
                result_queue = queue.enqueue(
                    getattr(actions, action_data["action"]), args=(action_data)
                )
                return result.responseID, result_queue
        return result.responseID
    except Exception:
        logging.exception("Creating new response failed ", exc_info=True)
        return False
