"""file that handles posting to replit grpahql endpoint for queries and mutations"""

import json
from requests import post as _post, get as _get, delete as _delete
from typing import Dict, Any
from .queries import q
from time import sleep
import logging

endpoint = "https://replit.com/graphql"
headers = {
            "X-Requested-With": "replit",
            'Origin': 'https://replit.com',
            'Accept': 'application/json',
            'Referrer': 'https://replit.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Host': "replit.com",
            "x-requested-with": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0",
        }

def post(connection: str, query: str, vars: Dict[str, Any] = {}):
    """post query with vars to replit graph query language"""
    _headers = headers
    _headers["Cookie"] = f"connect.sid={connection}"
    class FakeReq:
        def __init__(self):
            self.status_code = 429
    req = FakeReq()
    number_of_attempts = 0
    while req.status_code == 429 and number_of_attempts < 5: # only try 5 times
        req = _post(endpoint, json = {
                "query": q[query],
                "variables": vars,
            }, headers = _headers)
        if (req.status_code == 429):
            number_of_attempts += 1
            sleep(5 * (number_of_attempts)) # as not to overload the server, the sleep time increases per num attempts
            continue
        if (req.status_code == 200):
            print("Successful graphql!", query, vars, sep="\n")
        else:
            logging.error(req + '\n' + req.text)
        res = json.loads(req.text)
        try:
            _ = list(map(lambda x: x["data"], list(res["data"])))
            return _
        except:
            if ('data' in res['data']):
                return res["data"]["data"]
            else:
                return res["data"]