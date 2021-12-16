import uuid
import datetime
from utils import logger
from healthcheck import db_health, redis_health

from db import model, response_model, form_model, action_model

import actions

from redis import Redis
from rq import Queue


async def insert_response(data, queue):
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

        if queue is None or not redis_health():
            queue = Queue(connection=Redis())
        logging.info("Redis Connection sucessfully established")

        logging.info("Creating new response")
        result = response_model.create(
            response_id=uuid.uuid4(),
            form_id=data.formID,
            user_id=data.userID,
            responses=data.responses,
            created=datetime.datetime.now(),
        )

        # recording response into the form
        session=model().get_session_object()
        session.execute('''
                        UPDATE forms
                        SET responses = responses + ['{response}']
                        WHERE form_id={form_id};
                        '''.format(response=str(result.response_id),form_id=data.formID))

        # enqueing actions required to be triggered after every response
        fetch_form = form_model.get(form_id=data.formID)
        logging.info(fetch_form)
        logging.info("Triggering actions for the response if any")

        for actionId in fetch_form.actions:
            action_data = action_model.get(action_id=actionId)
            if action_data.trigger == "after_every_response":
                action_data.response_id = result.response_id
                result_queue = queue.enqueue(
                    getattr(actions, action_data["action"]), args=(action_data)
                )
                return result.response_id, result_queue
        return result.response_id
    except Exception:
        logging.exception("Creating new response failed ", exc_info=True)
        return False
