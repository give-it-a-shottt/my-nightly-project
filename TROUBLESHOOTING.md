# 🛠️ Nightly Sleep Service - 트러블슈팅 & 아키텍처 학습 로그

프로젝트를 처음부터 끝까지 구축하며 겪은 실제 에러 트러블슈팅(6칸 규칙)과 모듈별 고장 실험·보안 방어 기록입니다.

---

## 1. [Stage 0: S0-8] 프론트엔드-백엔드 연동 시 HTTP 405 & 422 에러

### ① HTTP 405 (Method Not Allowed) 트러블슈팅
| 칸 | 내용 |
| :--- | :--- |
| **1. 증상** | 프론트엔드에서 API 호출 시 브라우저 콘솔 및 Network 탭에 `405 Method Not Allowed` 반환 |
| **2. 가설** | 프론트엔드 API 클라이언트가 요청한 URL 경로 또는 HTTP 메서드(`GET`/`POST`)가 백엔드 FastAPI 라우터에 정의된 메서드와 불일치함 |
| **3. 확인 방법** | `http://localhost:8000/docs` (Swagger UI)에서 등록된 엔드포인트 경로와 허용 메서드를 확인하고, 브라우저 Network 탭의 Request URL / Request Method와 대조 |
| **4. 진짜 원인** | 엔드포인트 경로 또는 HTTP 메서드가 백엔드 라우터(`@router.post`, `@router.get`) 선언과 어긋나서, 해당 경로에 허용되지 않은 메서드로 요청이 들어감 |
| **5. 해결 방법** | `frontend/src/lib/api/users.ts` 및 `backend/app/api/v1/routers/users.py`의 URL prefix(`/api/v1/users`)와 HTTP 메서드를 정확히 일치시킴 |
| **6. 배운 원리** | `404 Not Found`는 "주소 자체가 없음"을 뜻하고, **`405 Method Not Allowed`는 "주소는 존재하지만 그 주소에서 해당 HTTP 메서드(GET/POST 등)는 받지 않음"**을 뜻한다. |

### ② HTTP 422 (Unprocessable Entity) 트러블슈팅
| 칸 | 내용 |
| :--- | :--- |
| **1. 증상** | 회원가입 요청(`POST /api/v1/users`) 시 `422 Unprocessable Entity` 발생 |
| **2. 가설** | 프론트엔드가 보낸 JSON Body의 필드명·타입·길이 조건이 백엔드 Pydantic 스키마(`UserCreate`)가 기대하는 규격과 다름 |
| **3. 확인 방법** | 브라우저 개발자 도구 Network 탭 → 해당 요청의 **Payload**(보낸 값)와 **Response**(`detail` 배열에 적힌 필드별 에러 위치 `loc`, `msg`) 확인 |
| **4. 진짜 원인** | 프론트엔드 요청 DTO와 백엔드 `schemas/user.py`의 `UserCreate` 필드 규격(또는 최소 글자 수 조건 `min_length=8` 등) 불일치 |
| **5. 해결 방법** | 프론트엔드의 요청 타입(`CreateUserRequest`)과 백엔드 Pydantic 스키마(`UserCreate`)의 필드명 및 유효성 조건을 동기화함 |
| **6. 배운 원리** | FastAPI에서 **`422 Unprocessable Entity`는 "요청 문법(JSON)은 맞지만, Pydantic DTO 검증(필드 누락, 타입 불일치, 길이 제한 등)을 통과하지 못했음"**을 알려주는 대표적인 상태 코드다. |

---

## 2. [Project 1: M1] JWT 인증/인가 구현 및 보안 고장 실험

### ① 모듈 파일명 오타 예방 (`serurity.py` → `security.py`)
- **발견 시점**: M1 보안 모듈 초기 파일 생성 단계
- **내용**: `backend/app/core/serurity.py`로 생성된 파일명을 `security.py`로 즉시 바로잡아 이후 `from app.core.security import ...` 시 발생할 `ModuleNotFoundError`를 사전 예방함.

