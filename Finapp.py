import streamlit as st
from database import init_db

st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="centered"
)

init_db()

st.title("Personal Finance Tracker 🇦🇪")
st.write("Database initialized successfully.")
