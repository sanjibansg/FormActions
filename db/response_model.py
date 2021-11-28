from model import model
import datetime

class response_model(model):
    def __init__(self):
        super().__init__()
        createQuery = '''
                         CREATE TYPE IF NOT EXISTS response(
                             questionId int,
                             answerId int
                         );
                         CREATE TABLE IF NOT EXISTS responses(
                         responseId int,
                         formId int,
                         userId text,
                         responses list<response>,
                         created timestamp,
                         PRIMARY KEY(responseId));'''
        self.session.execute(createQuery)

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
