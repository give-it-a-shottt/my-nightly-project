from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nightly Sleep Service"
    # postgresql+asyncpg 비동기 드라이버 주소
    DATABASE_URL: str = (
        "postgresql+asyncpg://nightly_user:nightly_password@localhost:5432/nightly_db"
    )
    # 💡 M1 추가: JWT 도장용 비밀키 및 수명 설정
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
