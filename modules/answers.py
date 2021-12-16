import uuid
from utils import logger
from healthcheck import db_health

from db import answer_model


async def insert_answer(data):
    """Function for inserting answers via answer model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param answerDB: Object to interact with the answers model

    :return answer_id: string representation of the UUID of the newly added answer
    """
    logging = logger("create answer")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")
        logging.info("[answer_model] Creating new answer")
        result = answer_model.create(
            answer_id=uuid.uuid4(), question_id=data.questionID, answer=data.answer
        )
        logging.info("[answer_model] New answer creation was successful")
        return result.answer_id
    except Exception:
        logging.exception("Creating new answer failed ", exc_info=True)
        return False
