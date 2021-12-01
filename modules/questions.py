from db.form_model import form_model
from utils import logger
from healthcheck import db_health
from db import question_model, form_model


async def insert_question(data, questionDB, formDB):
    """Function for inserting question via questions model object

    :param data: FastAPI BaseModel object containing the essential properties
    :param questionDB: Object to interact with the questions model
    :param formDB: Object to interact with the forms model

    :return questionId: string representation of the UUID of the newly added question
    """
    logging = logger("create question")
    try:
        if questionDB is None or not db_health():
            questionDB = question_model()
        if formDB is None or not db_health():
            formDB = form_model()
        logging.info("Creating new question")
        questionId = questionDB.add_question(
            {"formId": data.formID, "question": data.question, "format": data.format}
        )

        # updating form record with added question
        formDB.add_question(formId=data.formID, questionId=questionId)
        return questionId

    except Exception:
        logging.exception("Creating new question failed ", exc_info=True)
        return False
