# 경로: backend/app/schemas/webhook.py
from datetime import datetime
from pydantic import BaseModel, Field


class SleepWebhookPayload(BaseModel):
    idempotency_key: str = Field(..., min_length=5, max_length=100)
    user_id: int
    device_serial: str = Field(..., min_length=3, max_length=100)
    sleep_minutes: int = Field(..., ge=0, le=1440)
    sleep_score: int = Field(..., ge=0, le=100)


class SleepRecordResponse(BaseModel):
    id: int
    user_id: int
    device_serial: str
    sleep_minutes: int
    sleep_score: int
    idempotency_key: str
    recorded_at: datetime

    model_config = {"from_attributes": True}


class WebhookResultResponse(BaseModel):
    status: str  # "created" 또는 "already_processed"
    record: SleepRecordResponse
