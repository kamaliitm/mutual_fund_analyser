import requests
import pandas as pd
from datetime import datetime

# MFAPI endpoint for Indian mutual funds
MFAPI_BASE = "https://api.mfapi.in/mf/"

# Example: ICICI Prudential Equity & Debt Fund (ID: 100027)
# You can add more fund IDs as needed
FUND_IDS = [
    120251,  # ICICI Prudential Equity & Debt Direct Growth Fund
    122639,  # Parag Parikh Flexi Cap Direct Growth Fund
    119062,  # HDFC Hybrid Equity Fund
    101349,  # Nifty 50 Index Fund
    120684,  # Nifty Next 50 Index Fund
]

def fetch_nav(fund_id):
    url = f"{MFAPI_BASE}{fund_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    navs = data.get("data", [])
    df = pd.DataFrame(navs)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df.sort_values('date')
    df['nav'] = df['nav'].ffill()
    return df[['date', 'nav']]

if __name__ == "__main__":
    for fund_id in FUND_IDS:
        df = fetch_nav(fund_id)
        df.to_csv(f"data/nav_{fund_id}.csv", index=False)
        print(f"Saved NAV data for fund {fund_id}.")
