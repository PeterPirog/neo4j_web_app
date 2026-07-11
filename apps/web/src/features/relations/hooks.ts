import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createRelationship,
  deleteRelationship,
  fetchRelations,
} from "@/features/relations/api";

export const relationsQueryKey = ["relations"] as const;

export function useRelations() {
  return useQuery({
    queryKey: relationsQueryKey,
    queryFn: fetchRelations,
  });
}

export function useCreateRelationship() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createRelationship,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: relationsQueryKey });
      queryClient.invalidateQueries({ queryKey: ["people"] });
    },
  });
}

export function useDeleteRelationship() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteRelationship,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: relationsQueryKey });
      queryClient.invalidateQueries({ queryKey: ["people"] });
    },
  });
}
