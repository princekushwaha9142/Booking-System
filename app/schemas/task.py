from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskCategory


class TaskCreate(BaseModel):
    title:       str
    description: Optional[str]          = None
    category:    Optional[TaskCategory] = TaskCategory.OTHER
    due_date:    Optional[datetime]     = None


class TaskUpdate(BaseModel):
    title:       Optional[str]          = None
    description: Optional[str]          = None
    status:      Optional[TaskStatus]   = None
    category:    Optional[TaskCategory] = None
    due_date:    Optional[datetime]     = None


class TaskResponse(BaseModel):
    id:          int
    user_id:     int
    title:       str
    description: Optional[str]
    status:      TaskStatus
    category:    Optional[TaskCategory]
    due_date:    Optional[datetime]
    created_at:  datetime
    updated_at:  Optional[datetime]

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    total: int
    tasks: list[TaskResponse]