from sqlalchemy.orm import Session

from app.modules.projects.models import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all(self) -> list[Project]:
        return self.db.query(Project).all()

    def get_by_code(self, code: str) -> Project | None:
        return self.db.query(Project).filter(Project.code == code).first()