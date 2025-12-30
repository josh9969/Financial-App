import pandas as pd
from datetime import datetime

def expense_dataframe(raw_data):
    df = pd.DataFrame(
        raw_data,
        columns=["id", "date", "category", "amount", "note"]
    )
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def current_month_df(df):
    now = datetime.now()
    return df[
        (df["date"].dt.month == now.month) &
        (df["date"].dt.year == now.year)
    ]

