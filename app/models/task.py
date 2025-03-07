from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    CLOSED = "closed"
    FROZEN = "frozen"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
    priority: TaskPriority
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO
    participants: List[str] = Field(default_factory=list)

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None and v < datetime.utcnow():
            raise ValueError("Due date must be in the future")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    participants: Optional[List[str]] = None

class TaskResponse(TaskBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True 