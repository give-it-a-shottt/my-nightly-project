// 경로: frontend/src/lib/api/client.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// 브라우저 쿠키에서 access_token을 꺼내는 헬퍼 (middleware.ts와 공유하기 위해 쿠키 사용)
function getAccessToken(): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(/(?:^|;\s*)access_token=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : null;
}

export function setAuthTokens(accessToken: string, refreshToken: string) {
  // middleware.ts가 읽을 수 있도록 쿠키에 저장 (실무 배포 시에는 백엔드에서 HttpOnly 쿠키로 구워주는 것이 가장 안전합니다)
  document.cookie = `access_token=${encodeURIComponent(accessToken)}; path=/; max-age=900; SameSite=Lax`;
  localStorage.setItem("refresh_token", refreshToken);
}

export function clearAuthTokens() {
  document.cookie = "access_token=; path=/; max-age=0";
  localStorage.removeItem("refresh_token");
}

export const client = {
  async get(endpoint: string) {
    const token = getAccessToken();
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        // 💡 토큰이 있으면 Authorization 헤더에 Bearer 팔찌 부착!
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) throw new Error(`GET 요청 실패: ${res.status}`);
    const data = await res.json();
    return { data };
  },

  async post(endpoint: string, body: unknown) {
    const token = getAccessToken();
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`POST 요청 실패: ${res.status}`);
    const data = await res.json();
    return { data };
  },

  // 💡 M1 추가: OAuth2PasswordRequestForm 규격(application/x-www-form-urlencoded)에 맞춘 로그인 요청
  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append("username", email); // FastAPI OAuth2 폼은 username 필드에 이메일을 받음
    formData.append("password", password);

    const res = await fetch(`${BASE_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });
    if (!res.ok) throw new Error(`로그인 실패: ${res.status}`);
    const data = await res.json();
    setAuthTokens(data.access_token, data.refresh_token);
    return { data };
  },
};
