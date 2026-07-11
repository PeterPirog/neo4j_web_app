# Architecture

```text
Browser
  -> Next.js / React / TypeScript
  -> FastAPI
  -> service layer
  -> repository / query layer
  -> async Neo4j driver / neo4j-rust-ext
  -> Neo4j
```

## Backend

Backend code lives in `apps/api/app`.

- `main.py` creates the FastAPI app, configures lifespan, CORS and routers, and
  exposes root and health endpoints.
- `core/` contains config, CORS, errors and logging helpers.
- `db/neo4j.py` owns the async Neo4j driver lifecycle.
- `modules/<module>/router.py` owns HTTP endpoints.
- `modules/<module>/schemas.py` owns Pydantic models.
- `modules/<module>/service.py` owns application logic.
- `modules/<module>/repository.py` owns Neo4j calls.
- `modules/<module>/queries.py` owns Cypher.

## Frontend

Frontend code lives in `apps/web`.

- Next.js App Router owns routes and layouts.
- TanStack Query owns client-side fetching and invalidation.
- React Hook Form and Zod own form state and validation.
- Tailwind CSS owns the current design system.
- The generated OpenAPI client lives in `packages/api-client`.

## Neo4j Sessions

Use async sessions with an explicit database:

```python
async with driver.session(database=NEO4J_DATABASE) as session:
    result = await session.run(query, id=person_id)
```

Never use a synchronous Neo4j driver.

## MCP

MCP Neo4j is allowed only for agent diagnostics and must not be imported by the
runtime application.
