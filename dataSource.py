import json
import uuid
import customer
import account
import transaction

customerUniqueID = 111110
accountUniqueNumber = 1000
customersData = []

# this function:
# - Reads customers data from customer_data.txt file
# - Populates Customer Object from Python Data object created after loading file
# - Updates Customer and Account unique IDs with by identifying the max value for each
def loadCustmers():
    loadCustomersData()
    global customersData
    customers = []
    for customerData in customersData:
        customerDataObject = json.loads(customerData)
        newCustomer = customer.Customer(customerDataObject['id'], customerDataObject['name'], customerDataObject['pnr'])
        try:
            for accountDataObject in customerDataObject['accounts']:
                newAccount = account.Account(accountDataObject['type'], accountDataObject['number'], accountDataObject['balance'])
                try:
                    for transactionDataObject in accountDataObject['transactions']:
                        newTransaction = transaction.Transaction(transactionDataObject['transactionId'], transactionDataObject['customerId'], transactionDataObject['accountId'], transactionDataObject['date'], transactionDataObject['amount'])
                        newAccount.addTransactions(newTransaction)
                except KeyError:
                    pass
                newCustomer.addAccount(newAccount)
        except KeyError:
            pass

        customers.append(newCustomer)
    updateCustomerAndAccountUniqueID(customers)
    return customers


# this function:
# - Reads customers data from customer_data.txt file. The file contains data as JSON string
# - Parses JSON string to Python Object using json.load()
def loadCustomersData():
    try:
        with open('customer_data.txt', 'r') as openfile:
            jsonString = openfile.read()
            if jsonString is None or jsonString == '':
                return
            global customersData
            customersData = json.loads(jsonString)
    except FileNotFoundError:
        print("Could not load customer_data.txt")
        return

# this function:
# - Creates Python Data object from Customer Object So it can be further parsed to persist as JSON string
# - Writes new/updated customers data to customer_data.txt file in JSON string format
def updateCustomer(customerObj):
    customerOnlyData = """ "id":"{0}","name":"{1}","pnr":"{2}" """.format(customerObj.id, customerObj.name, customerObj.pnr)
    accountOnlyData = ""
    if len(customerObj.accounts) > 0:
        accountDataKey = ""","accounts": [ """
        accountsData = ""
        for accountObj in customerObj.accounts:
            accountData = """ "type":"{0}","number":"{1}","balance":"{2}" """.format(accountObj.account_type,
                                                                                     accountObj.account_number,
                                                                                     accountObj.balance)
            transactionOnlyData = ""
            if len(accountObj.transactions) > 0:
                transactionDataKey = ""","transactions": [ """
                transactionsData = ""
                for transactionObj in accountObj.transactions:
                    transactionData = """ "transactionId":"{0}","customerId":"{1}","accountId":"{2}","date":"{3}","amount":"{4}" """.format(transactionObj.transaction_id,
                                                                                                 transactionObj.customer_id,
                                                                                                 transactionObj.account_id,
                                                                                                 transactionObj.date,
                                                                                                 transactionObj.amount)
                    transactionData = "{" + transactionData + "},"
                    transactionsData = transactionsData + transactionData
                transactionOnlyData = transactionDataKey + transactionsData[:-1] + "]"

            accountData = "{" + accountData + transactionOnlyData + "},"
            accountsData = accountsData + accountData
        accountOnlyData = accountDataKey + accountsData[:-1] + "]"

    newCustomerData = "{" + customerOnlyData + accountOnlyData + "}"
    updateCustomerData(customerObj, newCustomerData)

# this function:
# - Writes new/updated customers data to customer_data.txt file in JSON string format
# - Validates if change is for existing customer or new customer. Then, update and add respectively
# - Parses Python Object to JSON string using json.dumps()
def updateCustomerData(customerObj, newCustomerData):
    newCustomer = True
    global customersData
    for customerData in customersData:
        customerDataObject = json.loads(customerData)
        if str(customerObj.id) == str(customerDataObject['id']):
            newCustomer = False
            index = customersData.index(customerData)
            customersData[index] = newCustomerData

    if newCustomer:
        customersData.append(newCustomerData)

    customerJson = json.dumps(customersData, indent=4)
    with open("customer_data.txt", "w") as outfile:
        outfile.write(customerJson)

#  To return the unique customer ID after adding +1 in previous customer ID
def getCustomerUniqueID():
    global customerUniqueID
    customerUniqueID = customerUniqueID + 1
    return customerUniqueID

#  To return the unique account ID after adding +1 in previous account ID
def getAccountUniqueNumber():
    global accountUniqueNumber
    accountUniqueNumber = accountUniqueNumber + 1
    return accountUniqueNumber


# - This function updates Customer and Account unique IDs by identifying the max value for each
def updateCustomerAndAccountUniqueID(customers):
    customerIds = []
    accountIds = []
    for customerObj in customers:
        customerIds.append(int(customerObj.id))
        for accountObj in customerObj.accounts:
            accountIds.append(int(accountObj.account_number))

    if len(customerIds) > 0:
        global customerUniqueID
        customerUniqueID = max(customerIds)
    if len(accountIds) > 0:
        global accountUniqueNumber
        accountUniqueNumber = max(accountIds)

#  To create and return the uuid hex value as unique transaction ID
def getTransactionUniqueID():
    return uuid.uuid4().hex