from db_builder import db, cur

def buy_stock(account, ticker, quantity):
    cur.execute(f'SELECT curr_price FROM Stocks WHERE ticker="{ticker}"')
    price = cur.fetchone()[0]
    try:
        cur.execute(f'SELECT quantity, avg_price FROM Holdings WHERE ticker="{ticker}" AND account_id="{account}"')
        holdings = cur.fetchone()
        curr_quantity = holdings[0]
        curr_avg_price = holdings[1]
    except:
        cur.execute(f'INSERT INTO Holdings (account_id, ticker, quantity, avg_price) VALUES ({account}, "{ticker}", 0, 0)')
        curr_quantity = 0
        curr_avg_price = 0
    new_quantity = curr_quantity + quantity
    total_holdings_price = (curr_quantity * curr_avg_price) + (quantity * price)
    new_avg = total_holdings_price / new_quantity
    cur.execute(f'UPDATE Holdings SET quantity = {new_quantity}, avg_price = {new_avg} WHERE ticker="{ticker}" AND account_id="{account}"')
    db.commit()

