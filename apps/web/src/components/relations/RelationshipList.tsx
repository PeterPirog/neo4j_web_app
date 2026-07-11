"use client";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { RelationshipRead } from "@/features/relations/schemas";
import { useDeleteRelationship } from "@/features/relations/hooks";

type RelationshipListProps = {
  relationships: RelationshipRead[];
};

export function RelationshipList({ relationships }: RelationshipListProps) {
  const deleteRelationship = useDeleteRelationship();

  if (relationships.length === 0) {
    return (
      <Card className="p-5">
        <p className="text-sm text-stone-600">
          No Person-to-Person relationships returned by the API.
        </p>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {relationships.map((relationship) => (
        <Card className="p-4" key={relationship.id}>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-semibold">{relationship.source_name}</span>
                <span className="rounded-md bg-graph-ink px-2 py-1 text-xs font-semibold text-white">
                  {relationship.relationship_type}
                </span>
                <span className="font-semibold">{relationship.target_name}</span>
              </div>
              {relationship.note && (
                <p className="mt-2 text-sm leading-6 text-stone-700">
                  {relationship.note}
                </p>
              )}
              {relationship.strength && (
                <p className="mt-1 text-sm text-stone-500">
                  Strength: {relationship.strength}/10
                </p>
              )}
            </div>
            <Button
              disabled={deleteRelationship.isPending}
              onClick={() => {
                if (window.confirm("Delete this relationship?")) {
                  deleteRelationship.mutate(relationship.id);
                }
              }}
              variant="danger"
            >
              Delete
            </Button>
          </div>
        </Card>
      ))}
    </div>
  );
}
