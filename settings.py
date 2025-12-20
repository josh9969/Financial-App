from database import get_connection

def get_settings():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT monthly_salary, needs_ratio, wants_ratio, savings_ratio FROM settings WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row

def save_settings(salary, needs, wants, savings):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO settings (id, monthly_salary, needs_ratio, wants_ratio, savings_ratio)
        VALUES (1, ?, ?, ?, ?)
    """, (salary, needs, wants, savings))
    conn.commit()
    conn.close()
