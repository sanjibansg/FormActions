import uuid
from utils import logger
from healthcheck import db_health

from db import answer_model
from cassandra.cqlengine.management import sync_table


async def insert_answer(data, answerDB):
    """Function for inserting answers via answer model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param answerDB: Object to interact with the answers model

    :return answerId: string representation of the UUID of the newly added answer
    """
    logging = logger("create answer")
    try:
        db_healthcheck = db_health()
        if db_healthcheck == {"db_health": "unavailable"}:
            raise Exception("Database healthcheck failed")
        logging.info("Creating new answer")
        sync_table(answer_model)
        result = answer_model.create(
            answerID=uuid.uuid4(), questionID=data.questionID, answer=data.answer
        )
        return result.answerID
    except Exception:
        logging.exception("Creating new answer failed ", exc_info=True)
        return False
