from db_builder import db, cur
from stock_manager import get_stock_price
from datetime import datetime

def get_current_holding(account, ticker):
    try:
        cur.execute(f'SELECT quantity, avg_price FROM Holdings WHERE ticker="{ticker}" AND account_id="{account}"')
        holdings = cur.fetchone()
        curr_quantity = holdings[0]
        curr_avg_price = holdings[1]
    except:
        cur.execute(f'INSERT INTO Holdings (account_id, ticker, quantity, avg_price) VALUES ({account}, "{ticker}", 0, 0)')
        curr_quantity = 0
        curr_avg_price = 0
        db.commit()
    return curr_quantity, curr_avg_price


def update_current_holding(account, ticker, quantity, avg):
    cur.execute(f'UPDATE Holdings SET quantity = {quantity}, avg_price = {avg} WHERE ticker="{ticker}" AND account_id="{account}"')
    db.commit()


def get_account_cash(account):
    cur.execute(f'SELECT cash FROM Accounts WHERE account_id="{account}"')
    bal = cur.fetchone()

    if not bal:
        print("This account does not exist")
        return None
    return bal[0]

def update_account_cash(account, cash):
    cur.execute(f'UPDATE Accounts SET cash = {cash} WHERE account_id="{account}"')
    db.commit()

def create_new_account(account_name, starting_cash):
    cur.execute(f'INSERT INTO Accounts (name, cash) VALUES ("{account_name}", {starting_cash})')
    db.commit()
    return cur.lastrowid

def buy_stock(account, ticker, quantity):
    price = get_stock_price(ticker)

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

    price = get_stock_price(ticker)
    
    new_quantity = curr_quantity - quantity
    update_current_holding(account, ticker, new_quantity, avg)

    curr_bal = get_account_cash(account)
    update_account_cash(account, curr_bal + (quantity * price))
    return True


def create_buy_order(account, ticker, quantity):
    if not buy_stock(account, ticker, quantity):
        return False
    price = get_stock_price(ticker)
    cur.execute(f'INSERT INTO Orders (executed, account_id, ticker, type, quantity, price) VALUES ("{datetime.now()}", {account}, "{ticker}", "BUY", {quantity}, {price})')
    db.commit()

def create_sell_order(account, ticker, quantity):
    if not sell_stock(account, ticker, quantity):
        return False
    price = get_stock_price(ticker)
    cur.execute(f'INSERT INTO Orders (executed, account_id, ticker, type, quantity, price) VALUES ("{datetime.now()}", {account}, "{ticker}", "SELL", {quantity}, {price})')
    db.commit()


def get_account_val(account):
    cur.execute(f'SELECT ticker, quantity FROM Holdings WHERE account_id={account}')
    holdings = cur.fetchall()

    account_value = 0

    for row in holdings:
        ticker = row[0]
        quantity = row[1]
        price = get_stock_price(ticker)
        account_value += quantity * price

    account_value += get_account_cash(account)

    return account_value


def store_account_val(account):
    val = get_account_val(account)
    
    cur.execute(f'INSERT INTO Account_values (date_saved, account_id, value) VALUES ("{datetime.now()}", {account}, {val})')
    db.commit()


if __name__ == "__main__":
    store_account_val(1)