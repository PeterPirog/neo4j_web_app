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

## Why Split Frontend and Backend

The frontend can evolve as a typed product UI without owning database access.
The backend remains the place for validation, authorization, API contracts and
database consistency.

## Why Frontend Does Not Talk To Neo4j

Direct database access from a browser would expose credentials, bypass backend
authorization and make Cypher part of the public client. All browser traffic
must go through FastAPI.

## Why FastAPI Is The Contract Layer

FastAPI provides Pydantic validation, generated OpenAPI and a stable JSON API
for frontend, tests and future integrations.

## Why Cypher Is In The Query Layer

Keeping Cypher in `queries.py` makes database behavior reviewable and prevents
route handlers or frontend code from embedding graph logic.
