from models import User

USERS = [
    {"username": "admin", "password": "adminpass", "role": "admin"},
    {"username": "user", "password": "userpass", "role": "user"},
    {"username": None, "password": None, "role": "guest"},
]


def get_user(credentials: User) -> User | None:
    for user in USERS:
        if user["username"] == credentials.username:
            return credentials
    return None
