# Database

PostgreSQL, run locally with Docker.

## Start it

```
cp .env.example .env        # once, from the repository root
docker compose up -d
```

The first start creates the database and runs every file in `db/migrations/` in name order.

## Useful commands

| Command | What it does |
|---|---|
| `docker compose ps` | Check the database is running and healthy |
| `docker compose exec db psql -U tathya` | Open a SQL prompt |
| `docker compose down` | Stop the database, keeping the data |
| `docker compose down -v` | Stop it and delete all data, so migrations run again on next start |

## Migrations

Files are numbered: `0001_init.sql`, `0002_...sql`. They only run automatically on a fresh database. Until a migration tool is added (tracked in TODO.md), apply a new file to an existing database by hand:

```
docker compose exec -T db psql -U tathya -d tathya < db/migrations/0002_example.sql
```
