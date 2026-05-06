from app.modules.accounts_payable.models import AccountPayable
from app.modules.accounts_payable.repository import AccountPayableRepository


class AccountPayableService:
    def __init__(self, repo: AccountPayableRepository):
        self.repo = repo

    def list_accounts_payable(self) -> list[AccountPayable]:
        return self.repo.get_all()