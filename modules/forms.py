import uuid
import datetime
from utils import logger

from healthcheck import db_health
from db import form_model
from cassandra.cqlengine.management import sync_table



async def insert_form(data, formDB):
    """Function for inserting form via forms model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param formDB: Object to interact with the forms model

    :return formId: string representation of the UUID of the newly added form
    """
    logging = logger("create form")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception('Database healthcheck failed')
        logging.info("Creating new form")
        sync_table(form_model)
        result=form_model.create(formID=uuid.uuid4(),clientID=data.clientID,deadline=data.deadline,created=datetime.datetime.now())
        logging.info("Form details added to DB successfully")
        return result.formID
    except Exception:
        logging.exception("Creating new form failed ", exc_info=True)
        return False
