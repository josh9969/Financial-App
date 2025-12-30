import pandas as pd
from datetime import datetime

def monthly_summary(df, salary):
    current_month = datetime.now().month
    current_year = datetime.now().year

    df["date"] = pd.to_datetime(df["date"])
    month_df = df[
        (df["date"].dt.month == current_month) &
        (df["date"].dt.year == current_year)
    ]

    total_spent = month_df["amount"].sum()
    remaining = salary - total_spent

    days_left = (
        (pd.Timestamp.now().replace(day=1) + pd.offsets.MonthEnd(1)) -
        pd.Timestamp.now()
    ).days + 1

    daily_limit = remaining / days_left if days_left > 0 else 0

    return total_spent, remaining, daily_limit, month_df
