// 경로: frontend/src/app/login/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { client } from "@/lib/api/client";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await client.login(email, password);
      router.push("/dashboard"); // 로그인 성공 시 수면 기록 대시보드로 바로 이동!
    } catch {
      setError("이메일 또는 비밀번호가 올바르지 않습니다. (401)");
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6">
      <form
        onSubmit={handleSubmit}
        className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-4">
        <h1 className="text-xl font-bold text-indigo-400">🌙 Nightly 로그인</h1>
        {error && (
          <p className="text-xs text-rose-400 bg-rose-950/50 p-3 rounded-lg border border-rose-800">
            {error}
          </p>
        )}
        <input
          type="email"
          placeholder="이메일"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm"
          required
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm"
          required
        />
        <button
          type="submit"
          className="w-full py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 font-medium text-sm">
          로그인
        </button>
      </form>
    </main>
  );
}
