from db_builder import db, cur
import alpaca_trade_api as api
from file_manager import get_tickers, get_key

BASE_URL = 'https://paper-api.alpaca.markets'
API_KEY, API_SECRET = get_key('alpaca.secret')
alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)

# Using the alpaca API, updates the current value of a set of stocks in the database
# Expects: a string file_name, which has a ticker on each line of the file and is stored
#          in this directory
def update_current_price(file_name):
    tickers = get_tickers(file_name)
    cur = db.cursor()
    for x in range(len(tickers)):
        data = alpaca.get_snapshot(tickers[x]).minute_bar
        cur.execute(f'UPDATE Stocks SET curr_price = {data.c} WHERE ticker="{tickers[x]}"')
    db.commit()

# Using the alpaca API, updates the last open value of a set of stocks in the database
# Expects: a string file_name, which has a ticker on each line of the file and is stored
#          in this directory
def update_last_open(file_name):
    tickers = get_tickers(file_name)
    cur = db.cursor()
    for x in range(len(tickers)):
        data = alpaca.get_snapshot(tickers[x]).daily_bar
        cur.execute(f'UPDATE Stocks SET last_open = {data.o} WHERE ticker="{tickers[x]}"')
    db.commit()

# Using the alpaca API, updates the last close value of a set of stocks in the database
# Expects: a string file_name, which has a ticker on each line of the file and is stored
#          in this directory
def update_last_close(file_name):
    tickers = get_tickers(file_name)
    cur = db.cursor()
    for x in range(len(tickers)):
        data = alpaca.get_snapshot(tickers[x]).prev_daily_bar
        cur.execute(f'UPDATE Stocks SET last_close = {data.c} WHERE ticker="{tickers[x]}"')
    db.commit()


# Using the alpaca API, updates all values of a set of stocks in the database
# Expects: a string file_name, which has a ticker on each line of the file and is stored
#          in this directory
def update_all(file_name):
    update_current_price(file_name)
    update_last_open(file_name)
    update_last_close(file_name)

# Get the current stock price of a given ticker, as of the last database update
# Expects: a stock ticker
# Returns: the price of the stock according to the Stocks table of the db
def get_stock_price(ticker):
    cur.execute(f'SELECT curr_price FROM Stocks WHERE ticker="{ticker}"')
    return(cur.fetchone()[0])

# Creates a row for each ticker in './file_name'
# If a row already exists for the ticker, it is skipped
def create_stock_rows(file_name):
    stocks = get_tickers(file_name)
    for stock in stocks:
        try:
            cur.execute(f'INSERT INTO Stocks (ticker, curr_price, last_open, last_close) VALUES ("{stock}", 0, 0, 0)')
        except:
            print(f'Skipping {stock}, as it already exists')
    db.commit()
