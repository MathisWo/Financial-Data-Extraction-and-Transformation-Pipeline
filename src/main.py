# extracting data form FMP-API, loading it into pandas data frame, transforming/cleaning and output csv file

import pandas as pd
import os

from src.extract import fetch_company_profile, fetch_income_statement
from src.transform import build_company_financials


def main():

    # reading file with valid symbols and adding unique symbols to list
    with open("data/valid_symbols.txt", "r") as f:
        line = f.read()

        symbols = [s.strip() for s in line.split(",")]
        company_symbols = []
        for symbol in symbols:
            if symbol not in company_symbols:
                company_symbols.append(symbol)


    all_frames: list[pd.DataFrame] = []

    # start fetching profile and financial data for every symbol
    for symbol in company_symbols:
        print(f"[INFO] Processing {symbol}...")
        profile = fetch_company_profile(symbol)
        income_df = fetch_income_statement(symbol, years=3)

        # skipping every symbol with no matching  data
        if profile is None or income_df is None:
            print(f"[WARN] Skipping {symbol} due to missing data.")
            continue
        
        # combining company profile and financial data
        company_df = build_company_financials(symbol, profile, income_df)
        all_frames.append(company_df)

    # warning if no data is fetched
    if not all_frames:
        raise RuntimeError("No data was collected. Check API key and symbols.")

    # create and save final data frame
    final_df = pd.concat(all_frames, ignore_index=True).sort_values("symbol", ascending=True)

    os.makedirs("data/processed", exist_ok=True)
    final_df.to_csv("data/processed/company_financials.csv", index=False)

    print("[INFO] Wrote csv-file to data folder.")


if __name__ == "__main__":
    main()