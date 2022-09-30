from db_builder import db, cur

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