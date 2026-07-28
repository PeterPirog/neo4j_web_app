# API Contracts

FastAPI exposes canonical JSON endpoints under `/api/v1`.

Legacy `/api` endpoints are kept as compatibility aliases and are hidden from
OpenAPI.

## Health

- `GET /api/v1/health`

## People

- `GET /api/v1/people`
- `POST /api/v1/people`
- `GET /api/v1/people/{person_id}`
- `PATCH /api/v1/people/{person_id}`
- `DELETE /api/v1/people/{person_id}`

## Relations

- `GET /api/v1/relations`
- `POST /api/v1/relations`
- `DELETE /api/v1/relations/{relationship_id}`

Allowed relationship types:

- `KNOWS`
- `WORKS_WITH`
- `MANAGES`
- `REPORTS_TO`
- `RELATED_TO`

## Placeholder Modules

- `GET /api/v1/permissions/health`
- `GET /api/v1/graph/health`
- `GET /api/v1/ai/health`
- `GET /api/v1/ml/health`

## Generate Client

Start FastAPI on port 8000 and run:

```powershell
npm run generate:api-client
```

The frontend uses API contracts and generated types. It must not contain Cypher.
