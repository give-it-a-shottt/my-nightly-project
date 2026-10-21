# 경로: backend/app/api/v1/routers/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# 💡 의존성 조립 공장: DB 세션 -> Repo -> Service 순서로 손을 잡게 해줌


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(user_in)


@router.get("", response_model=list[UserResponse])
async def read_users(
    service: UserService = Depends(get_user_service),
):
    return await service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(user_id)
