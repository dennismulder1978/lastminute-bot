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
              AND arrival_date = ?
            """,
            (
                deal.source,
                deal.title,
                deal.location,
                deal.url,
                deal.arrival_date.isoformat(),
            ),
        )

        return cursor.fetchone()

    def insert_deal(self, deal):
        self.conn.execute(
            """
            INSERT INTO deals
                (source, title, location, region, countrycode, url, price, arrival_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                deal.source,
                deal.title,
                deal.location,
                deal.region,
                deal.countrycode,
                deal.url,
                deal.price,
                deal.arrival_date.isoformat(),
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
              AND arrival_date = ?
            """,
            (
                deal.price,
                deal.source,
                deal.title,
                deal.location,
                deal.url,
                deal.arrival_date.isoformat(),
            ),
        )

        self.conn.commit()