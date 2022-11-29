import datetime

import customer
import account
import dataSource
import transaction

class Bank:
    def __init__(self):                           # empty customer list will be populated by calling the function 'add_customer'
        customers = []

    def initializeBank(self):                            # this function will load already existing customers in the file
        self.customers = dataSource.loadCustmers()

    def add_customer(self, customerId, name, pnr):       # this function will check if a customer already exists. if not, then it will
        if self.isCustomerAvaible(pnr):                   # create a new customer and append it to the 'cutomer[]'
            return "Customer already exists, False"
        newCustomer = customer.Customer(customerId, name, pnr)
        self.customers.append(newCustomer)
        dataSource.updateCustomer(newCustomer)
        return "Customer has been created"

    def add_account(self, pnr, accountNumber, accountType, initialBalance):
        if not self.isCustomerAvaible(pnr):
            return "Customer doesn't exists, -1"

        existingCustomer = self.getCustomer(pnr)
        newAccount = account.Account(accountType, accountNumber, initialBalance)
        existingCustomer.addAccount(newAccount)
        dataSource.updateCustomer(existingCustomer)
        return "Created account number: " + str(newAccount.account_number)

    def changeCustomerName(self, pnr, customerNewName):
        existingCustomer = self.getCustomer(pnr)
        existingCustomer.name = customerNewName
        dataSource.updateCustomer(existingCustomer)
        return "Customer name has been updated"

    def removeCustomerAccounts(self, pnr):
        existingCustomer = self.getCustomer(pnr)
        existingCustomer.accounts.clear()
        dataSource.updateCustomer(existingCustomer)
        return "Customer's associated accounts and transactions has been removed"

    def removeCustomerAccount(self, pnr, accountNumber):
        existingCustomer = self.getCustomer(pnr)

        if not self.isAccountAvaible(existingCustomer, accountNumber):
            return "Account doesn't exists, -1"

        existingAccount = self.getAccount(existingCustomer, accountNumber)
        existingCustomer.accounts.remove(existingAccount)
        dataSource.updateCustomer(existingCustomer)
        return "Account has been removed for Account ID: " + str(accountNumber)


    def depositToCustomerAccount(self, pnr, accountNumber, amount):
        existingCustomer = self.getCustomer(pnr)

        if not self.isAccountAvaible(existingCustomer, accountNumber):
            return "Account doesn't exists, -1"
        existingAccount = self.getAccount(existingCustomer, accountNumber)

        newTransaction = transaction.Transaction(dataSource.getTransactionUniqueID(), str(existingCustomer.id), existingAccount.account_number, datetime.datetime.now(), amount)
        existingAccount.balance = int(existingAccount.balance) + int(amount)
        existingAccount.addTransactions(newTransaction)
        dataSource.updateCustomer(existingCustomer)
        return "The amount of {} Rs has been deposited, available balance is {}".format(amount, existingAccount.balance)

    def withdrawFromCustomerAccount(self, pnr, accountNumber, amount):
        existingCustomer = self.getCustomer(pnr)

        if not self.isAccountAvaible(existingCustomer, accountNumber):
            return "Account doesn't exists, -1"
        existingAccount = self.getAccount(existingCustomer, accountNumber)

        newTransaction = transaction.Transaction(dataSource.getTransactionUniqueID(), str(existingCustomer.id), str(existingAccount.account_number), datetime.datetime.now(), -abs(int(amount)))
        existingAccount.balance = int(existingAccount.balance) - int(amount)
        existingAccount.addTransactions(newTransaction)
        dataSource.updateCustomer(existingCustomer)
        return "The amount of {} Rs has been withdrawn, available balance is {}".format(amount, existingAccount.balance)

    def isCustomerAvaible(self, pnr):
        for existingCustomer in self.customers:
            if existingCustomer.pnr == pnr:
                return True
        return False

    def getCustomer(self, pnr):
        for existingCustomer in self.customers:
            if existingCustomer.pnr == pnr:
                return existingCustomer
        return None

    def isAccountAvaible(self, existingCustomer, accountNumber):
        for existingAccount in existingCustomer.accounts:
            if str(existingAccount.account_number) == accountNumber:
                return True
        return False

    def getAccount(self, existingCustomer, accountNumber):
        for existingAccount in existingCustomer.accounts:
            if str(existingAccount.account_number) == accountNumber:
                return existingAccount
        return None