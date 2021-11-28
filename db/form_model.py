from .model import model
import datetime
from utils import logger

class form_model(model):
    def __init__(self):
        logging=logger("form model init")
        try:
            logging.info("[Connecting to Cassandra] Checking for forms table")
            super().__init__()
            createTypeQuery = '''
                            CREATE TYPE IF NOT EXISTS action(
                                actionId int,
                                trigger text
                            );'''
            self.session.execute(createTypeQuery)
            createQuery='''
                            CREATE TABLE IF NOT EXISTS forms(
                            formId int,
                            clientId int,
                            questions list<int>,
                            responses list<int>,
                            actions list<frozen <action>>,
                            created timestamp,
                            deadline timestamp,
                            PRIMARY KEY(formId));
                        '''
            self.session.execute(createQuery)
            logging.info("Forms table found sucessfully")
        except Exception:
            logging.exception("Error while connecting to forms table",exc_info=True)

    def add_form(self,data):
        insertQuery = '''
                      INSERT INTO forms (formId,clientId,questionId,actionId,created,deadline)
                      VALUES ({formId},{clientId},{questionId},{actionId},{created},{deadline});
                      '''.format(formId=data['formId'],clientId=data['clientId'],questions=data['questions'],
                                 actions=data['actions'],created=datetime.datetime.now(),deadline=data['deadline'])
        self.session.execute(insertQuery)

    def add_response(self,formId,response):
        updateQuery = '''
                      UPDATE forms
                      SET responses = responses + {response}
                      WHERE formId={formId};
                      '''.format(response=response,formId=formId)
        self.session.execute(updateQuery)

    def add_action(self,formId,action):
        updateQuery = '''
                      UPDATE forms
                      SET actions = actions+{action}
                      WHERE formId = {formId};
                      '''.format(action=action,formId=formId)
        self.session.execute(updateQuery)

    def fetch_form(self,formId):
        fetchQuery = '''
                     SELECT * FROM forms
                     WHERE formId={formId};
                     '''.format(formId=formId)
        result = self.session.execute(fetchQuery)
        return result
