# Neo4j Model

## Current Nodes

### Person

Properties:

- `id`
- `name`
- `email`
- `note`
- `created_at`
- `updated_at`

## Current Relationships

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

## Future Placeholders

- `User`
- `Role`
- `Permission`
- `Resource`
- `Action`
- `Prediction`

## Legacy Educational Model

The previous educational application also used `City` nodes and
`(:Person)-[:MIESZKA_W]->(:City)`. That code was removed from active runtime
during the Next.js + FastAPI API transformation. The old Jinja2 template is kept
under `apps/api/app/legacy_templates/` only as a reference.
