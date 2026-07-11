"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import {
  PersonFormValues,
  PersonRead,
  personFormSchema,
  toPersonCreate,
  toPersonUpdate,
} from "@/features/people/schemas";
import {
  useCreatePerson,
  useUpdatePerson,
} from "@/features/people/hooks";

type PersonFormProps = {
  person?: PersonRead | null;
  onDone?: () => void;
};

const emptyValues: PersonFormValues = {
  name: "",
  email: "",
  note: "",
};

export function PersonForm({ person, onDone }: PersonFormProps) {
  const createPerson = useCreatePerson();
  const updatePerson = useUpdatePerson();
  const isEditing = Boolean(person);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PersonFormValues>({
    resolver: zodResolver(personFormSchema),
    defaultValues: emptyValues,
  });

  useEffect(() => {
    if (person) {
      reset({
        name: person.name,
        email: person.email ?? "",
        note: person.note ?? "",
      });
      return;
    }
    reset(emptyValues);
  }, [person, reset]);

  const isSaving = createPerson.isPending || updatePerson.isPending;
  const mutationError = createPerson.error ?? updatePerson.error;

  async function onSubmit(values: PersonFormValues) {
    if (person) {
      await updatePerson.mutateAsync({
        personId: person.id,
        payload: toPersonUpdate(values),
      });
    } else {
      await createPerson.mutateAsync(toPersonCreate(values));
    }
    reset(emptyValues);
    onDone?.();
  }

  return (
    <Card className="p-5">
      <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
        <div>
          <h2 className="text-lg font-semibold">
            {isEditing ? "Edit person" : "Create person"}
          </h2>
        </div>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Name</span>
          <Input {...register("name")} autoComplete="name" />
          {errors.name && (
            <span className="text-sm text-red-700">{errors.name.message}</span>
          )}
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Email</span>
          <Input {...register("email")} autoComplete="email" type="email" />
          {errors.email && (
            <span className="text-sm text-red-700">{errors.email.message}</span>
          )}
        </label>

        <label className="block space-y-1">
          <span className="text-sm font-medium">Note</span>
          <Textarea {...register("note")} />
        </label>

        {mutationError && (
          <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {mutationError.message}
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          <Button disabled={isSaving} type="submit">
            {isSaving ? "Saving..." : isEditing ? "Save changes" : "Create"}
          </Button>
          {isEditing && (
            <Button onClick={onDone} type="button" variant="secondary">
              Cancel
            </Button>
          )}
        </div>
      </form>
    </Card>
  );
}
