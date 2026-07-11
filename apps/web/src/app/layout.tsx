import type { Metadata } from "next";
import { ReactNode } from "react";

import { AppShell } from "@/components/app-shell/AppShell";
import { QueryProvider } from "@/lib/query/QueryProvider";

import "./globals.css";

export const metadata: Metadata = {
  title: "Neo4j Graph Platform",
  description: "Next.js frontend for the FastAPI and Neo4j graph application.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <AppShell>{children}</AppShell>
        </QueryProvider>
      </body>
    </html>
  );
}
