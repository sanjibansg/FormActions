from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class form_model(Model):
    """Class for handling the forms table in cassandra"""
    __keyspace__   = "formactions"
    __table_name__ = "forms"
    formID    = UUID(primary_key=True)
    clientID  = Text()
    questions = List(Text)
    responses = list(Text)
    actions   = list(Text)
    created   = DateTime()
    deadline  = DateTime()
