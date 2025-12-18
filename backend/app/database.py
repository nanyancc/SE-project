from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from .config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.db_echo,
    future=True,
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_models() -> None:
    # 1. 创建表结构
    from .models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. 初始化种子数据 (防止外键报错)
    # 延迟导入，防止循环引用
    from .crud import ensure_test_users
    async with SessionLocal() as session:
        await ensure_test_users(session)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session