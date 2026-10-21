// frontend/src/hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchUsers, createUser } from "@/lib/api/users";

export function useUsers() {
  const queryClient = useQueryClient();

  // [조회] 'users'라는 이름표로 데이터를 캐싱하고 관리
  const usersQuery = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
  });

  // [생성] 백엔드에 POST 요청을 보내고, 성공하면 'users' 캐시를 무효화
  const createUserMutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  return {
    users: usersQuery.data ?? [],
    isLoading: usersQuery.isLoading,
    addUser: createUserMutation.mutate,
    isCreating: createUserMutation.isPending,
  };
}
