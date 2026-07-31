import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createPerson,
  deletePerson,
  fetchPeople,
  updatePerson,
} from "@/features/people/api";

export const peopleQueryKey = ["people"] as const;

export function usePeople() {
  return useQuery({
    queryKey: peopleQueryKey,
    queryFn: fetchPeople,
  });
}

export function useCreatePerson() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createPerson,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: peopleQueryKey });
    },
  });
}

export function useUpdatePerson() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updatePerson,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: peopleQueryKey });
    },
  });
}

export function useDeletePerson() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deletePerson,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: peopleQueryKey });
      queryClient.invalidateQueries({ queryKey: ["relations"] });
      queryClient.invalidateQueries({ queryKey: ["residences"] });
    },
  });
}
