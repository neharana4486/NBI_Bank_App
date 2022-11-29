class Account:
    def __init__(self, account_type, account_number, balance): # Account class has attributes account_type, account_number, balance. The 'transactions' is empty list,
        self.account_type= account_type                        # which is populated by calling 'addTransactions' function.
        self.account_number= account_number                    
        self.balance= balance                                  
        self.transactions = []

    def addTransactions(self, transactioin):
        self.transactions.append(transactioin)
