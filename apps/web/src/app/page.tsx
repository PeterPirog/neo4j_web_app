import Link from "next/link";

import { Card } from "@/components/ui/Card";

const layers = [
  "Browser",
  "Next.js",
  "FastAPI",
  "Service/query layer",
  "Async Neo4j driver",
  "Neo4j",
];

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <p className="text-sm font-semibold uppercase text-graph-accent">
          Graph application workspace
        </p>
        <h1 className="text-3xl font-semibold tracking-normal text-graph-ink">
          Neo4j Graph Platform
        </h1>
        <p className="max-w-3xl text-base leading-7 text-stone-600">
          A modular graph application moving from the educational Jinja2 UI to a
          typed Next.js frontend backed by FastAPI and parameterized Cypher.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <Card className="p-5">
          <h2 className="text-lg font-semibold">People</h2>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Manage Person nodes through the FastAPI JSON contract.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-graph-accent hover:text-emerald-800"
            href="/people"
          >
            Open People
          </Link>
        </Card>

        <Card className="p-5">
          <h2 className="text-lg font-semibold">Cities</h2>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Manage City nodes as a second graph entity type.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-graph-accent hover:text-emerald-800"
            href="/cities"
          >
            Open Cities
          </Link>
        </Card>

        <Card className="p-5">
          <h2 className="text-lg font-semibold">Relations</h2>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Create whitelisted Person-to-Person relationships with validated
            properties.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-graph-accent hover:text-emerald-800"
            href="/relations"
          >
            Open Relations
          </Link>
        </Card>

        <Card className="p-5">
          <h2 className="text-lg font-semibold">Residences</h2>
          <p className="mt-2 text-sm leading-6 text-stone-600">
            Connect Person and City nodes through MIESZKA_W relationships.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-graph-accent hover:text-emerald-800"
            href="/residences"
          >
            Open Residences
          </Link>
        </Card>
      </section>

      <section className="rounded-lg border border-graph-line bg-white p-5">
        <h2 className="text-lg font-semibold">Target Architecture</h2>
        <div className="mt-4 grid gap-2 sm:grid-cols-3 lg:grid-cols-6">
          {layers.map((layer) => (
            <div
              className="rounded-md border border-graph-line bg-graph-surface px-3 py-3 text-center text-sm font-medium"
              key={layer}
            >
              {layer}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
