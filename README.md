# Technician Feedback API

A small Python API for practicing HTTP endpoints and relational database access. It uses FastAPI, SQLAlchemy, and SQLite. AI-based team routing and priority decisions are intentionally left for a later step.

## Run it locally

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> to try the API in Swagger UI. The SQLite database file, `feedback.db`, is created in this directory the first time the app starts.

Run the tests with:

```bash
python -m pytest
```

## Endpoints

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/health` | Confirms the API is running |
| GET | `/api/v1/feedback` | Lists feedback records |
| GET | `/api/v1/feedback/{feedback_id}` | Gets one record |
| POST | `/api/v1/feedback` | Saves a new record |
| PUT | `/api/v1/feedback/{feedback_id}` | Replaces the editable fields of a record |

Example request body:

```json
{
  "technician_name": "Taylor",
  "feedback_text": "The app will not load my jobs.",
  "score": 1,
  "mood": "frustrated",
  "assigned_team": null,
  "priority": "normal",
  "status": "new"
}
```

`score` is optional and must be from 1 to 5. `mood` can be `frustrated`, `neutral`, or `positive`. For a PUT request, send the full request body; omitted optional fields are reset to their defaults.

## How the database connection works

`app/database.py` creates a SQLAlchemy engine and a session factory. The default connection string points to a local SQLite file. Each API request gets a database session, and SQLAlchemy uses the `Feedback` model in `app/models.py` to map Python objects to rows in the `feedback` table.

Set `DATABASE_URL` to use a different SQLAlchemy-compatible database later. For example, a work SQL Server environment may require an approved ODBC driver, connection string, and secrets-management setup; don't put real credentials in this repository. The SQLite choice is only for local practice and doesn't lock in the production database.

## Suggested next steps

1. Create feedback through Swagger and inspect the new row in `feedback.db`.
2. Try GET, then change the team, priority, or status with PUT.
3. Add filters such as status or assigned team to the list endpoint.
4. Add AI classification behind a service interface, then decide how to review or override its team and priority suggestions.
5. If this becomes a deployed service, add database migrations, authentication, and production database configuration before connecting it to real technician data.
