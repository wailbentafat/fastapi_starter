from cassandra.cqlengine import connection
from app.core.config import settings
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from app.models.coversation import Conversation

def create_keyspace():
    cluster = Cluster([settings.CASSANDRA_HOST])
    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.CASSANDRA_KEYSPACE}
        WITH replication = {{
            'class': 'SimpleStrategy',
            'replication_factor': '1'
        }};
    """)
    
    cluster.shutdown()


def init_cassandra():
    create_keyspace()

    connection.setup([settings.CASSANDRA_HOST], settings.CASSANDRA_KEYSPACE)

    sync_table(Conversation)
    
