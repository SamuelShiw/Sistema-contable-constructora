from sqlalchemy.orm import Session

from app.modules.treasury.models import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_all(self) -> list[Payment]:
        return (
            self.db.query(Payment)
            .order_by(Payment.payment_date.desc())
            .all()
        )