# 경로: backend/scripts/ensure_test_user.py
import asyncio
import sys
from pathlib import Path

# backend 폴더를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User


async def ensure_user_one():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.id == 1))
        user = result.scalar_one_or_none()

        test_password = "password1234"
        if user:
            # 기존 1번 회원의 비밀번호를 기억하기 쉽게 password1234로 재설정
            user.hashed_password = get_password_hash(test_password)
            await db.commit()
            print("=" * 55)
            print("✅ DB 1번 회원(id=1) 로그인 계정 안내 (비밀번호 초기화 완료)")
            print(f"   - 이메일(아이디): {user.email}")
            print(f"   - 비밀번호      : {test_password}")
            print("=" * 55)
        else:
            # 1번 회원이 아예 없으면 새로 생성
            new_user = User(
                email="sleep@nightly.com",
                name="수면테스터",
                hashed_password=get_password_hash(test_password),
                role="USER",
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            print("=" * 55)
            print(f"✅ 새 회원(id={new_user.id}) 생성 완료!")
            print(f"   - 이메일(아이디): {new_user.email}")
            print(f"   - 비밀번호      : {test_password}")
            print("=" * 55)


if __name__ == "__main__":
    asyncio.run(ensure_user_one())

