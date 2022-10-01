from db_builder import db, cur
from stock_manager import get_stock_price
from datetime import datetime

# Returns the amount of shares of a stock held by an account
# Expects: an account id and a stock ticker
# Returns: The number of shares and average price of those shares
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

# Updates the quantity and average price of shares of a stock held by an account
# Expects: an account id, a stock ticker, a quantity of shares, and an average price
def update_current_holding(account, ticker, quantity, avg):
    cur.execute(f'UPDATE Holdings SET quantity = {quantity}, avg_price = {avg} WHERE ticker="{ticker}" AND account_id="{account}"')
    db.commit()

# Gets the current balance of cash available to spend for a given account
# Expects: an account id
# Returns: the cash balance of that account
def get_account_cash(account):
    cur.execute(f'SELECT cash FROM Accounts WHERE account_id="{account}"')
    bal = cur.fetchone()

    if not bal:
        print("This account does not exist")
        return None
    return bal[0]

# Updates the amount of cash available to an account
# Expects: an account id, and a new balance of cash available
def update_account_cash(account, cash):
    cur.execute(f'UPDATE Accounts SET cash = {cash} WHERE account_id="{account}"')
    db.commit()

# Creates a new account with a given starting balance
# Expects: an account name and a starting balance of cash
# Returns: the account id
def create_new_account(account_name, starting_cash):
    cur.execute(f'INSERT INTO Accounts (name, cash) VALUES ("{account_name}", {starting_cash})')
    db.commit()
    return cur.lastrowid

# Attempts to buy shares of a stock in a given quantity for an account
# Expects: an accound id, a stock ticker, and a quantity of shares of the stock
# Returns: True if the transaction occurred,
#          False if the accounts balance is not sufficient to complete the purchase
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

# Attempts to sell shares of a stock in a given quantity for an account
# Expects: an accound id, a stock ticker, and a quantity of shares of the stock
# Returns: True if the transaction occurred,
#          False if the accounts does not hold enough shares of the stock to sell
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

# Creates a "Buy order," which is stored in the orders table of the db. Also calls buy_stock() to also perform the buy action
# Expects: an accound id, a stock ticker, and a quantity of shares of the stock
# Returns: True if the transaction occurred,
#          False if the accounts balance is not sufficient to complete the purchase
def create_buy_order(account, ticker, quantity):
    if not buy_stock(account, ticker, quantity):
        return False
    price = get_stock_price(ticker)
    cur.execute(f'INSERT INTO Orders (executed, account_id, ticker, type, quantity, price) VALUES ("{datetime.now()}", {account}, "{ticker}", "BUY", {quantity}, {price})')
    db.commit()
    return True

# Creates a "Sell order," which is stored in the orders table of the db. Also calls sell_stock() to also perform the buy action
# Expects: an accound id, a stock ticker, and a quantity of shares of the stock
# Returns: True if the transaction occurred,
#          False if the accounts does not hold enough shares of the stock to sell
def create_sell_order(account, ticker, quantity):
    if not sell_stock(account, ticker, quantity):
        return False
    price = get_stock_price(ticker)
    cur.execute(f'INSERT INTO Orders (executed, account_id, ticker, type, quantity, price) VALUES ("{datetime.now()}", {account}, "{ticker}", "SELL", {quantity}, {price})')
    db.commit()
    return True


# Calculates and returns the total worth of an account, including shares held and available cash balance
# Expects: an account id
# Returns: the value of that account
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

# Creates an entry in the account_values table to save historical account value data
# Expects: an account id
def store_account_val(account):
    val = get_account_val(account)
    
    cur.execute(f'INSERT INTO Account_values (date_saved, account_id, value) VALUES ("{datetime.now()}", {account}, {val})')
    db.commit()