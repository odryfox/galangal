from account.daos import AccountDAO


class RegisterAccountService:

    def __init__(
        self,
        account_dao: AccountDAO,
    ) -> None:
        self.account_dao = account_dao

    def execute(self):
        pass
