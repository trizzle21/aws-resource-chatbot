# Repository Guidelines

## Project Structure & Module Organization
- `api/` holds the Flask application code and entry points (`api/app/`, `api/wsgi.py`, `api/manage.py`).
- `api/app/handlers/` contains AWS resource handlers (SQS, Dynamo, Kinesis).
- `api/app/services/` contains integrations (Twilio, AWS assume-role).
- `api/testing/` contains unit tests and fixtures.
- `api/data/` contains local data assets (SQLite DB, schema, setup script).
- `docker-compose.yml` wires up the API and Redis for local use.

## Build, Test, and Development Commands
- `docker-compose up --build` runs the API container with Redis using `api/Dockerfile`.
- `python3 -m venv virtualenv && source virtualenv/bin/activate` creates a local venv.
- `pip install -r api/requirements/test.txt` installs test dependencies.
- `python -m unittest discover api/testing/` runs the current unit test suite.
- `sqlacodegen sqlite:///data/user.db` generates `api/app/models.py` when DB exists.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation and PEP 8 conventions.
- Use `snake_case` for functions/variables and `CamelCase` for classes.
- Test files follow `test_*.py` naming (see `api/testing/`).
- No formatter or linter is configured; keep changes consistent with existing style.

## Testing Guidelines
- Current tests use `unittest` discovery; `pytest` is listed but not the primary runner.
- New tests should live in `api/testing/` and mirror module names (e.g., `test_sqs.py`).
- All tests must pass before merging (per README).

## Commit & Pull Request Guidelines
- Commit history is informal and often starts with `master:`; keep messages short and descriptive.
- PRs should include a concise summary, test command output, and any required env/config notes.
- If behavior changes, mention affected AWS resource handlers or services.

## Configuration Tips
- `docker-compose.yml` loads environment variables from `.env`; keep secrets out of Git.
- Local Redis is required for the API container; ensure `redis` service is up.
