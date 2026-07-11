# Project Context

This project is a FastAPI + Neo4j graph application being transformed into a
monorepo with a Next.js frontend.

## Stack

- `apps/web`: Next.js, React, TypeScript, Tailwind CSS, TanStack Query, React
  Hook Form and Zod.
- `apps/api`: FastAPI JSON API.
- Neo4j access through the official async driver / `neo4j-rust-ext`.
- Pure parameterized Cypher.
- MCP Neo4j only as an agent diagnostic tool.

## Runtime Boundary

The frontend communicates only with FastAPI. It must not contain Cypher and must
not connect directly to Neo4j.

FastAPI communicates with Neo4j through:

- `router.py`
- `schemas.py`
- `service.py`
- `repository.py`
- `queries.py`

## Current Domain

- `Person` nodes.
- Whitelisted Person-to-Person relationships:
  - `KNOWS`
  - `WORKS_WITH`
  - `MANAGES`
  - `REPORTS_TO`
  - `RELATED_TO`

Placeholder modules:

- permissions
- graph explorer
- AI / GraphRAG
- ML

Legacy Jinja2 templates are preserved in `apps/api/app/legacy_templates/`.
