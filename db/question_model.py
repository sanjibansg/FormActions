from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class question_model(Model):
    """Class for handling the questions table in cassandra"""

    __keyspace__ = "formactions"
    __table_name__ = "questions"
    question_id = UUID(primary_key=True)
    form_id = Text()
    question = Text()
    question_format = Text()
    created = DateTime()
