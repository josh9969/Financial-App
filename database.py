import sqlite3
import os

DB_PATH = "data/expenses.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_salary REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def save_salary(salary):
    conn = get_connection()
    conn.execute("DELETE FROM settings")
    conn.execute(
        "INSERT INTO settings (id, monthly_salary) VALUES (1, ?)",
        (salary,)
    )
    conn.commit()
    conn.close()

def get_salary():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT monthly_salary FROM settings LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def add_expense(date, category, amount, note):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
        (date, category, amount, note)
    )
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    df = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return df

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def clear_all_expenses():
    conn = get_connection()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

