# modules for extracting data from FMP-API

import pandas as pd
from typing import Optional
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment



FMP_BASE_URL = "https://financialmodelingprep.com/stable/"
FMP_API_KEY = os.getenv("FMP_API_KEY")


# helper function for fetching data
def _get(url: str, params: dict | None = None) -> Optional[dict | list]:
    
    # at least api_key as parameter
    if params is None:
        params = {}
    params["apikey"] = FMP_API_KEY

    # request and store json in object called 'data'
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    return data


# fetching single company profile data using _get()
def fetch_company_profile(symbol: str) -> Optional[dict]:
    
    # creating path for data to be stored in cache
    os.makedirs("data/raw", exist_ok=True)
    cache_path = f"data/raw/profile_{symbol}.json"

    # try loading data from cache first
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)
        
    # if no data in cache, try using base url + profile API
    url = f"{FMP_BASE_URL}/profile?"
    data = _get(url, {"symbol": symbol})

    # if there is no matching data return None
    if not data:
        print(f"[WARN] Empty or invalid profile for {symbol}")
        return None

    profile = data[0]

    # save profile to cache
    with open(cache_path, "w") as f:
        json.dump(profile, f)

    return profile


# fetching last N (years parameter) annual income statements for a single company using _get()
def fetch_income_statement(symbol: str, years: int = 3) -> Optional[pd.DataFrame]:

    # creating path for data to be stored in cache
    os.makedirs("data/raw", exist_ok=True)
    cache_path = f"data/raw/income_{symbol}.pkl"

    # try loading data from cache first
    if os.path.exists(cache_path):
        return pd.read_pickle(cache_path)
    
    # if no data in cache, try using base url + profile API
    url = f"{FMP_BASE_URL}/income-statement?"
    data = _get(url, params={"symbol": symbol, "period": "annual", "limit": years})
    
    df = pd.DataFrame(data)

    # if there is no matching data return None
    if df.empty:
        print(f"[WARN] Empty or invalid income statement for {symbol}")
        return None


    # save income-statement to cache
    df.to_pickle(cache_path)

    return df
