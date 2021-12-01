from utils import logger
from healthcheck import db_health, redis_health
import actions
from db import form_model, action_model

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler


async def register_actions(data, formDB, actionDB, queue, scheduler):
    """Function for registering actions into a form

    :param data: FastAPI BaseModel object containing the essential properties
    :param formDB: Object to interact with the forms model
    :param actionDB: Object to interact with the actions model

    """
    logging = logger("register action")
    try:
        if formDB is None or not db_health():
            formDB = form_model()
        if actionDB is None or not db_health():
            actionDB = action_model()
        logging.info("Registering new action")
        actionId = actionDB.add_action(
            {
                "formId": data.formID,
                "action": data.action,
                "trigger": data.trigger,
                "meta": data.meta,
            }
        )

        # Updating form with registered action
        formDB.add_action(formId=data.formID, actionId=actionId)

        # enqueuing action if registered to be called on deadline
        action_data = data.__dict__
        action_data["actionId"] = actionId
        if queue is None or not redis_health():
            queue = Queue(connection=Redis())
        if data.trigger == "on_deadline":
            form_data = formDB.fetch_form(data.formID).one()
            result = scheduler.cron(
                cron_string="0 5 * * *",
                func=getattr(actions, data.action),
                args=[action_data],
            )
            result = queue.enqueue_at(form_data['deadline'], getattr(actions, action_data["action"]),  args=(action_data))

        # scheduling action if registered to be called on deadline
        if scheduler is None or not redis_health():
            scheduler = Scheduler(connection=Redis())
        if data.trigger == "daily":
            result = scheduler.cron(
                cron_string="0 5 * * *",
                func=getattr(actions, data.action),
                args=[action_data]
            )

    except Exception:
        logging.exception("Registering action failed ", exc_info=True)
