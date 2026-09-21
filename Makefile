.PHONY: migrate seed run test
migrate:
	alembic upgrade head
seed:
	curl -s -X POST http://127.0.0.1:$${PORT:-8092}/v1/seed | python3 -m json.tool
run:
	PORT=$${PORT:-8092} python -m orders_app.app
test:
	pytest -q
