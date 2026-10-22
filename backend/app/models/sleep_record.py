# 경로: backend/app/models/sleep_record.py
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SleepRecord(Base):
    __tablename__ = "sleep_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    device_serial: Mapped[str] = mapped_column(String(100), nullable=False)
    # 총 수면 시간(분) 및 수면 점수(0~100)
    sleep_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    sleep_score: Mapped[int] = mapped_column(Integer, nullable=False)
    # 💡 M2 핵심: 멱등성 키 (DB 레벨 UNIQUE 제약 조건으로 중복 저장 원천 차단!)
    idempotency_key: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
