from io import BytesIO

from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.modules.accounts_payable.models import AccountPayable
from app.modules.dashboard.service import DashboardService
from app.modules.purchases.models import Purchase


class ExportService:
    def __init__(self, db: Session):
        self.db = db

    def export_purchases_excel(self) -> BytesIO:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Purchases"

        sheet.append(
            [
                "ID",
                "Documento",
                "Proveedor ID",
                "Total",
                "Estado",
                "Fecha",
            ]
        )

        purchases = (
            self.db.query(Purchase)
            .order_by(Purchase.created_at.desc())
            .all()
        )

        for purchase in purchases:
            sheet.append(
                [
                    purchase.id,
                    purchase.document_number,
                    purchase.supplier_id,
                    float(purchase.total),
                    purchase.status,
                    str(purchase.issue_date),
                ]
            )

        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)

        return stream

    def export_accounts_payable_excel(self) -> BytesIO:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Accounts Payable"

        sheet.append(
            [
                "ID",
                "Proveedor ID",
                "Monto",
                "Saldo",
                "Estado",
                "Vencimiento",
            ]
        )

        accounts = (
            self.db.query(AccountPayable)
            .order_by(AccountPayable.created_at.desc())
            .all()
        )

        for account in accounts:
            sheet.append(
                [
                    account.id,
                    account.supplier_id,
                    float(account.amount),
                    float(account.balance),
                    account.status,
                    str(account.due_date),
                ]
            )

        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)

        return stream

    def export_dashboard_pdf(self) -> BytesIO:
        summary = DashboardService(self.db).get_summary()

        stream = BytesIO()
        pdf = canvas.Canvas(stream, pagesize=letter)

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(50, 750, "Dashboard Financiero")

        pdf.setFont("Helvetica", 12)

        y = 700

        lines = [
            f"Total Compras: {summary['total_purchases']}",
            f"Total Cuentas por Pagar: {summary['total_accounts_payable']}",
            f"Total Pagado: {summary['total_paid']}",
            f"Saldo Pendiente: {summary['pending_balance']}",
            f"Proyectos Activos: {summary['active_projects']}",
            f"Periodos Abiertos: {summary['open_periods']}",
        ]

        for line in lines:
            pdf.drawString(50, y, line)
            y -= 30

        pdf.save()
        stream.seek(0)

        return stream