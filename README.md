## Module 12 — FastAPI Calculator & User Management

### Overview

This module contains a small FastAPI application that provides calculation operations and user management (registration and authentication). The project includes unit, integration, and end-to-end tests and demonstrates typical patterns for building a REST API with authentication and database access.

This README describes how to set up, run, and test the Module 12 project.

### Goals
- Provide calculation endpoints (calculator operations).
- Provide user endpoints (register, login, secure endpoints).
- Include unit, integration, and e2e tests with coverage reporting.

### Repository layout (key files)
- `main.py` — Application entrypoint.
- `app/` — Application package
  - `crud.py` — Database CRUD helpers.
  - `db.py` — DB session/connection utilities.
  - `factory.py` — App/test factory utilities.
  - `models.py` — ORM models.
  - `schemas.py` — Pydantic schemas.
  - `security.py` — Auth helpers (hashing, tokens).
  - `operations/routers/` — Routers for endpoints:
    - `calculations.py` — Calculation endpoints.
    - `users.py` — User endpoints.
- `tests/` — Unit, integration, and e2e tests.
- `requirements.txt` — Python dependencies.
- `pytest.ini` — Pytest configuration.

### Requirements
- Python 3.8+
- pip
- Recommended: use a virtual environment (venv or virtualenv)

### Quick setup (local)
1. Create and activate virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

If you prefer containers, the repo contains a `Dockerfile` and `docker-compose.yml` for containerized runs.

### Run the app (development)

Run with Uvicorn (from repo root):

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 (or the configured host/port).

### Typical endpoints
Exact routes are defined under `app/operations/routers`.

- User endpoints (from `users.py`)
  - `POST /users/register` — register a user
  - `POST /users/login` — authenticate and receive a token
  - `GET /users/{id}` — get user details (protected)

- Calculation endpoints (from `calculations.py`)
  - `POST /calculate` or operation-specific routes — run calculations and receive results

Refer to the router files for exact paths and bodies.

### Testing

Run tests with pytest:

```bash
pytest -q
```

Run a specific test file:

```bash
pytest tests/unit/test_calculator.py -q
```

Generate coverage HTML:

```bash
pytest --cov=app --cov-report=html
```

Coverage output will be written to `htmlcov/` (open `htmlcov/index.html`).

Notes:
- `conftest.py` contains fixtures for test DB and test client setup.
- Integration tests may use a test DB or an in-memory SQLite instance depending on `db.py`/`factory.py`.

### Development tips
- Use the app factory in `factory.py` when writing tests to create isolated test clients.
- Keep secrets (JWT secret, DB URL) in environment variables and out of source control.

### Troubleshooting
- If tests fail due to DB errors, verify test DB settings in `db.py` and that the test process can write to any SQLite files used.
- If authentication tests fail, check token secret/expiry in `security.py`.

 
### Integration tests and manual OpenAPI checks

This section explains how to run integration tests specifically (tests that exercise multiple parts of the app together) and how to manually exercise the API using the FastAPI OpenAPI docs (Swagger UI) for quick manual verification.

1) Run integration tests

- Run all integration tests (folder):

```bash
pytest -q tests/integration
```

- Run a single integration test file (example):

```bash
pytest -q tests/test_calculation_integration.py
```

- Notes:
  - Some integration tests run in-process using the app factory and fixtures in `tests/conftest.py`. Others may expect a running server. If a test fails with connection errors, start the app (see next section) and re-run the tests.
  - If your test environment requires a test database URL or other env vars, set them before running pytest. Check `conftest.py`, `db.py`, or `factory.py` for variables such as `TEST_DATABASE_URL`.

2) Manual checks using OpenAPI (Swagger UI / ReDoc)

- Start the development server (from the repository root):

```bash
uvicorn main:app --reload
```

- Open the interactive API docs in your browser:
  - Swagger UI (interactive): http://127.0.0.1:8000/docs
  - ReDoc (read-only docs): http://127.0.0.1:8000/redoc

- Typical manual verification flow:
  1. In `/docs`, expand the `POST /users/register` endpoint and use the "Try it out" button to register a user. Use the JSON body fields required by your `users` router (check the `users.py` file for exact schema names). Example body (adjust keys if your schema uses `email`/`username`):

```json
{
  "username": "testuser",
  "password": "password123"
}
```

  2. Use `POST /users/login` (via the docs) to obtain an access token. Example response will typically include a token (e.g. `access_token` or `token`).

  3. Click "Authorize" in the Swagger UI (top-right) and paste `Bearer <TOKEN>` (include the word `Bearer`), or provide the `Authorization` header when calling other endpoints. This will let you test protected endpoints (for example `GET /users/{id}` or calculation endpoints that require auth).

- Example curl flow (replace host/port and field names to match your app):

```bash
# register
curl -s -X POST "http://127.0.0.1:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}' | jq

# login -> get token (assumes JSON response with access_token)
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}' | jq -r '.access_token')

# call protected endpoint with Bearer token
curl -s "http://127.0.0.1:8000/users/1" -H "Authorization: Bearer ${TOKEN}" | jq
```

3) If integration tests need a running server

- If a test expects network access to the running app (rather than using an in-process test client), start the server first and then run the specific integration tests:

```bash
# in one terminal
uvicorn main:app --reload

# in another terminal
pytest -q tests/integration
```

If you're unsure which mode the tests use, open `tests/conftest.py` and look for fixtures that create a `TestClient` (in-process) or expect a `SERVER_URL` / live server (external).

