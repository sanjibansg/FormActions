from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from utils import logger


class model:
    """Class for handling database connections"""

    def __init__(self):
        logging = logger("action model init")
        try:
            self.cluster = Cluster()
            self.session = self.cluster.connect()
            self.session.execute(
                """CREATE KEYSPACE IF NOT EXISTS formactions
                                    with replication={'class': 'SimpleStrategy', 'replication_factor' : 2};"""
            )
            self.session = self.cluster.connect("formactions")
            self.session.row_factory = dict_factory
        except Exception:
            logging.exception(
                "Error while connecting to cassandra cluster", exc_info=True
            )

    def get_session_object(self):
        """Function that returns the session object useful for executing queries in cassandra

        :return session: Session object for cassandra

        """
        return self.session
