from cassandra.cluster import Cluster

class model():
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute('''CREATE KEYSPACE IF NOT EXISTS formactions
                                with replication={'class': 'SimpleStrategy', 'replication_factor' : 2};''')
