import sys
sys.path.append('../')

from account_manager import *
from file_manager import get_tickers

def algo(acct_id, trade_volume):
    tickers = get_tickers('../stocks2.txt')
    for ticker in tickers:
        cur.execute(f'SELECT curr_price, last_open FROM Stocks WHERE ticker="{ticker}"')
        stock = cur.fetchone()
        change = stock[0]/stock[1] - 1
        if change > 0.02:
            print(ticker, "| SELL")
            create_sell_order(acct_id, ticker, trade_volume)
        if change < -0.02:
            print(ticker, "| BUY")
            create_buy_order(acct_id, ticker, trade_volume)

def init():
    acct_id = create_new_account("Open to Now (Stock list 2)", 100000)
    print(acct_id)

if __name__ == '__main__':
    algo(3, 100)