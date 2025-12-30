import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, get_connection
from settings import save_settings, load_settings
from analytics import monthly_summary
from datetime import date

st.set_page_config(page_title="Personal Finance Tracker 🇦🇪", layout="centered")
init_db()

st.title("Personal Finance Tracker 🇦🇪")

# ---------- SIDEBAR: SETTINGS ----------
st.sidebar.header("Monthly Settings")

settings = load_settings()

salary = st.sidebar.number_input(
    "Monthly Salary (AED)",
    min_value=0.0,
    value=float(settings["monthly_salary"]) if settings is not None else 0.0
)

needs = st.sidebar.slider(
    "Needs %",
    0.0, 1.0,
    value=float(settings["needs_ratio"]) if settings is not None else 0.5
)

wants = st.sidebar.slider(
    "Wants %",
    0.0, 1.0,
    value=float(settings["wants_ratio"]) if settings is not None else 0.3
)

savings = round(1 - (needs + wants), 2)

if savings < 0:
    st.sidebar.error("Percentages exceed 100%")
else:
    st.sidebar.write(f"Savings %: {savings * 100:.0f}%")
    if st.sidebar.button("Save Settings"):
        save_settings(salary, needs, wants, savings)
        st.sidebar.success("Settings saved")

# ---------- EXPENSE INPUT ----------
st.subheader("Add Expense")

with st.form("expense_form"):
    exp_date = st.date_input("Date", value=date.today())
    category = st.selectbox(
        "Category",
        ["Rent", "Food", "Transport", "Utilities", "Subscriptions", "Shopping", "Savings", "Misc"]
    )
    amount = st.number_input("Amount (AED)", min_value=0.0, step=1.0)
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Expense")

if submitted and amount > 0:
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
        (str(exp_date), category, amount, note)
    )
    conn.commit()
    conn.close()
    st.success("Expense added")

# ---------- LOAD DATA ----------
conn = get_connection()
df = pd.read_sql("SELECT * FROM expenses", conn)
conn.close()

if df.empty or settings is None:
    st.info("Add salary settings and start logging expenses.")
    st.stop()

# ---------- ANALYTICS ----------
total_spent, remaining, daily_limit, month_df = monthly_summary(df, salary)

st.subheader("This Month Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"AED {total_spent:,.2f}")
col2.metric("Remaining", f"AED {remaining:,.2f}")
col3.metric("Daily Allowance", f"AED {daily_limit:,.2f}")

if remaining < 0:
    st.error("You’ve exceeded your monthly salary. No excuses.")

# ---------- CHARTS ----------
st.subheader("Spending by Category")
cat_fig = px.pie(
    month_df,
    values="amount",
    names="category",
    hole=0.4
)
st.plotly_chart(cat_fig, use_container_width=True)

st.subheader("Daily Spending Trend")
daily = month_df.groupby("date")["amount"].sum().reset_index()
line_fig = px.line(daily, x="date", y="amount", markers=True)
st.plotly_chart(line_fig, use_container_width=True)

# ---------- RAW DATA ----------
with st.expander("View All Expenses"):
    st.dataframe(month_df.sort_values("date", ascending=False))
