from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import conversation
from fastapi.staticfiles import StaticFiles
from cassandra import connection
from app.config import settings
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from app.models.coversation import Conversation
from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.models.user import User
from app.api import payment, user
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


mongo_client = AsyncMongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB]

async def init_mongo():
    await init_beanie(database=mongo_db, document_models=[User])
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_cassandra()
    await init_mongo()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(
    conversation.router, prefix="/conversations", tags=["Conversations"]
)
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
