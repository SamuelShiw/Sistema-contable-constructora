from fastapi import APIRouter

api_router = APIRouter()


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