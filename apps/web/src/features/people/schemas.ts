import { z } from "zod";

import type { components } from "@neo4j-web-app/api-client";

export type PersonRead = components["schemas"]["PersonRead"];
export type PersonCreate = components["schemas"]["PersonCreate"];
export type PersonUpdate = components["schemas"]["PersonUpdate"];

export const personFormSchema = z.object({
  name: z.string().trim().min(1, "Name is required"),
  email: z.union([
    z.string().trim().email("Enter a valid email"),
    z.literal(""),
  ]),
  note: z.string().optional(),
});

export type PersonFormValues = z.infer<typeof personFormSchema>;

export function toPersonCreate(values: PersonFormValues): PersonCreate {
  return {
    name: values.name.trim(),
    email: values.email ? values.email.trim() : null,
    note: values.note?.trim() || null,
  };
}

export function toPersonUpdate(values: PersonFormValues): PersonUpdate {
  return toPersonCreate(values);
}
