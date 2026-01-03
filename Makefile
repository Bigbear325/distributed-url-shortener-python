.PHONY: up down db logs frontend

up: db
	@echo "Starting application..."
	@echo "Please open a new terminal for frontend:"
	@echo "  make frontend"
	@echo "Backend is running in Docker."

db:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

frontend:
	cd frontend && npm install && npm run dev
