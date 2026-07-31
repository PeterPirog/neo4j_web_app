# Neo4j Model

Canonical database assets live under `database/neo4j`.

The older `cypher/` directory is retained for compatibility with local
references. It is not the first place to design new schema changes.

## Current Nodes

### Person

Properties:

- `id`
- `name`
- `email`
- `note`
- `created_at`
- `updated_at`

### City

Properties:

- `id`
- `name`
- `country`
- `note`
- `created_at`
- `updated_at`

## Current Relationships

### Person-To-Person

Person-to-Person relationships are created through a whitelist:

- `KNOWS`
- `WORKS_WITH`
- `MANAGES`
- `REPORTS_TO`
- `RELATED_TO`

Relationship properties:

- `id`
- `note`
- `strength`
- `created_at`
- `updated_at`

Current relation creation uses `MERGE` for one relationship of a given type
between the same source and target person. Repeating the same create request
updates the existing relationship properties instead of creating a duplicate.

### Person-To-City

Residence relationships connect people to cities:

```cypher
(:Person)-[:MIESZKA_W]->(:City)
```

`MIESZKA_W` is static Cypher, not a dynamic relationship type. It is managed by
the `residences` API module and represented in the frontend route
`/residences`.

Relationship properties:

- `created_at`
- `updated_at`

## Future Placeholders

- `User`
- `Role`
- `Permission`
- `Resource`
- `Action`
- `Prediction`

## Historical Note

The old Jinja2 template is kept under `apps/api/app/legacy_templates/` only as a
historical reference. It also showed `Person`, `City` and `MIESZKA_W`, but new UI
work should use the Next.js routes and FastAPI JSON API instead of Jinja2 forms.

## Add A New Domain Object

When adding the next graph concept, update the model first:

1. Add the node labels, relationship types and properties to this document.
2. Add idempotent constraints or indexes in `database/neo4j`.
3. Add parameterized Cypher in the backend query layer.
4. Expose the data through FastAPI schemas and routes.
5. Regenerate the TypeScript OpenAPI client.
6. Build the Next.js feature using the generated types.
