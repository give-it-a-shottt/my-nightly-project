# 경로: backend/app/models/device.py
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 기기 고유 일련번호 (예: "SN-WATCH-001")
    serial_number: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    # 어느 회원의 기기인지 연결
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
