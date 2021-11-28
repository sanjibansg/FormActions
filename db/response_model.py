from .model import model
import datetime
from utils import logger

class response_model(model):
    def __init__(self):
        logging=logger("response model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for responses table")
            super().__init__()
            createTypeQuery = '''
                            CREATE TYPE IF NOT EXISTS response(
                                questionId int,
                                answerId int
                            );
                            '''
            self.session.execute(createTypeQuery)
            createQuery = '''
                            CREATE TABLE IF NOT EXISTS responses(
                            responseId int,
                            formId int,
                            userId text,
                            responses list<frozen <response>>,
                            created timestamp,
                            PRIMARY KEY(responseId));'''
            self.session.execute(createQuery)
            logging.info("Responses table found sucessfully")
        except Exception:
            logging.exception("Error while connecting to responses table",exc_info=True)

    def add_response(self,data):
        insertQuery = '''
                      INSERT INTO responses
                      VALUES({responseId},{formId},{userId},{responses},{created});
                      '''.format(responseId=data['responseId'],formId=data['formId'],userId=data['userId'],
                                 responses=data['responses'],created=datetime.datetime.now())
        self.session.execute(insertQuery)

    def fetch_response(self,responseId):
        fetchQuery = '''
                     SELECT * FROM responses
                     WHERE responseId={responseId}
                     '''.format(responseId=responseId)
        result = self.session.execute(fetchQuery)
        return result
