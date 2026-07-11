import { apiClient } from "@/lib/api/client";
import type {
  RelationshipCreate,
  RelationshipRead,
} from "@/features/relations/schemas";

function apiError(error: unknown): Error {
  if (error && typeof error === "object" && "detail" in error) {
    return new Error(String((error as { detail: unknown }).detail));
  }
  return new Error("API request failed");
}

export async function fetchRelations(): Promise<RelationshipRead[]> {
  const { data, error } = await apiClient.GET("/api/relations");
  if (error) {
    throw apiError(error);
  }
  return data ?? [];
}

export async function createRelationship(
  payload: RelationshipCreate,
): Promise<RelationshipRead> {
  const { data, error } = await apiClient.POST("/api/relations", {
    body: payload,
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data;
}

export async function deleteRelationship(relationshipId: string): Promise<boolean> {
  const { data, error } = await apiClient.DELETE(
    "/api/relations/{relationship_id}",
    {
      params: { path: { relationship_id: relationshipId } },
    },
  );
  if (error || !data) {
    throw apiError(error);
  }
  return data.deleted;
}
