from fastapi import HTTPException, status
import jwt
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_by_email(email)
        # 회원이 없거나 비밀번호 두부 모양이 다르면 401 거절!
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )
        return TokenResponse(
            access_token=create_access_token(user.id, user.role),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[
                settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="리프레시 토큰이 아닙니다.")
            user_id = int(payload.get("sub"))
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="만료되었거나 유효하지 않은 리프레시 토큰입니다.")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="존재하지 않는 회원입니다.")

        # 💡 RTR(Refresh Token Rotation): Access Token뿐만 아니라 Refresh Token도 새로 발급!
        return TokenResponse(
            access_token=create_access_token(user.id, user.role),
            refresh_token=create_refresh_token(user.id),
        )
