import { apiClient } from "@/lib/api/client";
import type { PersonCreate, PersonRead, PersonUpdate } from "@/features/people/schemas";

function apiError(error: unknown): Error {
  if (error && typeof error === "object" && "detail" in error) {
    return new Error(String((error as { detail: unknown }).detail));
  }
  return new Error("API request failed");
}

export async function fetchPeople(): Promise<PersonRead[]> {
  const { data, error } = await apiClient.GET("/api/people");
  if (error) {
    throw apiError(error);
  }
  return data ?? [];
}

export async function createPerson(payload: PersonCreate): Promise<PersonRead> {
  const { data, error } = await apiClient.POST("/api/people", {
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
  const { data, error } = await apiClient.PATCH("/api/people/{person_id}", {
    params: { path: { person_id: args.personId } },
    body: args.payload,
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data;
}

export async function deletePerson(personId: string): Promise<boolean> {
  const { data, error } = await apiClient.DELETE("/api/people/{person_id}", {
    params: { path: { person_id: personId } },
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data.deleted;
}
