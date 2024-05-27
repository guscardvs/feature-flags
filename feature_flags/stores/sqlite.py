import sqlite3

from feature_flags.utils import Singleton

from .store import Flag, Store, Value


class SQLiteStore(Store, Singleton):
    def __init__(self, db_file: str = 'feature_flags.db') -> None:
        self.db_file = db_file
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feature_flags (
                flag TEXT PRIMARY KEY,
                value INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def save(self, flag: Flag, value: Value) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO feature_flags (flag, value) VALUES (?, ?)
        """,
            (flag, int(value)),
        )
        conn.commit()
        conn.close()

    def save_bulk(self, flags: dict[Flag, Value]) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for flag, value in flags.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO feature_flags (flag, value) VALUES (?, ?)
            """,
                (flag, int(value)),
            )
        conn.commit()
        conn.close()

    def get(self, flag: Flag) -> Value | None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT value FROM feature_flags WHERE flag = ?
        """,
            (flag,),
        )
        result = cursor.fetchone()
        conn.close()
        return bool(result[0]) if result else None

    def get_all(self) -> dict[Flag, Value]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT flag, value FROM feature_flags
        """)
        result = cursor.fetchall()
        conn.close()
        return {flag: bool(value) for flag, value in result}

    def clear(self) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM feature_flags
        """)
        conn.commit()
        conn.close()
