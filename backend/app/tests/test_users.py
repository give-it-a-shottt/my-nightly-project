# 경로: backend/tests/test_users.py
from datetime import datetime, timezone
import pytest
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService

# 💡 실제 PostgreSQL 없이 메모리 리스트로만 동작하는 '가짜 창고 담당'


class FakeUserRepository:
    def __init__(self):
        self.users: list[User] = []
        self._id_counter = 1

    async def get_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    async def create(self, email: str, name: str, hashed_password: str) -> User:
        user = User(
            id=self._id_counter,
            email=email,
            name=name,
            hashed_password=hashed_password,
            created_at=datetime.now(timezone.utc),
        )
        self._id_counter += 1
        self.users.append(user)
        return user


@pytest.mark.asyncio
async def test_register_user_success():
    # Given: 가짜 창고 담당을 주방장(UserService)에게 주입 (DB 연결 0%)
    fake_repo = FakeUserRepository()
    service = UserService(user_repo=fake_repo)
    user_in = UserCreate(email="inkyo@example.com",
                         name="정인교", password="password1234")

    # When: 회원가입 비즈니스 로직 실행
    created_user = await service.register_user(user_in)

    # Then: 아이디가 부여되고 비밀번호가 해싱되어 저장되었는지 검증
    assert created_user.id == 1
    assert created_user.email == "inkyo@example.com"
    assert created_user.hashed_password == "hashed_password1234"


@pytest.mark.asyncio
async def test_register_duplicate_email_fails():
    # Given: 이미 가입된 회원이 있는 상태
    fake_repo = FakeUserRepository()
    service = UserService(user_repo=fake_repo)
    user_in = UserCreate(email="dup@example.com",
                         name="홍길동", password="password1234")
    await service.register_user(user_in)

    # When & Then: 똑같은 이메일로 다시 가입하면 409 에러가 터져야 정상!
    with pytest.raises(HTTPException) as exc_info:
        await service.register_user(user_in)
    assert exc_info.value.status_code == 409
