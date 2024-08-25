import requests
import pandas as pd
import time
import json
import http.client
import os
class OvernightFeeBot():
    def __init__(self, api_key, identifier, password, **kwargs):
        self.api_key = api_key
        self.identifier = identifier
        self.password = password
        self.demo = kwargs.get("demo", False)
        if self.demo : 
            self.base_url = "demo-api-capital.backend-capital.com"
        else:
            self.base_url = "api-capital.backend-capital.com"
    def create_new_session(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = json.dumps({
            "identifier": self.identifier,
            "password": self.password
        })
        headers = {
        'X-CAP-API-KEY': self.api_key,
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v1/session", payload, headers)
        res = conn.getresponse()
        self.security_token = res.getheader('X-SECURITY-TOKEN')
        self.cst = res.getheader('CST')
        return res
    
    def get_session_detail(self):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'X-CAP-ACCESS-TOKEN': self.security_token,
            'CST': self.cst
        }
        conn.request("GET", "/api/v1/session", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
    
    def get_transaction_hist(self, **kwargs):
        """
        from_date: Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter
        To_date: Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter
        lastPeriod: Limits the timespan in seconds through to current time (not applicable if a date range has been specified). Cannot be bigger than current Unix timestamp value. 
        type: Transaction type,  Possible values: INACTIVITY_FEE, RESERVE, VOID, UNRESERVE, WRITE_OFF_OR_CREDIT, CREDIT_FACILITY, FX_COMMISSION, COMPLAINT_SETTLEMENT, DEPOSIT, WITHDRAWAL, REFUND, WITHDRAWAL_MONEY_BACK, TRADE, SWAP, TRADE_COMMISSION, TRADE_COMMISSION_GSL, NEGATIVE_BALANCE_PROTECTION, TRADE_CORRECTION, CHARGEBACK, ADJUSTMENT, BONUS, TRANSFER, CORPORATE_ACTION, CONVERSION, REBATE, TRADE_SLIPPAGE_PROTECTION
        """
        from_date:str = kwargs.get("from_date", None)
        to_date:str = kwargs.get("to_date", None)
        lastPeriod:str = kwargs.get("lastPeriod", None)
        transactionType:str = kwargs.get("transactionType", None)
        query_params:dict = {
            f"from={from_date}": from_date,
            f"to={to_date}": to_date,
            f"lastPeriod={lastPeriod}": lastPeriod,
            f"transactionType={transactionType}": transactionType
        }
        params: list[str] = []
        for key,value in query_params.items():
            if value != None:
                params.append(key)
        query = "&".join(params)
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        print(self.security_token)
        print(self.cst)
        print(query)
        headers = {
            'X-CAP-ACCESS-TOKEN': self.security_token,
            'CST': self.cst
        }
        if query != "":
            conn.request("GET", f"/api/v1/history/transactions?{query}", payload, headers)
        else:
            conn.request("GET", "/api/v1/history/transactions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        return data

bot = OvernightFeeBot('Ap4ukeVKKZY7aVpG', "2211054370abc@gmail.com", 'Abc20030315;', demo=True)
session = bot.create_new_session()
print(bot.get_session_detail())
