# Mutual Fund Analyzer

This project fetches historical NAV data for Indian mutual funds, calculates rolling returns and standard deviation, and generates line charts for comparison.

## Structure
- `data/`: CSV files for NAVs and analytics
- `charts/`: Generated chart images
- `main.py`: Entry point for analysis
- `fetch_nav.py`: Fetches NAV data from AMFI/MFAPI
- `analytics.py`: Calculates rolling returns, std dev, and other metrics
- `charting.py`: Generates line charts from CSV

## Usage
1. Configure your list of funds in `main.py`.
2. Run analysis to fetch data, compute metrics, and generate charts.
3. Optionally, generate charts from an existing CSV using `charting.py`.

## Requirements
- Python 3.8+
- pandas, numpy, matplotlib, requests

## To Do
- Implement data fetching, analytics, and charting modules.
- Document workflow and sample outputs.
