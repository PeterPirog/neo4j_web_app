import type { PersonCreate, PersonRead, PersonUpdate } from "@/features/people/schemas";
import { apiClient } from "@/shared/api/client";
import { apiError } from "@/shared/api/errors";

export async function fetchPeople(): Promise<PersonRead[]> {
  const { data, error } = await apiClient.GET("/api/v1/people");
  if (error) {
    throw apiError(error);
  }
  return data ?? [];
}

export async function createPerson(payload: PersonCreate): Promise<PersonRead> {
  const { data, error } = await apiClient.POST("/api/v1/people", {
    body: payload,
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data;
}

export async function updatePerson(args: {
  personId: string;
  payload: PersonUpdate;
}): Promise<PersonRead> {
  const { data, error } = await apiClient.PATCH("/api/v1/people/{person_id}", {
    params: { path: { person_id: args.personId } },
    body: args.payload,
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data;
}

export async function deletePerson(personId: string): Promise<boolean> {
  const { data, error } = await apiClient.DELETE("/api/v1/people/{person_id}", {
    params: { path: { person_id: personId } },
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data.deleted;
}
