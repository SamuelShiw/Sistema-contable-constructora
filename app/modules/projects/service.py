from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.projects.models import Project
from app.modules.projects.repository import ProjectRepository
from app.modules.projects.schemas import ProjectCreate


VALID_PROJECT_STATUSES = {
    "PLANNED",
    "IN_PROGRESS",
    "PAUSED",
    "FINISHED",
    "CANCELLED",
}


class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def create_project(self, data: ProjectCreate) -> Project:
        if data.status not in VALID_PROJECT_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado de proyecto inválido",
            )

        if data.start_date and data.end_date and data.start_date > data.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser mayor a la fecha final",
            )

        existing = self.repo.get_by_code(data.code)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un proyecto con ese código",
            )

        project = Project(**data.model_dump())
        return self.repo.create(project)

    def list_projects(self) -> list[Project]:
        return self.repo.get_all()