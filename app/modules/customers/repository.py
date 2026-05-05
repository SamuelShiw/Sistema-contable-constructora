from sqlalchemy.orm import Session

from app.modules.customers.models import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_all(self) -> list[Customer]:
        return self.db.query(Customer).filter(Customer.is_active.is_(True)).all()

    def get_by_document(self, document_number: str) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.document_number == document_number)
            .first()
        )