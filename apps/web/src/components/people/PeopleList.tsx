"use client";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { PersonRead } from "@/features/people/schemas";
import { useDeletePerson } from "@/features/people/hooks";

type PeopleListProps = {
  people: PersonRead[];
  onEdit: (person: PersonRead) => void;
};

export function PeopleList({ people, onEdit }: PeopleListProps) {
  const deletePerson = useDeletePerson();

  if (people.length === 0) {
    return (
      <Card className="p-5">
        <p className="text-sm text-stone-600">No people returned by the API.</p>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {people.map((person) => (
        <Card className="p-4" key={person.id}>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <h2 className="truncate text-base font-semibold">{person.name}</h2>
              {person.email && (
                <p className="mt-1 text-sm text-stone-500">{person.email}</p>
              )}
              {person.note && (
                <p className="mt-2 text-sm leading-6 text-stone-700">
                  {person.note}
                </p>
              )}
            </div>
            <div className="flex shrink-0 gap-2">
              <Button onClick={() => onEdit(person)} variant="secondary">
                Edit
              </Button>
              <Button
                disabled={deletePerson.isPending}
                onClick={() => {
                  if (window.confirm("Delete this person?")) {
                    deletePerson.mutate(person.id);
                  }
                }}
                variant="danger"
              >
                Delete
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
