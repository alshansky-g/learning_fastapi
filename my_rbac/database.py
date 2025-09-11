from models import User, UserIn

USERS = [
    {"username": "admin1", "password": "adminpass", "role": "admin"},
    {"username": "admin2", "password": "adminpass", "role": "admin"},
    {"username": "admin3", "password": "adminpass", "role": "admin"},
    {"username": "user1", "password": "userpass", "role": "user"},
    {"username": "user2", "password": "userpass", "role": "user"},
    {"username": "user3", "password": "userpass", "role": "user"},
]


def get_user(credentials: UserIn) -> User:
    for user in USERS:
        if user["username"] == credentials.username:
            return User(**user)
    return User()
