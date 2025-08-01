# LLM Server Monitoring System Makefile

.PHONY: help start stop restart logs clean test build dev mock setup

# Default target
help:
	@echo "LLM Monitor - Available commands:"
	@echo "  make start       - Start monitoring stack"
	@echo "  make stop        - Stop monitoring stack"
	@echo "  make restart     - Restart monitoring stack"
	@echo "  make dev         - Start in development mode"
	@echo "  make mock        - Start with mock data"
	@echo "  make logs        - View all service logs"
	@echo "  make clean       - Stop and remove all data"
	@echo "  make test        - Run all tests"
	@echo "  make build       - Build all Docker images"
	@echo "  make setup       - Initial setup (create .env)"

# Setup environment
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please review and update as needed."; \
	else \
		echo ".env file already exists."; \
	fi

# Start services
start: setup
	docker compose -f docker/docker-compose.yml up -d
	@echo "Services started. Access Grafana at http://localhost:23000"

# Stop services
stop:
	docker compose -f docker/docker-compose.yml down

# Restart services
restart: stop start

# Start in development mode
dev: setup
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up

# Start with mock data
mock: setup
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.mock.yml up

# View logs
logs:
	docker compose -f docker/docker-compose.yml logs -f

# Specific service logs
logs-%:
	docker compose -f docker/docker-compose.yml logs -f $*

# Clean everything (including volumes)
clean:
	docker compose -f docker/docker-compose.yml down -v
	@echo "All services stopped and data volumes removed."

# Build Docker images
build:
	docker compose -f docker/docker-compose.yml build

# Run tests
test:
	@echo "Running unit tests..."
	@if [ -d "tests/unit" ]; then \
		pytest tests/unit/; \
	else \
		echo "No unit tests found."; \
	fi

# Run specific test suites
test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-e2e:
	pytest tests/e2e/

# Check service health
health:
	@echo "Checking service health..."
	@docker compose -f docker/docker-compose.yml ps
	@echo ""
	@echo "Prometheus health:"
	@curl -s http://localhost:23001/-/healthy || echo "Prometheus not healthy"
	@echo ""
	@echo "Grafana health:"
	@curl -s http://localhost:23000/api/health || echo "Grafana not healthy"
	@echo ""
	@echo "Loki health:"
	@curl -s http://localhost:23002/ready || echo "Loki not healthy"

# Development shortcuts
shell-%:
	docker compose -f docker/docker-compose.yml exec $* /bin/sh

# Backup dashboards
backup-dashboards:
	@mkdir -p backups/dashboards
	@echo "Backing up Grafana dashboards..."
	@docker compose -f docker/docker-compose.yml exec grafana \
		curl -s http://localhost:3000/api/search | \
		jq -r '.[] | .uid' | \
		xargs -I {} docker compose exec grafana \
		curl -s http://localhost:3000/api/dashboards/uid/{} > backups/dashboards/{}.json
	@echo "Dashboards backed up to backups/dashboards/"

# Validate configuration
validate:
	@echo "Validating Docker Compose configuration..."
	@docker compose -f docker/docker-compose.yml config > /dev/null
	@echo "✓ docker-compose.yml is valid"
	@docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml config > /dev/null
	@echo "✓ docker-compose.dev.yml is valid"
	@docker compose -f docker/docker-compose.yml -f docker/docker-compose.mock.yml config > /dev/null
	@echo "✓ docker-compose.mock.yml is valid"