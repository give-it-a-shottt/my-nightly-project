// 경로: frontend/src/app/dashboard/page.tsx
"use client"; // App Router에서 useQuery 등 클라이언트 훅을 사용하기 위한 선언

import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation"; // Pages Router의 'next/router' 대신 사용
import { client, clearAuthTokens } from "@/lib/api/client";

interface SleepRecord {
  id: number;
  user_id: number;
  device_serial: string;
  sleep_minutes: number;
  sleep_score: number;
  idempotency_key: string;
  recorded_at: string;
}

export default function DashboardPage() {
  const router = useRouter();

  // 로그인한 회원의 수면 기록 목록 조회 (JWT Access Token이 헤더에 자동 부착됨)
  const {
    data: records,
    isLoading,
    isError,
    refetch,
  } = useQuery<SleepRecord[]>({
    queryKey: ["my-sleep-records"],
    queryFn: async () => {
      const res = await client.get("/api/v1/webhooks/sleep/me");
      return res.data;
    },
  });

  const handleLogout = () => {
    clearAuthTokens();
    router.push("/login");
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-3xl mx-auto space-y-6">
        <header className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold text-indigo-400">
              🌙 내 수면 기록 대시보드
            </h1>
            <p className="text-sm text-slate-400">
              수면 기기 웹훅(HMAC 검증 + 멱등성 보장)으로 수집된 데이터입니다.
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => refetch()}
              className="px-3 py-2 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700">
              새로고침
            </button>
            <button
              onClick={handleLogout}
              className="px-3 py-2 text-xs rounded-lg bg-rose-950/60 text-rose-300 border border-rose-800">
              로그아웃
            </button>
          </div>
        </header>

        {isLoading && (
          <p className="text-slate-400 text-sm">수면 데이터를 불러오는 중...</p>
        )}
        {isError && (
          <div className="p-4 rounded-xl bg-rose-950/50 border border-rose-800 text-rose-300 text-sm">
            데이터를 불러오지 못했습니다. 먼저 로그인(`/login`)을 해주세요!
          </div>
        )}

        {records && records.length === 0 && (
          <p className="text-slate-400 text-sm">
            아직 수집된 수면 기록이 없습니다.
          </p>
        )}

        <div className="grid gap-4">
          {records?.map((rec) => {
            const hours = Math.floor(rec.sleep_minutes / 60);
            const mins = rec.sleep_minutes % 60;
            return (
              <div
                key={rec.id}
                className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                      기기: {rec.device_serial}
                    </span>
                    <span className="text-xs text-slate-500">
                      멱등성 키: {rec.idempotency_key}
                    </span>
                  </div>
                  <p className="text-lg font-semibold">
                    총 수면 시간: {hours}시간 {mins}분
                  </p>
                  <p className="text-xs text-slate-400">
                    측정 시각:{" "}
                    {new Date(rec.recorded_at).toLocaleString("ko-KR")}
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">
                    수면 점수
                  </span>
                  <span className="text-3xl font-extrabold text-emerald-400">
                    {rec.sleep_score}점
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}
