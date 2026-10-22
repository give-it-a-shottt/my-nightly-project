# 경로: backend/app/api/v1/routers/webhooks.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.deps import get_current_user
from app.core.database import get_db
from app.core.security import verify_webhook_signature
from app.models.user import User
from app.repositories.sleep_repository import SleepRepository
from app.schemas.webhook import (
    SleepRecordResponse,
    SleepWebhookPayload,
    WebhookResultResponse,
)
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


def get_webhook_service(db: AsyncSession = Depends(get_db)) -> WebhookService:
    return WebhookService(SleepRepository(db))


# 1. 수면 기기가 호출하는 웹훅 수신 입구 (Depends로 HMAC 서명 문지기 배치!)
@router.post(
    "/sleep",
    response_model=WebhookResultResponse,
    dependencies=[Depends(verify_webhook_signature)],
)
async def receive_sleep_webhook(
    payload: SleepWebhookPayload,
    service: WebhookService = Depends(get_webhook_service),
):
    return await service.process_sleep_webhook(payload)


# 2. 로그인한 회원이 내 수면 기록을 조회하는 API (프론트 대시보드용)
@router.get("/sleep/me", response_model=list[SleepRecordResponse])
async def read_my_sleep_records(
    current_user: User = Depends(get_current_user),
    service: WebhookService = Depends(get_webhook_service),
):
    return await service.get_my_sleep_records(current_user.id)
