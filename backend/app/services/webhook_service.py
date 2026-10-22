# 경로: backend/app/services/webhook_service.py
from sqlalchemy.exc import IntegrityError

from app.repositories.sleep_repository import SleepRepository
from app.schemas.webhook import (
    SleepRecordResponse,
    SleepWebhookPayload,
    WebhookResultResponse,
)


class WebhookService:
    def __init__(self, repo: SleepRepository):
        self.repo = repo

    async def process_sleep_webhook(
        self, payload: SleepWebhookPayload
    ) -> WebhookResultResponse:
        # 1차 방어: 이미 처리된 멱등성 키인지 먼저 조회
        existing = await self.repo.get_by_idempotency_key(payload.idempotency_key)
        if existing:
            return WebhookResultResponse(
                status="already_processed",
                record=SleepRecordResponse.model_validate(existing),
            )

        # 2차 방어: 0.001초 차이 동시 요청으로 둘 다 INSERT 시도할 때 IntegrityError 방어
        try:
            new_record = await self.repo.create_sleep_record(payload)
            return WebhookResultResponse(
                status="created",
                record=SleepRecordResponse.model_validate(new_record),
            )
        except IntegrityError:
            await self.repo.db.rollback()
            existing = await self.repo.get_by_idempotency_key(payload.idempotency_key)
            return WebhookResultResponse(
                status="already_processed",
                record=SleepRecordResponse.model_validate(existing),
            )

    async def get_my_sleep_records(self, user_id: int) -> list[SleepRecordResponse]:
        records = await self.repo.get_by_user_id(user_id)
        return [SleepRecordResponse.model_validate(r) for r in records]
