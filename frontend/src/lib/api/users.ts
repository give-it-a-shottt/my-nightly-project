// frontend/src/lib/api/users.ts
import { client } from "./client";

// 백엔드 UserResponse DTO와 1:1 매핑되는 타입
export interface User {
  id: number;
  name: string;
  email: string;
}

export async function fetchUsers(): Promise<User[]> {
  const res = await client.get("/api/v1/users");
  return res.data;
}

export async function createUser(data: {
  name: string;
  email: string;
  password: string;
}): Promise<User> {
  const res = await client.post("/api/v1/users", data);
  return res.data;
}
