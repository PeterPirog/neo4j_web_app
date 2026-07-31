# Target Architecture

```text
Browser
  |
  v
Next.js / React / TypeScript
  |
  v
FastAPI JSON API
  |
  v
Service layer
  |
  v
Repository / query layer
  |
  v
Async Neo4j driver / neo4j-rust-ext
  |
  v
Neo4j
```

## Layers

- Browser renders the web UI.
- Next.js owns routing, layouts, client state and API calls.
- FastAPI is the contract boundary and generates OpenAPI.
- Services contain application decisions.
- Repositories execute Neo4j calls.
- Query files contain parameterized Cypher.
- Neo4j stores graph data.

## Request Flow

Use the `Person` feature as the reference path:

```text
apps/web/src/app/people/page.tsx
  -> apps/web/src/features/people/hooks.ts
  -> apps/web/src/features/people/api.ts
  -> packages/api-client
  -> GET/POST/PATCH/DELETE /api/v1/people
  -> apps/api/app/modules/people/router.py
  -> service.py
  -> repository.py
  -> queries.py
  -> Neo4j
```

Each layer should add only its own responsibility. Pages compose UI, hooks own
client cache behavior, FastAPI owns the HTTP contract, services own application
decisions, repositories own Neo4j calls, and query files own Cypher.

The same path is used for `City`. Cross-entity graph behavior is shown through
the `residences` module, which connects `Person` and `City` through
`MIESZKA_W`.

## Why Split Frontend and Backend

The frontend can evolve as a typed product UI without owning database access.
The backend remains the place for validation, authorization, API contracts and
database consistency.

## Why Frontend Does Not Talk To Neo4j

Direct database access from a browser would expose credentials, bypass backend
authorization and make Cypher part of the public client. All browser traffic
must go through FastAPI.

## API Versioning

Canonical API routes live under `/api/v1`. Legacy `/api` routes can remain as
temporary compatibility aliases, but generated OpenAPI clients should target the
versioned routes.

## Why FastAPI Is The Contract Layer

FastAPI provides Pydantic validation, generated OpenAPI and a stable JSON API
for frontend, tests and future integrations.

## Why Cypher Is In The Query Layer

Keeping Cypher in `queries.py` makes database behavior reviewable and prevents
route handlers or frontend code from embedding graph logic.

## Neo4j Assets

Long-term Neo4j migrations, constraints, indexes, seeds and diagnostics live in
`database/neo4j`. Runtime code may verify required schema compatibility, but
reviewed migrations are the canonical database change path.

The older `cypher/` directory is compatibility material for previous local
references. New learning material and new schema work should start in
`database/neo4j`.