### ② 기존 가짜 해시(`hashed_...`) 계정과 Bcrypt 도입 간 호환 주의
| 칸 | 내용 |
| :--- | :--- |
| **1. 증상** | S0-7에서 만든 기존 회원 계정으로 M1 로그인(`POST /api/v1/auth/login`) 시도 시 `ValueError: Invalid salt` 또는 인증 실패 가능성 |
| **2. 가설** | S0-7에서는 임시로 `f"hashed_{password}"` 문자열을 DB에 저장했으나, M1의 `bcrypt.checkpw()`는 `$2b$12$...` 규격의 진짜 Bcrypt 해시 문자열만 검사할 수 있음 |
| **3. 확인 방법** | DB `users` 테이블의 `hashed_password` 컬럼 값이 `$2b$`로 시작하는지 확인 |
| **4. 진짜 원인** | 단방향 해싱 도입 전 임시 평문 접두사(`hashed_`)로 저장된 더미 데이터는 Bcrypt 알고리즘 규격의 Salt 포맷을 가지고 있지 않음 |
| **5. 해결 방법** | `user_service.py`를 `get_password_hash()`(Bcrypt)로 교체한 뒤 신규 회원을 가입시켜 테스트 진행 |
| **6. 배운 원리** | 비밀번호 해싱 알고리즘을 변경하거나 도입할 때는 기존 DB에 저장된 해시 포맷과의 호환성을 반드시 확인해야 한다. |

### ③ [고장 실험] 토큰 타입 검증(`type == "access"`) 누락 시 보안 취약점 (Token Type Confusion)
| 칸 | 내용 |
| :--- | :--- |
| **1. 실험 상황** | `deps.py`의 `get_current_user`에서 `if payload.get("type") != "access":` 검증 로직을 제거하고, `Authorization: Bearer <refresh_token>`으로 일반 API(`GET /api/v1/auth/me`)를 호출함 |
| **2. 예측 및 결과** | `401 Unauthorized`로 거절되어야 마땅하지만, **`200 OK`로 정상 통과되어 회원 정보가 반환됨** |
| **3. 진짜 원인** | `refresh_token` 역시 동일한 서버의 `SECRET_KEY`로 서명된 유효한 JWT이며, 내부에 `"sub": str(user_id)`와 `"exp"`(7일)를 똑같이 포함하고 있기 때문 |
| **4. 해결 방법** | 토큰 발급 시 Payload에 `"type": "access"`와 `"type": "refresh"`를 명시하고, 인증 문지기(`get_current_user`)에서는 `payload.get("type") != "access"`일 때 즉시 `401` 에러를 발생시킴 |
| **5. 배운 원리** | Access Token(15분)과 Refresh Token(7일)을 분리할 때는 만료 시간만 다르게 줄 것이 아니라, **토큰의 용도(`type` 클레임)를 반드시 검증해야 7일짜리 Refresh Token이 무적 Access Token으로 악용되는 사고를 막을 수 있다.** |

### ④ [아키텍처 Q&A 정리] 오늘 헷갈렸던 개념 완벽 격파
1. **단방향 해싱(Bcrypt) vs 양방향 암호화**:
   - 양방향 암호화는 키가 있으면 원본 복호화가 가능하지만, 비밀번호에 쓰는 **Bcrypt는 단방향 해싱**이므로 원본 복구가 절대 불가능하다. 따라서 고객이 비밀번호를 분실하면 "원래 비밀번호 안내"가 아니라 **"새 비밀번호 재설정"**만 가능하다.
2. **JWT와 Access/Refresh Token의 관계**:
   - **JWT**는 위조 방지 서명이 들어간 토큰의 **'기술 규격(재질)'**이고, **Access/Refresh Token**은 토큰의 **'역할(수명 15분 출입증 vs 수명 7일 재발급권)'**이다.
3. **RTR (Refresh Token Rotation)**:
   - Refresh Token으로 Access Token을 재발급받을 때, **기존 Refresh Token도 함께 폐기하고 새 Refresh Token으로 교체**하여 재발급권 탈취 위험까지 방어하는 기법이다.
4. **인증 실패(`401`) vs 인가 실패(`403`)**:
   - 토큰이 없거나 만료/위조된 경우(누구인지 모름)는 **`401 Unauthorized`**, 로그인은 되었으나 관리자(`ADMIN`) 등급이 아닌 경우(권한 부족)는 **`403 Forbidden`**으로 명확히 분리해야 프론트엔드가 올바른 후속 처리(재로그인 vs 권한 안내)를 할 수 있다.

