from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from sqlalchemy import and_, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from crud_app import crud
from crud_app.database import get_session
from crud_app.models import ToDo as ToDoModel
from crud_app.schemas import ToDo, ToDoCreate, ToDoUpdate
from crud_app.services import get_analytics_dict, request_timed

app = FastAPI()

AsyncDBSession = Annotated[AsyncSession, Depends(get_session)]


@app.get("/todos", response_model=list[ToDo])
async def get_todos(session: AsyncDBSession,
                    limit: Annotated[int, Query(ge=1, le=100)] = 10,
                    offset: Annotated[int, Query()] = 0,
                    sort_by: Annotated[str | None, Query()] = None,
                    completed: Annotated[bool | None, Query()] = None,
                    created_after: Annotated[str | None, Query()] = None,
                    created_before: Annotated[str | None, Query()] = None,
                    title_contains: Annotated[str | None, Query()] = None):
    query = select(ToDoModel)

    conditions = []
    if completed is not None:
        conditions.append(ToDoModel.completed == completed)
    if created_after:
        dt = datetime.strptime(created_after, "%Y-%m-%d")
        conditions.append(ToDoModel.created_at >= dt)
    if created_before:
        dt = datetime.strptime(created_before, "%Y-%m-%d")
        conditions.append(ToDoModel.created_at <= dt)
    if title_contains:
        conditions.append(ToDoModel.title.ilike(f"%{title_contains}%"))

    if conditions:
        query = query.where(and_(*conditions))

    if sort_by:
        sort_by = desc(sort_by[1:]) if sort_by.startswith('-') else sort_by  # type: ignore
    todos = await session.scalars(query.order_by(sort_by).
                                  limit(limit).offset(offset))
    return todos.all()


@app.post("/todos", response_model=ToDo)
async def create_todo(todo: ToDoCreate, session: AsyncDBSession):
    todo_db = ToDoModel(**todo.model_dump())
    session.add(todo_db)
    await session.commit()
    return todo_db


@app.patch("/todos")
async def update_todos_status(session: AsyncDBSession,
                              ids: Annotated[str, Query()],
                              status: Annotated[bool, Query()]):
    list_ids = [int(n) for n in ids.split(',')]
    result = await session.execute(update(ToDoModel).where(
        ToDoModel.id.in_(list_ids)).values(completed=status))
    await session.commit()
    return {"updated": result.rowcount}


@app.get("/todos/analytics")
@request_timed
async def get_analytics(session: AsyncDBSession):
    analytics = await get_analytics_dict(session)
    return analytics


@app.get("/todos/{todo_id}", response_model=ToDo)
async def get_todo(todo_id: int, session: AsyncDBSession):
    todo_db = await crud.get_todo_or_404(session, ToDoModel, todo_id)
    return todo_db


@app.put("/todos/{todo_id}", response_model=ToDo)
async def update_todo(todo_id: int, session: AsyncDBSession, todo: ToDoCreate):
    todo_db = await crud.get_todo_or_404(session, ToDoModel, todo_id)
    update_todo = ToDoUpdate(**todo.model_dump())
    await session.execute(update(ToDoModel).where(
        ToDoModel.id == todo_id).values(**update_todo.model_dump()))
    await session.commit()
    await session.refresh(todo_db)
    return todo_db
