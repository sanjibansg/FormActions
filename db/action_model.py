from .model import model
import uuid
from utils import logger


class Meta(object):
    """Class for registering user defined datatype to cassandra

    :param meta_property: name of the meta_property
    :param meta_value: value of the meta_property

    """

    def __init__(self, meta_property, meta_value):
        self.meta_property = meta_property
        self.meta_value = meta_value


class action_model(model):
    """Class for handling the actions table in cassandra"""

    def __init__(self):
        logging = logger("action model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for actions table")
            super().__init__()
            createMetaTypeQuery = """
                                CREATE TYPE IF NOT EXISTS metadata(
                                meta_property text,
                                meta_value text
                            );"""
            self.session.execute(createMetaTypeQuery)
            createQuery = """
                            CREATE TABLE IF NOT EXISTS actions(
                            actionId uuid,
                            formId text,
                            action text,
                            trigger text,
                            meta   list<frozen<metadata>>,
                            PRIMARY KEY(actionId));"""
            self.session.execute(createQuery)
            self.cluster.register_user_type("formactions", "metadata", Meta)
            logging.info("Actions table found sucessfully")
        except Exception:
            logging.exception("Error while connecting to actions table", exc_info=True)

    def add_action(self, data):
        """Function to add new action into actions table

        :param data: Object which stores the essential properties like formId,action,trigger, meta data

        :return actionId: string representation of the UUID of the newly added action

        """
        logging = logger("action model insert")
        try:
            logging.info("[ActionDB] Inserting into actions table")
            actionId = uuid.uuid4()
            self.session.execute(
                "INSERT INTO actions (actionId,formId,action,trigger,meta) VALUES (%s,%s,%s,%s,%s)",
                (
                    actionId,
                    data["formId"],
                    data["action"],
                    data["trigger"],
                    [Meta(i["meta_property"], i["meta_value"]) for i in data["meta"]],
                ),
            )
            logging.info("[ActionDB] Insertion into actions table successful")
            return str(actionId)
        except Exception:
            logging.exception("Error while inserting into actions table", exc_info=True)
            return False

    def fetch_action(self, actionId):
        """Function to fetch action from the actions table

        :param actionId: string containing the UUID of the action

        :return result: ResultSet from cassandra containing the action details

        """
        logging = logger("action model fetch")
        try:
            logging.info("[ActionDB] Fetching from actions table")
            fetchQuery = """
                        SELECT * FROM actions
                        WHERE actionId={actionId}
                        """.format(
                actionId=actionId
            )
            result = self.session.execute(fetchQuery)
            logging.info("[ActionDB] Fetch from actions table successful")
            return result
        except Exception:
            logging.exception("Error while fetching from actions table", exc_info=True)
            return False
