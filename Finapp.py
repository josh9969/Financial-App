import streamlit as st
import pandas as pd
from datetime import datetime
from database import *
from analytics import *

st.set_page_config(
    page_title="Personal Finance Tracker 🇦🇪",
    layout="centered"
)

init_db()

st.title("Personal Finance Tracker 🇦🇪")

# ------------------ SIDEBAR: SALARY ------------------
st.sidebar.header("Monthly Salary")

current_salary = get_salary()
salary_input = st.sidebar.number_input(
    "Enter Monthly Salary (AED)",
    min_value=0.0,
    value=float(current_salary),
    step=100.0
)

if st.sidebar.button("Save Salary"):
    save_salary(salary_input)
    st.sidebar.success("Salary saved")

# ------------------ ADD EXPENSE ------------------
st.subheader("Add Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=datetime.today())
        amount = st.number_input("Amount (AED)", min_value=0.0)
    with col2:
        category = st.selectbox(
            "Category",
            ["Rent", "Food", "Transport", "Subscriptions",
             "Shopping", "Utilities", "Savings", "Misc"]
        )
        note = st.text_input("Note (optional)")

    submitted = st.form_submit_button("Add Expense")

if submitted and amount > 0:
    add_expense(str(date), category, amount, note)
    st.success("Expense added")

# ------------------ LOAD DATA ------------------
raw = get_expenses()
df = expense_dataframe(raw)

if df.empty:
    st.info("No expenses logged yet.")
    st.stop()

month_df = current_month_df(df)

# ------------------ DASHBOARD ------------------
st.divider()
st.subheader("This Month Overview")

total_spent = month_df["amount"].sum()
salary = get_salary()
remaining = salary - total_spent

days_left = (pd.Timestamp.now().days_in_month -
             datetime.now().day) + 1
daily_limit = remaining / days_left if days_left > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Spent", f"AED {total_spent:,.2f}")
c2.metric("Remaining", f"AED {remaining:,.2f}")
c3.metric("Daily Allowance", f"AED {daily_limit:,.2f}")

# ------------------ CHARTS ------------------
st.subheader("Spending by Category")
st.bar_chart(month_df.groupby("category")["amount"].sum())

st.subheader("Daily Spending Trend")
st.line_chart(month_df.groupby("date")["amount"].sum())

# ------------------ DELETE EXPENSES ------------------
st.divider()
st.subheader("All Expenses")

for _, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    col1.write(row["date"].date())
    col2.write(row["category"])
    col3.write(f"AED {row['amount']:.2f}")
    if col4.button("❌", key=row["id"]):
        delete_expense(row["id"])
        st.experimental_rerun()

# ------------------ RESET / REFRESH ------------------
st.divider()
st.subheader("Danger Zone")

if st.button("🗑️ Clear ALL Expenses"):
    clear_all_expenses()
    st.warning("All expenses deleted")
    st.experimental_rerun()

