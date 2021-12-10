from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model

class question_model(Model):
    """Class for handling the questions table in cassandra"""
    __keyspace__   = "formactions"
    __table_name__ = "questions"
    questionID = UUID(primary_key=True)
    formID     = Text()
    question   = Text()
    question_format = Text()
    created  = DateTime()
