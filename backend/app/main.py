from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.mongo import init_mongo
from app.api import user_routes, conversation_routes, payment_routes
from app.db.cassandra import init_cassandra
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_cassandra()
    await init_mongo()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(
    conversation_routes.router, prefix="/conversations", tags=["Conversations"]
)
app.include_router(payment_routes.router, prefix="/payments", tags=["Payments"])
