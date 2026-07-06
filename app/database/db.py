from pathlib import Path

DB_FILE = Path("data/holidayhunter.db")


def initialize_database():
    DB_FILE.parent.mkdir(exist_ok=True)
    DB_FILE.touch(exist_ok=True)