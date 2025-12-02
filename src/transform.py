# modules for transforming extracted data

from typing import Dict
import pandas as pd

# combine profile & income statement into df, one row per year
def build_company_financials(symbol: str, profile: Dict, income_df: pd.DataFrame) -> pd.DataFrame:

    # select + rename columns from income statement
    cols_map = {
        "symbol": "symbol",
        "fiscalYear": "year",
        "revenue": "revenue",
        "reportedCurrency": "currency",
        "grossProfit": "gross_profit",
        "operatingIncome": "operating_income",
        "netIncome": "net_income",
        "eps": "earnings_per_share",
    }

    # warning if selected columns do not appear in df
    missing_cols = [c for c in cols_map.keys() if c not in income_df.columns]
    if missing_cols:
        print(f"[WARN] Missing expected columns for {symbol}: {missing_cols}")

    # keep only existing cols
    use_cols = [c for c in cols_map.keys() if c in income_df.columns]
    df = income_df[use_cols].rename(columns={c: cols_map[c] for c in use_cols})

    # add profile info
    df["company_name"] = profile.get("companyName", symbol)
    df["country"] = profile.get("country", None)
    df["industry"] = profile.get("industry", None)


    # ensure proper order
    col_order = [
        "company_name",
        "symbol",
        "country",
        "industry",
        "year",
        "revenue",
        "currency",
        "gross_profit",
        "operating_income",
        "net_income",
        "earnings_per_share"
    ]
    existing = [c for c in col_order if c in df.columns]
    df = df[existing]

    # sort by year descending or ascending as you prefer
    df = df.sort_values("year", ascending=False)

    return df