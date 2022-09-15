
# expects: the name of a file which holds an alpaca key id and secret key
# returns: the key id and secret key
def get_key(file_name):
    # API Key ID and Secret Key should be stored in the subdirectory 'secrets'
    # The file name should be {file_name}
    # The Key ID should be on the first line,
    # Followed by the Secret Key on the second line
    f = open(f'/secrets/{file_name}')
    secrets = f.readlines()
    f.close()
    secrets[0] = secrets[0][0:-1]
    return secrets[0], secrets[1]

# expects: the name of a file which holds a list of stock tickers
# returns: a list of those stock tickers as strings
def get_tickers(file_name):
    f = open(f'./{file_name}')
    tickers = f.readlines()
    f.close()
    return tickers