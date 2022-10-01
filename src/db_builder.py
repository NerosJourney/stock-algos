from file_manager import get_tickers
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="nero",
    database="stock_algo_data"
)

cur = db.cursor()

# Creates a table which holds general information about each ticker
# Stores (attributes): Stock Ticker (ticker), Current Stock Price (curr_price), Price at last open (last_open), Price at last close (last_close) 
def init_stocks_table():
    create_stocks_table = 'CREATE TABLE Stocks (ticker VARCHAR(6) PRIMARY KEY NOT NULL, curr_price DECIMAL(6,2), last_open DECIMAL(6,2), last_close DECIMAL(6,2))'
    cur.execute(create_stocks_table)

# Creates a table which stores account information
# Stores (attributes): Account ID (account_id), Account name (name), Free cash currently available (cash)
def init_accounts_table():
    create_accouts_table = 'CREATE TABLE Accounts (account_id smallint PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50), cash DECIMAL(10,2))'
    cur.execute(create_accouts_table)

# Creates a table which stores information on each accounts currently-held stocks
# Stores (attributes): account_id, Stock ticker (ticker), Quantity of shares held (quantity), The average price the shares where bought at (avg_price)
def init_holdings_table():
    create_holdings_table = 'CREATE TABLE Holdings (account_id smallint NOT NULL, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), ticker VARCHAR(6) NOT NULL, FOREIGN KEY (ticker) REFERENCES Stocks(ticker), quantity int NOT NULL, avg_price DECIMAL(6,2) NOT NULL, PRIMARY KEY(account_id, ticker))'
    cur.execute(create_holdings_table)

# Creates a table which stores transaction history for each account
# Stores (attributes): Time the order was executed (executed), account_id, ticker, Buy or Sell order (type), Quantity of shares bought/sold (quantity), Price the shares were bought/sold at (price)
def init_orders_table():
    create_orders_table = 'CREATE TABLE Orders (executed DATETIME, account_id smallint, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), ticker VARCHAR(6), FOREIGN KEY (ticker) REFERENCES Stocks(ticker), type ENUM ("BUY", "SELL") NOT NULL, quantity int NOT NULL, price DECIMAL(6,2) NOT NULL, PRIMARY KEY(executed, account_id, ticker))'
    cur.execute(create_orders_table)

# Creates a table which stores historical information on account values over time
# Stores (attributes): The date the information is from (date_saved), account_id, The total value of shares + cash in account (value)
def init_account_vals_table():
    create_account_vals_table = 'CREATE TABLE Account_Values (date_saved DATETIME, account_id SMALLINT, FOREIGN KEY (account_id) REFERENCES Accounts(account_id), value DECIMAL(10,2), PRIMARY KEY(date_saved, account_id))'
    cur.execute(create_account_vals_table)