from typing import Annotated

from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import FileResponse

from app.config import load_config
from app.logger import logger
from app.models.models import Feedback, UserCreate

app = FastAPI()
config = load_config()

if config.debug:
    app.debug = True
else:
    app.debug = False


PREMIUM_USER_ADDITION = "Ваш отзыв будет рассмотрен в приоритетном порядке."
feedbacks = []


fake_db = [
    {"username": "Ivan", "user_info": "i love beer"},
    {"username": "Kate", "user_info": "hobbies: dancing, partying"},
]


users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_doe", "email": "jane@example.com"},
    3: {"username": "alice_jones", "email": "alice@example.com"},
    4: {"username": "bob_white", "email": "bob@example.com"},
}


@app.get("/users/")
async def get_all_users():
    return fake_db


@app.get("/db")
def get_db_info():
    logger.info(f"Подключение к базе данных: {config.db.database_url}")
    return {"database_url": config.db.database_url}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info("Ищем пользователя с id=%s", user_id)
    if user_id in users:
        return users[user_id]
    return {"error": "user not found"}


@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    logger.info("Удаляем пользователя с id=%s", user_id)
    return {"result": f"Пользователь с id={user_id} удалён"}


@app.post("/feedback")
async def post_review(feedback: Feedback, is_premium: bool | None = None):
    feedbacks.append(feedback.model_dump(exclude_none=True))
    logger.info("Сохранен отзыв: %s", feedback)
    message = {"message": f"Отзыв сохранен. Благодарим, {feedback.name}."}
    if is_premium:
        message = {"message": f"{message['message']} {PREMIUM_USER_ADDITION}"}
    return message


@app.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    logger.info("Принят файл %s", file)
    return {"file_size": len(file)}


@app.post("/upload-image/")
async def upload_image(file: UploadFile):
    logger.info(file.content_type)
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Только JPG и PNG разрешены"}
    return {"filename": file.filename, "content_type": file.content_type}


@app.get("/file/download")
def download_file():
    return FileResponse(path="Roadmap backend.pdf",
                        filename="Бэкэнд роадмап питон.pdf",
                        media_type="multipart/form-data")


@app.get("/items/")
async def read_item(q: str = Query(..., pattern="^fixedprefix_")):
    return {"q": q}


@app.post("/create_user")
def create_user(user: UserCreate):
    return user.model_dump(exclude_none=True)
