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

Use `apps/web/src/shared/api/client.ts`, which creates the generated OpenAPI
client from `packages/api-client`.

Frontend code must not contain Cypher and must not connect to Neo4j directly.
Every browser request should go to FastAPI.

## Feature File Pattern

For a feature such as `people`, keep the responsibilities split:

- `src/features/people/api.ts` calls FastAPI through the generated client.
- `src/features/people/hooks.ts` owns TanStack Query keys, queries and mutations.
- `src/features/people/schemas.ts` maps OpenAPI types and Zod form validation.
- `src/components/people/` contains reusable UI for forms and lists.
- `src/app/people/page.tsx` composes the page and page-level state.

The same pattern is used for `cities`, `relations` and `residences`.

When a backend schema changes, regenerate `packages/api-client/src/schema.d.ts`
before relying on TypeScript in the frontend.
