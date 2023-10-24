
class Client:
    def __init__(self,name, surname):
        self.name = name
        self.surname = surname
        self.money = 0
    
    def input_cash(self, cash_to_input):
        self.money = self.money + cash_to_input
    
    def withdraw_cash(self, cash_to_withdraw):
        if self.money - cash_to_withdraw >= 0:
            self.money = self.money - cash_to_withdraw
            return 1
        else:
            print("Error : not enough money in your account")
            return -1
class Bank(Client):
    def __init__(self, name):
        self.name = name
        self.client_list = []
        

    def add_client(self,new_client):
        self.client_list.append(new_client)
        
    
    def money_transfer(self, client_1, client_2, amount):
        if client_1.withdraw_cash(amount):
            client_2.input_cash(amount)
    

    
    
if __name__ == "__main__":

    client_1 = Client("Jan","Kowalski")
    client_2 = Client("Anna","Kowalska")
    bank1 = Bank("Santander")
    bank1.add_client(client_1)
    bank1.add_client(client_2)
    client_1.input_cash(200)
    bank1.money_transfer(client_1,client_2,200)
    print(client_1.money)
    print(client_2.money)
