# Neo4j Web App

FastAPI + Jinja2 + Bootstrap 5 application backed by local Neo4j through the official async Neo4j driver.

## Run locally

```powershell
uvicorn app.main:app --reload
```

## Runtime stack

- FastAPI
- Jinja2 Templates
- Bootstrap 5
- `neo4j-rust-ext` / official async Neo4j driver
- Pure parameterized Cypher
- Local Neo4j database

## Configuration

Copy `.env.example` to `.env` locally and fill in your own Neo4j password. Do not commit `.env`.

Required variables:

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `NEO4J_DATABASE`

## AI and agent context

Agent-facing context lives in:

- `AGENTS.md`
- `.ai/PROJECT_CONTEXT.md`
- `.ai/ARCHITECTURE.md`
- `.ai/AGENT_RULES.md`
- `.ai/MCP_NEO4J_GUIDE.md`
- `.ai/CYPHER_STYLE_GUIDE.md`
- `.ai/SECURITY_RULES.md`
- `.ai/DEFINITION_OF_DONE.md`

MCP Neo4j is allowed only as an agent diagnostic tool. It must not be added as a runtime dependency of the FastAPI application.

## Cypher files

- `cypher/schema.cypher` - safe idempotent constraints and indexes.
- `cypher/diagnostics.cypher` - read-only diagnostics.
- `cypher/seed_dev.cypher` - optional non-destructive local seed.
- `cypher/dangerous_reset.cypher` - disabled reset template with warnings.
