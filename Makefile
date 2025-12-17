.PHONY: up down seed clean

# 1. Start Infrastructure
up:
	@echo "🚀 Starting Kairos Platform..."
	docker-compose -f deploy/docker-compose.yaml up -d

# 2. Stop Infrastructure
down:
	@echo "🛑 Stopping Services..."
	docker-compose -f deploy/docker-compose.yaml down

# 3. Load Data (Requires Python & SQLAlchemy)
seed:
	@echo "🌱 Seeding Database..."
	python scripts/seed_fake_data.py

# 4. View Logs
logs:
	docker-compose -f deploy/docker-compose.yaml logs -f