from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from models import User
from rbac import PermissionChecker

app = FastAPI()


@app.get("/admin/")
async def admin_info(
    user: Annotated[User, Depends(PermissionChecker(["admin"]))]
):
    return {"message": f"Welcome, {user.username}"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
