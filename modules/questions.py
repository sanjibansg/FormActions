import uuid
import datetime
from utils import logger
from healthcheck import db_health
from db import model, question_model


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
        logging.info("Creating new question")
        result = question_model.create(
            question_id=uuid.uuid4(),
            form_id=data.formID,
            question=data.question,
            question_format=data.format,
            created=datetime.datetime.now(),
        )

        # updating form record with added question
        session=model().get_session_object()
        session.execute("""
                        UPDATE forms
                        SET questions = questions + ['{question}']
                        WHERE form_id={formId};
                        """.format(
                question=str(result.question_id), formId=data.formID
            ))
        return result.question_id

    except Exception:
        logging.exception("Creating new question failed ", exc_info=True)
        return False
