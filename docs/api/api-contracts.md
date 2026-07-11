# API Contracts

FastAPI exposes JSON endpoints under `/api`.

## Health

- `GET /api/health`

## People

- `GET /api/people`
- `POST /api/people`
- `GET /api/people/{person_id}`
- `PATCH /api/people/{person_id}`
- `DELETE /api/people/{person_id}`

## Relations

- `GET /api/relations`
- `POST /api/relations`
- `DELETE /api/relations/{relationship_id}`

Allowed relationship types:

- `KNOWS`
- `WORKS_WITH`
- `MANAGES`
- `REPORTS_TO`
- `RELATED_TO`

## Placeholder Modules

- `GET /api/permissions/health`
- `GET /api/graph/health`
- `GET /api/ai/health`
- `GET /api/ml/health`

## Generate Client

Start FastAPI on port 8000 and run:

```powershell
npm run generate:api-client
```

The frontend uses API contracts and generated types. It must not contain Cypher.
