from model import model
import datetime

class form_model(model):
    def __init__(self):
        super().__init()
        createQuery = '''
                         CREATE TYPE IF NOT EXISTS action(
                             actionId int,
                             trigger text
                         );
                         CREATE TABLE IF NOT EXISTS forms(
                         formId int,
                         clientId int,
                         questions set<int>,
                         responses set<int>,
                         actions list<action>,
                         created timestamp,
                         deadline timestamp,
                         PRIMARY KEY(formId));'''
        self.session.execute(createQuery)

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
