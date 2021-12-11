import uuid
import datetime
from utils import logger
from healthcheck import db_health
from db import question_model, form_model
from cassandra.cqlengine.management import sync_table


async def insert_question(data):
    """Function for inserting question via questions model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param questionDB: Object to interact with the questions model
    :param formDB: Object to interact with the forms model

    :return questionId: string representation of the UUID of the newly added question
    """
    logging = logger("create question")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")
        sync_table(question_model)
        sync_table(form_model)
        logging.info("Creating new question")
        result = question_model.create(
            questionID=uuid.uuid4(),
            formID=data.formID,
            question=data.question,
            question_format=data.format,
            created=datetime.datetime.now(),
        )

        # updating form record with added question
        form_model.objects(formID=data.formID).if_exists().update(
            questions__append=result.questionID
        )
        return result.questionID

    except Exception:
        logging.exception("Creating new question failed ", exc_info=True)
        return False
