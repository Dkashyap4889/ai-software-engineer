from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True
