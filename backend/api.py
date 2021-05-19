#imports
from flask import Flask, request
import json
import datetime

app = Flask(__name__)   #declare flask app

user_list = {}  #user dictionary key = name, value = User object

@app.route('/transaction')
def make_transaction():

    #get transaction info
    payer = request.args.get('payer')
    points = request.args.get('points')
    timestamp = request.args.get('timestamp')


    #format points to integer
    try:    
        points = int(points)                                                    
    except:
        return "invalid. points value is not int" , 400


    #check if payer in dict (add if not) and for first positive transaction
    if payer not in user_list:
        if points >= 0 :
            user_list[payer] = User(payer)
        else:
            return "invalid. first transaction on account must be positive" , 400


    #update balance, return error if accnt would go negative
    if not user_list[payer].update_balance(points):
        return "invalid. transaction would result in negative balance" , 400
    

    user_list[payer].add_transaction(timestamp, points)     #add transaction to record


    return "successful transaction" , 200


@app.route('/balance')
def balance():
    balance_return = {}

    #create dictionary of payer name (key) and current balance (value)
    for _,value in user_list.items():
        balance_return[value.name]  = value.balance

    return json.dumps(balance_return) , 200     #return as json


@app.route('/spend')
def spend():
    amount = request.args.get('points') #get spend amount

    #convert amount to int
    try:
        amount = int(amount)
    except:
        return "invalid. points amnt not int", 400

    #check if there are enough points to spend
    total_points = get_total_points()
    if total_points < amount:
        return "invalid. not enough points available for spend" , 400


    spending_dict = {} # key: payer name, value: amount spent

    #spending loop
    while amount != 0:
        transaction = get_oldest_transaction()
        if not transaction:         #see if is an oldest transaction
            return 'error.no transactions' , 400

        #transaction of form [name, [timestamp, amount]]
        name = transaction[0]
        points = transaction[1][1]

        #check if amount is fully covered
        if points < amount:
            points_spent = points   
        else:
            points_spent = amount  
        

        #update spending dictionary with payer and new points spent
        if name in spending_dict:
            spending_dict[name] -= points_spent
        else:
            spending_dict[name] = points_spent*-1
        
        #adjust remaining spend value
        amount -= points_spent

    #update balances and convert to json format
    return_jsons = []
    for name in spending_dict:
        user_list[name].update_balance(spending_dict[name])
        return_jsons.append({'payer' : name, 'points' : spending_dict[name]})




    return json.dumps(return_jsons) , 200

def get_total_points():
    """Gets total points in system
    Args:
    None

    Returns:
    total: total number of avaailable points
    """
    total = 0
    for _,value in user_list.items():
        for val in value.transactions:
            total += val[1]
    return total

def get_oldest_transaction():
    """Finds oldest transaction among all payers
    Args:
    None

    Returns:
    oldest_transaction: [payer (str), [timestamp (str), amount (int)]]
    False: no available transactions to get points from 
    """
    transactions = {}
    for _, value in user_list.items():
        try:
            transactions[value.name] = value.transactions[0]      #first transaction in list is oldest bc sorted
        except:
            continue
    
    if len(transactions) == 0:      
        return False    #no transactions available
    
    oldest_transaction = min(transactions.items(), key=lambda x: x[1][0])   #min of oldest transaction from each user
    user_list[oldest_transaction[0]].remove_transaction(oldest_transaction[1][0], oldest_transaction[1][1]) 
    return oldest_transaction

class User:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = list()
    
    def update_balance(self, amount):
        """Updates balance field.
        Args:
        amount: amount to be added or subtracted from balance

        Returns:
        True: successful balance update
        False: update would result in negative balance
        """
        if self.balance + amount < 0:
            return False

        self.balance += amount
        return True

    def get_balance(self):
        return self.balance

    def add_transaction(self, timestamp, amount):
        """Adds transaction to transaction field and sorts by date in-place.
        Args:
        amount: amount of points associated w transaction

        Returns:
        None
        """

        self.transactions.append([timestamp, amount])
        self.transactions.sort(key = lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ'))

    def remove_transaction(self, timestamp, amount):
        """Removes transaction. Adds back same transaction if amount is less than
            points already associated with passed transaction
        Args:
        timestamp: timestamp of transaction to be removed
        amount: amount of points to be taken from transaction

        Returns:
        None
        """

        elem = self.transactions.pop(0)

        #add same timestamp if only partial is taken from balance
        if elem[1] > amount:
            new_value = elem[1] - amount
            self.add_transaction(timestamp, new_value)
            
    
