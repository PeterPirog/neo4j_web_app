# Agent Rules

## Priorities

1. Do not break existing application behavior.
2. Do not add runtime dependencies without need and user approval.
3. Keep Next.js + FastAPI + async Neo4j driver as the core architecture.
4. Parameterize every user input in Cypher.
5. Treat MCP Neo4j as a diagnostic tool, not application runtime.

## Forbidden Without Explicit Approval

- Overwriting `.env`.
- Adding real passwords, tokens or secret URIs.
- Resetting the database.
- Broad data deletion.
- Installing packages when the user did not request it.
- Migrating to ORM, OGM or GraphQL.
- Replacing the async Neo4j driver with a synchronous driver.

## Before Editing

- Inspect existing files and patterns in `apps/api/app` and `apps/web/src`.
- Merge with existing content instead of blindly overwriting files.
- For Neo4j diagnostics, prefer read-only `MATCH ... RETURN ... LIMIT`.
- When uncertain, describe risk instead of running destructive operations.

## After Editing

- Run available tests or basic verification.
- If tests are unavailable, describe what was not verified.
- List changed files and the reason for the changes.
