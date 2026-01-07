import sqlite3
import os
from typing import List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

os.makedirs(BASE_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    company TEXT,
    role TEXT,
    industry TEXT,
    website TEXT,
    linkedin TEXT,
    country TEXT,
    status TEXT,
    payload TEXT
)
""")
conn.commit()

def insert_leads(leads: List[dict]):
    for lead in leads:
        cur.execute("""
            INSERT INTO leads (
                name, email, company, role, industry,
                website, linkedin, country, status, payload
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead.get("name"),
            lead.get("email"),
            lead.get("company"),
            lead.get("role"),
            lead.get("industry"),
            lead.get("website"),
            lead.get("linkedin"),
            lead.get("country"),
            "NEW",
            str(lead)
        ))
    conn.commit()

def fetch_by_status(status: str) -> List[Tuple[int, str]]:
    cur.execute(
        "SELECT id, payload FROM leads WHERE status=?",
        (status,)
    )
    return cur.fetchall()

def update_status(lead_id: int, status: str):
    cur.execute(
        "UPDATE leads SET status=? WHERE id=?",
        (status, lead_id)
    )
    conn.commit()

def update_payload(lead_id: int, payload: dict):
    cur.execute(
        "UPDATE leads SET payload=? WHERE id=?",
        (str(payload), lead_id)
    )
    conn.commit()

def mark_failed(lead_id: int, reason: str):
    cur.execute(
        "UPDATE leads SET status=? WHERE id=?",
        ("FAILED", lead_id)
    )
    conn.commit()

def get_metrics():
    cur.execute("""
        SELECT status, COUNT(*) as count
        FROM leads
        GROUP BY status
    """)
    return cur.fetchall()

def fetch_all():
    cur.execute("""
        SELECT id, name, email, company, role,
               industry, country, status
        FROM leads
        ORDER BY id DESC
    """)
    return cur.fetchall()