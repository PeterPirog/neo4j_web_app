# ADR 0001: Target Architecture Next.js + FastAPI + Neo4j

## Status

Accepted.

## Context

The project started as an educational FastAPI, Jinja2 and Neo4j CRUD app. It is
being prepared for long-term development by separate frontend, backend,
database and machine learning workstreams.

## Decision

Use:

- Next.js, React and TypeScript for the frontend.
- FastAPI as the backend API contract.
- Service, repository and query layers for backend structure.
- Official async Neo4j driver / neo4j-rust-ext for database access.
- Pure parameterized Cypher.

## Consequences

- The frontend consumes JSON APIs and OpenAPI types.
- Cypher stays in backend query files.
- Neo4j credentials stay server-side.
- Backend modules can grow independently.

## Alternatives

- Jinja2 only: simple, but weak for a rich long-term frontend.
- Vue/Nuxt: viable, but not selected for this project.
- GraphQL-first: deferred until the domain and access rules mature.
- Frontend directly to Neo4j: rejected because it exposes credentials and
  bypasses backend validation and authorization.

## Final Decision

Adopt the Next.js + FastAPI + Neo4j architecture.
