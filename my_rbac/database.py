from models import User, UserIn

USERS = [
    {"username": "admin", "password": "adminpass", "role": "admin"},
    {"username": "user", "password": "userpass", "role": "user"},
]


def get_user(credentials: UserIn) -> User:
    for user in USERS:
        if user["username"] == credentials.username:
            return User(**user)
    return User()
