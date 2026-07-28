import type {
  RelationshipCreate,
  RelationshipRead,
} from "@/features/relations/schemas";
import { apiClient } from "@/shared/api/client";
import { apiError } from "@/shared/api/errors";

export async function fetchRelations(): Promise<RelationshipRead[]> {
  const { data, error } = await apiClient.GET("/api/v1/relations");
  if (error) {
    throw apiError(error);
  }
  return data ?? [];
}

export async function createRelationship(
  payload: RelationshipCreate,
): Promise<RelationshipRead> {
  const { data, error } = await apiClient.POST("/api/v1/relations", {
    body: payload,
  });
  if (error || !data) {
    throw apiError(error);
  }
  return data;
}

export async function deleteRelationship(relationshipId: string): Promise<boolean> {
  const { data, error } = await apiClient.DELETE(
    "/api/v1/relations/{relationship_id}",
    {
      params: { path: { relationship_id: relationshipId } },
    },
  );
  if (error || !data) {
    throw apiError(error);
  }
  return data.deleted;
}
