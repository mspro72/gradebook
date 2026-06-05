.PHONY: compose-up compose-down run test coverage check

compose-up:
	docker compose up -d

compose-down:
	docker compose down

run:
	poetry run python run.py

test:
	poetry run pytest tests/

coverage:
	poetry run pytest tests/ --cov=app --cov-report=term-missing

check: test coverage