from asyncio.windows_events import NULL
from db_builder import db, cur
from account_manager import *

def buy_stock(account, ticker, quantity):
    cur.execute(f'SELECT curr_price FROM Stocks WHERE ticker="{ticker}"')
    price = cur.fetchone()[0]

    acc_bal = get_account_cash(account)

    if(quantity * price > acc_bal):
        print("Not enough money :(")
        return False

    curr_quantity, curr_avg_price = get_current_holding(account, ticker)
    new_quantity = curr_quantity + quantity

    total_holdings_price = (curr_quantity * curr_avg_price) + (quantity * price)
    new_avg = total_holdings_price / new_quantity

    update_current_holding(account, ticker, new_quantity, new_avg)
    update_account_cash(account, acc_bal - (quantity * price))
    return True


def sell_stock(account, ticker, quantity):
    curr_quantity, avg = get_current_holding(account, ticker)
    if(quantity > curr_quantity):
        print("ERROR! YOU DON'T OWN THAT STOCK")
        return False

    cur.execute(f'SELECT curr_price FROM Stocks WHERE ticker="{ticker}"')
    price = cur.fetchone()[0]
    
    new_quantity = curr_quantity - quantity
    update_current_holding(account, ticker, new_quantity, avg)

    curr_bal = get_account_cash(account)
    update_account_cash(account, curr_bal + (quantity * price))
    return True


def create_buy_order(account, ticker, quantity):
    #TODO Implement
    pass

def create_sell_order(account, ticker, quantity):
    #TODO Implement
    pass