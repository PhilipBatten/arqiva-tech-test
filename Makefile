.PHONY: run stop clean

# Variables
VALUE ?= dynamic string

help:
	@echo "Available commands:"
	@echo "  make run      - Start the application"
	@echo "  make stop     - Stop all containers"
	@echo "  make clean    - Remove all containers and volumes"

run:
	@echo "Building and starting application and LocalStack..."
	docker compose build
	docker compose up -d
	@echo "Waiting for services to be ready..."

stop:
	@echo "Stopping services..."
	docker compose down

clean: stop
	@echo "Cleaning up..."
	docker compose down -v
	rm -rf ./volume
