import account
# while creatig an object, attributes customerId, name and pnr will be passsed in the begining. 'account' is an empty list which will later have
# data of different accounts of a customer, which will be added by calling 'addAccount' function. Thus every customer will have info of all of its accounts.
class Customer():
    def __init__(self, customerId, name, pnr):
        self.id = customerId
        self.name= name
        self.pnr= pnr
        self.accounts = []

    def addAccount(self, account):
        self.accounts.append(account)
