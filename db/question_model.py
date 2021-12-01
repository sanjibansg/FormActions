from .model import model
import datetime
import uuid
from utils import logger


class question_model(model):
    """Class for handling the questions table in cassandra"""

    def __init__(self):
        logging = logger("question model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for questions table")
            super().__init__()
            createQuery = """
                            CREATE TABLE IF NOT EXISTS questions(
                            questionId uuid,
                            formId text,
                            question text,
                            format text,
                            created timestamp,
                            PRIMARY KEY(questionId));"""
            self.session.execute(createQuery)
            logging.info("Questions table found sucessfully")
        except:
            logging.exception(
                "Error while connecting to questions table", exc_info=True
            )

    def add_question(self, data):
        """Function to add new question into questions table

        :param data: Object which stores the essential properties like formId,question,format

        :return questionId: string representation of the UUID of the newly added question

        """
        logging = logger("question model insert")
        try:
            logging.info("[QuestionDB] Inserting into question table")
            questionId = uuid.uuid4()
            self.session.execute(
                "INSERT INTO questions (questionId,formId,question,format,created) VALUES (%s,%s,%s,%s,%s)",
                (
                    questionId,
                    data["formId"],
                    data["question"],
                    data["format"],
                    datetime.datetime.now(),
                ),
            )
            return str(questionId)
        except Exception:
            logging.exception(
                "Error while inserting into questions table", exc_info=True
            )
            return False

    def fetch_question(self, questionId):
        """Function to fetch question from the questions table

        :param questionId: string containing the UUID of the question

        :return result: ResultSet from cassandra containing the question details

        """
        logging = logger("question model fetch")
        try:
            logging.info("[QuestionDB] Fetching from question table")
            fetchQuery = """
                            SELECT * FROM questions
                            WHERE questionId = {questionId};
                            """.format(
                questionId=questionId
            )
            result = self.session.execute(fetchQuery)
            return result
        except Exception:
            logging.exception(
                "Error while fetching from into questions table", exc_info=True
            )
            return False
