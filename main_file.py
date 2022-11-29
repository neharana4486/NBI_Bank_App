import bank
import customer
import account
import dataSource

newBank = bank.Bank()
newBank.initializeBank()

print("Welcome to Py_Bank. ")

while True:
    print("****************************************************")
    print("- To add a new customer, press 1")
    print("- To access existing customer: press 2")
    print("- To print list of customers in the Bank, press 3")
    print("- Exit : press 4")
    mainChoice = int(input(""))
    if mainChoice== 1:
        name = input(" Enter name: ")
        pnr = input("Enter personal number: ")

        uniqueCustomerId = dataSource.getCustomerUniqueID()
        result = newBank.add_customer(uniqueCustomerId, name, pnr)
        print(result)
    elif mainChoice== 2:
        pnr = input("Enter personal number: ")
        if not newBank.isCustomerAvaible(pnr):
            print("Customer doesn't exists, -1")
            break

        while True:
            print("****************************************************")
            print("- To change customer name, press 1")
            print("- To remove customer's associated accounts and transactions, press 2")
            print("- To view customer and it's accounts, press 3")
            print("- To add an account, press 4")
            print("- To access existing account, press 5")
            print("- Back, press 6")

            customerChoices= int(input(""))

            if customerChoices == 1:
                customerNewName = input("Enter customer's new name: ")
                result = newBank.changeCustomerName(pnr, customerNewName)
                print(result)

            elif customerChoices == 2:
                result = newBank.removeCustomerAccounts(pnr)
                print(result)

            elif customerChoices== 3:
               exitstingCustomer = newBank.getCustomer(pnr)
               print("Customer NAME: " + exitstingCustomer.name +", Custmer PNR: " + exitstingCustomer.pnr+", Custmer ID: " + str(exitstingCustomer.id))
               for account in exitstingCustomer.accounts:
                   print("Account Number: " + str(account.account_number) + " Account Type: "
                         + account.account_type + " Account Balance: " + str(account.balance))

            elif customerChoices== 4:
                uniqueAccountNumber = dataSource.getAccountUniqueNumber()
                accountType = "Debit Account"
                initialBalance = 0
                result = newBank.add_account(pnr, uniqueAccountNumber, accountType, initialBalance)
                print(result)

            elif customerChoices == 5:
                accountNumber = input("Enter your account number: ")
                while True:
                    print("****************************************************")
                    print("- To delete the account, press 1")
                    print("- To deposit in the account, press 2")
                    print("- To withdraw from the account, press 3")
                    print("- To view account with transactions, press 4")
                    print("- Back, press 5")
                    accountChoice = int(input(""))

                    if accountChoice == 1:
                        result = newBank.removeCustomerAccount(pnr, accountNumber)
                        print(result)

                    elif accountChoice == 2:
                        amount = input("Enter the amount to deposit: ")
                        result = newBank.depositToCustomerAccount(pnr, accountNumber, amount)
                        print(result)

                    elif accountChoice == 3:
                        amount = input("Enter the amount to withdraw: ")
                        result = newBank.withdrawFromCustomerAccount(pnr, accountNumber, amount)
                        print(result)

                    elif accountChoice == 4:
                        existingAccount = newBank.getAccount(newBank.getCustomer(pnr), accountNumber)
                        if existingAccount is not None:
                            print("Account Number: " + str(existingAccount.account_number) + " Account Type: "
                              + existingAccount.account_type + " Account Balance: " + str(existingAccount.balance))
                            for transactionObj in existingAccount.transactions:
                                print("Transaction ID: {}, Customer ID: {}, Account ID: {}, Date: {}, Amount: {}".format(transactionObj.transaction_id, transactionObj.customer_id, transactionObj.account_id, transactionObj.date, transactionObj.amount))

                    elif accountChoice == 5:
                        break

                    else:
                        print("Please enter the right number.")
                        continue
            elif customerChoices == 6:
                break
            else:
                print("Please enter the right number.")
                continue
    elif mainChoice == 3:
        for exitstingCustomer in newBank.customers:
            print("Customer NAME: " + exitstingCustomer.name + ", Custmer PNR: " + exitstingCustomer.pnr + ", Custmer ID: " + str(exitstingCustomer.id))
    elif mainChoice == 4:
        break
    else:
        print("Please enter the right choice.")
        continue
