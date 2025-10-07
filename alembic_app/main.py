from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://gleb:81972651@localhost:5433/gleb"
engine = create_async_engine(DATABASE_URL)
get_async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
