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
            AND url = ?
            AND arrival_date = ?
            """,
            (
                deal.source,
                deal.url,
                deal.arrival_date.isoformat(),
            ),
        )

        return cursor.fetchone()

    def insert_deal(self, deal):
        try:
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
        
        except sqlite3.IntegrityError:

            print("\n=== DUPLICATE ===")
            print("Source :", deal.source)
            print("Title  :", deal.title)
            print("Arrival:", deal.arrival_date)
            print("URL    :", deal.url)

            cursor = self.conn.execute(
                """
                SELECT *
                FROM deals
                WHERE source = ?
                AND url = ?
                AND arrival_date = ?
                """,
                (
                    deal.source,
                    deal.url,
                    deal.arrival_date.isoformat(),
                ),
            )

            print("Existing row:")
            print(cursor.fetchone())

            raise


    def update_price(self, deal):
        cursor = self.conn.execute(
            """
            UPDATE deals
            SET price = ?,
                last_seen = CURRENT_TIMESTAMP
            WHERE source = ?
            AND url = ?
            AND arrival_date = ?
            """,
            (
                deal.price,
                deal.source,
                deal.url,
                deal.arrival_date.isoformat(),
            ),
        )

        self.conn.commit()

        if cursor.rowcount != 1:
            raise RuntimeError(
                f"update_price() werkte {cursor.rowcount} rijen bij "
                f"voor {deal.source} | {deal.arrival_date} | {deal.url}"
            )