# Neo4j Database Assets

This directory is the long-term home for Neo4j database assets.

- `migrations/` contains reviewed, ordered schema/data migrations.
- `constraints/` contains reusable idempotent constraint snippets.
- `indexes/` contains reusable idempotent index snippets.
- `seeds/` contains non-destructive development seed data.
- `diagnostics/` contains read-only inspection queries.
- `dangerous/` contains destructive scripts that require explicit approval.

Application runtime must use the official async Neo4j driver. MCP Neo4j remains
an agent-only diagnostic tool and is not part of runtime.

The active teaching model currently contains `Person` and `City` nodes,
whitelisted Person-to-Person relationships, and the static
`(:Person)-[:MIESZKA_W]->(:City)` relationship.

The legacy `cypher/` directory is kept for compatibility while references move
to this structure. Prefer this directory for new migrations, seeds and
diagnostics.
