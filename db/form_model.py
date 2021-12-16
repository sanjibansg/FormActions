from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class form_model(Model):
    """Class for handling the forms table in cassandra"""

    __keyspace__ = "formactions"
    __table_name__ = "forms"
    form_id = UUID(primary_key=True)
    client_id = Text()
    questions = List(Text)
    responses = List(Text)
    actions = List(Text)
    created = DateTime()
    deadline = DateTime()
