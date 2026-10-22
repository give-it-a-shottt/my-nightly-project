from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import users, auth, webhooks  # 상단 import에 추가

app = FastAPI(
    title="Nightly Sleep Service API",
    description="AI 수면 코칭 & 구독 커머스 백엔드 API",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(webhooks.router)

# 3000번 포트(Next.js 프론트엔드)에서 오는 요청을 허용할 명단
origins = [
    "http://localhost:3000",
]


# 브라우저에게 "이 출처에서 온 자바스크립트 요청은 안전하니 통과시켜라"고 응답 헤더를 달아주는 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 허용할 도메인 목록
    allow_credentials=True,      # 쿠키/인증 정보 포함 허용
    allow_methods=["*"],         # GET, POST, PUT, DELETE 등 모든 HTTP 메서드 허용
    allow_headers=["*"],         # 모든 요청 헤더 허용
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
