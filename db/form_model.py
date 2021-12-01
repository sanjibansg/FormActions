from .model import model
import datetime
import uuid
from utils import logger


class form_model(model):
    """Class for handling the forms table in cassandra"""

    def __init__(self):
        logging = logger("form model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for forms table")
            super().__init__()
            createQuery = """
                            CREATE TABLE IF NOT EXISTS forms(
                            formId uuid,
                            clientId text,
                            questions list<text>,
                            responses list<text>,
                            actions list<text>,
                            created timestamp,
                            deadline timestamp,
                            PRIMARY KEY(formId));
                        """
            self.session.execute(createQuery)
            logging.info("Forms table found/created sucessfully")
        except Exception:
            logging.exception("Error while connecting to forms table", exc_info=True)

    def add_form(self, data):
        """Function to add new forms into forms table

        :param data: Object which stores the essential properties like clientId, deadline

        :return actionId: UUID of the newly added form

        """
        logging = logger("form model insert")
        try:
            logging.info("[FormsDB] Inserting into forms table")
            formId = uuid.uuid4()
            self.session.execute(
                "INSERT INTO forms (formId,clientId,created,deadline) VALUES (%s,%s,%s,%s)",
                (
                    formId,
                    data["clientId"],
                    datetime.datetime.now(),
                    str(data["deadline"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                ),
            )
            logging.info("[FormsDB] Insertion from forms table successful")
            return str(formId)
        except Exception:
            logging.exception("Error while inserting into forms table", exc_info=True)
            return False

    def add_question(self, formId, questionId):
        """Function to add questions in a form

        :param formId: str representation of UUID of the form
        :param questionId: str representation of UUID of the question

        """
        logging = logger("forms model add question")
        try:
            logging.info("[FormsDB] Updating forms with question")
            updateQuery = """
                        UPDATE forms
                        SET questions = questions + ['{question}']
                        WHERE formId={formId};
                        """.format(
                question=questionId, formId=formId
            )
            self.session.execute(updateQuery)
            logging.info("[FormsDB] Updation forms with question successful")
            return True
        except Exception:
            logging.exception("Error while updating forms with question", exc_info=True)
            return False

    def add_response(self, formId, responseId):
        """Function to add responses in a form

        :param formId: str representation of UUID of the form
        :param responseId: str representation of UUID of the response

        """
        logging = logger("forms model add response")
        try:
            logging.info("[FormsDB] Updating forms with response")
            updateQuery = """
                        UPDATE forms
                        SET responses = responses + ['{response}']
                        WHERE formId={formId};
                        """.format(
                response=responseId, formId=formId
            )
            self.session.execute(updateQuery)
            logging.info("[FormsDB] Updation forms with response successful")
            return True
        except Exception:
            logging.exception("Error while updating forms with answer", exc_info=True)
            return False

    def add_action(self, formId, actionId):
        """Function to add action in a form

        :param formId: str representation of UUID of the form
        :param actionId: str representation of UUID of the action

        """
        logging = logger("form model action update")
        try:
            logging.info("[FormsDB] Updating forms with action")
            self.session.execute(
                "UPDATE forms SET actions = actions+['{actionId}'] WHERE formId = {formId};".format(
                    actionId=actionId, formId=formId
                )
            )
            logging.info("[FormsDB] Updation forms with action successful")
            return True
        except Exception:
            logging.exception("Error while updating forms with action", exc_info=True)
            return False

    def fetch_form(self, formId):
        """Function to fetch from forms table

        :param formId: str representation of UUID of the form

        :return result: ResultSet from cassandra containing the form details
        """
        logging = logger("form model fetch")
        try:
            logging.info("[FormsDB] Fetching from forms table")
            fetchQuery = """
                        SELECT * FROM forms
                        WHERE formId={formId};
                        """.format(
                formId=formId
            )
            result = self.session.execute(fetchQuery)
            logging.info("[FormsDB] Fetching from forms table sucessful")
            return result
        except Exception:
            logging.exception("Error while from forms", exc_info=True)
            return False
