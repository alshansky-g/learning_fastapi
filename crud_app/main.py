from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from crud_app import crud
from crud_app.database import get_session
from crud_app.models import ToDo as ToDoModel
from crud_app.schemas import ToDo, ToDoBase

app = FastAPI()

AsyncDBSession = Annotated[AsyncSession, Depends(get_session)]


@app.post("/todos", response_model=ToDo)
async def create_todo(todo: ToDoBase, session: AsyncDBSession):
    todo_db = ToDoModel(**todo.model_dump())
    session.add(todo_db)
    await session.commit()
    return todo_db


@app.get("/todos/{todo_id}", response_model=ToDo)
async def get_todo(todo_id: int, session: AsyncDBSession):
    todo_db = await crud.get_todo_or_404(session, ToDoModel, todo_id)
    return todo_db


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, session: AsyncDBSession, todo: ToDoBase):
    todo_db = await crud.get_todo_or_404(session, ToDoModel, todo_id)
    await session.execute(update(ToDoModel).where(
        ToDoModel.id == todo_id).values(**todo.model_dump()))
    await session.commit()
    await session.refresh(todo_db)
    return todo_db
