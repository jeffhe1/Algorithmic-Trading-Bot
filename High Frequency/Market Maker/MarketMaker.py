from datetime import datetime
from time import sleep
from alpaca.broker.client import BrokerClient
from alpaca.trading.client import TradingClient
class MMAlgo:
    def __init__(self, api_key, secret_key):
        self.trader = TradingClient(api_key, secret_key)
        
    def get_lob(self):
        pass

    def quote(self, mid_price):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    key = "PKCN4TF8UO57FKBL4SAD"
    secret = "cInEgFi26tYhr1Ie9FR7phR55HjeMiDAgdtmdCeB"
    mm = MMAlgo(key, secret)
    mm.run()
