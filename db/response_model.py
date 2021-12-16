from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class response_model(Model):
    """Class for handling the responses table in cassandra"""

    __keyspace__ = "formactions"
    __table_name__ = "responses"
    response_id = UUID(primary_key=True)
    form_id = Text()
    user_id = Text()
    responses = List(Text)
    created = DateTime()
