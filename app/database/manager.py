import sqlite3

from app.database.db import DB_FILE


class DatabaseManager:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)

    def close(self):
        self.conn.close()

    def get_deal(self, deal):
        cursor = self.conn.execute(
            """
            SELECT id, price
            FROM deals
            WHERE source = ?
              AND title = ?
              AND location = ?
              AND url = ?
            """,
            (
                deal.source,
                deal.title,
                deal.location,
                deal.url,
            ),
        )

        return cursor.fetchone()

    def insert_deal(self, deal):
        self.conn.execute(
            """
            INSERT INTO deals
                (source, title, location, url, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                deal.source,
                deal.title,
                deal.location,
                deal.url,
                deal.price,
            ),
        )

        self.conn.commit()


    def update_price(self, deal):
        self.conn.execute(
            """
            UPDATE deals
            SET price     = ?,
                last_seen = CURRENT_TIMESTAMP
            WHERE source = ?
              AND title = ?
              AND location = ?
              AND url = ?
            """,
            (
                deal.price,
                deal.source,
                deal.title,
                deal.location,
                deal.url,
            ),
        )

        self.conn.commit()