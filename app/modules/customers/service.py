from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import CustomerCreate


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def create_customer(self, data: CustomerCreate) -> Customer:
        existing = self.repo.get_by_document(data.document_number)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un cliente con ese documento",
            )

        customer = Customer(**data.model_dump())
        return self.repo.create(customer)

    def list_customers(self) -> list[Customer]:
        return self.repo.get_all()