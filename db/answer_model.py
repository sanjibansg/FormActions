from model import model

class answer_model(model):
    def __init__(self):
        super().__init__()
        createQuery = '''
                         CREATE TABLE IF NOT EXISTS answers(
                         answerId int,
                         questionId int,
                         answer text,
                         PRIMARY KEY(answerId));'''
        self.session.execute(createQuery)

    def add_answer(self,data):
        insertQuery = '''
                      INSERT INTO answers
                      VALUES({answerId},{questionId},{answer});
                      '''.format(answerId=data['answerId'],questionId=data['questionId'],answer=data['answer'])
        self.session.execute(insertQuery)

    def fetch_answer(self,answerId):
        fetchQuery = '''
                     SELECT * FROM answers
                     WHERE answerId={answerId}
                     '''.format(answerId=answerId)
        result = self.session.execute(fetchQuery)
        return result
