from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    hashed_password = ctx.hash(password)
    return hashed_password


def check_hashes(password_in: str, hashed_password):
    return ctx.verify(password_in, hashed_password)
