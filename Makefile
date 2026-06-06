.PHONY: help build up down clean serve logs

help:
	@echo "Available commands:"
	@echo "  make build   - Build Docker image"
	@echo "  make up      - Start all containers in background"
	@echo "  make down    - Stop all containers"
	@echo "  make serve   - Build, start and show logs (development)"
	@echo "  make logs    - Show logs"
	@echo "  make clean   - Remove containers and volumes"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

serve: build up logs

logs:
	docker compose logs -f

clean:
	docker compose down -v