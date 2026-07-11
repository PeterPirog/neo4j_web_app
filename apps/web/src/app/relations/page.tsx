"use client";

import { RelationshipForm } from "@/components/relations/RelationshipForm";
import { RelationshipList } from "@/components/relations/RelationshipList";
import { usePeople } from "@/features/people/hooks";
import { useRelations } from "@/features/relations/hooks";

export default function RelationsPage() {
  const peopleQuery = usePeople();
  const relationsQuery = useRelations();

  return (
    <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
      <section className="space-y-4">
        <div>
          <h1 className="text-2xl font-semibold">Relations</h1>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Relationship types are validated in the frontend and again by the API.
          </p>
        </div>
        <RelationshipForm people={peopleQuery.data ?? []} />
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-lg font-semibold">Relationship list</h2>
          {(peopleQuery.isLoading || relationsQuery.isLoading) && (
            <span className="text-sm text-stone-500">Loading...</span>
          )}
        </div>

        {peopleQuery.isError && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {peopleQuery.error.message}
          </div>
        )}

        {relationsQuery.isError && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {relationsQuery.error.message}
          </div>
        )}

        <RelationshipList relationships={relationsQuery.data ?? []} />
      </section>
    </div>
  );
}
