from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.accounts_payable.repository import AccountPayableRepository
from app.modules.treasury.models import Payment
from app.modules.treasury.repository import PaymentRepository
from app.modules.treasury.schemas import PaymentCreate


class PaymentService:
    def __init__(self, db: Session):
        self.payment_repo = PaymentRepository(db)
        self.account_payable_repo = AccountPayableRepository(db)

    def create_payment(self, data: PaymentCreate) -> Payment:
        account_payable = self.account_payable_repo.get_by_id(data.account_payable_id)

        if account_payable is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por pagar no encontrada",
            )

        if account_payable.status in {"PAID", "CANCELLED"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cuenta por pagar no permite pagos",
            )

        if data.amount > account_payable.balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El monto del pago no puede superar el saldo pendiente",
            )

        payment = Payment(
            company_id=account_payable.company_id,
            supplier_id=account_payable.supplier_id,
            account_payable_id=account_payable.id,
            payment_date=data.payment_date,
            payment_method=data.payment_method,
            amount=data.amount,
            reference=data.reference,
            status="CONFIRMED",
        )

        account_payable.balance -= data.amount

        if account_payable.balance == 0:
            account_payable.status = "PAID"
        else:
            account_payable.status = "PARTIAL"

        self.account_payable_repo.save(account_payable)

        return self.payment_repo.create(payment)

    def list_payments(self) -> list[Payment]:
        return self.payment_repo.get_all()