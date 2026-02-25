.PHONY: setup-backend setup-frontend dev-backend dev-frontend dev

setup-backend:
	cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt
	@echo "Copiez backend/.env.example vers backend/.env et remplissez ANTHROPIC_API_KEY et SECRET_KEY"

setup-frontend:
	cd frontend && npm install

setup: setup-backend setup-frontend

dev-backend:
	cd backend && .venv/bin/uvicorn main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# Lancer backend et frontend dans des terminaux séparés (macOS)
dev:
	@echo "Ouvrez deux terminaux et lancez :"
	@echo "  Terminal 1 : make dev-backend"
	@echo "  Terminal 2 : make dev-frontend"
