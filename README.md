# Sistema Contable Constructora

Backend profesional desarrollado con:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Docker
- Clean Architecture

## Estado actual

✅ FASE 1 - Infraestructura base completada

## Endpoints base

- GET /
- GET /health
- GET /db-check

## Ejecución

```bash
docker compose up -d
uvicorn app.main:app --reload