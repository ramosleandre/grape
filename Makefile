.PHONY: help up down build logs shell-web shell-api test-web test-api lint-web lint-api clean install

# Default target
help:
	@echo "Grape Development Commands"
	@echo "=========================="
	@echo "make up          - Start all services"
	@echo "make down        - Stop all services"
	@echo "make build       - Build all containers"
	@echo "make logs        - View logs from all services"
	@echo "make shell-web   - Open shell in web container"
	@echo "make shell-api   - Open shell in api container"
	@echo "make test-web    - Run frontend tests"
	@echo "make test-api    - Run backend tests"
	@echo "make lint-web    - Lint frontend code"
	@echo "make lint-api    - Lint backend code"
	@echo "make clean       - Remove containers, volumes, and build artifacts"
	@echo "make install     - Install dependencies locally (outside Docker)"

# Start services
up:
	docker-compose up -d
	@echo "✓ Services started. Frontend: http://localhost:3000, Backend: http://localhost:8000"

# Stop services
down:
	docker-compose down

# Build all containers
build:
	docker-compose build

# View logs
logs:
	docker-compose logs -f

# Shell access
shell-web:
	docker-compose exec web sh

shell-api:
	docker-compose exec api bash

# Run tests
test-web:
	docker-compose exec web npm run test

test-api:
	docker-compose exec api uv run pytest tests/ -v

# Linting
lint-web:
	docker-compose exec web npm run lint
	docker-compose exec web npm run format

lint-api:
	docker-compose exec api ruff check . --fix
	docker-compose exec api black .
	docker-compose exec api ruff format .

# Clean up
clean:
	docker-compose down -v --remove-orphans
	rm -rf apps/web/.next apps/web/node_modules
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✓ Cleaned up Docker containers, volumes, and build artifacts"

# Local installation (optional - for IDE support)
install:
	cd apps/web && npm install
	cd apps/backend && uv venv && uv pip install -r requirements.txt
	@echo "✓ Dependencies installed locally"
