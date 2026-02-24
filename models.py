from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)