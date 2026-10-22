# 경로: backend/app/repositories/sleep_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sleep_record import SleepRecord
from app.schemas.webhook import SleepWebhookPayload


class SleepRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_idempotency_key(self, key: str) -> SleepRecord | None:
        stmt = select(SleepRecord).where(SleepRecord.idempotency_key == key)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_sleep_record(self, data: SleepWebhookPayload) -> SleepRecord:
        record = SleepRecord(
            user_id=data.user_id,
            device_serial=data.device_serial,
            sleep_minutes=data.sleep_minutes,
            sleep_score=data.sleep_score,
            idempotency_key=data.idempotency_key,
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_by_user_id(self, user_id: int) -> list[SleepRecord]:
        stmt = (
            select(SleepRecord)
            .where(SleepRecord.user_id == user_id)
            .order_by(SleepRecord.recorded_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
