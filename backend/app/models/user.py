from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    # 기본키 및 인덱스 부여
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 중복 불가, 이메일 조회를 위한 인덱스 지정
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    # 사용자 이름 (UserCreate의 min 2 / max 50과 맞춤)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # 비밀번호 해시값 저장
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    # 💡 M1 추가: 권한 구분 ("USER" 또는 "ADMIN"), 기본값은 "USER"
    role: Mapped[str] = mapped_column(
        String(20), default="USER", server_default="USER", nullable=False)
    # 서버 시간 기준 생성 시각 자동 기록
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
