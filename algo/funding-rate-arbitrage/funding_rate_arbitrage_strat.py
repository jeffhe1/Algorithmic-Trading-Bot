import os
from dotenv import load_dotenv
import numpy as np
from pybit.unified_trading import HTTP
import time
from time import sleep
import matplotlib.pyplot as plt
import math

class FundingRateStrat:
    def __init__(self, api_key:str, api_secret_key:str, **kwargs):
        """
        api_key: API key
        api_secret_key: API secret key
        fee_rate: fee rate [SPOT Taker, SPOT Maker, DERIVATIVE Taker, DERIVATIVE Maker]
        """
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.fee_rate = kwargs.get('fee_rate', {'SPOT Taker': 0.001, 'SPOT Maker':0.001, 'DERIVATIVE Taker': 0.00055, 'DERIVATIVE Maker':0.0002})
        self.session = HTTP(
            testnet=kwargs.get('testnet', False),
            api_key=api_key,
            api_secret=api_secret_key,
            demo=kwargs.get('demo', False)
        )


    def get_funding_rates_and_time(self, symbols:dict) -> tuple[float, float, float]:
        """
        symbol: symbol e.g. "BTCUSDT"
        """

        print("Retrieving Funding Rate and Countdown Time for " + symbols['futures'])
        return (float(self.session.get_tickers(
            category='linear',
            symbol=symbols['futures']
        )['result']['list'][0]['fundingRate']), float(self.session.get_tickers(
            category='linear',
            symbol=symbols['futures']
        )['result']['list'][0]['nextFundingTime'])/1000 - time.time(), float(self.session.get_instruments_info(
            category='linear',
            symbol=symbols['futures']
        )['result']['list'][0]['fundingInterval']) * 60)
    
    def get_funding_rate(self, symbol:dict, **kwargs) -> list[float]:
        """
        symbol: symbol e.g. "BTCUSDT"
        plot:bool = kwargs.get('plot', False)
        limit:int = kwargs.get('limit', 20)
        """
        plot:bool = kwargs.get('plot', False)
        limit:int = kwargs.get('limit', 20)
        symbol = symbol[1]

        print("Retrieving Funding Rate History for " + symbol)
        ret = [self.session.get_funding_rate_history(
            category='linear',
            symbol=symbol,
            limit=limit,
        )['result']['list']]

        rates:list[float] =[float(ret[0][i]['fundingRate']) for i in range(len(ret[0]))]

        if plot:
            plt.plot(np.array(rates) * 100)
            plt.hlines(y=self.fee_rate['DERIVATIVE Maker']*100,colors='red',xmin=0,xmax=len(rates))
            plt.hlines(y=-self.fee_rate['DERIVATIVE Taker']*100,colors='red',xmin=0,xmax=len(rates))
            plt.show()
        return rates
    
    def order_sizes(self, symbols, **kwargs) -> tuple[float, float]:
        """
        avaliableFund : input your custom quantity available to strategy, default: 100% USDT available
        """
        availableFund : float = kwargs.get('availableFund', float(self.session.get_coin_balance(
            accountType="UNIFIED",
            coin="USDT"
        )['result']['balance']['walletBalance']))
        leverage : float = kwargs.get('leverage', 10)
        spot_price = float(self.session.get_tickers(category='spot', symbol=symbols['spot'])['result']['list'][0]['lastPrice'])
        futures_price = float(self.session.get_tickers(category='linear', symbol=symbols['futures'])['result']['list'][0]['lastPrice'])
        spot_qty = availableFund * leverage / spot_price
        futures_qty = availableFund * leverage / (futures_price * (leverage + 1))
        return (futures_qty, spot_qty)
        



    def execute_strategy(self, symbols:dict, **kwargs) -> int:
        cycles = kwargs.get('cycles', 9)
        fundingRate, countdown, fundingInterval= self.get_funding_rates_and_time(symbols)
        countdown = countdown + cycles * fundingInterval

        try:
            self.session.get_tickers(category='linear', symbol=symbols['futures'])
            self.session.get_tickers(category='spot', symbol=symbols['spot'])
        except:
            print("Not pair does not exist, try again...\n")
            return   0 
        try:
            if fundingRate > 0:
                qty = self.order_sizes(symbols)
                # Place order legs
                print(qty)
                print("Funding Rate is above fee rate. Execute Strategy\n")
                self.session.place_order(
                    category = 'linear', 
                    symbol=symbols['futures'] ,
                    side="Sell",
                    order_type="Market",
                    qty=round(qty[0],1))
                print(str(qty[0])+" "+ symbols['futures'] + " sell futures placed successfully")

                self.session.place_order(
                    category = 'spot', 
                    isLeverage=0, 
                    symbol=symbols['spot'] ,
                    side="Buy",
                    order_type="Market",
                    qty=round(qty[1],1), 
                    marketUnit="baseCoin")
                print(str(qty[1])+" "+ symbols['spot']  + " buy spots placed successfully")
                
                print("Order placed successfully\n")
                print("Waiting till countdown finish in " + str(countdown//3600) + " Hours " + str(countdown%3600//60) + " Minutes \n")
                temp = 100
                while countdown - temp > 0:
                    sleep(temp)
                    countdown -= temp
                    print("Waiting till countdown finish in " + str(countdown//3600) + " Hours" + str(countdown%3600//60) + " Minutes\n")
                sleep(2)

                self.session.place_order(
                    category = 'linear', 
                    symbol=symbols['future'],
                    side="Buy",
                    order_type="Market",
                    qty=0,
                    reduceOnly=True, 
                    closeOnTrigger=True)
                self.session.place_order(
                    category = 'spot',
                    isLeverage=0,
                    symbol=symbols['spot'],
                    side="Sell",
                    order_type="Market",
                    qty=round(qty[1] * (1 - self.fee_rate['SPOT Taker'])),
                    marketUnit="baseCoin")
                # Total fees collected for the duration of the strategy
                tot_fees = 0
                try: 
                    tot_fees = sum(abs([fees[0]["execFee"] for fees in self.session.get_executions(category='linear',limit=cycles+1,execType='Funding')['result']['list']]))
                    print("Position exited, total collected fees: " + str(tot_fees) + " USDT\n")
                except:
                    return tot_fees
                return tot_fees
            else:
                            print("Funding Rate is below fee rate. Strategy unsuccessful waiting till next round\n")
                            print("Sleeping for 1 Hour")
                            sleep(3600)
                            print("Trying again...\n")
                            self.execute_strategy()
            """
            elif fundingRate <0: 
                qty = self.input_quantity(symbol[0], available_fund)
                self.session.place_order(category = 'linear', symbol=symbol[1] ,side="Buy",order_type="Market",qty=qty)
                print(str(qty)+" "+ symbol[1] + " buy futures placed successfully")
                self.session.place_order(category = 'spot', isLeverage=1,symbol=symbol[0] ,side="Sell",order_type="Market",qty=qty)
                print(str(qty)+" "+ symbol[0] + " sell spot placed successfully")
                print("Strategy execution successful\n")
                print("Waiting till countdown finish in " + str(countdown//3600) + "Hours " + str(countdown%3600//60) + "Minutes\n")
                temp = 100
                while countdown > 0:
                    sleep(temp)
                    countdown -= temp
                    print("Waiting till countdown finish in " + str(countdown) + "seconds")
                sleep(10)
                self.session.place_order(category = 'linear', symbol=symbol[1] ,side="Sell",order_type="Market",qty=qty)
                self.session.place_order(category = 'spot', isLeverage=0,symbol=symbol[0] ,side="Buy",order_type="Market",qty=qty)
                return totmkdi_fees
            """
            
        except KeyboardInterrupt:
             print("Manually exiting program...")
             self.session.place_order(
                    category = 'linear', 
                    symbol=symbols['future'] ,
                    side="Sell",
                    order_type="Market",
                    qty=round(qty * (1 - self.fee_rate['SPOT Taker']),1))

             self.session.place_order(
                category = 'spot', 
                isLeverage=0, 
                symbol=symbols['future'] ,
                side="Buy",
                order_type="Market",
                qty=qty, 
                marketUnit="baseCoin")
             exit()   
            
        except Exception as e:
            print("Error while placing order")
            print(e) 
            return 0
    def strategy_backtest(startdate:str, enddate:str, symbols:str, **kwargs):
        """
        """

        pass

load_dotenv()
api_key = os.getenv("TESTNET_API_KEY")
api_secret_key= os.getenv("TESTNET_API_SECRET_KEY")
coin_pair = {'spot': 'ETHUSDT', 'futures':'ETHUSDT'}
FundingRateStrat(api_key, api_secret_key).execute_strategy(coin_pair, cycles=0)