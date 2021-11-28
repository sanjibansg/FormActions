from .model import model
from utils import logger

class action_model(model):
    def __init__(self):
        logging=logger("action model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for actions table")
            super().__init__()
            createQuery = '''
                            CREATE TABLE IF NOT EXISTS actions(
                            actionId int,
                            action text,
                            meta   list<text>,
                            PRIMARY KEY(actionId));'''
            self.session.execute(createQuery)
            logging.info("Actions table found sucessfully")
        except Exception:
            logging.exception("Error while connecting to actions table",exc_info=True)


    def add_action(self,data):
        insertQuery = '''
                      INSERT INTO actions
                      VALUES({actionId},{action},{meta});
                      '''.format(actionId=data['actionId'],action=data['action'],meta=data['meta'])
        self.session.execute(insertQuery)

    def fetch_action(self,actionId):
        fetchQuery = '''
                     SELECT * FROM actions
                     WHERE action={actionId}
                     '''.format(actionId=actionId)
        result = self.session.execute(fetchQuery)
        return result
