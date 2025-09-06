from models import User, UserInDB

USER_DB = []


def get_user_from_db(user_in: User):
    for user in USER_DB:
        if user["username"] == user_in.username:
            return UserInDB(username=user_in.username,
                            hashed_password=user["hashed_password"])
    return None


def save_user_to_db(username: str, hashed_password: str):
    USER_DB.append(UserInDB(username=username,
                            hashed_password=hashed_password).model_dump())
    print(USER_DB)
