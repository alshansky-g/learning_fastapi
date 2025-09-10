from secrets import compare_digest

USERS_DB = [
    {"username": "ivan", "password": "321456"},
    {"username": "gleb", "password": "123456"},
]

REFRESH_TOKENS = {}


def get_user_from_db(username: str):
    for user in USERS_DB:
        if compare_digest(user["username"], username):
            return user


def save_user_to_db(username: str, hashed_password: str):
    USERS_DB.append({"username": username, "password": hashed_password})


def get_token_from_db(username: str):
    return REFRESH_TOKENS.get(username)


def save_token_to_db(username: str, refresh_token: str):
    REFRESH_TOKENS[username] = refresh_token
