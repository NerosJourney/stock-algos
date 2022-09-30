from file_manager import get_tickers
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="nero",
    database="stock_algo_data"
)

cur = db.cursor()


# Creates a table which holds general information about each ticker
# Attributes: ticker, curr_price, open, last_close
def init_stocks_table():
    create_stocks_table = 'CREATE TABLE Stocks (ticker VARCHAR(6) PRIMARY KEY NOT NULL, curr_price DECIMAL(6,2), last_open DECIMAL(6,2), last_close DECIMAL(6,2))'
    cur.execute(create_stocks_table)

def init_accounts_table():
    create_accouts_table = 'CREATE TABLE Accounts (account_id smallint PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50), cash DECIMAL(10,2))'
    cur.execute(create_accouts_table)

def init_holdings_table():
    create_holdings_table = 'CREATE TABLE Holdings (account_id smallint NOT NULL, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), ticker VARCHAR(6) NOT NULL, FOREIGN KEY (ticker) REFERENCES Stocks(ticker), quantity int NOT NULL, avg_price DECIMAL(6,2) NOT NULL, PRIMARY KEY(account_id, ticker))'
    cur.execute(create_holdings_table)

def init_orders_table():
    create_orders_table = 'CREATE TABLE Orders (executed DATETIME, account_id smallint, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), ticker VARCHAR(6), FOREIGN KEY (ticker) REFERENCES Stocks(ticker), type ENUM ("BUY", "SELL") NOT NULL, quantity int NOT NULL, price DECIMAL(6,2) NOT NULL, PRIMARY KEY(executed, account_id, ticker))'
    cur.execute(create_orders_table)

def init_account_vals_table():
    create_account_vals_table = 'CREATE TABLE Account_Values (date_saved DATETIME, account_id SMALLINT, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), value DECIMAL(10,2), PRIMARY KEY(date_saved, account_id))'
    cur.execute(create_account_vals_table)

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


if __name__ == '__main__':
    init_account_vals_table()
    # init_orders_table()
    # init_holdings_table()
    # init_accounts_table()
    # create_new_account("Test", 10_000)
    # init_stocks_table()
    # create_stock_rows('stocks1.txt')
    # create_stock_rows('stocks2.txt')
    pass
