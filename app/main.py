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


users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_doe", "email": "jane@example.com"},
    3: {"username": "alice_jones", "email": "alice@example.com"},
    4: {"username": "bob_white", "email": "bob@example.com"},
}


@app.get("/")
def read_root():
    logger.info("Обработка рут гет запроса")
    return {"message": "Hello, World!"}


@app.get("/users/")
def read_users(username: str | None = None,
               email: str | None = None,
               limit: int = 10):
    filtered_users = users

    if username:
        filtered_users = {key: user for key, user in filtered_users.items()
                          if username.lower() in user["username"].lower()}
    if email:
        filtered_users = {key: user for key, user in filtered_users.items()
                          if email.lower() in user["email"].lower()}
    return dict(list(filtered_users.items())[:limit])


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
    if user_id in users:
        return users[user_id]
    return {"error": "user not found"}


@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: int):
    logger.info('Удаляем пользователя с id=%s', user_id)
    return {
        "result": f"Пользователь с id={user_id} удалён"
    }
