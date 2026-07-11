"use client";

import { useState } from "react";

import { PeopleList } from "@/components/people/PeopleList";
import { PersonForm } from "@/components/people/PersonForm";
import type { PersonRead } from "@/features/people/schemas";
import { usePeople } from "@/features/people/hooks";

export default function PeoplePage() {
  const [editingPerson, setEditingPerson] = useState<PersonRead | null>(null);
  const peopleQuery = usePeople();

  return (
    <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
      <section className="space-y-4">
        <div>
          <h1 className="text-2xl font-semibold">People</h1>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Person nodes are loaded from FastAPI, not directly from Neo4j.
          </p>
        </div>
        <PersonForm
          onDone={() => setEditingPerson(null)}
          person={editingPerson}
        />
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-lg font-semibold">People list</h2>
          {peopleQuery.isLoading && (
            <span className="text-sm text-stone-500">Loading...</span>
          )}
        </div>

        {peopleQuery.isError && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {peopleQuery.error.message}
          </div>
        )}

        <PeopleList
          onEdit={setEditingPerson}
          people={peopleQuery.data ?? []}
        />
      </section>
    </div>
  );
}
