from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.projects.schemas import ProjectCreate, ProjectResponse
from app.modules.projects.service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("/", response_model=ProjectResponse)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    return ProjectService(db).create_project(payload)


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
) -> list[ProjectResponse]:
    return ProjectService(db).list_projects()