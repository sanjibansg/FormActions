from .model import model
import datetime
import uuid
from utils import logger


class response_model(model):
    """Class for handling the responses table in cassandra"""

    def __init__(self):
        logging = logger("response model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for responses table")
            super().__init__()
            createQuery = """
                            CREATE TABLE IF NOT EXISTS responses(
                            responseId uuid,
                            formId text,
                            userId text,
                            responses list<text>,
                            created timestamp,
                            PRIMARY KEY(responseId));"""
            self.session.execute(createQuery)
            logging.info("Responses table found sucessfully")
        except Exception:
            logging.exception(
                "Error while connecting to responses table", exc_info=True
            )

    def add_response(self, data):
        """Function to add new response into responses table

        :param data: Object which stores the essential properties like formId,userId,responses

        :return responseId: string representation of the UUID of the newly added response

        """
        logging = logger("response model insert")
        try:
            logging.info("[ResponseDB] Inserting into ResponseDB")
            responseId = uuid.uuid4()
            self.session.execute(
                "INSERT INTO responses (responseId,formId,userId,responses,created) VALUES (%s,%s,%s,%s,%s)",
                (
                    responseId,
                    data["formId"],
                    data["userId"],
                    data["responses"],
                    datetime.datetime.now(),
                ),
            )
            return str(responseId)
        except Exception:
            logging.exception(
                "Error while inserting into responses table", exc_info=True
            )
            return False

    def fetch_response(self, responseId):
        """Function to fetch response from the responses table

        :param responseId: string containing the UUID of the response

        :return result: ResultSet from cassandra containing the response details

        """
        logging = logger("response model fetch")
        try:
            fetchQuery = """
                            SELECT * FROM responses
                            WHERE responseId={responseId}
                            """.format(
                responseId=responseId
            )
            result = self.session.execute(fetchQuery)
            return result
        except Exception:
            logging.exception(
                "Error while fetching from responses table", exc_info=True
            )
            return False
