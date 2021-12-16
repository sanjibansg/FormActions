from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class answer_model(Model):
    """Class for handling the answers table in cassandra"""

    __keyspace__ = "formactions"
    __table_name__ = "answers"
    answer_id = UUID(primary_key=True)
    question_id = Text()
    answer = Text()
