SERVICES = auth user vacancy search

# === Development ===

dev:  ## Start all services
	docker compose up -d

dev-infra:  ## Start infrastructure only (DB, RabbitMQ, Kafka)
	docker compose up -d ccheck.db ccheck.rabbitmq ccheck.kafka

dev-%:  ## Start a specific service (e.g. dev-auth, dev-user)
	docker compose up -d ccheck.$*.web

stop:  ## Stop all services
	docker compose stop

stop-infra:  ## Stop infrastructure only
	docker compose stop ccheck.db ccheck.rabbitmq ccheck.kafka

stop-%:  ## Stop a specific service (e.g. stop-auth, stop-user)
	docker compose stop ccheck.$*.web

# === Env ===

env-init:  ## Create .env files from templates
	@for f in enviroment/*.env.template; do \
		name="$$(basename "$$f" .env.template)"; \
		cp -n "$$f" "enviroment/.$$name.env" && echo "Created enviroment/.$$name.env" || echo "Skipped enviroment/.$$name.env (exists)"; \
	done
	@for f in backend/*/env.template; do \
		dir="$$(dirname "$$f")"; \
		cp -n "$$f" "$$dir/.env" && echo "Created $$dir/.env" || echo "Skipped $$dir/.env (exists)"; \
	done

# === Build ===

build:  ## Build all Docker images
	docker compose build

build-auth:  ## Build auth Docker image
	docker compose build ccheck.auth.web

build-user:  ## Build user Docker image
	docker compose build ccheck.user.web

build-vacancy:  ## Build vacancy Docker image
	docker compose build ccheck.vacancy.web

build-search:  ## Build search Docker image
	docker compose build ccheck.search.web

build-frontend:  ## Build frontend Docker image
	docker compose build ccheck.frontend.web

# === Utility ===

logs:  ## Tail logs from all services
	docker compose logs -f

ps:  ## List running services
	docker compose ps

down:  ## Stop all services
	docker compose down

clean: clean-docker clean-python  ## Clean everything

clean-docker:  ## Remove Docker containers and volumes
	docker compose down -v

clean-python:  ## Clean Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
