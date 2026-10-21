from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import RefreshRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

# 1. 로그인 (Swagger 자물쇠 버튼과 호환되도록 OAuth2PasswordRequestForm 사용, username 칸에 이메일 입력!)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(email=form_data.username, password=form_data.password)

# 2. 토큰 재발급 (RTR)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh_tokens(body.refresh_token)

# 3. 내 정보 조회 (로그인한 사람만 통과 - 1단계 문지기)


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# 4. 관리자 전용 테스트 API (ADMIN만 통과 - 2단계 문지기)


@router.get("/admin-only")
async def admin_only_check(admin_user: User = Depends(require_admin)):
    return {"message": f"환영합니다 관리자 {admin_user.name}님!"}
