# 경로: backend/app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 1. 회원가입 요청 상자 (비밀번호 포함)


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)

# 2. 회원 응답 상자 (⚠️ 보안상 password 필드는 절대 넣지 않음!)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str  # 💡 M1 추가: 내 권한이 USER인지 ADMIN인지 응답에 포함
    created_at: datetime

    # SQLAlchemy의 User 모델 객체를 이 Pydantic 상자로 자동 변환해 주는 설정
    model_config = ConfigDict(from_attributes=True)


# 💡 M1 추가: 로그인 및 토큰 재발급 시 내려줄 토큰 세트 상자
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
