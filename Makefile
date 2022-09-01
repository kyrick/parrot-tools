

lint:
	poetry run isort --check-only parrot_tools tests
	poetry run black --check parrot_tools tests
	poetry run flake8 parrot_tools tests
	poetry run mypy parrot_tools

test:
	poetry run pytest tests -s -v --tb=native --cov=parrot_tools --cov-report=term-missing --cov-report=html
