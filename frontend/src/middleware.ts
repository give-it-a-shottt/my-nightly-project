// 경로: frontend/src/middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // 쿠키에 access_token 팔찌가 있는지 확인
  const token = request.cookies.get("access_token")?.value;

  // 팔찌 없이 /mypage 나 /admin 으로 들어가려고 하면 -> /login 화면으로 튕겨냄!
  if (
    !token &&
    (request.nextUrl.pathname.startsWith("/mypage") ||
      request.nextUrl.pathname.startsWith("/admin"))
  ) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/mypage/:path*", "/admin/:path*"],
};
