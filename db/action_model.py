from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType

import uuid
from utils import logger

class action_meta(UserType):
    """Class for registering user defined datatype to cassandra

    :param meta_property: name of the meta_property
    :param meta_value: value of the meta_property

    """
    meta_property = Text()
    meta_value    = Text()

class action_model(Model):
    """Class for handling the actions table in cassandra"""
    __keyspace__   = "formactions"
    __table_name__ = "actions"
    actionID = UUID(primary_key=True)
    formID   = Text()
    action   = Text()
    trigger  = Text()
    meta     = List(UserDefinedType(action_meta))
