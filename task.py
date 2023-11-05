import logging 
import multiprocessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BalanceError(Exception):
    pass

def check_debt(method):
    def wrapper(client,*args,**kwargs):
        money_to_withdraw = args[0]
        if client.money - money_to_withdraw < client.max_debt:
            raise BalanceError('not enough money')
        else:
            return method(client,*args,**kwargs)
    return wrapper

class Client:
    
    max_debt = -200
    
    def __init__(self,name,surname):
        self.name = name
        self.surname = surname
        self.money = 0
        
    
    def input_cash(self, cash_to_input):
        self.money = self.money + cash_to_input
        return self.money
 
    @check_debt
    def withdraw_cash(self, cash_to_withdraw):
        self.money = self.money - cash_to_withdraw
        return self.money
    
    def close_account(self,bank):
        self.money = None
        bank.delete_client(self.name,self.surname)

    def open_account(self,bank):
        self.money = 0
        bank.add_client(self)    

class Bank:
    def __init__(self, name):
        self.name = name
        self.client_list = []
        self.file_path = None
   
    def update_client_file(self,client):
        with open(f'{self.name}.txt', 'a') as file:
            file.write(f'{client.name} {client.surname} \n')  
    
    def add_client(self,new_client):
        self.client_list.append(new_client)
        if self.file_path is not None:
            self.update_client_file(new_client)

    
    @staticmethod
    def money_transfer(client_1,amount,client_2):
        if client_1.withdraw_cash(amount):
            client_2.input_cash(amount)
    
    def create_client_file(self):
        with open(f'{self.name}.txt','w') as file:
            self.file_path = f'{self.name}.txt'
            for client in self.client_list:
                file.write(f'{client.name} {client.surname} \n')
    
    
    def delete_client(self,name,surname):
        found_client = None
        for client in self.client_list:
            if client.name == name and client.surname == surname:
                found_client = client
                break
        if found_client is not None:
            self.client_list.remove(found_client)
        if self.file_path is not None:
            self.create_client_file()  


def Transactions(client_1,transactions,client_2=None,bank=None):
    for transaction in transactions:
        operation,amount = transaction
        if operation == 'input':
            client_1.input_cash(amount)
            logger.info(f'{client_1.name} {client_1.surname} balance: {client_1.money}')
        elif operation == 'withdraw':
            client_1.withdraw_cash(amount)
            logger.info(f'{client_1.name} {client_1.surname} balance: {client_1.money}')
        elif operation == 'transfer':
            bank.money_transfer(client_1,amount,client_2)
            logger.info(f'{client_1.name} {client_1.surname} balance : {client_1.money}')
            logger.info(f'{client_2.name} {client_2.surname} balance : {client_2.money}')

    
if __name__ == "__main__":
    santander = Bank('Santander')
    mbank = Bank("Mbank")
    client_1 = Client('name_1','surname_1')
    client_2 = Client('name_2','surname_2')
    client_3 = Client('name_3','surname_3')
    client_1.open_account(santander)
    client_2.open_account(mbank)
    santander.create_client_file()
    client_3.open_account(santander)

    client_1_transactions = [("input", 100), ("withdraw", 50)]
    client_2_transactions = [("input", 200), ("withdraw", 75)]
    client_3_transactions = [("input", 300), ("withdraw", 100)]
    transfer_transaction  = [("transfer",25),("transfer",15)]

    pool = multiprocessing.Pool()
    pool.apply(Transactions, (client_1, client_1_transactions))
    pool.apply(Transactions, (client_2, client_2_transactions))
    pool.apply(Transactions, (client_3, client_3_transactions))
    pool.apply(Transactions,(client_1,transfer_transaction,client_3,santander))
    pool.close()
    pool.join()
 
    client_2.close_account(mbank)
    mbank.create_client_file()
    client_1.close_account(santander)
    client_3.close_account(santander)
