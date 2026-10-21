# 경로: backend/app/repositories/user_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db  # DB 세션과 손을 잡음

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, email: str, name: str, hashed_password: str) -> User:
        new_user = User(email=email, name=name,
                        hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)  # DB가 생성한 id, created_at을 받아옴
        return new_user
