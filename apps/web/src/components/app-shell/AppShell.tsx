import { ReactNode } from "react";

import { Navigation } from "@/components/app-shell/Navigation";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-graph-line bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="text-base font-semibold text-graph-ink">
              Neo4j Web App
            </div>
            <div className="text-sm text-stone-500">Next.js + FastAPI + Neo4j</div>
          </div>
          <Navigation />
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  );
}
