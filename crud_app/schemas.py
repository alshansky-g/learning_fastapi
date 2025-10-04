from pydantic import BaseModel, ConfigDict


class ToDoBase(BaseModel):
    title: str
    description: str
    completed: bool = False


class ToDo(ToDoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
