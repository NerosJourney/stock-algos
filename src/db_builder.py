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
    create_holdings_table = 'CREATE TABLE Holdings (account_id smallint NOT NULL, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), ticker VARCHAR(6) NOT NULL, FOREIGN KEY (ticker) REFERENCES Stocks(ticker), quantity int NOT NULL, avg_price DECIMAL(6,2) NOT NULL)'
    cur.execute(create_holdings_table)

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

def create_new_account(account_name, starting_cash):
    cur.execute(f'INSERT INTO Accounts (name, cash) VALUES ("{account_name}", {starting_cash})')
    db.commit()
    return cur.lastrowid


if __name__ == '__main__':
    # init_holdings_table()
    # init_accounts_table()
    # create_new_account("Test", 10_000)
    # init_stocks_table()
    # create_stock_rows('stocks1.txt')
    # create_stock_rows('stocks2.txt')
    pass
