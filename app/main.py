from fastapi import FastAPI

from app.config import load_config
from app.logger import logger
from app.models.models import User

app = FastAPI()
config = load_config()

if config.debug:
    app.debug = True
else:
    app.debug = False


@app.get("/")
def read_root():
    logger.info("Обработка рут гет запроса")
    return {"message": "Hello, World!"}


@app.get("/users")
def get_users():
    logger.info("Получаем список юзеров")
    return {"user": "yes"}


@app.post("/add_user")
def is_user_adult(user: User):
    logger.info("Приняли данные пользователя %s", user)
    return {"name": user.name, "age": user.age, "is_adult": user.age >= 18}


@app.get("/db")
def get_db_info():
    logger.info(f"Подключение к базе данных: {config.db.database_url}")
    return {"database_url": config.db.database_url}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info("Ищем пользователя с id=%s", user_id)
    return {
        "user_id": user_id,
        "user_info": f"Информация о пользователе с id={user_id}",
    }


@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: int):
    logger.info('Удаляем пользователя с id=%s', user_id)
    return {
        "result": f"Пользователь с id={user_id} удалён"
    }
