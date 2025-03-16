import requests
import time
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import re
import numpy as np
import statsmodels.api as sm

def print_log(*args):
    print(f"[{str(datetime.now())[:-3]}] ", end="")
    print(*args)

def get_search_results(params):
    req_sr = requests.get("https://store.steampowered.com/search/results/", params=params)
    if req_sr.status_code != 200:
        print_log(f"Failed to get search results: {req_sr.status_code}")
        return {"items": []}
    try:
        search_results = req_sr.json()
    except Exception as e:
        print_log(f"Failed to parse search results: {e}")
        return {"items": []}
    return search_results

