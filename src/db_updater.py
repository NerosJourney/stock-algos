import alpaca_trade_api as api
from db_builder import db
from file_manager import get_tickers, get_key
import json

BASE_URL = 'https://paper-api.alpaca.markets'
API_KEY, API_SECRET = get_key('alpaca.secret')
alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)

def update_current_price(file_name):
    tickers = get_tickers(file_name)
    cur = db.cursor()
    for x in range(len(tickers)):
        data = alpaca.get_snapshot(tickers[x]).minute_bar
        cur.execute(f'UPDATE Stocks SET curr_price = {data.c} WHERE ticker="{tickers[x]}"')
    db.commit()

update_current_price('stocks1.txt')
update_current_price('stocks2.txt')