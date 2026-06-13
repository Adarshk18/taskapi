from fastapi import FastAPI
from app.routers import tasks
from app.database import Base, engine

Base.meatdata.create_all(bind=engine)


app = FastAPI(title="Task Manager API")
app.include.router(tasks.router)

@app.get("/health")
def health():
    return {"status": "ok"}