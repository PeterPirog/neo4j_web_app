# API

FastAPI JSON API for the Neo4j Web App.

The canonical backend dependency file is `apps/api/requirements.txt`. The root
`requirements.txt` exists only as a compatibility shim for older local commands.

## Run

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Health

Open `http://127.0.0.1:8000/api/health`.

## Architecture

The API keeps Cypher out of route handlers:

- `router.py` exposes HTTP endpoints.
- `schemas.py` defines Pydantic input and output models.
- `service.py` owns application logic.
- `repository.py` owns Neo4j calls.
- `queries.py` owns parameterized Cypher.

Legacy educational Jinja2 templates are kept in `app/legacy_templates/` as
reference material. They are not the target frontend.
