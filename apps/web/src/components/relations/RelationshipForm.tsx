"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Textarea } from "@/components/ui/Textarea";
import type { PersonRead } from "@/features/people/schemas";
import {
  relationshipFormSchema,
  relationshipTypes,
  RelationshipFormValues,
  toRelationshipCreate,
} from "@/features/relations/schemas";
import { useCreateRelationship } from "@/features/relations/hooks";

type RelationshipFormProps = {
  people: PersonRead[];
};

const emptyValues: RelationshipFormValues = {
  source_person_id: "",
  target_person_id: "",
  relationship_type: "KNOWS",
  note: "",
  strength: "",
};

export function RelationshipForm({ people }: RelationshipFormProps) {
  const createRelationship = useCreateRelationship();
  const hasEnoughPeople = people.length >= 2;

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<RelationshipFormValues>({
    resolver: zodResolver(relationshipFormSchema),
    defaultValues: emptyValues,
  });

  useEffect(() => {
    reset({
      ...emptyValues,
      source_person_id: people[0]?.id ?? "",
      target_person_id: people[1]?.id ?? "",
    });
  }, [people, reset]);

  async function onSubmit(values: RelationshipFormValues) {
    await createRelationship.mutateAsync(toRelationshipCreate(values));
    reset({
      ...emptyValues,
      source_person_id: people[0]?.id ?? "",
      target_person_id: people[1]?.id ?? "",
    });
  }

  return (
    <Card className="p-5">
      <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
        <div>
          <h2 className="text-lg font-semibold">Create relationship</h2>
        </div>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Source person</span>
          <Select disabled={!hasEnoughPeople} {...register("source_person_id")}>
            {people.map((person) => (
              <option key={person.id} value={person.id}>
                {person.name}
              </option>
            ))}
          </Select>
          {errors.source_person_id && (
            <span className="text-sm text-red-700">
              {errors.source_person_id.message}
            </span>
          )}
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Target person</span>
          <Select disabled={!hasEnoughPeople} {...register("target_person_id")}>
            {people.map((person) => (
              <option key={person.id} value={person.id}>
                {person.name}
              </option>
            ))}
          </Select>
          {errors.target_person_id && (
            <span className="text-sm text-red-700">
              {errors.target_person_id.message}
            </span>
          )}
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Relationship type</span>
          <Select {...register("relationship_type")}>
            {relationshipTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </Select>
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Note</span>
          <Textarea {...register("note")} />
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Strength</span>
          <Input
            max={10}
            min={1}
            placeholder="1-10"
            type="number"
            {...register("strength")}
          />
          {errors.strength && (
            <span className="text-sm text-red-700">
              {errors.strength.message}
            </span>
          )}
        </label>

        {createRelationship.error && (
          <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {createRelationship.error.message}
          </div>
        )}

        <Button
          disabled={!hasEnoughPeople || createRelationship.isPending}
          type="submit"
        >
          {createRelationship.isPending ? "Saving..." : "Create"}
        </Button>
      </form>
    </Card>
  );
}
