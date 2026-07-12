import requests
import pandas as pd
from datetime import datetime
import os

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
    funds_to_update = [120251, 122639]  # ICICI and Parag
    
    for fund_id in funds_to_update:
        csv_path = f"data/nav_{fund_id}.csv"
        last_date = None
        if os.path.exists(csv_path):
            existing_df = pd.read_csv(csv_path, parse_dates=['date'])
            if not existing_df.empty:
                last_date = existing_df['date'].max()
        
        df = fetch_nav(fund_id)
        
        if last_date is not None:
            df = df[df['date'] > last_date]
        
        if not df.empty:
            if os.path.exists(csv_path):
                existing_df = pd.read_csv(csv_path, parse_dates=['date'])
                combined_df = pd.concat([existing_df, df]).drop_duplicates(subset='date').sort_values('date')
                combined_df.to_csv(csv_path, index=False)
            else:
                df.to_csv(csv_path, index=False)
            print(f"Updated NAV data for fund {fund_id} with {len(df)} new entries.")
        else:
            print(f"No new data for fund {fund_id}.")
