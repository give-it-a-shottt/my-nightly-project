// frontend/src/app/users/page.tsx
"use client";

import { useState } from "react";
import { useUsers } from "@/hooks/useUsers";

export default function UsersPage() {
  const { users, isLoading, addUser, isCreating } = useUsers();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password) return;

    addUser(
      { name, email, password },
      {
        onSuccess: () => {
          setName("");
          setEmail("");
          setPassword("");
        },
      },
    );
  };

  return (
    <main className="max-w-xl mx-auto p-8 font-sans">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        회원 관리 (Stage 0)
      </h1>

      {/* 회원 등록 폼 */}
      <form
        onSubmit={handleSubmit}
        className="mb-8 p-4 bg-gray-50 border rounded-lg space-y-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            이름
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="홍길동"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            이메일
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="gildong@example.com"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            비밀번호 (8자 이상)
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="********"
            minLength={8}
            required
          />
        </div>
        <button
          type="submit"
          disabled={isCreating}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400">
          {isCreating ? "등록 중..." : "회원 등록"}
        </button>
      </form>

      {/* 회원 목록 */}
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        등록된 회원 목록
      </h2>
      {isLoading ? (
        <p className="text-gray-500">목록을 불러오는 중...</p>
      ) : users.length === 0 ? (
        <p className="text-gray-500">등록된 회원이 없습니다.</p>
      ) : (
        <ul className="divide-y border rounded-lg overflow-hidden bg-white">
          {users.map((user) => (
            <li key={user.id} className="p-4 flex justify-between items-center">
              <span className="font-medium text-gray-900">{user.name}</span>
              <span className="text-sm text-gray-500">{user.email}</span>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
