from db.form_model import form_model
from utils import logger
from healthcheck import db_health
from db import form_model


async def insert_form(data, formDB):
    """Function for inserting form via forms model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param formDB: Object to interact with the forms model

    :return formId: string representation of the UUID of the newly added form
    """
    logging = logger("create form")
    try:
        if formDB is None or not db_health():
            formDB = form_model()
        logging.info("Creating new form")
        formId = formDB.add_form({"clientId": data.clientID, "deadline": data.deadline})
        logging.info("Form details added to DB successfully")
        return formId
    except Exception:
        logging.exception("Creating new form failed ", exc_info=True)
        return False
