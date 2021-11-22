from model import model

class action_model(model):
    def __init__(self):
        super().__init__()
        createQuery = '''
                         CREATE TABLE IF NOT EXISTS actions(
                         actionId int,
                         action text,
                         PRIMARY KEY(actionId));'''
        self.session.execute(createQuery)

    def add_action(self,data):
        insertQuery = '''
                      INSERT INTO actions
                      VALUES({actionId},{action});
                      '''.format(actionId=data['actionId'],action=data['action'])
        self.session.execute(insertQuery)

    def fetch_action(self,actionId):
        fetchQuery = '''
                     SELECT * FROM actions
                     WHERE action={actionId}
                     '''.format(actionId=actionId)
        result = self.session.execute(fetchQuery)
        return result
