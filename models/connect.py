from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import settings

async_engine = create_async_engine(
    url=settings.SQLA_ASYNC_URL,
    echo=False,
)

async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)