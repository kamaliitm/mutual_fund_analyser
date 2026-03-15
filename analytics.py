import pandas as pd
import numpy as np
from datetime import timedelta

ROLLING_PERIODS = {
    '3Y': '1095D',
    '5Y': '1825D',
    '7Y': '2555D',
    '10Y': '3650D',
}

def analyze_fund(fund_id):
    nav_df = pd.read_csv(f"data/nav_{fund_id}.csv")
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df['nav'] = nav_df['nav'].ffill()
    nav_df.set_index('date', inplace=True)
    results = {}
    for label, period in ROLLING_PERIODS.items():
        # Calculate rolling return over the period
        rolling_return = nav_df['nav'].pct_change(freq=period) * 100
        # For std dev, use rolling std of daily returns over the same period.
        # Using daily returns makes the volatility measure comparable across funds.
        daily_returns = nav_df['nav'].pct_change()
        rolling_std = daily_returns.rolling(window=period, min_periods=1).std() * 100
        results[label] = {
            'rolling_return': rolling_return,
            'rolling_std': rolling_std,
        }
    return results

def main(fund_ids):
    fund_names = {
        120251: 'ICICI Prudential Equity & Debt Direct Growth Fund',
        122639: 'Parag Parikh Flexi Cap Direct Growth Fund',
        101349: 'Nifty 50 Index Fund',
        120684: 'Nifty Next 50 Index Fund'
    }
    for label in ROLLING_PERIODS.keys():
        rr_data = {}
        std_data = {}
        for fund_id in fund_ids:
            res = analyze_fund(fund_id)
            fund_name = fund_names.get(fund_id, f'Fund {fund_id}')
            rr_data[fund_name] = res[label]['rolling_return']
            std_data[fund_name] = res[label]['rolling_std']
        
        # Create DataFrames
        rr_df = pd.DataFrame(rr_data).dropna(how='all')
        std_df = pd.DataFrame(std_data).dropna(how='all')
        
        # Save to CSV
        rr_df.to_csv(f"data/rolling_return_{label.lower()}.csv")
        std_df.to_csv(f"data/rolling_std_{label.lower()}.csv")
        print(f"Saved rolling_return_{label.lower()}.csv and rolling_std_{label.lower()}.csv")
    
    # Also save the summary analytics.csv for charts
    all_results = []
    for fund_id in fund_ids:
        res = analyze_fund(fund_id)
        for label in ROLLING_PERIODS.keys():
            rr_val = res[label]['rolling_return'].dropna().iloc[-1] if not res[label]['rolling_return'].dropna().empty else np.nan
            std_val = res[label]['rolling_std'].dropna().iloc[-1] if not res[label]['rolling_std'].dropna().empty else np.nan
            all_results.append({
                'fund_id': fund_id,
                'period': label,
                'rolling_return': rr_val,
                'rolling_std': std_val,
            })
    df = pd.DataFrame(all_results)
    df.to_csv("data/analytics.csv", index=False)
    print("Saved analytics to data/analytics.csv")

if __name__ == "__main__":
    FUND_IDS = [120251, 122639, 101349, 120684]  # ICICI Prudential Equity & Debt Direct Growth Fund, Parag Parikh Flexi Cap Direct Growth Fund, Nifty 50 Index Fund, Nifty Next 50 Index Fund
    main(FUND_IDS)
