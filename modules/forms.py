import uuid
import datetime
from utils import logger

from healthcheck import db_health
from db import form_model


async def insert_form(data):
    """Function for inserting form via forms model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param formDB: Object to interact with the forms model

    :return formId: string representation of the UUID of the newly added form
    """
    logging = logger("create form")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")
        logging.info("[forms_model] Creating new form")
        result = form_model.create(
            form_id=uuid.uuid4(),
            client_id=data.clientID,
            deadline=data.deadline,
            created=datetime.datetime.now(),
        )
        logging.info("[form_model] New answer creation was successful")
        return result.form_id
    except Exception:
        logging.exception("Creating new form failed ", exc_info=True)
        return False
