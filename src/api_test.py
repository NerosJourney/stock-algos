import alpaca_trade_api as api
from alpaca_trade_api.stream import Stream

BASE_URL = 'https://paper-api.alpaca.markets'

# Returns both the key and the secret for alpaca's api
def get_key():
    # API Key ID and Secret Key should be stored in the root directory of this project
    # The file name should be 'alpaca.secret'
    # The Key ID should be on the first line,
    # Followed by the Secret Key on the second line
    f = open('./secrets/alpaca.secret')
    secrets = f.readlines()
    f.close()
    secrets[0] = secrets[0][0:-1]
    return secrets[0], secrets[1]

API_KEY, API_SECRET = get_key()
alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)
stream = Stream(API_KEY, API_SECRET, base_url=BASE_URL, data_feed='iex')

async def bar_callback(b):
    print(b)

print(alpaca.get_snapshot('AAPL').minute_bar, '\n' , alpaca.get_snapshot('AAPL').daily_bar)

# print(alpaca.get_bars('AMZN', '1Week', '2022-06-01', '2022-09-01').df)

# symbol= 'BTCUSD'
# stream.subscribe_crypto_bars(bar_callback, symbol)
# stream.subscribe_crypto_bars(bar_callback, 'ETHUSD')

# stream.run()
