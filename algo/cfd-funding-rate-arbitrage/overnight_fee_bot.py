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
        return res
    
    def get_session_detail(self, sec_token, cst):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = ''
        headers = {
            'X-CAP-ACCESS-TOKEN': sec_token,
            'CST': cst
        }
        conn.request("GET", "/api/v1/session", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
    

bot = OvernightFeeBot('Ap4ukeVKKZY7aVpG', "2211054370abc@gmail.com", 'Abc20030315;', demo=True)
session = bot.create_new_session()
SEC_TOKEN = session.getheader('X-SECURITY-TOKEN')
CST = session.getheader('CST')
print(bot.get_session_detail(SEC_TOKEN, CST))