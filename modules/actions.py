import uuid
from utils import logger
from healthcheck import db_health, redis_health

import actions

from db import form_model, action_model, action_meta
from cassandra.cqlengine.management import sync_table

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler


async def register_actions(data, queue, scheduler):
    """Function for registering actions into a form

    :param data: FastAPI BaseModel object containing the essential properties
    :param formDB: Object to interact with the forms model
    :param actionDB: Object to interact with the actions model

    """
    logging = logger("register action")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")

        logging.info("Registering new action")
        sync_table(action_model)
        sync_table(form_model)
        result = action_model.create(
            actionID=uuid.uuid4(),
            formID=data.formID,
            action=data.action,
            trigger=data.trigger,
            meta=[Meta(i["meta_property"], i["meta_value"]) for i in data["meta"]],
        )

        # Updating form with registered action
        form_model.objects(formID=data.formID).if_exists().update(
            actions__append=str(result.actionID)
        )

        # enqueuing action if registered to be called on deadline
        action_data = data.__dict__
        action_data["actionId"] = result.actionID
        if queue is None or not redis_health():
            queue = Queue(connection=Redis())
        if data.trigger == "on_deadline":
            form_data = form_model.objects(formID=data.formID)
            result = scheduler.cron(
                cron_string="0 5 * * *",
                func=getattr(actions, data.action),
                args=[action_data],
            )
            result = queue.enqueue_at(
                form_data["deadline"],
                getattr(actions, action_data["action"]),
                args=(action_data),
            )

        # scheduling action if registered to be called on deadline
        if scheduler is None or not redis_health():
            scheduler = Scheduler(connection=Redis())
        if data.trigger == "daily":
            result = scheduler.cron(
                cron_string="0 5 * * *",
                func=getattr(actions, data.action),
                args=[action_data],
            )
        return action_data["actionId"]

    except Exception:
        logging.exception("Registering action failed ", exc_info=True)
