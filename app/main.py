from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # runs when app STARTS, not on import
    yield

app = FastAPI(title="Task API", lifespan=lifespan)
app.include_router(tasks.router)

@app.get("/health")
def health():
    return {"status": "ok"}