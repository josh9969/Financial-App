from database import get_connection
import pandas as pd

def save_settings(salary, needs, wants, savings):
    conn = get_connection()
    conn.execute("DELETE FROM settings")
    conn.execute("""
        INSERT INTO settings (id, monthly_salary, needs_ratio, wants_ratio, savings_ratio)
        VALUES (1, ?, ?, ?, ?)
    """, (salary, needs, wants, savings))
    conn.commit()
    conn.close()

def load_settings():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM settings", conn)
    conn.close()
    return df.iloc[0] if not df.empty else None
