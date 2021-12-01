from utils import logger
from healthcheck import db_health
from db import answer_model


async def insert_answer(data, answerDB):
    """Function for inserting answers via answer model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param answerDB: Object to interact with the answers model

    :return answerId: string representation of the UUID of the newly added answer
    """
    logging = logger("create answer")
    try:
        if answerDB is None or not db_health():
            answerDB = answer_model()
        logging.info("Creating new answer")
        answerId = answerDB.add_answer(
            {"questionId": data.questionID, "answer": data.answer}
        )
        return answerId
    except Exception:
        logging.exception("Creating new answer failed ", exc_info=True)
        return False
