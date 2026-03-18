.PHONY: run migrate seed setup clean

run:
	uvicorn src.main:app --reload --port 8000

migrate:
	python -m src.infrastructure.database.migrate

seed:
	python -m src.infrastructure.database.migrate --seed

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	cp -n .env.example .env || true
	@echo "Setup complete. Activate venv with: source .venv/bin/activate"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
