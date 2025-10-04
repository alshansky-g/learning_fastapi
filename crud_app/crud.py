from fastapi import HTTPException, status


async def get_todo_or_404(session, model, id):
    todo_db = await session.get(model, id)
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"todo с id={id} не существует")
    return todo_db
