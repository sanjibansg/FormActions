from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

from utils import logger


class model:
    """Class for handling database connections"""

    def __init__(self):
        logging = logger("action model init")
        try:
            auth_provider = PlainTextAuthProvider(
                username="cassandra", password="cassandra"
            )
            self.cluster = Cluster(
                ["172.30.0.2", "172.30.0.3"], auth_provider=auth_provider
            )
            self.session = self.cluster.connect()
            self.session.execute(
                """CREATE KEYSPACE IF NOT EXISTS formactions
                                    with replication={'class': 'SimpleStrategy', 'replication_factor' : 2};"""
            )
            self.session = self.cluster.connect("formactions")
            self.session.row_factory = dict_factory
            connection.register_connection("cluster1", ["172.30.0.2"], default=True)
            connection.set_default_connection("cluster1")

        except Exception:
            logging.exception(
                "Error while connecting to cassandra cluster", exc_info=True
            )

    def get_session_object(self):
        """Function that returns the session object useful for executing queries in cassandra

        :return session: Session object for cassandra

        """
        return self.session
