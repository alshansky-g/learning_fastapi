from secrets import compare_digest

from schemas import UserInDB

USER_DB = []


def get_user_from_db(username: str):
    for user in USER_DB:
        if compare_digest(user["username"], username):
            return UserInDB(username=username,
                            hashed_password=user["hashed_password"])
    return None


def save_user_to_db(user: UserInDB):
    USER_DB.append(user.model_dump())
