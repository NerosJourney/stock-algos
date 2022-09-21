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
        curr_quantity = 0
        curr_avg_price = 0
    print(price, curr_quantity, curr_avg_price)

buy_stock(1, 'AAPL', 1)