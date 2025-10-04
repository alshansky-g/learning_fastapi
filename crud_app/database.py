from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from crud_app.config import config

engine = create_async_engine(url=config.database_url)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session
