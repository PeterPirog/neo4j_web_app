import { z } from "zod";

import type { components } from "@neo4j-web-app/api-client";

export const relationshipTypes = [
  "KNOWS",
  "WORKS_WITH",
  "MANAGES",
  "REPORTS_TO",
  "RELATED_TO",
] as const;

export type RelationshipRead = components["schemas"]["RelationshipRead"];
export type RelationshipCreate = components["schemas"]["RelationshipCreate"];
export type RelationshipType = (typeof relationshipTypes)[number];

export const relationshipFormSchema = z
  .object({
    source_person_id: z.string().trim().min(1, "Source person is required"),
    target_person_id: z.string().trim().min(1, "Target person is required"),
    relationship_type: z.enum(relationshipTypes),
    note: z.string().optional(),
    strength: z
      .string()
      .optional()
      .refine((value) => {
        if (!value) {
          return true;
        }
        const numeric = Number(value);
        return Number.isInteger(numeric) && numeric >= 1 && numeric <= 10;
      }, "Strength must be a number from 1 to 10"),
  })
  .refine((value) => value.source_person_id !== value.target_person_id, {
    path: ["target_person_id"],
    message: "Target person must be different",
  });

export type RelationshipFormValues = z.infer<typeof relationshipFormSchema>;

export function toRelationshipCreate(
  values: RelationshipFormValues,
): RelationshipCreate {
  return {
    source_person_id: values.source_person_id,
    target_person_id: values.target_person_id,
    relationship_type: values.relationship_type,
    note: values.note?.trim() || null,
    strength: values.strength ? Number(values.strength) : null,
  };
}
