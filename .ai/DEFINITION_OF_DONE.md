# Definition of Done

A change is ready when it:

- Preserves the Next.js + FastAPI + async Neo4j driver architecture.
- Does not add Django, SQLAlchemy, neomodel, OGM or GraphQL.
- Does not add MCP Neo4j as a runtime dependency.
- Uses parameterized Cypher.
- Does not store secrets in the repository.
- Does not modify real `.env` files.
- Does not perform destructive Neo4j operations without explicit approval.
- Keeps backend code separated into routers, schemas, services, repositories and
  query files.
- Keeps frontend communication limited to the FastAPI API.
- Includes basic verification: tests, compile checks, app import, app startup or
  a documented limitation.

For schema or data changes:

- Keep idempotent schema Cypher in `cypher/constraints` or `cypher/indexes`.
- Keep read-only diagnostics in `cypher/diagnostics`.
- Describe the impact on existing data.
