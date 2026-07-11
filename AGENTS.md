# AGENTS.md

## Project Goal

This repository is being developed as a long-term Neo4j graph application with:

- Next.js / React / TypeScript frontend in `apps/web`.
- FastAPI JSON API in `apps/api`.
- Service, repository and query layers for Neo4j access.
- Official async Neo4j driver / `neo4j-rust-ext`.
- Pure parameterized Cypher.
- Local Neo4j database.
- MCP Neo4j only as an agent diagnostic tool.

The current implemented domain covers:

- `Person` nodes.
- Whitelisted Person-to-Person relationships.
- Placeholder modules for permissions, graph explorer, AI / GraphRAG and ML.

Legacy Jinja2 templates from the educational app are preserved in
`apps/api/app/legacy_templates/`.

## Mandatory Architecture

Do not use:

- Django.
- Django ORM.
- SQLAlchemy.
- neomodel.
- OGM.
- GraphQL at this stage.
- Synchronous Neo4j driver.
- Runtime MCP dependencies.

Use:

- FastAPI.
- async/await.
- `from neo4j import AsyncGraphDatabase`.
- Raw Cypher.
- Parameterized queries.
- Service layer, repository layer and query files for Neo4j access.
- Next.js / React / TypeScript for the target frontend.

## Neo4j Rules

Application runtime communicates with Neo4j only through the official async
driver.

MCP Neo4j may be used by agents for:

- diagnostics,
- schema inspection,
- node counts,
- relationship previews,
- read-only Cypher checks.

MCP Neo4j is not part of application runtime.

Do not delete database data without explicit user approval. Do not run
destructive Cypher such as broad `DETACH DELETE`, `DROP CONSTRAINT`, `DROP
INDEX` or database resets unless the user explicitly requests it.

## Cypher Safety

Always parameterize user data.

Good:

```cypher
MATCH (p:Person {id: $person_id})
RETURN p
```

Bad:

```python
query = f"MATCH (p:Person {{id: '{person_id}'}}) RETURN p"
```

Dynamic relationship types are allowed only after whitelist validation.

## Agent Workflow

Before code changes:

- Read `README.md`, `AGENTS.md` and relevant files in `.ai/`.
- Inspect current patterns in `apps/api/app` and `apps/web/src`.
- Decide whether the change affects runtime or diagnostics only.
- Do not install packages unless the user requested it.
- Do not modify `.env` and do not add secrets.

## Definition of Done

A change is done when:

- It keeps FastAPI + async Neo4j driver architecture.
- It does not introduce ORM, OGM, SQLAlchemy, Django or runtime MCP.
- It uses parameterized Cypher.
- It keeps clear separation of routers, services, repositories and queries.
- It keeps frontend API access through FastAPI only.
- It is verified by tests, compile checks, app startup or a clear risk note.
