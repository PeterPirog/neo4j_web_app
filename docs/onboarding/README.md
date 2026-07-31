# Onboarding

Start with the root `README.md`, then read the learning path:

- `docs/onboarding/neo4j-to-web-app.md`

Use the reference documents when you need details about a specific layer:

- `docs/architecture/target-architecture.md`
- `docs/api/api-contracts.md`
- `docs/frontend/frontend-guide.md`
- `docs/data-model/neo4j-model.md`

The project is intended to teach the path from a Neo4j graph model to a typed
web application:

```text
Neo4j model
  -> parameterized Cypher
  -> async FastAPI repository/service/router
  -> OpenAPI
  -> generated TypeScript client
  -> Next.js UI
```

Do not commit local `.env` files or MCP configurations with secrets.
