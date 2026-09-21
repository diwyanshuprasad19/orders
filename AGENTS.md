# Agent / AI coding guide

Use this file so code written here stays consistent and **human**, not AI-slop.

Implementation / bugfix / meaningful refactor work follows the **autonomous
production-engineering workflow** in `.cursor/rules/autonomous-engineering.mdc`
and `.cursor/agents/`.

## Principles
- Match existing project structure and naming; do not invent parallel frameworks.
- Prefer small, reviewable diffs; one concern per PR.
- Never commit secrets (`.env`, keys, tokens). Use examples only.
- Add or update tests when changing behavior.
- Document operator-facing changes in README or PR body.

## Anti-slop (enforced by `make anti-slop` / `make auto`)
See `ANTI_SLOP.md`. Tools: **aislop** (≥80), **sloplint**, **agent-slop-lint**, **ruff**.

## Before finishing a task
1. `make -C ../platform-ops local-gate REPO=orders`
2. `make -C ../platform-ops anti-slop REPO=orders`
3. Summarize risk (auth, data, deploy) in the PR.

## Stack awareness (orders)
- FastAPI orders service (:8092), Postgres + Alembic, circuit breaker → inventory
- Domain: customers, orders, payments, shipments, refunds, order events
- Seed: POST /v1/seed; set INVENTORY_URL=http://127.0.0.1:8091

## Data locally
- Postgres DBs: `inventory_db` / `orders_db` (or shared platform-ops data stack).
- Migrations: `alembic upgrade head` in-repo.
