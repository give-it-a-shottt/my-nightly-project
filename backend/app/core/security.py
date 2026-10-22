from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import bcrypt
from fastapi import Header, HTTPException, Request, status
import jwt
from app.core.config import settings

# 1. Bcrypt 단방향 해싱 (콩 -> 두부)
# str ──encode──→ bytes ──bcrypt──→ bytes ──decode──→ str (DB 저장)


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

# 2. 비밀번호 대조 (입력한 콩으로 만든 두부 == DB 두부?)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

# 3. Access Token 생성 (수명 15분, type="access")


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role,
               "type": "access", "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# 4. Refresh Token 생성 (수명 7일, type="refresh")


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + \
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 💡 5. [M2 추가] 웹훅 HMAC-SHA256 서명 검증 문지기 (Depends용)
async def verify_webhook_signature(
    request: Request,
    x_signature: str = Header(..., description="HMAC-SHA256 hex digest"),
) -> None:
    # ① 가공 전 원본 바이트(bytes) 그대로 추출
    raw_body: bytes = await request.body()
    expected_sig = hmac.new(
        settings.WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    # ② 타이밍 공격 방어를 위한 상수 시간 비교
    if not hmac.compare_digest(expected_sig, x_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="위조된 웹훅 서명입니다 (Invalid HMAC signature).",
        )
