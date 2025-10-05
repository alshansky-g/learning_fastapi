from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ToDoCreate(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    completed: bool = Field(default=False)


class ToDoUpdate(ToDoCreate):
    completed_at: datetime = Field(default_factory=datetime.now)


class ToDo(ToDoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
