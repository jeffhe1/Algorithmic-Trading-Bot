import os
from dotenv import load_dotenv
from time import sleep
from pybit.unified_trading import HTTP
load_dotenv()
api_key = os.getenv("TESTNET_API_KEY")
api_secret_key= os.getenv("TESTNET_API_SECRET_KEY")
coin_pair = ['ETHUSDT','ETHUSDT']

session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret_key
)

symbol_list = [result for result in session.get_tickers(category='spot',)['result']['list']]  

print(symbol_list)