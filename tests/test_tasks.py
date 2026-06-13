from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for tests (no real Postgres needed in CI)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_create_task():
    r = client.post("/tasks/", json={"title": "Buy milk"})
    assert r.status_code == 200
    assert r.json()["title"] == "Buy milk"
    assert r.json()["done"] == False

def test_list_tasks():
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_mark_done():
    r = client.post("/tasks/", json={"title": "Test task"})
    task_id = r.json()["id"]
    r2 = client.patch(f"/tasks/{task_id}/done")
    assert r2.json()["done"] == True