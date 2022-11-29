class Transaction():
    def __init__(self, transaction_id, customer_id, account_id, date, amount):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.account_id = account_id
        self.date = date
        self.amount = amount