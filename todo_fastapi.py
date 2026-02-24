from starlette.middleware import cors
import analytics
import db_clickhouse
from db_clickhouse import client
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from ai import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analytics.router, prefix = "/analytics", tags = ["Analytics"])
models.Base.metadata.create_all(bind=engine)

app.include_router(agent.router, prefix = "/ai", tags= ["AI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoCreate(BaseModel):
    task: str

class TodoUpdate(BaseModel):
    task: str
    completed: bool

@app.post("/todos")
def create_todo(task: str,
                db: Session = Depends(get_db)):

    todo = models.Todo(
        task= task,
        completed=False
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    try:
        print("INSERTING INTO CLICKHOUSE...")
        client.insert(
            "todo_events",
            [[todo.id,
              "created",
              datetime.utcnow()
            ]],
            column_names=[
                "todo_id",
                "event_type",
                "event_time"
            ]
        )
    except Exception as e:
        #print("ClickHouse logging failed:", e)
        import traceback
        traceback.print_exc()

    return todo

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int,
                todo: TodoUpdate,
                db: Session = Depends(get_db)):

    existing = db.query(models.Todo)\
        .filter(models.Todo.id == todo_id)\
        .first()

    if not existing:
        return {"error": "Not Found"}

    previously_completed = existing.completed

    existing.task = todo.task
    existing.completed = todo.completed

    if todo.completed and not previously_completed:
        existing.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(existing)

    if todo.completed and not previously_completed:
        try:
            client.insert(
                "todo_events",
                [[existing.id,
                  "completed",
                  datetime.utcnow()]],
                column_names=[
                    "todo_id",
                    "event_type",
                    "event_time"
                ]
            )
        except Exception as e:
            print("ClickHouse logging failed:", e)

    return existing

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int,
                db: Session = Depends(get_db)):

    todo = db.query(models.Todo)\
        .filter(models.Todo.id == todo_id)\
        .first()

    if not todo:
        return {"error": "Not Found"}

    db.delete(todo)
    db.commit()

    return {"message": "Deleted"}