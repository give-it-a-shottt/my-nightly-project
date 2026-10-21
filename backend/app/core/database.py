from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 커넥션 풀 생성: 풀 사이즈 10개, 급증 시 20개까지 추가 허용
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass

# FastAPI 엔드포인트 의존성(Depends)으로 주입할 비동기 세션 제너레이터


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # async with를 통해 작업 종료 또는 에러 발생 시 무조건 풀에 커넥션을 반납합니다
    async with AsyncSessionLocal() as session:
        yield session
