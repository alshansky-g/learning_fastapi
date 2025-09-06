import asyncio

from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], bcrypt__rounds=10)


async def hash_password(password: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, ctx.hash, password)


async def verify_password(password: str, hashed_password: str) -> bool:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, ctx.verify,
                                      password, hashed_password)
