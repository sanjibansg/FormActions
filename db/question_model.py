from model import model
import datetime

class question_model(model):
    def __init__(self):
        super().__init__()
        createQuery = '''
                         CREATE TABLE IF NOT EXISTS questions(
                         questionId int,
                         formId int,
                         question text,
                         format text,
                         created timestamp
                         PRIMARY KEY(questionId));'''
        self.session.execute(createQuery)

    def add_question(self,data):
        insertQuery = '''
                      INSERT INTO questions
                      VALUES({questionId},{formId},{question},{format},{created});
                      '''.format(questionId=data['questionId'],formId=data['formId'],question=data['question'],
                                 format=data['format'],created=datetime.datetime.now())
        self.session.execute(insertQuery)

    def fetch_question(self,questionId):
        fetchQuery = '''
                     SELECT * FROM questions
                     WHERE questionId = {questionId};
                     '''.format(questionId=questionId)
        self.session.execute(fetchQuery)
