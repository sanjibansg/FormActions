import uuid
from utils import logger
from healthcheck import db_health, redis_health

import actions

from db import model, form_model, action_model, action_meta_data

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

        logging.info("[action_model] Registering new action")
        result = action_model.create(
            action_id=uuid.uuid4(),
            form_id=data.formID,
            action=data.action,
            trigger=data.trigger,
            meta=[
                action_meta_data(meta_property=i["meta_property"], meta_value=i["meta_value"])
                for i in data.meta
            ],
        )

        logging.info("[action_model] Updating forms with new action")
        # Updating form with registered action
        session=model().get_session_object()
        session.execute(
                "UPDATE forms SET actions = actions+['{actionId}'] WHERE form_id = {formId};".format(
                    actionId=str(result.action_id), formId=data.formID
                )
            )

        logging.info("[action_model] Scheduling actions if any")
        # enqueuing action if registered to be called on deadline
        action_data = data.__dict__
        action_data["actionId"] = result.action_id
        if queue is None or not redis_health():
            queue = Queue(connection=Redis())
        if data.trigger == "on_deadline":
            form_data = form_model.objects(form_id=data.formID)
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
        logging.info("[action_model] Registering action was successful")
        return action_data["actionId"]

    except Exception:
        logging.exception("Registering action failed ", exc_info=True)
