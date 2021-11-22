from cassandra.cluster import Cluster
from cassandra.query import dict_factory

class model():
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute('''CREATE KEYSPACE IF NOT EXISTS formactions
                                with replication={'class': 'SimpleStrategy', 'replication_factor' : 2};''')
        self.session = self.cluster.connect('formactions')
        self.session.row_factory = dict_factory
