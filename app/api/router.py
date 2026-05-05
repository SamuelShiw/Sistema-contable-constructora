from fastapi import APIRouter

from app.modules.auth.router import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)


@api_router.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Sistema Contable Constructora running",
        "status": "ok",
    }


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }