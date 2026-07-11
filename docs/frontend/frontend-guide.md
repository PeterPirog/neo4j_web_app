# Frontend Guide

The frontend lives in `apps/web` and uses:

- React for UI components.
- TypeScript for contracts and component types.
- Next.js App Router for pages and layouts.
- TanStack Query for fetching, cache and invalidation.
- React Hook Form for forms.
- Zod for frontend validation.
- Tailwind CSS for the current design system.
- OpenAPI client types from `packages/api-client`.
- Playwright for smoke end-to-end tests.

## Add A Page

Create `apps/web/src/app/<route>/page.tsx`. Use feature hooks for data and keep
API calls out of page components when they are shared.

## Add A Form

Create a Zod schema in `src/features/<feature>/schemas.ts`, a component in
`src/components/<feature>/`, and a mutation hook in
`src/features/<feature>/hooks.ts`.

## API Access

Use `src/lib/api/client.ts`, which re-exports the generated OpenAPI client.
Frontend code must not contain Cypher and must not connect to Neo4j directly.
