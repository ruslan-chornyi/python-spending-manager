# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A personal expense tracker with three front-ends (Telegram bot, FastAPI REST API, CLI) that all share one SQLAlchemy/PostgreSQL data layer. It is a learning project: the owner writes the code, so act as a mentor. Give hints and explain the reasoning first, and write full solutions only when asked.

## Commands

```bash
docker compose up --build        # PostgreSQL + Telegram bot (bot is the only app service in Compose)
docker compose up db             # database only, for running the API/CLI on the host
uvicorn api:app --reload         # REST API, docs at http://127.0.0.1:8000/docs
python bot.py                    # bot outside Docker
python main.py                   # CLI
python -c "from app.storage import init_db; init_db()"   # create tables (nothing calls init_db automatically)
```

There are no tests, linter config, or migration tool yet. pytest is on the roadmap.

`.env` holds the real bot token. Never read it (it is denied in `.claude/settings.json`). Use `.env.example` for the variable format. Its `DATABASE_URL` uses host `db`, which only resolves inside Compose. A process running on the host needs `localhost:5432` instead.

## Architecture

- `app/db.py`: engine, `SessionLocal`, `Base`. Sessions use `expire_on_commit=False`, which lets ORM objects be returned and read after the `with SessionLocal()` block closes. `api.py` relies on this when it returns `new_expense` after `save_expense`.
- `app/storage.py`: the only place that touches the DB. Every function opens its own short-lived **sync** session, and the async bot and async API handlers call it directly. `save_expense` lowercases `category`, and all category filtering assumes lowercase.
- `app/models.py`: `Expense` (UUID string PK, `user_id` BigInteger = Telegram user id) and `Apikey` (stores only a SHA-256 `key_hash`).
- Schema changes: there is no Alembic. `Base.metadata.create_all` creates missing tables but never alters existing ones.

### Per-interface user identity

- **Bot** (`bot.py`, aiogram 3, `MemoryStorage` FSM): identity is `message.from_user.id`. The multi-step dialogs use the states in `app/states.py`. Every state handler cancels when the input starts with `/`. `/delete` stores the user's own expense ids in FSM data and maps the chosen number to an id.
- **API** (`api.py`): identity comes from the `X-API-Key` header via the `get_current_user` dependency (key → hash → `api_keys.user_id`). The README's `?user_id=` endpoints are outdated. `create_api_key(user_id)` exists in storage but has no endpoint or caller yet, so keys are created manually.
- **CLI** (`main.py`): writes with `user_id=0`, but reads via `load_expense()`, which returns **all** users' expenses.

### Misc

- `scripts/migrate.py` was a one-off import of the legacy `data/expenses.txt`. It opens a relative `../data/...` path.
- The Dockerfile uses `python:3.12-slim`, but the README says Python 3.13. `requirements.txt` is unpinned.
