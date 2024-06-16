import os
from dotenv import load_dotenv
from time import sleep
from pybit.unified_trading import HTTP
from funding_rate_arbitrage_strat import FundingRateStrat

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret_key= os.getenv("API_SECRET_KEY")

def main():
    fees_collected = 0
    coin_pair = ['PEPEUSDT', '1000PEPEUSDT']
    counter = 0
    while True:
        print("Iteration count: "+ str(counter))
        try: 
            fees_collected += FundingRateStrat(api_key, api_secret_key).execute_strategy(coin_pair, cycles=1)
        except KeyboardInterrupt:
            print("Manually exiting program...")

            break
        except Exception as e:
            print(e)
            print("Stopping bot due to error...")
            break
        counter += 1
    print("Total fees collected: " + str(fees_collected))
    return


if __name__ == "__main__":
    main()
    

