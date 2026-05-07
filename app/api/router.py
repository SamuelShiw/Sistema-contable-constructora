from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.companies.router import router as companies_router
from app.modules.accounting_periods.router import router as accounting_periods_router
from app.modules.customers.router import router as customers_router
from app.modules.suppliers.router import router as suppliers_router
from app.modules.projects.router import router as projects_router
from app.modules.cost_centers.router import router as cost_centers_router
from app.modules.chart_accounts.router import router as chart_accounts_router
from app.modules.journal_entries.router import router as journal_entries_router
from app.modules.purchases.router import router as purchases_router
from app.modules.accounts_payable.router import router as accounts_payable_router
from app.modules.treasury.router import router as payments_router
from app.modules.audit.router import router as audit_router
from app.modules.reports.router import router as reports_router
from app.modules.dashboard.router import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(companies_router)
api_router.include_router(accounting_periods_router)
api_router.include_router(customers_router)
api_router.include_router(suppliers_router)
api_router.include_router(projects_router)
api_router.include_router(cost_centers_router)
api_router.include_router(chart_accounts_router)
api_router.include_router(journal_entries_router)
api_router.include_router(purchases_router)
api_router.include_router(accounts_payable_router)
api_router.include_router(payments_router)
api_router.include_router(audit_router)
api_router.include_router(reports_router)
api_router.include_router(dashboard_router)


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