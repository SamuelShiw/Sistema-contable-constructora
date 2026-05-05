from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import check_database_connection


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend modular para sistema contable de empresa constructora.",
)


app.include_router(api_router)


@app.get("/db-check")
def db_check() -> dict[str, str]:
    if not check_database_connection():
        return {
            "database": "error",
            "message": "No se pudo conectar a PostgreSQL",
        }

    return {
        "database": "connected",
        "message": "Conexión a PostgreSQL exitosa",
    }