from utils import logger
from healthcheck import db_health, redis_health
from db import response_model, form_model, action_model
import actions

from redis import Redis
from rq import Queue


def insert_response(data, responseDB, formDB, actionDB, queue):
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
        if responseDB is None or not db_health():
            responseDB = response_model()
        if formDB is None or not db_health():
            formDB = form_model()
        if actionDB is None or not db_health():
            actionDB = action_model()
        if queue is None or not redis_health():
            queue = Queue(connection=Redis())

        logging.info("Redis Connection sucessfully established")
        logging.info("Creating new response")
        responseId = responseDB.add_response(
            {"formId": data.formID, "userId": data.userID, "responses": data.responses}
        )

        # recording response into the form
        formDB.add_response(data.formID, responseId)

        # enqueing actions required to be triggered after every response
        fetch_form = formDB.fetch_form(data.formID)
        logging.info("Triggering actions for the response if any")

        for actionId in fetch_form.one()["actions"]:
            action_data = actionDB.fetch_action(actionId).one()
            if action_data["trigger"] == "after_every_response":
                action_data["responseId"] = responseId
                result = queue.enqueue(
                    getattr(actions, action_data["action"]), args=(action_data)
                )
                return responseId, result
        return responseId
    except Exception:
        logging.exception("Creating new response failed ", exc_info=True)
        return False
