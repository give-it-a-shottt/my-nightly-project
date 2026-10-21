# 경로: backend/app/services/user_service.py
from fastapi import HTTPException, status
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo  # 창고 담당과 손을 잡음

    async def register_user(self, user_in: UserCreate) -> User:
        # 1. 이메일 중복 검사
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 가입된 이메일입니다."
            )

        # 2. 비밀번호 임시 해싱 (진짜 암호화 bcrypt/argon2는 M1 로그인 모듈에서 장착합니다!)
        hashed_pw = get_password_hash(user_in.password)

        # 3. 창고 담당에게 저장 지시 후 User 객체 반환
        return await self.user_repo.create(
            email=user_in.email,
            name=user_in.name,
            hashed_password=hashed_pw
        )

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 회원입니다."
            )
        return user

    async def get_all_users(self) -> list[User]:
        return await self.user_repo.get_all()
