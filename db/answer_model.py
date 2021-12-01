from .model import model
import uuid
from utils import logger


class answer_model(model):
    """Class for handling the answer table in cassandra"""

    def __init__(self):
        logging = logger("answer model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for answers table")
            super().__init__()
            createQuery = """
                                CREATE TABLE IF NOT EXISTS answers(
                                answerId uuid,
                                questionId uuid,
                                answer text,
                                PRIMARY KEY(answerId));"""
            self.session.execute(createQuery)
            logging.info("[Connecting to Cassandra] Answers table found sucessfully")
        except Exception:
            logging.exception("Error while connecting to answer table", exc_info=True)

    def add_answer(self, data):
        """Function for inserting new answer into answers table

        :param data: Object which stores the essential properties like questionId,answer

        :return answerId: UUID of the newly added action
        """
        logging = logger("answer model insert")
        try:
            logging.info("[AnswerDB] Inserting into answers table")
            answerId = uuid.uuid4()
            self.session.execute(
                "INSERT INTO answers (answerId,questionId,answer) VALUES (%s,%s,%s)",
                (answerId, data["questionId"], data["answer"]),
            )
            logging.info("[AnswerDB] Insertion into actions table successful")
            return str(answerId)
        except Exception:
            logging.exception("Error while inserting into answer table", exc_info=True)

    def fetch_answer(self, answerId):
        """Function for fetching answer from the answers table

        :param answerId: string containing the UUID of the action

        :return result: ResultSet from cassandra containing the action details
        """
        logging = logger("answer model fetch")
        try:
            logging.info("[AnswerDB] Fetching from answers table")
            fetchQuery = """
                        SELECT * FROM answers
                        WHERE answerId={answerId}
                        """.format(
                answerId=answerId
            )
            result = self.session.execute(fetchQuery)
            logging.info("[AnswerDB] Fetch from answers table successful")
            return result
        except Exception:
            logging.exception("Error while fetching into answer table", exc_info=True)
