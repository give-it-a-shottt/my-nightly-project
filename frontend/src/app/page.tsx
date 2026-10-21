"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>("연결 확인 중...");
  const [isError, setIsError] = useState<boolean>(false);

  useEffect(() => {
    // 3000번 프론트엔드 브라우저에서 8000번 백엔드로 직접 fetch 요청을 보냅니다.
    fetch("http://localhost:8000/health")
      .then((res) => {
        if (!res.ok) throw new Error("서버 응답 오류");
        return res.json();
      })
      .then((data) => {
        setBackendStatus(`연결 성공: ${data.status}`);
        setIsError(false);
      })
      .catch((err) => {
        setBackendStatus("연결 실패 (CORS 또는 서버 미실행)");
        setIsError(true);
      });
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl text-center space-y-4">
        <span className="text-3xl">🌙</span>
        <h1 className="text-2xl font-bold tracking-tight text-indigo-400">
          Nightly Sleep Service
        </h1>
        <p className="text-sm text-slate-400">
          AI 기반 수면 데이터 분석 및 맞춤형 수면 케어 구독 플랫폼
        </p>

        <div className="pt-4 border-t border-slate-800 space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-emerald-950 text-emerald-400 border border-emerald-800">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            프론트엔드 (Port 3000) 정상
          </div>

          <div
            className={`block px-3 py-1.5 rounded-lg text-xs font-medium border ${
              isError
                ? "bg-rose-950 text-rose-300 border-rose-800"
                : "bg-slate-800 text-slate-300 border-slate-700"
            }`}>
            백엔드 상태: {backendStatus}
          </div>
        </div>
      </div>
    </main>
  );
}
