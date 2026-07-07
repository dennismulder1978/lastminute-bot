import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_FILE = BASE_DIR / "data" / "holidayhunter.db"


def initialize_database():

    DB_FILE.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            url TEXT,
            price REAL NOT NULL,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source, title)
        )
    """)

    conn.commit()

    # Controleer direct of de tabel bestaat
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    conn.close()